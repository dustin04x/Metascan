use hex;
use rayon::prelude::*;
use std::fmt;
use std::io::{self, Write};
use std::str;

// --- CONSTANTS (English Letter Frequency) ---
const ENGLISH_FREQS: [f64; 26] = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, // A-G
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, // H-N
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, // O-U
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074, // V-Z
];

// A bunch of common English words. You can extend this list.
// Short words (>=3) only to avoid insane noise.
static COMMON_WORDS: &[&str] = &[
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her",
    "she", "or", "will", "my", "one", "all", "would", "there", "their",
    "what", "so", "up", "out", "if", "about", "who", "get", "which",
    "go", "me", "when", "make", "can", "like", "time", "no", "just",
    "him", "know", "take", "people", "into", "year", "your", "good",
    "some", "could", "them", "see", "other", "than", "then", "now",
    "look", "only", "come", "its", "over", "think", "also", "back",
    "after", "use", "two", "how", "our", "work", "first", "well",
    "way", "even", "new", "want", "because", "any", "these", "give",
    "day", "most", "hello", "world", "test", "flag", "password",
];

// --- ENUMS ---

#[derive(Debug, Clone, Copy, PartialEq)]
enum DataFormat {
    Hex,
    Binary, // bits
    Text,
}

impl fmt::Display for DataFormat {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            DataFormat::Hex => write!(f, "Hex"),
            DataFormat::Binary => write!(f, "Binary Bits"),
            DataFormat::Text => write!(f, "Raw Text"),
        }
    }
}

// --- HELPER FUNCTIONS ---

/// Converts a string of "010101" into a Vec<u8>
fn from_binary_str(s: &str) -> Result<Vec<u8>, String> {
    // Remove spaces/newlines so "0101 0101" works
    let clean: String = s.chars().filter(|c| !c.is_whitespace()).collect();

    if clean.len() % 8 != 0 {
        return Err(format!(
            "Binary string length ({}) is not a multiple of 8.",
            clean.len()
        ));
    }

    clean
        .as_bytes()
        .chunks(8)
        .map(|chunk| {
            let chunk_str = str::from_utf8(chunk).unwrap();
            u8::from_str_radix(chunk_str, 2)
                .map_err(|_| format!("Invalid character in chunk: {}", chunk_str))
        })
        .collect()
}

/// Converts Vec<u8> into a string "01010101 11110000"
fn to_binary_str(bytes: &[u8]) -> String {
    bytes
        .iter()
        .map(|b| format!("{:08b}", b))
        .collect::<Vec<String>>()
        .join(" ")
}

fn xor_repeating(input: &[u8], key: &[u8]) -> Vec<u8> {
    input
        .iter()
        .zip(key.iter().cycle())
        .map(|(b, k)| b ^ k)
        .collect()
}

/// Chi-squared scoring for "English-likeness" at the letter frequency level.
/// Lower = more likely English.
fn score_chi_squared(text: &[u8]) -> f64 {
    let mut counts = [0usize; 26];
    let mut ignored = 0usize;
    let mut space_count = 0usize;
    let mut total = 0usize;

    for &b in text {
        total += 1;

        if b.is_ascii_alphabetic() {
            let lower = b.to_ascii_lowercase();
            let idx = (lower - b'a') as usize;
            if idx < 26 {
                counts[idx] += 1;
            }
        } else if b == b' ' {
            space_count += 1;
        } else if !b.is_ascii_punctuation() && !b.is_ascii_whitespace() {
            // weird byte (not letter, not space, not punctuation)
            ignored += 1;
        }
    }

    if total == 0 {
        return f64::MAX;
    }

    // Too many garbage bytes? Kill this candidate.
    if ignored > total / 3 {
        return f64::MAX;
    }

    // Only count actual letters for chi-squared
    let total_letters: usize = counts.iter().sum();
    if total_letters == 0 {
        return f64::MAX;
    }
    let total_letters_f = total_letters as f64;

    let mut chi_sq = 0.0;
    for (i, &observed) in counts.iter().enumerate() {
        let expected = total_letters_f * ENGLISH_FREQS[i];
        if expected <= 0.0 {
            continue;
        }
        let diff = observed as f64 - expected;
        chi_sq += (diff * diff) / expected;
    }

    // Light penalty if space ratio is far from ~18%
    let space_ratio = space_count as f64 / total as f64;
    let space_penalty = (space_ratio - 0.18).abs() * 50.0;

    chi_sq + space_penalty
}

/// Word-based bonus: the more common words appear, the better.
/// We *subtract* this from the chi-squared score.
fn word_bonus(text: &str) -> f64 {
    let lower = text.to_ascii_lowercase();
    let mut bonus = 0.0;

    for w in COMMON_WORDS {
        if w.len() < 3 {
            continue;
        }
        if lower.contains(w) {
            // longer words = more confidence, but don't explode
            bonus += (w.len() as f64).sqrt();
        }
    }

    bonus
}

/// Combined scoring: lower = better.
/// Chi-squared + penalties, then minus a strong word bonus.
fn score_candidate(bytes: &[u8]) -> f64 {
    let chi = score_chi_squared(bytes);
    if !chi.is_finite() || chi == f64::MAX {
        return f64::MAX;
    }

    let text = match std::str::from_utf8(bytes) {
        Ok(t) => t,
        Err(_) => return f64::MAX,
    };

    let bonus = word_bonus(text);
    // Tune multiplier: higher = words matter more
    chi - bonus * 10.0
}

// --- IO LOGIC ---

fn ask(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap();
    let mut s = String::new();
    io::stdin().read_line(&mut s).unwrap();
    s.trim().to_string()
}

fn select_format(label: &str) -> DataFormat {
    loop {
        println!("\nSelect {} Format:", label);
        println!("  1. Hex (e.g., 4142)");
        println!("  2. Binary (e.g., 01000001 01000010)");
        println!("  3. Raw Text (e.g., AB)");
        let choice = ask("Choice [1-3]: ");

        match choice.as_str() {
            "1" => return DataFormat::Hex,
            "2" => return DataFormat::Binary,
            "3" => return DataFormat::Text,
            _ => println!("Invalid choice."),
        }
    }
}

fn parse_input(label: &str, format: DataFormat) -> Vec<u8> {
    loop {
        let input_str = ask(&format!("\nEnter {} ({}): ", label, format));

        let result = match format {
            DataFormat::Text => Ok(input_str.as_bytes().to_vec()),
            DataFormat::Hex => hex::decode(input_str.replace(' ', "")).map_err(|e| e.to_string()),
            DataFormat::Binary => from_binary_str(&input_str),
        };

        match result {
            Ok(bytes) => return bytes,
            Err(e) => println!("Error: {}", e),
        }
    }
}

fn format_output(bytes: &[u8], format: DataFormat) -> String {
    match format {
        DataFormat::Text => String::from_utf8_lossy(bytes).to_string(),
        DataFormat::Hex => hex::encode(bytes),
        DataFormat::Binary => to_binary_str(bytes),
    }
}

// --- EXECUTION MODES ---

struct ResultCandidate {
    key: Vec<u8>,
    output_bytes: Vec<u8>,
    score: f64,
}

fn run_brute_force(input: &[u8], output_fmt: DataFormat) {
    let depth_str = ask("\nBrute-force key length (bytes)? [1-2]: ");
    let key_len: usize = depth_str.parse().unwrap_or(1);

    if key_len == 0 || key_len > 2 {
        println!("Only 1 or 2 byte keys supported for this demo.");
        return;
    }

    let top_str = ask("How many top candidates to show? [default 10]: ");
    let top_n: usize = top_str.parse().unwrap_or(10);

    println!("[+] Cracking...");
    let max_keys = 1u64 << (key_len * 8);

    let mut candidates: Vec<ResultCandidate> = (0..max_keys)
        .into_par_iter()
        .filter_map(|k| {
            let key_bytes = match key_len {
                1 => vec![k as u8],
                2 => vec![(k >> 8) as u8, (k & 0xFF) as u8],
                _ => return None,
            };

            let out = xor_repeating(input, &key_bytes);
            let score = score_candidate(&out);

            // Filter obvious garbage; keep threshold high so we don't lose good stuff
            if !score.is_finite() || score == f64::MAX || score > 10_000.0 {
                return None;
            }

            Some(ResultCandidate {
                key: key_bytes,
                output_bytes: out,
                score,
            })
        })
        .collect();

    // Lower score = better (English-like + word hits)
    candidates.sort_by(|a, b| a.score.partial_cmp(&b.score).unwrap());

    println!("\n===== TOP RESULTS =====");
    for (i, res) in candidates.iter().take(top_n).enumerate() {
        let key_disp = hex::encode(&res.key);
        let out_disp = format_output(&res.output_bytes, output_fmt);

        println!(
            "#{}: Key[0x{}] Score[{:.2}] -> {}",
            i + 1,
            key_disp,
            res.score,
            out_disp
        );
    }
}

fn run_known_key(input: &[u8], output_fmt: DataFormat) {
    let key_fmt = select_format("Key");
    let key_bytes = parse_input("Key", key_fmt);

    let output = xor_repeating(input, &key_bytes);
    let out_disp = format_output(&output, output_fmt);

    println!("\n===== RESULT =====");
    println!("{}", out_disp);
}

fn main() {
    println!("--- Rusty XOR Tool (Binary Edition) ---");

    // 1. Get Input
    let in_fmt = select_format("Input Ciphertext");
    let input_bytes = parse_input("Ciphertext", in_fmt);
    println!("[+] Loaded {} bytes.", input_bytes.len());

    // 2. Select Output Format
    let out_fmt = select_format("Desired Output");

    // 3. Select Mode
    println!("\nSelect Mode:");
    println!("  1. Brute Force (Crack the key)");
    println!("  2. Decrypt/Encrypt (I have the key)");
    let mode = ask("Choice: ");

    match mode.as_str() {
        "1" => run_brute_force(&input_bytes, out_fmt),
        "2" => run_known_key(&input_bytes, out_fmt),
        _ => println!("Invalid mode."),
    }
}
