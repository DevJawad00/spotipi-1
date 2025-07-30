#!/usr/bin/env python3
"""
Simple RGB Matrix Test Script

This script tests the RGB matrix hardware to ensure it's working properly.
"""

import numpy as np
import time
import sys
import os

def test_matrix_basic():
    """Test basic matrix functionality."""
    print("🎯 Testing RGB Matrix Hardware...")
    print("=" * 40)
    
    try:
        # Try to import the matrix library
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
        
        print("✅ RGB Matrix library imported successfully")
        
        # Configure matrix options
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "adafruit-hat"  # or "regular"
        options.gpio_slowdown = 1
        options.brightness = 50
        
        print("🔧 Matrix configuration:")
        print(f"   - Size: {options.rows}x{options.cols}")
        print(f"   - Hardware mapping: {options.hardware_mapping}")
        print(f"   - Brightness: {options.brightness}")
        
        # Create matrix instance
        matrix = RGBMatrix(options=options)
        print("✅ Matrix initialized successfully")
        
        # Create a canvas
        canvas = matrix.CreateFrameCanvas()
        print("✅ Canvas created successfully")
        
        # Test 1: Red screen
        print("\n🔴 Test 1: Red screen (3 seconds)")
        canvas.Fill(255, 0, 0)  # Red
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(3)
        
        # Test 2: Green screen
        print("🟢 Test 2: Green screen (3 seconds)")
        canvas.Fill(0, 255, 0)  # Green
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(3)
        
        # Test 3: Blue screen
        print("🔵 Test 3: Blue screen (3 seconds)")
        canvas.Fill(0, 0, 255)  # Blue
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(3)
        
        # Test 4: White screen
        print("⚪ Test 4: White screen (3 seconds)")
        canvas.Fill(255, 255, 255)  # White
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(3)
        
        # Test 5: Animated pattern
        print("🌈 Test 5: Animated pattern (5 seconds)")
        for i in range(50):
            # Create a moving rainbow pattern
            for y in range(64):
                for x in range(64):
                    r = int(128 + 127 * np.sin((x + i) * 0.1))
                    g = int(128 + 127 * np.sin((y + i) * 0.1))
                    b = int(128 + 127 * np.sin((x + y + i) * 0.1))
                    canvas.SetPixel(x, y, r, g, b)
            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.1)
        
        # Test 6: Clear screen
        print("⬛ Test 6: Clear screen")
        canvas.Fill(0, 0, 0)  # Black
        canvas = matrix.SwapOnVSync(canvas)
        
        print("\n✅ All matrix tests completed successfully!")
        print("🎉 Your RGB matrix is working properly!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import RGB Matrix library: {e}")
        print("   Make sure the library is installed correctly")
        return False
        
    except Exception as e:
        print(f"❌ Matrix test failed: {e}")
        print("   Check your hardware connections and configuration")
        return False

def test_matrix_simple():
    """Test matrix with simple color display."""
    print("🎯 Simple Matrix Test...")
    print("=" * 30)
    
    try:
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
        
        # Simple configuration
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.hardware_mapping = "adafruit-hat"
        options.brightness = 30
        
        matrix = RGBMatrix(options=options)
        canvas = matrix.CreateFrameCanvas()
        
        print("✅ Matrix initialized")
        
        # Show a simple pattern
        for y in range(64):
            for x in range(64):
                # Create a simple gradient
                r = int(255 * x / 64)
                g = int(255 * y / 64)
                b = 128
                canvas.SetPixel(x, y, r, g, b)
        
        canvas = matrix.SwapOnVSync(canvas)
        print("🎨 Pattern displayed - Press Ctrl+C to stop")
        
        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Test stopped by user")
            canvas.Fill(0, 0, 0)  # Clear screen
            canvas = matrix.SwapOnVSync(canvas)
        
        return True
        
    except Exception as e:
        print(f"❌ Simple test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🎵 SpotiPi RGB Matrix Test")
    print("=" * 30)
    
    # Check if running on Raspberry Pi
    if not os.path.exists('/proc/cpuinfo'):
        print("⚠️  This doesn't appear to be a Raspberry Pi")
        print("   Matrix tests may not work correctly")
        print()
    
    # Ask user which test to run
    print("Choose a test:")
    print("1. Basic matrix test (recommended)")
    print("2. Simple pattern test")
    print("3. Both tests")
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled")
        return
    
    if choice == "1":
        test_matrix_basic()
    elif choice == "2":
        test_matrix_simple()
    elif choice == "3":
        test_matrix_basic()
        print("\n" + "=" * 30)
        test_matrix_simple()
    else:
        print("❌ Invalid choice. Running basic test...")
        test_matrix_basic()

if __name__ == "__main__":
    main() 