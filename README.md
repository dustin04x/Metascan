# 🔍 MetaScan

<div align="center">

**Advanced Image Metadata Extraction & Forensics Tool**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-1.0-blue.svg)](#)
[![Client-Side](https://img.shields.io/badge/100%25-Client--Side-green.svg)](#)
[![CTF Ready](https://img.shields.io/badge/CTF-Ready-red.svg)](#)

*A comprehensive web-based image forensics tool designed for privacy-conscious metadata extraction and analysis*

[🚀 **Live Demo**](https://dustin04x.github.io/Metascan/) • [💻 **GitHub Repository**](https://github.com/dustin04x/Metascan) • [👤 **Developer**](https://github.com/dustin04x)

</div>

---

## ✨ What is MetaScan?

MetaScan is a **complete metadata extraction tool** that operates entirely **client-side** within your browser. Designed with privacy and CTF competitions in mind, it allows you to analyze image files without any server uploads, ensuring complete confidentiality of your data.

### 🎯 Perfect For:
- 🔒 **CTF Players** - Extract hidden flags and analyze steganography
- 🕵️ **Digital Forensics** - Comprehensive image analysis and investigation
- 🌍 **OSINT Practitioners** - Location data extraction and device identification
- 🎓 **Security Researchers** - Metadata analysis and privacy auditing
- 🔐 **Privacy Advocates** - Check images for hidden metadata before sharing

---

## 🌟 Key Features

### 🔍 **Core Extraction Capabilities**
- **📸 Complete EXIF Data**: All IFD sections (IFD0, ExifIFD, GPS, Interop, IFD1)
- **🧮 Binary Analysis**: Magic bytes, entropy calculation, hex dumps
- **📝 String Extraction**: All readable strings (minimum 4 characters)
- **🎭 Steganography Detection**: Pattern detection and file size analysis
- **📍 GPS Location**: Coordinates with Google Maps integration
- **📐 Image Properties**: Dimensions, aspect ratio, megapixels

### 🚩 **CTF-Specific Features**
- **Flag Detection**: Automatically searches for `flag{` and `FLAG{` patterns
- **Entropy Analysis**: Detect encryption/compression in files
- **Hex Values**: All EXIF fields with hex representation
- **Null Byte Detection**: Find padding and hidden data
- **File Signature Analysis**: Magic bytes and header inspection

### 🎨 **User Experience**
- **💻 Hacker Aesthetic**: Dark theme with green terminal styling
- **📋 One-Click Actions**: Copy to clipboard, download results, clear output
- **📁 Multi-File Support**: Process multiple images with tabs
- **📱 Responsive Design**: Works perfectly on all devices
- **🔒 100% Privacy**: No uploads, complete local processing

---

## 🛠️ Supported File Formats

<div align="center">

| Format | Extension | Metadata Support | Binary Analysis | Flag Detection |
|--------|-----------|------------------|-----------------|----------------|
| **JPEG** | `.jpg`, `.jpeg` | ✅ Full EXIF | ✅ Complete | ✅ Active |
| **PNG** | `.png` | ✅ EXIF/XMP | ✅ Complete | ✅ Active |
| **WebP** | `.webp` | ✅ EXIF | ✅ Complete | ✅ Active |
| **HEIC** | `.heic` | ✅ EXIF | ✅ Complete | ✅ Active |
| **TIFF** | `.tiff`, `.tif` | ✅ Full EXIF | ✅ Complete | ✅ Active |

</div>

---

## 🚀 Quick Start

### Option 1: Web Version (Recommended)
```bash
# Just open in your browser - no installation required!
🌐 Visit: https://dustin04x.github.io/Metascan/
```

### Option 2: Local Setup
```bash
# Clone the repository
git clone https://github.com/dustin04x/Metascan.git

# Navigate to the project
cd Metascan/exif_viewer/

# Open in your browser
open index.html  # macOS
# or
start index.html  # Windows
# or
xdg-open index.html  # Linux
```

### 📋 Usage Steps
1. **🎯 Select**: Drag & drop an image or click "SELECT FILES"
2. **⚡ Analyze**: Watch real-time metadata extraction
3. **📊 Review**: Explore comprehensive analysis results
4. **💾 Export**: Copy to clipboard or download as `.txt` file

---

## 🎨 Design Philosophy

MetaScan features a **terminal-inspired hacker aesthetic** designed for the security community:

<div align="center">

```css
🎨 Color Scheme:
  Background:  Pure Black (#000000)
  Primary:     Dark Green (#00cc00)
  Accent:      White (#ffffff) for ASCII art
  Borders:     Transparent Green (#00cc0033)
```

</div>

- **🌑 Dark Theme**: Easy on the eyes during long analysis sessions
- **💚 Terminal Green**: Classic hacker aesthetic with modern touch
- **⚡ Monospace Fonts**: Perfect for code and technical data
- **🎯 ASCII Art Logo**: Eye-catching header with styling flair

---

## 🏗️ Technical Architecture

### 🧱 Built With
- **📄 HTML5** - Modern web standards
- **🎨 CSS3** - Advanced styling and animations
- **⚡ Vanilla JavaScript** - Pure JS for maximum performance
- **📚 piexifjs** - EXIF data extraction library

### 🔧 Technical Details
```javascript
// Core Capabilities
- Client-side processing (100% browser-based)
- No server dependencies
- Real-time metadata parsing
- Advanced binary analysis
- Entropy calculation (Shannon entropy)
- String pattern matching
- Steganography detection algorithms
```

### 📊 Performance Metrics
- **📈 Language Distribution**:
  - JavaScript: 63.1%
  - CSS: 26.3%
  - HTML: 10.6%

---

## 🎯 CTF Use Cases

### 🔍 **Forensics Challenges**
```bash
# Hidden Flag Detection
Scenario: Extract hidden flags from image metadata
Method: Upload → Check "Extracted Strings" → Find flag{...}

# GPS Coordinates Analysis  
Scenario: Location data from photos
Method: Upload → Check "EXIF - GPS" → Get coordinates → Google Maps

# Steganography Detection
Scenario: Hidden data in file structure
Method: Upload → Check "Steganography Check" → Analyze anomalies
```

### 🕵️ **OSINT Applications**
- **📍 Location Intelligence**: Extract GPS coordinates for mapping
- **📱 Device Fingerprinting**: Camera make/model identification
- **⏰ Timeline Analysis**: Timestamp and software version detection
- **🔍 Pattern Recognition**: Hidden data pattern analysis

---

## 🏆 Example Output

When you analyze an image, MetaScan provides:

### 📋 **File Information**
```
📁 Filename: image.jpg
📏 File Size: 2.4 MB
🎯 Format: JPEG
📐 Dimensions: 1920x1080 (2.07 MP)
```

### 🧮 **Binary Analysis**
```
🔢 Entropy: 7.82/8.0 (High - likely encrypted/compressed)
🔮 Magic Bytes: FF D8 FF E1 (JPEG Exif)
📊 Printable ASCII: 45.2%
🔢 Null Bytes: 1,247
```

### 📍 **GPS Data**
```
🌍 Latitude: 40.7128° N
🌍 Longitude: 74.0060° W
📅 Date: 2024-12-07 10:30:15
🗺️ Maps Link: [Open in Google Maps](https://maps.google.com/?q=40.7128,-74.0060)
```

### 🚩 **Flag Detection**
```
🎯 Potential Flags Found:
  - flag{CTF_m3t4d4t4_3xtr4ct10n_succ3ss}
```

---

## 🔒 Privacy & Security

### 🛡️ **100% Client-Side Processing**
- ✅ **No Server Uploads**: All processing happens locally
- ✅ **No Data Collection**: Zero tracking or analytics
- ✅ **No External Calls**: Complete offline operation
- ✅ **Privacy First**: Your files never leave your device

### 🔐 **Security Features**
```bash
# Data Protection
🛡️ Client-side processing only
🔒 No file transmission to servers
📊 No user tracking or analytics
💾 No data storage or logging
🌐 Works offline after first load
```

---

## 📚 Educational Value

### 🎓 **Learning Objectives**
- Understand image metadata structure
- Learn EXIF data analysis techniques
- Practice steganography detection
- Develop digital forensics skills
- Master CTF methodologies

### 👥 **Target Audience**
- 🔍 **CTF Players**: Perfect for forensics challenges
- 🎓 **Students**: Digital forensics and security courses
- 🔬 **Researchers**: Academic and commercial research
- 🌍 **OSINT Practitioners**: Open source intelligence gathering
- 🔐 **Privacy Advocates**: Metadata awareness and protection

---

## 🤝 Contributing

We welcome contributions from the security community! Here's how you can help:

### 💡 **Ideas for Enhancement**
- 🔧 **More File Formats**: PDF, Office documents, video files
- 🚀 **Advanced Detection**: More sophisticated steganography tools
- ⚙️ **Batch Processing**: Multiple file analysis
- 📊 **Export Options**: JSON, CSV, XML formats
- 🎨 **UI Improvements**: Enhanced visualizations

### 🛠️ **Development Setup**
```bash
# Fork and clone
git clone https://github.com/dustin04x/Metascan.git

# Create feature branch
git checkout -b feature/amazing-feature

# Make your changes
# Test thoroughly

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Create Pull Request
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **💚 piexifjs Library**: Powerful EXIF data extraction
- **🎯 ExifTool Inspiration**: Phil Harvey's legendary tool
- **🌟 Security Community**: Continuous feedback and support
- **🎨 Design Inspiration**: Terminal aesthetics and hacker culture

---

## 📞 Contact & Support

<div align="center">

**🔗 Connect with the Developer**

[![GitHub](https://img.shields.io/badge/GitHub-dustin04x-181717?style=flat&logo=github)](https://github.com/dustin04x)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Skander%20Wali-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/skander-wali-901040391/)

</div>

---

## ⭐ Show Your Support

If MetaScan has been helpful in your CTF journey or security research, please consider:

- ⭐ **Starring** the repository
- 🐛 **Reporting** bugs and issues
- 💡 **Suggesting** new features
- 🤝 **Contributing** to the codebase
- 📢 **Sharing** with the security community

---

<div align="center">

**Made with ❤️ by [dustin04x](https://github.com/dustin04x) for the security community**

*Empowering digital forensics through open source innovation*

[🚀 **Try MetaScan Now**](https://dustin04x.github.io/Metascan/) • [📋 **Report Issues**](https://github.com/dustin04x/Metascan/issues) • [💬 **Discussions**](https://github.com/dustin04x/Metascan/discussions)

</div>

---

> **💡 Pro Tip**: MetaScan works perfectly offline after the initial load. Bookmark it for your next CTF competition!

```bash
__/\\\\____________/\\\\__/\\\\\\\\\\\\\\\__/\\\\\\\\\\\\\\\_____/\\\\\\\\\__________________/\\\\\\\\\\\__________/\\\\\\\\\_____/\\\\\\\\\_____/\\\\\_____/\\\_        
 _\/\\\\\\________/\\\\\\_\/\\\///////////__\///////\\\/////____/\\\\\\\\\\\\\______________/\\\/////////\\\_____/\\\////////____/\\\\\\\\\\\\\__\/\\\\\\___\/\\\_       
  _\/\\\//\\\____/\\\//\\\_\/\\\___________________\/\\\________/\\\/////////\\\____________\//\\\______\///____/\\\/____________/\\\/////////\\\_\/\\\/\\\__\/\\\_      
   _\/\\\\///\\\/\\\/_\/\\\_\/\\\\\\\\\\\___________\/\\\_______\/\\\_______\/\\\_____________\////\\\__________/\\\_____________\/\\\_______\/\\\_\/\\\//\\\_\/\\\_     
    _\/\\\__\///\\\/___\/\\\_\/\\\///////____________\/\\\_______\/\\\\\\\\\\\\\\\________________\////\\\______\/\\\_____________\/\\\\\\\\\\\\\\\_\/\\\\//\\\\/\\\_    
     _\/\\\____\///_____\/\\\_\/\\\___________________\/\\\_______\/\\\/////////\\\___________________\////\\\___\//\\\____________\/\\\/////////\\\_\/\\\_\//\\\/\\\_   
      _\/\\\_____________\/\\\_\/\\\___________________\/\\\_______\/\\\_______\/\\\____________/\\\______\//\\\___\///\\\__________\/\\\_______\/\\\_\/\\\__\//\\\\\\_  
       _\/\\\_____________\/\\\_\/\\\\\\\\\\\\\\\_______\/\\\_______\/\\\_______\/\\\___________\///\\\\\\\\\\\/______\////\\\\\\\\\_\/\\\_______\/\\\_\/\\\___\//\\\\\_ 
        _\///______________\///__\///////////////________\///________\///________\///______________\///////////___________\/////////__\///________\///__\///_____\/////__
```
