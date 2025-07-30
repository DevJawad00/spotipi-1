#!/usr/bin/env python3
"""
SpotiPi Test Script

This script tests all components to ensure they're working correctly.
"""

import sys
import os
import numpy as np

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import spotipy
        print("✅ spotipy imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import spotipy: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ PIL imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import PIL: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        import numpy
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import numpy: {e}")
        return False
    
    try:
        from rgbmatrix import RGBMatrix
        print("✅ rgbmatrix imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import rgbmatrix: {e}")
        print("   This is expected if not running on Raspberry Pi")
    
    return True

def test_config():
    """Test configuration file."""
    print("\n🔍 Testing configuration...")
    
    try:
        import config
        print("✅ config.py imported successfully")
        
        # Check if credentials are set
        if (config.SPOTIFY_CLIENT_ID == "your_client_id_here" or 
            config.SPOTIFY_CLIENT_SECRET == "your_client_secret_here"):
            print("⚠️  Spotify credentials not configured")
            print("   Please edit config.py with your credentials")
        else:
            print("✅ Spotify credentials configured")
        
        print(f"✅ Matrix dimensions: {config.MATRIX_WIDTH}x{config.MATRIX_HEIGHT}")
        print(f"✅ Update interval: {config.UPDATE_INTERVAL}s")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import config: {e}")
        return False

def test_spotify_client():
    """Test Spotify client (without authentication)."""
    print("\n🔍 Testing Spotify client...")
    
    try:
        from spotify_client import SpotifyClient
        print("✅ SpotifyClient class imported successfully")
        
        # Test without authentication
        print("⚠️  Skipping authentication test (requires credentials)")
        return True
    except ImportError as e:
        print(f"❌ Failed to import SpotifyClient: {e}")
        return False

def test_image_processor():
    """Test image processor."""
    print("\n🔍 Testing image processor...")
    
    try:
        from image_processor import ImageProcessor
        print("✅ ImageProcessor class imported successfully")
        
        # Create test image
        processor = ImageProcessor()
        test_image = processor._create_placeholder_image()
        
        print(f"✅ Created test image: {test_image.shape}")
        print(f"✅ Image data type: {test_image.dtype}")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import ImageProcessor: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing ImageProcessor: {e}")
        return False

def test_matrix_display():
    """Test matrix display (simulation mode)."""
    print("\n🔍 Testing matrix display...")
    
    try:
        from matrix_display import MatrixDisplay
        print("✅ MatrixDisplay class imported successfully")
        
        # Test in simulation mode
        display = MatrixDisplay()
        
        if display.matrix is None:
            print("✅ Running in simulation mode")
        else:
            print("✅ RGB matrix hardware detected")
        
        # Test display methods
        test_image = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
        display.display_image(test_image, 0.1)
        print("✅ Display test completed")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import MatrixDisplay: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing MatrixDisplay: {e}")
        return False

def test_cache_directory():
    """Test cache directory."""
    print("\n🔍 Testing cache directory...")
    
    try:
        import config
        cache_dir = config.IMAGE_CACHE_DIR
        
        if os.path.exists(cache_dir):
            print(f"✅ Cache directory exists: {cache_dir}")
        else:
            os.makedirs(cache_dir, exist_ok=True)
            print(f"✅ Created cache directory: {cache_dir}")
        
        # Test write permissions
        test_file = os.path.join(cache_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✅ Cache directory is writable")
        
        return True
    except Exception as e:
        print(f"❌ Error testing cache directory: {e}")
        return False

def main():
    """Run all tests."""
    print("🎵 SpotiPi Test Suite")
    print("=" * 30)
    
    tests = [
        test_imports,
        test_config,
        test_spotify_client,
        test_image_processor,
        test_matrix_display,
        test_cache_directory
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 30)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SpotiPi is ready to use.")
        print("\nNext steps:")
        print("1. Configure Spotify credentials in config.py")
        print("2. Run: python3 auth_spotify.py")
        print("3. Run: python3 main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Run: python3 setup.py")
        print("2. Check that all dependencies are installed")
        print("3. Verify your configuration")

if __name__ == "__main__":
    main() 