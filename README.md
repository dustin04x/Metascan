# MetaScan

A web application for local image forensics metadata inspection. Analyzes images for EXIF data, GPS coordinates, file hashes, entropy, and other forensic indicators—all processed locally without external network calls.

## Features

- **Local Processing**: All analysis happens on your machine
- **Comprehensive Metadata Extraction**:
  - EXIF (camera make, model, datetime, exposure, ISO, focal length, etc.)
  - GPS coordinates (decimal degrees format)
  - XMP and IPTC (best-effort extraction)
  - Embedded thumbnails
- **Forensic Analysis**:
  - Cryptographic hashes (MD5, SHA1, SHA256)
  - Shannon entropy (randomness indicator)
  - LSB (Least Significant Bit) variance detection
  - Anomaly detection (suspicious findings)
- **User-Friendly Interface**:
  - Drag-and-drop file upload
  - Responsive tabbed metadata view
  - JSON export and thumbnail download
  - Simple hex viewer stub

## Privacy

This application does **not** send your images or metadata to any external server. All processing is performed locally on your machine. However:

- **Local storage**: The metadata is retained in your browser session until you refresh.
- **Browser cache**: Your browser may cache the image data.
- For production use, consider adding explicit privacy policies and terms.

## Project Structure

```
MetaScan/
├── backend/
│   ├── app.py                 # FastAPI main application
│   ├── requirements.txt        # Python dependencies
│   └── test_app.py           # Unit tests
├── frontend/
│   ├── index.html             # Main HTML page
│   ├── app.js                 # Vanilla JavaScript
│   ├── styles.css             # All styles (consolidated)
│   ├── package.json           # http-server dependency
│   └── vite.config.js         # (deprecated - using http-server now)
├── README.md                  # This file
└── .gitignore
```

## Prerequisites

- **Python 3.11+**
- **Node.js 16+** and npm/yarn
- Recent versions of pip

## Installation

### Backend Setup

1. **Create a virtual environment** (recommended):
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests** (optional):
   ```bash
   pytest test_app.py -v
   ```

### Frontend Setup

1. **Install dependencies** (http-server for serving static files):
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

### Start Backend

From the `backend` directory:

```bash
# With virtual environment activated:
python app.py

# or using uvicorn directly:
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Backend will be available at `http://localhost:8000`

Health check: `curl http://localhost:8000/health`

### Start Frontend

From the `frontend` directory:

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

Note: The frontend is vanilla HTML/CSS/JavaScript with no build step needed.

### Open in Browser

Navigate to `http://localhost:5173` and upload an image to analyze.

## API Documentation

### POST /api/inspect

Analyzes an image file and returns forensic metadata.

**Request**:
```bash
curl -X POST -F "file=@image.jpg" http://localhost:8000/api/inspect
```

**Response** (Success - 200):
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
      "orientation": 1,
      "iso": 400,
      "f_number": "f/2.8",
      "exposure": "1/500",
      "focal_length": "85.0mm",
      "software": null,
      "other_tags": { ... }
    },
    "gps": {
      "lat": 40.7128,
      "lon": -74.0060,
      "alt": 10.5
    },
    "xmp_data": { ... },
    "iptc_data": { ... },
    "thumbnail_base64": "iVBORw0KGgoAAAANSUhEU...",
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

**Response** (Error - 400/500):
```json
{
  "success": false,
  "error": "Error message",
  "detail": "Human-readable detail"
}
```

### GET /health

Simple health check endpoint.

## Testing

### Backend Unit Tests

```bash
cd backend
pytest test_app.py -v

# With coverage:
pytest test_app.py --cov=app --cov-report=html
```

**Test Coverage**:
- Hash calculation consistency and correctness
- Entropy computation (uniform, random, repeating patterns)
- LSB variance detection
- Anomaly detection (high entropy, GPS, missing EXIF)

## Dependencies

### Backend
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **Pillow**: Image processing
- **piexif**: EXIF extraction and manipulation
- **exifread**: Alternative EXIF reader
- **python-magic-bin**: MIME type detection
- **pytest**: Testing framework

### Frontend
- **Vanilla HTML/CSS/JavaScript**: Pure vanilla implementation with no framework
- **http-server**: Static file serving

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

## Deployment to GitHub Pages

The frontend is automatically deployed to GitHub Pages when you push to the main branch.

### Setup (One-time)

1. Go to your GitHub repository settings
2. Navigate to **Settings → Pages**
3. Set **Source** to "Deploy from a branch"
4. Set **Branch** to `main` and folder to `/ (root)`
5. Click **Save**

### Auto-Deploy with GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically:
- Installs dependencies
- Builds the frontend
- Deploys to GitHub Pages on every push to `main`

Your frontend will be available at: `https://dustin04x.github.io/Metascan/`

### Using the Deployed Frontend

The deployed frontend needs a backend to function. You have two options:

**Option 1: Use a Local Backend**
1. Clone the repository locally
2. Follow the "Running the Application" section above
3. The local frontend will connect to your local backend (http://localhost:8000)

**Option 2: Deploy Backend Separately** (Advanced)
- Deploy the backend to a service like Heroku, AWS, DigitalOcean, etc.
- Modify `frontend/app.js` line with the API endpoint to point to your deployed backend

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

## Known Limitations & Future Improvements

- **Hex viewer** is currently a stub (requires backend integration to stream raw bytes)
- **XMP/IPTC extraction** is basic; complex nested structures may not parse fully
- **GPS reverse geocoding** is not implemented (opt-in, requires external service)
- **Performance**: Large images (>50MB) are rejected; adjust limit as needed
- **Format support**: Primarily tested on JPEG and PNG; TIFF, WebP support via Pillow

## Configuration

### Backend

Edit `backend/app.py` to customize:
- `MAX_FILE_SIZE`: Change the file size limit (currently 50MB)
- CORS origins: Modify `allow_origins` for production
- Host/port: Change in `uvicorn.run()` call

### Frontend

Edit `frontend/app.js` to customize:
- Backend API endpoint (currently `http://localhost:8000`)
- Tab names and behavior
- Result display formatting

## Troubleshooting

**Q: CORS error when connecting frontend to backend**
```
A: Ensure backend is running on http://localhost:8000 and frontend proxy 
   is configured correctly in vite.config.js
```

**Q: "python-magic" not found on Windows**
```
A: The requirements.txt includes python-magic-bin (Windows binary version).
   If issues persist, install: pip install python-magic-bin
```

**Q: No EXIF data on some images**
```
A: Some images (screenshots, web graphics) may not include EXIF.
   This is normal and flagged as an anomaly.
```

**Q: Large images fail to upload**
```
A: Default limit is 50MB. Increase in backend app.py:
   if len(file_bytes) > 50 * 1024 * 1024:  # Change this
```

## Sample Image for Testing

To test the application, use any JPEG or PNG image. For images with GPS:
- Use photos taken with a smartphone or GPS-enabled camera
- Or use the sample images online (e.g., from camera manufacturer test suites)

## License

This project is provided as-is for educational and research purposes.

## Support & Contributing

For issues, improvements, or contributions:
1. Test locally with `pytest` and browser DevTools
2. Check error logs in console (backend terminal and browser console)
3. Ensure dependencies are installed correctly

---

**Made with ❤️ for digital forensics and metadata analysis.**
