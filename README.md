# 🔍 MetaScan - Local Image Forensics Tool

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MetaScan** is a comprehensive web-based image forensics tool designed for local metadata extraction and analysis. Built with privacy in mind, all processing happens locally on your machine without any external network calls.

## ✨ Key Features

### 🔒 Privacy-First Architecture
- **100% Local Processing** - No data sent to external servers
- **Client-side analysis** - All computations performed locally
- **Browser-based interface** - No server-side storage

### 📊 Comprehensive Metadata Extraction
- **EXIF Data**: Camera settings, timestamps, orientation, ISO, exposure details
- **GPS Coordinates**: Embedded location data in decimal degrees format
- **XMP/IPTC Data**: Extended metadata with best-effort parsing
- **Embedded Thumbnails**: Extracted image previews

### 🔐 Forensic Analysis
- **Cryptographic Hashes**: MD5, SHA1, SHA256 for integrity verification
- **Shannon Entropy**: Randomness indicator for detecting alterations
- **LSB Variance**: Least Significant Bit analysis for steganography detection
- **Anomaly Detection**: Automated flagging of suspicious findings

### 🎨 User-Friendly Interface
- **Drag & Drop Upload**: Intuitive file handling
- **Responsive Design**: Works on desktop and mobile devices
- **Tabbed Navigation**: Organized metadata presentation
- **Export Options**: JSON download and thumbnail extraction
- **Basic Hex Viewer**: Raw byte inspection

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 16+** (for frontend development server)
- **Modern web browser**

### Installation

#### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/dustin04x/Metascan.git
cd Metascan/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests (optional)
pytest test_app.py -v
```

#### 2. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install
```

### Running the Application

#### Start Backend
```bash
# From backend directory (with virtual environment activated)
python app.py

# Alternative using uvicorn directly
uvicorn app:app --host 127.0.0.1 --port 8000 --reload

# Backend will be available at http://localhost:8000
```

#### Start Frontend
```bash
# From frontend directory
npm run dev

# Frontend will be available at http://localhost:5173
```

#### Access the Application
Open your browser and navigate to **http://localhost:5173** to start analyzing images.

## 📖 API Documentation

### Endpoints

#### POST `/api/inspect`
Analyzes an uploaded image file and returns comprehensive metadata.

**Request:**
```bash
curl -X POST -F "file=@image.jpg" http://localhost:8000/api/inspect
```

**Success Response:**
```json
{
  "success": true,
  "data": {
    "file_info": {
      "filename": "photo.jpg",
      "size_bytes": 245600,
      "mime": "image/jpeg",
      "format": "JPEG",
      "width": 1920,
      "height": 1440
    },
    "exif": {
      "datetime_original": "2024:01:15 14:30:22",
      "make": "Canon",
      "model": "Canon EOS 5D Mark IV",
      "iso": 400,
      "f_number": "f/2.8",
      "exposure": "1/500",
      "focal_length": "85.0mm"
    },
    "gps": {
      "lat": 40.7128,
      "lon": -74.006,
      "alt": 10.5
    },
    "hashes": {
      "md5": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
      "sha1": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
      "sha256": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z..."
    },
    "entropy": 7.452,
    "lsb_variance": 0.2341,
    "anomalies": [
      "GPS coordinates embedded: 40.7128, -74.0060",
      "Edited with: Adobe Lightroom"
    ]
  }
}
```

#### GET `/health`
Simple health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🔧 Configuration

### Backend Configuration
Located in `backend/app.py`:

```python
# File size limit (default: 50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

# CORS origins
allow_origins = ["http://localhost:5173"]

# Server settings (uvicorn.run() call)
host = "127.0.0.1"
port = 8000
```

### Frontend Configuration
Located in `frontend/app.js`:

```javascript
// Backend API endpoint
const API_BASE_URL = "http://localhost:8000";

// Tab names and display settings
// Result formatting options
```

## 📁 Project Structure

```
Metascan/
├── backend/
│   ├── app.py              # FastAPI main application
│   ├── requirements.txt     # Python dependencies
│   └── test_app.py          # Unit tests
├── frontend/
│   ├── index.html           # Main HTML page
│   ├── app.js              # Vanilla JavaScript logic
│   ├── styles.css          # All styles consolidated
│   └── package.json        # http-server dependency
├── README.md               # This file
├── .gitignore             # Git ignore rules
├── .env.example           # Environment variables example
└── START_METASCAN.bat     # Windows startup script
```

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
cd backend
pytest test_app.py -v

# Run with coverage report
pytest test_app.py --cov=app --cov-report=html

# Run specific test categories
pytest test_app.py -k "hash"      # Test hash calculations
pytest test_app.py -k "entropy"   # Test entropy calculations
pytest test_app.py -k "lsb"       # Test LSB variance detection
```

### Test Coverage Areas
- Hash calculation consistency and correctness
- Entropy computation (uniform, random, repeating patterns)
- LSB variance detection algorithms
- Anomaly detection logic (GPS, missing EXIF, high entropy)

## 🚀 Production Deployment

### Backend (Production)
```bash
# Install Gunicorn
pip install gunicorn

# Run with production settings
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Frontend (Production)
```bash
# The frontend requires no build step
# Serve with any static web server:

# Using Python
python -m http.server 5173 --directory frontend

# Using Node.js http-server
npx http-server frontend -p 5173

# Or use nginx, Apache, etc.
```

## Building for Production

### Backend

```bash
# No special build needed; run with Gunicorn or similar:
pip install gunicorn
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Frontend

The frontend is vanilla HTML/CSS/JavaScript and requires no build step.
Simply serve the `frontend/` folder with any static web server:

```bash
# Using Node.js http-server:
npm run dev

# Or with any other server (nginx, Apache, Python, etc.)
python -m http.server 5173 --directory frontend
```


## 🔍 Troubleshooting

### Common Issues

#### CORS Error
**Issue**: Frontend cannot connect to backend
**Solution**: Ensure backend is running on `http://localhost:8000` and check CORS configuration

#### Python Magic Installation (Windows)
**Issue**: `python-magic` not found
**Solution**: The requirements include `python-magic-bin` for Windows. If issues persist:
```bash
pip install python-magic-bin
```

#### No EXIF Data
**Issue**: Images show no metadata
**Explanation**: Some images (screenshots, web graphics) don't contain EXIF data. This is normal and will be flagged as an anomaly.

#### Upload Failures
**Issue**: Large images fail to upload
**Solution**: Increase file size limit in `backend/app.py`:
```python
if len(file_bytes) > 50 * 1024 * 1024:  # Change this value
```

## 🎯 Use Cases

- **Digital Forensics**: Analyze images for legal/investigative purposes
- **Privacy Assessment**: Identify embedded metadata that might reveal personal information
- **Image Verification**: Verify image integrity through cryptographic hashes
- **Steganography Detection**: Detect hidden data using LSB analysis
- **Educational Research**: Learn about image metadata and digital forensics

## 🔒 Privacy Statement

This application processes all images locally on your machine. **No images, metadata, or analysis results are sent to external servers**. However, note that:

- Metadata remains in your browser session until refresh
- Your browser may cache image data
- For production use, implement explicit privacy policies

## 📝 Sample Testing

To test the application:
1. Use any JPEG or PNG image
2. For GPS data testing, use photos from smartphones or GPS-enabled cameras
3. Download sample forensic images from camera manufacturer test suites

## 🤝 Contributing

1. Test your changes locally with `pytest` and browser DevTools
2. Check error logs in both backend terminal and browser console
3. Ensure all dependencies are correctly installed
4. Submit issues and improvements via GitHub

## 📄 License

This project is provided as-is for educational and research purposes. See [LICENSE](LICENSE) for more details.

## 🛠️ Technologies Used

- **Backend**: Python 3.11+, FastAPI, Uvicorn
- **Image Processing**: Pillow, piexif, exifread
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **Development**: Node.js, http-server, pytest

---

**⚡ Start analyzing images locally with MetaScan - your privacy-focused forensics solution!**

