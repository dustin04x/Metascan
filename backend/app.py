"""
MetaScan Backend - FastAPI image forensics metadata inspector
"""
import os
import sys
import hashlib
import base64
from io import BytesIO
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import magic
from PIL import Image
from PIL.ExifTags import TAGS as EXIF_TAGS
import piexif

# Optional imports - gracefully handle missing packages
try:
    import exifread
except ImportError:
    exifread = None

try:
    import pyheif
except ImportError:
    pyheif = None


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class FileInfo:
    filename: str
    size_bytes: int
    mime: str
    format: str
    width: Optional[int] = None
    height: Optional[int] = None


@dataclass
class ExifData:
    datetime_original: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    orientation: Optional[int] = None
    exposure: Optional[str] = None
    f_number: Optional[str] = None
    iso: Optional[int] = None
    focal_length: Optional[str] = None
    software: Optional[str] = None
    other_tags: Dict[str, Any] = None

    def __post_init__(self):
        if self.other_tags is None:
            self.other_tags = {}


@dataclass
class GPSData:
    lat: Optional[float] = None
    lon: Optional[float] = None
    alt: Optional[float] = None


@dataclass
class ForensicResult:
    file_info: FileInfo
    exif: ExifData
    gps: Optional[GPSData]
    xmp_data: Dict[str, Any]
    iptc_data: Dict[str, Any]
    thumbnail_base64: Optional[str] = None
    hashes: Dict[str, str] = None
    entropy: float = 0.0
    lsb_variance: float = 0.0
    anomalies: List[str] = None

    def __post_init__(self):
        if self.hashes is None:
            self.hashes = {}
        if self.anomalies is None:
            self.anomalies = []


# ============================================================================
# Core Analysis Functions
# ============================================================================

def calculate_hashes(file_bytes: bytes) -> Dict[str, str]:
    """Calculate MD5, SHA1, and SHA256 hashes."""
    return {
        "md5": hashlib.md5(file_bytes).hexdigest(),
        "sha1": hashlib.sha1(file_bytes).hexdigest(),
        "sha256": hashlib.sha256(file_bytes).hexdigest(),
    }


def calculate_entropy(file_bytes: bytes) -> float:
    """
    Calculate Shannon entropy of file as a measure of randomness.
    Returns value between 0 (uniform) and 8 (maximum entropy for bytes).
    """
    if not file_bytes:
        return 0.0
    
    byte_counts = [0] * 256
    for byte in file_bytes:
        byte_counts[byte] += 1
    
    entropy = 0.0
    file_length = len(file_bytes)
    for count in byte_counts:
        if count > 0:
            probability = count / file_length
            entropy -= probability * (probability and __import__('math').log2(probability) or 0)
    
    return entropy


def calculate_lsb_variance(image: Image.Image) -> float:
    """
    Simple LSB (Least Significant Bit) variance score.
    Higher values suggest possible steganography.
    """
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        pixels = list(image.getdata())
        if not pixels:
            return 0.0
        
        # Extract LSBs from red channel
        lsbs = [pixel[0] & 1 for pixel in pixels]
        
        # Calculate variance (0 = all same, 1 = perfect alternation)
        mean = sum(lsbs) / len(lsbs)
        variance = sum((x - mean) ** 2 for x in lsbs) / len(lsbs)
        
        return variance
    except Exception:
        return 0.0


def extract_exif_data(image: Image.Image, file_bytes: bytes) -> ExifData:
    """Extract EXIF data from image using PIL and piexif."""
    exif_data = ExifData()
    
    try:
        # Try piexif for structured EXIF
        ifd_dict = piexif.load(BytesIO(file_bytes))
        
        # 0th IFD (main image)
        ifd_0th = ifd_dict.get("0th", {})
        
        # Extract key EXIF tags
        if piexif.ImageIFD.Make in ifd_0th:
            exif_data.make = ifd_0th[piexif.ImageIFD.Make][0].decode().strip('\x00')
        if piexif.ImageIFD.Model in ifd_0th:
            exif_data.model = ifd_0th[piexif.ImageIFD.Model][0].decode().strip('\x00')
        if piexif.ImageIFD.Orientation in ifd_0th:
            exif_data.orientation = ifd_0th[piexif.ImageIFD.Orientation][0]
        if piexif.ImageIFD.Software in ifd_0th:
            exif_data.software = ifd_0th[piexif.ImageIFD.Software][0].decode().strip('\x00')
        
        # Exif IFD
        exif_ifd = ifd_dict.get("Exif", {})
        if piexif.ExifIFD.DateTimeOriginal in exif_ifd:
            exif_data.datetime_original = exif_ifd[piexif.ExifIFD.DateTimeOriginal][0].decode()
        if piexif.ExifIFD.ExposureTime in exif_ifd:
            val = exif_ifd[piexif.ExifIFD.ExposureTime][0]
            exif_data.exposure = f"{val[0]}/{val[1]}"
        if piexif.ExifIFD.FNumber in exif_ifd:
            val = exif_ifd[piexif.ExifIFD.FNumber][0]
            exif_data.f_number = f"f/{val[0] / val[1]:.1f}"
        if piexif.ExifIFD.ISOSpeedRatings in exif_ifd:
            exif_data.iso = exif_ifd[piexif.ExifIFD.ISOSpeedRatings][0]
        if piexif.ExifIFD.FocalLength in exif_ifd:
            val = exif_ifd[piexif.ExifIFD.FocalLength][0]
            exif_data.focal_length = f"{val[0] / val[1]:.1f}mm"
        
        # Store all other tags
        for ifd_name in ("0th", "Exif", "GPS", "1st"):
            ifd = ifd_dict.get(ifd_name, {})
            for tag, value in ifd.items():
                tag_name = piexif.TAGS[ifd_name][tag]["name"]
                if tag_name not in ["Make", "Model", "Orientation", "Software", 
                                    "DateTimeOriginal", "ExposureTime", "FNumber",
                                    "ISOSpeedRatings", "FocalLength"]:
                    try:
                        if isinstance(value, bytes):
                            exif_data.other_tags[tag_name] = value.decode(errors='ignore')
                        elif isinstance(value, tuple):
                            exif_data.other_tags[tag_name] = str(value)
                        else:
                            exif_data.other_tags[tag_name] = value
                    except Exception:
                        pass
    
    except Exception:
        # Fallback: try PIL's getexif()
        try:
            pil_exif = image.getexif()
            if pil_exif:
                for tag_id, value in pil_exif.items():
                    tag_name = EXIF_TAGS.get(tag_id, tag_id)
                    if tag_name == 'DateTime':
                        exif_data.datetime_original = str(value)
                    elif tag_name == 'Make':
                        exif_data.make = str(value)
                    elif tag_name == 'Model':
                        exif_data.model = str(value)
                    elif tag_name == 'Orientation':
                        exif_data.orientation = value
                    else:
                        exif_data.other_tags[tag_name] = str(value)
        except Exception:
            pass
    
    return exif_data


def extract_gps_data(file_bytes: bytes) -> Optional[GPSData]:
    """Extract GPS coordinates from EXIF data."""
    try:
        ifd_dict = piexif.load(BytesIO(file_bytes))
        gps_ifd = ifd_dict.get("GPS", {})
        
        if not gps_ifd:
            return None
        
        gps_data = GPSData()
        
        # GPS latitude
        if piexif.GPSIFD.GPSLatitude in gps_ifd:
            lat_data = gps_ifd[piexif.GPSIFD.GPSLatitude]
            lat = lat_data[0][0] / lat_data[0][1] + lat_data[1][0] / lat_data[1][1] / 60 + lat_data[2][0] / lat_data[2][1] / 3600
            if piexif.GPSIFD.GPSLatitudeRef in gps_ifd:
                lat_ref = gps_ifd[piexif.GPSIFD.GPSLatitudeRef][0].decode()
                if lat_ref == 'S':
                    lat = -lat
            gps_data.lat = lat
        
        # GPS longitude
        if piexif.GPSIFD.GPSLongitude in gps_ifd:
            lon_data = gps_ifd[piexif.GPSIFD.GPSLongitude]
            lon = lon_data[0][0] / lon_data[0][1] + lon_data[1][0] / lon_data[1][1] / 60 + lon_data[2][0] / lon_data[2][1] / 3600
            if piexif.GPSIFD.GPSLongitudeRef in gps_ifd:
                lon_ref = gps_ifd[piexif.GPSIFD.GPSLongitudeRef][0].decode()
                if lon_ref == 'W':
                    lon = -lon
            gps_data.lon = lon
        
        # GPS altitude
        if piexif.GPSIFD.GPSAltitude in gps_ifd:
            alt_data = gps_ifd[piexif.GPSIFD.GPSAltitude][0]
            gps_data.alt = alt_data[0] / alt_data[1]
        
        return gps_data if (gps_data.lat or gps_data.lon) else None
    
    except Exception:
        return None


def extract_xmp_data(file_bytes: bytes) -> Dict[str, Any]:
    """
    Best-effort XMP extraction.
    XMP is typically embedded as XML in JPEG/PNG.
    """
    xmp_data = {}
    try:
        # XMP usually starts with <?xpacket
        xmp_start = file_bytes.find(b'<?xpacket')
        xmp_end = file_bytes.find(b'<?xpacket end')
        
        if xmp_start != -1 and xmp_end != -1:
            xmp_bytes = file_bytes[xmp_start:xmp_end + len(b'<?xpacket end')]
            xmp_str = xmp_bytes.decode('utf-8', errors='ignore')
            
            # Simple extraction of key XMP fields
            import re
            # Extract common XMP namespaces
            xmp_data['raw'] = xmp_str[:500]  # First 500 chars
            
            # Look for common fields
            if 'CreatorTool' in xmp_str or 'creator' in xmp_str:
                xmp_data['has_creator_info'] = True
    except Exception:
        pass
    
    return xmp_data


def extract_iptc_data(file_bytes: bytes) -> Dict[str, Any]:
    """
    Best-effort IPTC extraction.
    IPTC is less common in modern images but still present in some.
    """
    iptc_data = {}
    try:
        # IPTC marker: 0x1C
        if b'\x1c' in file_bytes:
            iptc_data['has_iptc'] = True
    except Exception:
        pass
    
    return iptc_data


def extract_thumbnail(image: Image.Image) -> Optional[str]:
    """Extract thumbnail if present and return as base64."""
    try:
        if hasattr(image, 'thumbnail_size') and image.thumbnail_size:
            # PIL doesn't easily expose embedded thumbnails, but we can create one
            thumb = image.copy()
            thumb.thumbnail((150, 150))
            thumb_bytes = BytesIO()
            thumb.save(thumb_bytes, format='JPEG')
            thumb_bytes.seek(0)
            return base64.b64encode(thumb_bytes.getvalue()).decode('utf-8')
    except Exception:
        pass
    
    return None


def detect_anomalies(file_info: FileInfo, exif: ExifData, gps: Optional[GPSData],
                    hashes: Dict[str, str], entropy: float) -> List[str]:
    """Detect potential forensic anomalies."""
    anomalies = []
    
    # High entropy might indicate encryption/compression or tampering
    if entropy > 7.5:
        anomalies.append("High entropy detected (possible encryption/compression)")
    
    # Missing EXIF on camera-type images
    if file_info.format in ['JPEG', 'TIFF'] and not exif.make and not exif.model:
        anomalies.append("No camera EXIF data found (possible screenshot or edited)")
    
    # GPS coordinates present (privacy concern)
    if gps and gps.lat and gps.lon:
        anomalies.append(f"GPS coordinates embedded: {gps.lat:.4f}, {gps.lon:.4f}")
    
    # Orientation tag (indicates possible manipulation)
    if exif.orientation and exif.orientation != 1:
        anomalies.append(f"Image orientation rotated (value: {exif.orientation})")
    
    # Software/editor tags
    if exif.software:
        anomalies.append(f"Edited with: {exif.software}")
    
    return anomalies


# ============================================================================
# FastAPI Setup
# ============================================================================

app = FastAPI(title="MetaScan", version="0.1.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/inspect")
async def inspect_image(file: UploadFile = File(...)):
    """
    Inspect an image file and return forensic metadata.
    
    Accepts: multipart/form-data with 'file' field
    Returns: JSON with complete metadata analysis
    """
    # Validate file upload
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    filename = file.filename or "unknown"
    
    try:
        # Read file bytes
        file_bytes = await file.read()
        
        if not file_bytes:
            raise HTTPException(status_code=400, detail="File is empty")
        
        if len(file_bytes) > 50 * 1024 * 1024:  # 50MB limit
            raise HTTPException(status_code=400, detail="File too large (max 50MB)")
        
        # Detect MIME type
        mime = magic.from_buffer(file_bytes, mime=True)
        
        # Open with Pillow
        image = Image.open(BytesIO(file_bytes))
        
        # Basic file info
        file_info = FileInfo(
            filename=filename,
            size_bytes=len(file_bytes),
            mime=mime,
            format=image.format or "Unknown",
            width=image.width,
            height=image.height,
        )
        
        # Extract metadata
        exif = extract_exif_data(image, file_bytes)
        gps = extract_gps_data(file_bytes)
        xmp = extract_xmp_data(file_bytes)
        iptc = extract_iptc_data(file_bytes)
        
        # Extract thumbnail
        thumbnail_b64 = extract_thumbnail(image)
        
        # Calculate hashes
        hashes = calculate_hashes(file_bytes)
        
        # Calculate entropy and LSB variance
        entropy = calculate_entropy(file_bytes)
        lsb_variance = calculate_lsb_variance(image)
        
        # Detect anomalies
        anomalies = detect_anomalies(file_info, exif, gps, hashes, entropy)
        
        # Build result
        result = ForensicResult(
            file_info=file_info,
            exif=exif,
            gps=gps,
            xmp_data=xmp,
            iptc_data=iptc,
            thumbnail_base64=thumbnail_b64,
            hashes=hashes,
            entropy=round(entropy, 4),
            lsb_variance=round(lsb_variance, 4),
            anomalies=anomalies,
        )
        
        # Convert dataclasses to dict
        return {
            "success": True,
            "data": {
                "file_info": asdict(result.file_info),
                "exif": asdict(result.exif),
                "gps": asdict(result.gps) if result.gps else None,
                "xmp_data": result.xmp_data,
                "iptc_data": result.iptc_data,
                "thumbnail_base64": result.thumbnail_base64,
                "hashes": result.hashes,
                "entropy": result.entropy,
                "lsb_variance": result.lsb_variance,
                "anomalies": result.anomalies,
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "detail": "Failed to analyze image"
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
