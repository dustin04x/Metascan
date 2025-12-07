# MetaScan - Complete Metadata Extraction Tool

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-00cc00)
![License](https://img.shields.io/badge/license-MIT-00cc00)
![Platform](https://img.shields.io/badge/platform-Web-00cc00)
![Privacy](https://img.shields.io/badge/privacy-100%25%20Client--Side-00cc00)

**CTF-focused metadata extraction tool - Extract EVERYTHING from images**

[Features](#-features) • [Usage](#-usage) • [CTF Applications](#-ctf-applications) • [Deploy](#-deployment)

</div>

---

## 🎯 Features

### Core Extraction
- ✅ **Complete EXIF Data** - All IFD sections (IFD0, ExifIFD, GPS, Interop, IFD1)
- ✅ **Binary Analysis** - Magic bytes, entropy, hex dumps
- ✅ **String Extraction** - All readable strings (min 4 chars)
- ✅ **Steganography Detection** - File size analysis, pattern detection
- ✅ **Hidden Data Checks** - Comments, trailing data, suspicious patterns
- ✅ **Thumbnail Analysis** - Extract and analyze embedded thumbnails
- ✅ **GPS Location** - Coordinates with Google Maps integration
- ✅ **Image Properties** - Dimensions, aspect ratio, megapixels

### CTF-Specific
- 🔍 **Flag Detection** - Searches for `flag{` and `FLAG{` patterns
- 🔍 **Entropy Calculation** - Detect encryption/compression
- 🔍 **Hex Values** - All EXIF fields shown with hex representation
- 🔍 **Null Byte Count** - Detect padding/hidden data
- 🔍 **Printable ASCII %** - Analyze file composition
- 🔍 **First/Last Bytes** - Check file headers and footers

### User Experience
- 🎨 **Hacker Aesthetic** - Dark theme with green terminal styling
- 🎨 **ASCII Art Header** - Cool MetaScan logo in white
- 📋 **Copy to Clipboard** - One-click copy all metadata
- 💾 **Download Results** - Save as .txt file
- 📁 **Multiple Files** - Process multiple images with tabs
- 🔒 **100% Client-Side** - No uploads, complete privacy

---

## 🚀 Usage

### Quick Start

1. Open `index.html` in your browser
2. Drag & drop an image or click "SELECT FILES"
3. View comprehensive metadata extraction
4. Copy or download results

### What Gets Extracted

```
███╗   ███╗███████╗████████╗ █████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗
████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║
██╔████╔██║█████╗     ██║   ███████║███████╗██║     ███████║██╔██╗ ██║
██║╚██╔╝██║██╔══╝     ██║   ██╔══██║╚════██║██║     ██╔══██║██║╚██╗██║
██║ ╚═╝ ██║███████╗   ██║   ██║  ██║███████║╚██████╗██║  ██║██║ ╚████║
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

▼ File Information
▼ Binary Analysis
▼ Extracted Strings
▼ EXIF - IFD0 (Image)
▼ EXIF - ExifIFD (Camera)
▼ EXIF - GPS (Location)
▼ Image Properties
▼ Steganography Check
```

---

## 🎮 CTF Applications

### Forensics Challenges
- Extract hidden flags from image metadata
- Analyze file signatures and magic bytes
- Detect steganography tools (steghide, LSB)
- Find embedded data in EXIF comments

### OSINT Challenges
- GPS coordinates from photos
- Camera make/model identification
- Timestamp analysis
- Software version detection

### Stego Challenges
- File size anomaly detection
- Entropy analysis for encryption
- String extraction for hidden messages
- Thumbnail data analysis

### Example CTF Scenarios

**Scenario 1: Hidden Flag in EXIF**
```
Upload image → Check "Extracted Strings" → Find flag{...}
```

**Scenario 2: GPS Coordinates**
```
Upload image → Check "EXIF - GPS" → Get coordinates → Google Maps
```

**Scenario 3: Steganography Detection**
```
Upload image → Check "Steganography Check" → Suspicious file size
```

---

## 🛠️ Technical Details

### Technologies
- **HTML5** - Structure
- **CSS3** - Hacker green theme
- **Vanilla JavaScript** - No frameworks
- **piexifjs** - EXIF extraction library

### File Structure
```
exif_viewer/
├── index.html          # Main application
├── style.css           # Hacker green theme
├── script.js           # Extraction logic
└── README.md           # Documentation
```

### Extraction Methods

**EXIF Data**
- Uses piexifjs library
- Extracts all IFD sections
- Includes hex values for analysis

**Binary Analysis**
- File signature detection
- Entropy calculation (Shannon entropy)
- Byte distribution analysis

**String Extraction**
- Scans for printable ASCII (32-126)
- Minimum 4 character strings
- Shows up to 50 strings

**Steganography Detection**
- File size vs expected size ratio
- Pattern matching for tool signatures
- Comment field extraction
- Trailing data detection

---

## 🎨 Design

### Color Scheme
- **Background**: Pure black (#000000)
- **Primary**: Dark green (#00cc00)
- **Accent**: White (#ffffff) for ASCII art
- **Borders**: Transparent green (#00cc0033)

### Features
- Sticky navbar with social links
- Responsive design
- Terminal-style output
- Monospace fonts throughout
- Smooth hover effects

---

## 🔒 Privacy & Security

### Client-Side Processing
- ✅ All processing in browser
- ✅ No server uploads
- ✅ No data collection
- ✅ No tracking/analytics
- ✅ Works offline after first load

### Use Cases
- ✅ CTF competitions
- ✅ Digital forensics training
- ✅ OSINT investigations
- ✅ Privacy-conscious metadata checking
- ✅ Educational purposes

---

## 📦 Deployment

### Local Usage
Simply open `index.html` in any modern browser.

### Web Hosting
Upload to any static hosting:
- **GitHub Pages** - Free hosting
- **Netlify** - Automatic deployments
- **Vercel** - Fast CDN
- **Any web server** - No backend needed

### Requirements
- Modern browser (Chrome, Firefox, Edge, Safari)
- JavaScript enabled
- Internet connection (for piexifjs CDN on first load)

---

## 🎓 Educational Use

### Learning Objectives
- Understand image metadata structure
- Learn EXIF data analysis
- Practice steganography detection
- Develop forensics skills
- Master CTF techniques

### Recommended For
- CTF players
- Digital forensics students
- Security researchers
- OSINT practitioners
- Privacy advocates

---

## 🤝 Contributing

This is an open-source educational tool. Contributions welcome!

### Ideas for Enhancement
- Support for more file formats (PDF, Office docs)
- Advanced steganography detection
- Metadata removal/modification
- Batch processing
- Export to JSON/CSV

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

## 🙏 Credits

- **Developer**: [dustin04x](https://github.com/dustin04x)
- **Library**: [piexifjs](https://github.com/hMatoba/piexifjs)
- **Inspiration**: ExifTool by Phil Harvey

---

## 🔗 Links

- **GitHub**: [dustin04x](https://github.com/dustin04x)
- **LinkedIn**: [dustin04x](https://linkedin.com/in/dustin04x)

---

<div align="center">

**MetaScan v1.0 - Extract Everything**

Made with 💚 for the CTF community

</div>
