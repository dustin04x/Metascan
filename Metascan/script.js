// Global state
let filesData = [];
let currentFileIndex = 0;

// DOM Elements
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const uploadArea = document.getElementById('uploadArea');
const resultsSection = document.getElementById('resultsSection');
const fileTabs = document.getElementById('fileTabs');
const metadataOutput = document.getElementById('metadataOutput');
const copyAllBtn = document.getElementById('copyAllBtn');
const downloadBtn = document.getElementById('downloadBtn');
const clearBtn = document.getElementById('clearBtn');

// Event Listeners
browseBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
});

uploadArea.addEventListener('click', (e) => {
    if (e.target !== browseBtn && !browseBtn.contains(e.target)) {
        fileInput.click();
    }
});

fileInput.addEventListener('change', handleFileSelect);
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
copyAllBtn.addEventListener('click', copyAllMetadata);
downloadBtn.addEventListener('click', downloadMetadata);
clearBtn.addEventListener('click', clearAll);

// Drag and Drop
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
    if (files.length > 0) {
        processFiles(files);
    }
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files).filter(f => f.type.startsWith('image/'));
    if (files.length > 0) {
        processFiles(files);
    }
}

// Process files
async function processFiles(files) {
    filesData = [];
    fileTabs.innerHTML = '';

    showMessage(`Processing ${files.length} file(s)...`, 'info');

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const metadata = await extractAllMetadata(file);
        filesData.push({
            name: file.name,
            size: file.size,
            type: file.type,
            metadata: metadata
        });
    }

    displayResults();
    resultsSection.style.display = 'block';
    showMessage(`Successfully extracted metadata from ${files.length} file(s)!`, 'success');
}

// Extract EVERYTHING - CTF focused
async function extractAllMetadata(file) {
    return new Promise((resolve) => {
        const reader = new FileReader();

        reader.onload = function (e) {
            try {
                const arrayBuffer = e.target.result;
                const metadata = {};
                const bytes = new Uint8Array(arrayBuffer);

                // === FILE INFORMATION ===
                metadata['File Information'] = {
                    'File Name': file.name,
                    'File Size': formatFileSize(file.size) + ` (${file.size} bytes)`,
                    'File Type': file.type || 'Unknown',
                    'MIME Type': file.type,
                    'Last Modified': file.lastModifiedDate ? file.lastModifiedDate.toISOString() : 'Unknown',
                    'File Extension': file.name.split('.').pop().toUpperCase()
                };

                // === BINARY ANALYSIS ===
                metadata['Binary Analysis'] = {
                    'File Signature (Magic Bytes)': bytesToHex(bytes.slice(0, 16)),
                    'First 32 Bytes (Hex)': bytesToHex(bytes.slice(0, 32)),
                    'Last 32 Bytes (Hex)': bytesToHex(bytes.slice(-32)),
                    'Entropy': calculateEntropy(bytes).toFixed(4),
                    'Null Bytes Count': countNullBytes(bytes),
                    'Printable ASCII %': calculatePrintablePercent(bytes).toFixed(2) + '%'
                };

                // === STRING EXTRACTION ===
                const strings = extractStrings(bytes);
                if (strings.length > 0) {
                    metadata['Extracted Strings'] = {};
                    strings.slice(0, 50).forEach((str, idx) => {
                        metadata['Extracted Strings'][`String ${idx + 1}`] = str;
                    });
                    if (strings.length > 50) {
                        metadata['Extracted Strings']['Note'] = `... and ${strings.length - 50} more strings`;
                    }
                }

                // === EXIF DATA ===
                try {
                    const dataUrl = arrayBufferToDataURL(arrayBuffer, file.type);
                    const exifObj = piexif.load(dataUrl);

                    if (exifObj) {
                        // IFD0 (Image File Directory)
                        if (exifObj['0th'] && Object.keys(exifObj['0th']).length > 0) {
                            metadata['EXIF - IFD0 (Image)'] = processExifTags(exifObj['0th'], piexif.ImageIFD);
                        }

                        // Exif IFD (Detailed camera data)
                        if (exifObj['Exif'] && Object.keys(exifObj['Exif']).length > 0) {
                            metadata['EXIF - ExifIFD (Camera)'] = processExifTags(exifObj['Exif'], piexif.ExifIFD);
                        }

                        // GPS IFD (Location data)
                        if (exifObj['GPS'] && Object.keys(exifObj['GPS']).length > 0) {
                            metadata['EXIF - GPS (Location)'] = processExifTags(exifObj['GPS'], piexif.GPSIFD);
                        }

                        // Interop IFD
                        if (exifObj['Interop'] && Object.keys(exifObj['Interop']).length > 0) {
                            metadata['EXIF - Interop'] = processExifTags(exifObj['Interop'], piexif.InteropIFD);
                        }

                        // 1st IFD (Thumbnail)
                        if (exifObj['1st'] && Object.keys(exifObj['1st']).length > 0) {
                            metadata['EXIF - IFD1 (Thumbnail)'] = processExifTags(exifObj['1st'], piexif.ImageIFD);
                        }

                        // Thumbnail data
                        if (exifObj['thumbnail']) {
                            metadata['Thumbnail Data'] = {
                                'Has Thumbnail': 'Yes',
                                'Thumbnail Size': exifObj['thumbnail'].length + ' bytes',
                                'Thumbnail Data (First 64 bytes hex)': bytesToHex(exifObj['thumbnail'].slice(0, 64))
                            };
                        }
                    }
                } catch (exifError) {
                    metadata['EXIF Note'] = {
                        'Status': 'No EXIF data found or error extracting',
                        'Error': exifError.message
                    };
                }

                // === IMAGE PROPERTIES ===
                const img = new Image();
                img.onload = function () {
                    metadata['Image Properties'] = {
                        'Width': img.width + ' px',
                        'Height': img.height + ' px',
                        'Aspect Ratio': (img.width / img.height).toFixed(4),
                        'Megapixels': ((img.width * img.height) / 1000000).toFixed(2) + ' MP',
                        'Total Pixels': (img.width * img.height).toLocaleString()
                    };

                    // === HIDDEN DATA DETECTION ===
                    metadata['Steganography Check'] = {
                        'File Size vs Expected': compareFileSizes(file.size, img.width, img.height, file.type),
                        'Suspicious Patterns': detectSuspiciousPatterns(bytes),
                        'Comment Fields': extractComments(bytes),
                        'Trailing Data': bytes.length > 1000 ? 'Check last bytes for hidden data' : 'None detected'
                    };

                    resolve(metadata);
                };
                img.onerror = function () {
                    metadata['Image Properties'] = {
                        'Status': 'Could not load image for analysis'
                    };
                    resolve(metadata);
                };
                img.src = arrayBufferToDataURL(arrayBuffer, file.type);

            } catch (error) {
                console.error('Error extracting metadata:', error);
                resolve({
                    'Error': {
                        'Message': 'Could not extract metadata: ' + error.message
                    }
                });
            }
        };

        reader.readAsArrayBuffer(file);
    });
}

// === HELPER FUNCTIONS ===

// Process EXIF tags with ALL details
function processExifTags(tags, tagNames) {
    const result = {};
    for (let tag in tags) {
        const tagName = tagNames[tag] || `Unknown_Tag_${tag}`;
        let value = tags[tag];

        // Keep raw values for CTF analysis
        if (Array.isArray(value)) {
            if (value.length === 2 && typeof value[0] === 'number' && typeof value[1] === 'number') {
                result[tagName] = `${value[0]}/${value[1]} (${value[1] !== 0 ? (value[0] / value[1]).toFixed(4) : 'N/A'})`;
            } else {
                result[tagName] = value.join(', ');
            }
        } else if (typeof value === 'object') {
            result[tagName] = JSON.stringify(value);
        } else {
            result[tagName] = value;
        }

        // Add hex representation for suspicious values
        if (typeof value === 'string' && value.length < 100) {
            result[tagName + ' (Hex)'] = stringToHex(value);
        }
    }
    return result;
}

// Convert bytes to hex string
function bytesToHex(bytes) {
    return Array.from(bytes)
        .map(b => b.toString(16).padStart(2, '0'))
        .join(' ')
        .toUpperCase();
}

// String to hex
function stringToHex(str) {
    return Array.from(str)
        .map(c => c.charCodeAt(0).toString(16).padStart(2, '0'))
        .join(' ')
        .toUpperCase();
}

// Calculate entropy (for detecting encryption/compression)
function calculateEntropy(bytes) {
    const freq = new Array(256).fill(0);
    for (let i = 0; i < bytes.length; i++) {
        freq[bytes[i]]++;
    }

    let entropy = 0;
    for (let i = 0; i < 256; i++) {
        if (freq[i] > 0) {
            const p = freq[i] / bytes.length;
            entropy -= p * Math.log2(p);
        }
    }
    return entropy;
}

// Count null bytes
function countNullBytes(bytes) {
    let count = 0;
    for (let i = 0; i < bytes.length; i++) {
        if (bytes[i] === 0) count++;
    }
    return count;
}

// Calculate printable ASCII percentage
function calculatePrintablePercent(bytes) {
    let printable = 0;
    for (let i = 0; i < bytes.length; i++) {
        if (bytes[i] >= 32 && bytes[i] <= 126) printable++;
    }
    return (printable / bytes.length) * 100;
}

// Extract readable strings (CTF useful)
function extractStrings(bytes, minLength = 4) {
    const strings = [];
    let current = '';

    for (let i = 0; i < bytes.length; i++) {
        if (bytes[i] >= 32 && bytes[i] <= 126) {
            current += String.fromCharCode(bytes[i]);
        } else {
            if (current.length >= minLength) {
                strings.push(current);
            }
            current = '';
        }
    }

    if (current.length >= minLength) {
        strings.push(current);
    }

    return strings;
}

// Compare file sizes for steganography detection
function compareFileSizes(actualSize, width, height, type) {
    const expectedSize = width * height * 3; // Rough estimate
    const ratio = actualSize / expectedSize;

    if (ratio > 1.5) {
        return `SUSPICIOUS: File is ${ratio.toFixed(2)}x larger than expected`;
    } else if (ratio > 1.2) {
        return `WARNING: File is ${ratio.toFixed(2)}x larger than expected`;
    }
    return `Normal (${ratio.toFixed(2)}x expected size)`;
}

// Detect suspicious patterns
function detectSuspiciousPatterns(bytes) {
    const patterns = [];

    // Check for common steganography tools signatures
    const signatures = [
        { name: 'steghide', pattern: [0x73, 0x74, 0x65, 0x67, 0x68, 0x69, 0x64, 0x65] },
        { name: 'LSB', pattern: [0x4C, 0x53, 0x42] }
    ];

    // Simple pattern detection
    const str = String.fromCharCode(...bytes.slice(0, 1000));
    if (str.includes('flag{') || str.includes('FLAG{')) patterns.push('Possible flag found in data');
    if (str.includes('password') || str.includes('secret')) patterns.push('Sensitive keywords detected');

    return patterns.length > 0 ? patterns.join(', ') : 'None detected';
}

// Extract comment fields
function extractComments(bytes) {
    const str = String.fromCharCode(...bytes);
    const comments = [];

    // Look for common comment markers
    if (str.includes('Comment:')) comments.push('Comment field detected');
    if (str.includes('Description:')) comments.push('Description field detected');
    if (str.includes('<!--')) comments.push('HTML comment detected');

    return comments.length > 0 ? comments.join(', ') : 'None found';
}

// Convert ArrayBuffer to DataURL
function arrayBufferToDataURL(buffer, type) {
    const bytes = new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < bytes.length; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return 'data:' + type + ';base64,' + btoa(binary);
}

// Display results
function displayResults() {
    fileTabs.innerHTML = '';
    filesData.forEach((file, index) => {
        const tab = document.createElement('button');
        tab.className = 'file-tab' + (index === 0 ? ' active' : '');
        tab.textContent = file.name;
        tab.onclick = () => showFile(index);
        fileTabs.appendChild(tab);
    });

    showFile(0);
}

// Show specific file metadata
function showFile(index) {
    currentFileIndex = index;

    document.querySelectorAll('.file-tab').forEach((tab, i) => {
        tab.classList.toggle('active', i === index);
    });

    const file = filesData[index];
    let output = '';

    output += `<span style="color: white;">
███╗   ███╗███████╗████████╗ █████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗
████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║
██╔████╔██║█████╗     ██║   ███████║███████╗██║     ███████║██╔██╗ ██║
██║╚██╔╝██║██╔══╝     ██║   ██╔══██║╚════██║██║     ██╔══██║██║╚██╗██║
██║ ╚═╝ ██║███████╗   ██║   ██║  ██║███████║╚██████╗██║  ██║██║ ╚████║
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                                                        
           [ COMPLETE METADATA EXTRACTION - CTF EDITION ]
           [ File: ${file.name} ]
           [ Size: ${formatFileSize(file.size)} ]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
</span>
`;

    for (let section in file.metadata) {
        const sectionData = file.metadata[section];

        if (Object.keys(sectionData).length > 0) {
            output += `\n▼ ${section}\n`;
            output += `${'─'.repeat(75)}\n`;

            const maxKeyLength = Math.max(...Object.keys(sectionData).map(k => k.length));

            for (let key in sectionData) {
                const paddedKey = key.padEnd(maxKeyLength + 2);
                output += `  ${paddedKey}: ${sectionData[key]}\n`;
            }
        }
    }

    output += `\n${'━'.repeat(75)}\n`;
    output += `[ END OF SCAN ]\n`;

    metadataOutput.innerHTML = output;
}

// Copy all metadata
function copyAllMetadata() {
    const text = metadataOutput.textContent;
    navigator.clipboard.writeText(text).then(() => {
        showMessage('Metadata copied to clipboard!', 'success');
    }).catch(() => {
        showMessage('Failed to copy to clipboard', 'error');
    });
}

// Download metadata
function downloadMetadata() {
    const file = filesData[currentFileIndex];
    const text = metadataOutput.textContent;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${file.name}_metascan.txt`;
    link.click();
    URL.revokeObjectURL(url);
    showMessage('Metadata downloaded!', 'success');
}

// Clear all
function clearAll() {
    filesData = [];
    currentFileIndex = 0;
    fileInput.value = '';
    fileTabs.innerHTML = '';
    metadataOutput.textContent = '';
    resultsSection.style.display = 'none';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i];
}

// Show message
function showMessage(text, type = 'success') {
    const existingMessage = document.querySelector('.message');
    if (existingMessage) existingMessage.remove();

    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.innerHTML = `
        <span>${type === 'success' ? '✓' : type === 'error' ? '✗' : type === 'info' ? 'ℹ' : '⚠'}</span>
        <span>${text}</span>
    `;

    const container = document.querySelector('.container');
    container.insertBefore(message, container.firstChild);

    setTimeout(() => {
        message.style.opacity = '0';
        setTimeout(() => message.remove(), 300);
    }, 3000);
}

// Initialize
console.log('🔍 MetaScan v1.0 - CTF Edition loaded!');
console.log('📸 Ready for complete metadata extraction');
