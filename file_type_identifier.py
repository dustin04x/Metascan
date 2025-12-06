#!/usr/bin/env python3
"""file_type_identifier.py - Python alternative to Linux 'file' command

Detects file types by analyzing magic bytes/signatures in file headers.
Usage: python3 file_type_identifier.py <file> [file2 ...]

Examples:
    python3 file_type_identifier.py example.png
    python3 file_type_identifier.py document.pdf archive.zip
    python3 file_type_identifier.py /path/to/file
"""

import sys
from pathlib import Path
from typing import Dict, Tuple, List

# Magic byte signatures mapped to file types
FILE_SIGNATURES: Dict[bytes, str] = {
    # Archives & Compression
    b'Rar!\x1A\x07': 'RAR archive data',
    b'\x52\x61\x72\x21\x1A\x07\x00': 'RAR archive data',
    b'7z\xBC\xAF\x27\x1C': '7-zip archive data',
    b'PK\x03\x04': 'Zip archive data',
    b'PK\x05\x06': 'Zip archive data',
    b'PK\x07\x08': 'Zip archive data',
    b'\x1F\x8B\x08': 'gzip compressed data',
    b'BZh': 'bzip2 compressed data',
    b'\xFD7zXZ\x00': 'xz compressed data',
    b'AR\x02': 'current ar archive',
    b'\x37\xE4\x53\x96': 'Microsoft Cabinet (CAB) archive',
    
    # Images
    b'\xFF\xD8\xFF\xE0': 'JPEG image data',
    b'\xFF\xD8\xFF\xE1': 'JPEG image data',
    b'\xFF\xD8\xFF\xE2': 'JPEG image data',
    b'\xFF\xD8\xFF\xDB': 'JPEG image data',
    b'\x89PNG\r\n\x1A\n': 'PNG image data',
    b'GIF89a': 'GIF image data',
    b'GIF87a': 'GIF image data',
    b'BM': 'PC bitmap data',
    b'II*\x00': 'TIFF image data',
    b'MM\x00*': 'TIFF image data',
    b'\x00\x00\x01\x00': 'MS Windows icon resource',
    b'\x00\x00\x02\x00': 'MS Windows cursor',
    b'\x00\x00\x00\x0CjP  ': 'JPEG 2000 image',
    
    # Audio & Video
    b'RIFF': 'RIFF (little-endian) data',
    b'ID3': 'ID3 version',
    b'\xFF\xFB': 'MPEG audio layer III',
    b'\xFF\xF3': 'MPEG audio layer III',
    b'\xFF\xF2': 'MPEG audio layer III',
    b'fLaC': 'FLAC audio bitstream data',
    b'OggS': 'Ogg data',
    b'MThd': 'MIDI audio data',
    b'FORM': 'FORM (probably AIFF-C audio data)',
    b'\x00\x00\x00\x14ftyp': 'ISO Media, MP4',
    b'ftyp': 'ISO Media, MP4',
    b'\x1A\x45\xDF\xA3': 'Matroska video stream',
    
    # Documents
    b'%PDF-': 'PDF document',
    b'\xD0\xCF\x11\xE0': 'Composite Document File data',
    b'PK\x03\x04\x14\x00\x06': 'Microsoft Word 2007+',
    b'\x25\x21\x50\x53': 'PostScript document text',
    b'{\\rtf': 'Rich Text Format data',
    b'<?xml': 'XML document text',
    
    # Executables & Code
    b'MZ': 'MS-DOS executable (EXE), OS/2 .COM or Windows',
    b'\x7FELF': 'ELF 64-bit LSB executable',
    b'\xCA\xFE\xBA\xBE': 'Mach-O fat binary',
    b'\xFE\xED\xFA\xCE': 'Mach-O 32-bit',
    b'\xFE\xED\xFA\xCF': 'Mach-O 64-bit',
    b'\x4C\xFA\xED\xFE': 'Mach-O universal binary',
    b'\x00asm': 'WebAssembly binary module',
    b'\x03\xF3\x0D\x0A': 'Java class file',
    b'CAF\xEB': 'Java class file',
    b'\x42\x43\xC0\xDE': 'LLVM bitcode',
    
    # Text encoding
    b'\xEF\xBB\xBF': 'UTF-8 Unicode (with BOM) text',
    b'\xFF\xFE\x00\x00': 'UTF-32LE (BOM)',
    b'\x00\x00\xFE\xFF': 'UTF-32BE (BOM)',
    b'\xFF\xFE': 'UTF-16LE (BOM)',
    b'\xFE\xFF': 'UTF-16BE (BOM)',
    
    # Other formats
    b'CD001': 'ISO 9660 CD-ROM filesystem data',
    b'\xA1\xB2\xC3\xD4': 'pcap capture file',
    b'\xD4\xC3\xB2\xA1': 'pcap capture file',
    b'SQLite format 3': 'SQLite 3.x database',
    b'\x00\x05\x16\x00': 'dBase III database',
    b'From ': 'mail message text',
}

def identify_file_type(file_path: str) -> str:
    """Identify file type by reading magic bytes."""
    path = Path(file_path)
    
    if not path.exists():
        return f"{file_path}: No such file or directory"
    
    if not path.is_file():
        return f"{file_path}: directory"
    
    try:
        with open(path, 'rb') as f:
            # Read first 32KB to capture most signatures
            header = f.read(32768)
    except PermissionError:
        return f"{file_path}: Permission denied"
    except Exception as e:
        return f"{file_path}: Error reading file: {e}"
    
    if not header:
        return f"{file_path}: empty"
    
    # Sort signatures by length (longest first) for better matching
    sorted_signatures = sorted(FILE_SIGNATURES.items(), key=lambda x: len(x[0]), reverse=True)
    
    # Try to match signatures
    for signature, description in sorted_signatures:
        if len(header) >= len(signature) and header.startswith(signature):
            return f"{file_path}: {description}"
        
        # Some signatures can appear later in file (like 'ftyp' in MP4)
        if signature in header:
            return f"{file_path}: {description}"
    
    # Check if it's likely text
    if is_text_file(header):
        return f"{file_path}: ASCII text"
    
    return f"{file_path}: data"

def is_text_file(data: bytes, threshold: float = 0.9) -> bool:
    """Check if data is mostly printable ASCII text."""
    if not data:
        return False
    
    printable = 0
    total = 0
    
    for byte in data[:8192]:  # Check first 8KB
        total += 1
        # Allow common control characters (tab, newline, carriage return)
        if byte in (9, 10, 13) or 32 <= byte <= 126:
            printable += 1
    
    return (printable / total) >= threshold if total > 0 else False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 file_type_identifier.py <file> [file2 ...]")
        sys.exit(1)
    
    for file_path in sys.argv[1:]:
        result = identify_file_type(file_path)
        print(result)

if __name__ == '__main__':
    main()