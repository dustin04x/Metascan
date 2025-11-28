"""
Unit tests for MetaScan backend analysis functions.
"""
import pytest
from io import BytesIO
from PIL import Image
from backend.app import (
    calculate_hashes,
    calculate_entropy,
    calculate_lsb_variance,
    FileInfo,
    detect_anomalies,
    ExifData,
)


class TestHashing:
    """Test cryptographic hash functions."""
    
    def test_calculate_hashes_consistency(self):
        """Test that hashing is consistent."""
        data = b"test image data"
        hashes1 = calculate_hashes(data)
        hashes2 = calculate_hashes(data)
        
        assert hashes1 == hashes2
        assert len(hashes1["md5"]) == 32
        assert len(hashes1["sha1"]) == 40
        assert len(hashes1["sha256"]) == 64
    
    def test_calculate_hashes_different_data(self):
        """Test that different data produces different hashes."""
        data1 = b"test data 1"
        data2 = b"test data 2"
        
        hashes1 = calculate_hashes(data1)
        hashes2 = calculate_hashes(data2)
        
        assert hashes1 != hashes2
    
    def test_calculate_hashes_empty(self):
        """Test hashing empty data."""
        hashes = calculate_hashes(b"")
        assert hashes["md5"] == "d41d8cd98f00b204e9800998ecf8427e"
        assert hashes["sha1"] == "da39a3ee5e6b4b0d3255bfef95601890afd80709"


class TestEntropy:
    """Test entropy calculation."""
    
    def test_entropy_uniform_data(self):
        """Uniform data (all zeros) should have near-zero entropy."""
        data = b"\x00" * 256
        entropy = calculate_entropy(data)
        assert entropy < 0.1
    
    def test_entropy_random_data(self):
        """Random data should have high entropy."""
        import os
        data = os.urandom(256)
        entropy = calculate_entropy(data)
        assert entropy > 7.0  # Should be close to maximum (8.0)
    
    def test_entropy_empty(self):
        """Empty data should have zero entropy."""
        entropy = calculate_entropy(b"")
        assert entropy == 0.0
    
    def test_entropy_repeating_pattern(self):
        """Repeating pattern should have low entropy."""
        data = b"ABAB" * 64
        entropy = calculate_entropy(data)
        assert entropy < 3.0


class TestLSBVariance:
    """Test LSB variance detection."""
    
    def test_lsb_variance_uniform_image(self):
        """Uniform color image should have low LSB variance."""
        img = Image.new('RGB', (100, 100), color=(255, 0, 0))
        variance = calculate_lsb_variance(img)
        assert variance < 0.1
    
    def test_lsb_variance_with_image(self):
        """Test LSB variance on a simple image."""
        img = Image.new('RGB', (64, 64), color=(128, 64, 32))
        variance = calculate_lsb_variance(img)
        assert 0.0 <= variance <= 1.0
    
    def test_lsb_variance_grayscale_conversion(self):
        """Test that grayscale images are handled."""
        img = Image.new('L', (64, 64), color=128)
        # Should not raise exception
        variance = calculate_lsb_variance(img)
        assert isinstance(variance, float)


class TestAnomalyDetection:
    """Test forensic anomaly detection."""
    
    def test_anomaly_high_entropy(self):
        """High entropy should trigger anomaly."""
        file_info = FileInfo(
            filename="test.jpg",
            size_bytes=1000,
            mime="image/jpeg",
            format="JPEG",
            width=640,
            height=480
        )
        exif = ExifData()
        
        anomalies = detect_anomalies(file_info, exif, None, {}, 7.6)
        assert any("entropy" in a.lower() for a in anomalies)
    
    def test_anomaly_gps_detected(self):
        """GPS coordinates should be flagged."""
        from backend.app import GPSData
        
        file_info = FileInfo(
            filename="test.jpg",
            size_bytes=1000,
            mime="image/jpeg",
            format="JPEG"
        )
        exif = ExifData()
        gps = GPSData(lat=40.7128, lon=-74.0060, alt=10.0)
        
        anomalies = detect_anomalies(file_info, exif, gps, {}, 5.0)
        assert any("GPS" in a for a in anomalies)
    
    def test_anomaly_no_exif_on_jpeg(self):
        """JPEG without EXIF might indicate screenshot."""
        file_info = FileInfo(
            filename="test.jpg",
            size_bytes=1000,
            mime="image/jpeg",
            format="JPEG"
        )
        exif = ExifData()  # Empty EXIF
        
        anomalies = detect_anomalies(file_info, exif, None, {}, 5.0)
        assert any("EXIF" in a or "screenshot" in a.lower() for a in anomalies)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
