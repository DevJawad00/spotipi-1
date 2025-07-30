#!/usr/bin/env python3
"""
Simple Matrix Display Test

This script tests the matrix display functionality without requiring Spotify authentication.
"""

import numpy as np
import time
import sys
import os

def test_matrix_display():
    """Test matrix display with a simple image."""
    print("🎯 Testing Matrix Display...")
    print("=" * 30)
    
    try:
        # Import the matrix display module
        from matrix_display import MatrixDisplay
        print("✅ MatrixDisplay imported successfully")
        
        # Create matrix display instance
        display = MatrixDisplay()
        print("✅ Matrix display initialized")
        
        if display.matrix is None:
            print("❌ No matrix hardware detected")
            return False
        
        print("✅ Matrix hardware detected")
        
        # Create a simple test image (red gradient)
        print("🎨 Creating test image...")
        test_image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Create a red gradient
        for y in range(64):
            for x in range(64):
                intensity = int(255 * (x + y) / 128)
                test_image[y, x] = [intensity, 0, 0]  # Red gradient
        
        print("✅ Test image created")
        
        # Display the image
        print("🖼️  Displaying test image...")
        display.display_image(test_image, 0.1)
        
        print("✅ Image displayed successfully!")
        print("🎉 Matrix display is working!")
        
        # Keep it displayed for a few seconds
        time.sleep(5)
        
        # Create a different test image (blue pattern)
        print("🔵 Creating blue pattern...")
        test_image2 = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Create a blue checkerboard pattern
        for y in range(64):
            for x in range(64):
                if (x // 8 + y // 8) % 2 == 0:
                    test_image2[y, x] = [0, 0, 255]  # Blue
                else:
                    test_image2[y, x] = [0, 0, 0]    # Black
        
        display.display_image(test_image2, 0.1)
        print("✅ Blue pattern displayed!")
        
        time.sleep(5)
        
        # Create a green circle
        print("🟢 Creating green circle...")
        test_image3 = np.zeros((64, 64, 3), dtype=np.uint8)
        
        center_x, center_y = 32, 32
        radius = 20
        
        for y in range(64):
            for x in range(64):
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                if distance <= radius:
                    test_image3[y, x] = [0, 255, 0]  # Green
        
        display.display_image(test_image3, 0.1)
        print("✅ Green circle displayed!")
        
        time.sleep(5)
        
        # Clear the display
        print("⬛ Clearing display...")
        black_image = np.zeros((64, 64, 3), dtype=np.uint8)
        display.display_image(black_image, 0.1)
        
        print("✅ Display cleared!")
        print("🎉 All matrix display tests completed successfully!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import MatrixDisplay: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Matrix display test failed: {e}")
        return False

def test_simple_colors():
    """Test simple color display."""
    print("🎨 Testing Simple Colors...")
    print("=" * 25)
    
    try:
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
        
        # Configure matrix
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.hardware_mapping = "adafruit-hat"
        options.brightness = 50
        options.gpio_slowdown = 1
        
        matrix = RGBMatrix(options=options)
        canvas = matrix.CreateFrameCanvas()
        
        print("✅ Matrix initialized")
        
        # Test different colors
        colors = [
            ("Red", (255, 0, 0)),
            ("Green", (0, 255, 0)),
            ("Blue", (0, 0, 255)),
            ("Yellow", (255, 255, 0)),
            ("Magenta", (255, 0, 255)),
            ("Cyan", (0, 255, 255)),
            ("White", (255, 255, 255))
        ]
        
        for color_name, (r, g, b) in colors:
            print(f"🎨 Displaying {color_name}...")
            canvas.Fill(r, g, b)
            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(2)
        
        # Clear
        canvas.Fill(0, 0, 0)
        canvas = matrix.SwapOnVSync(canvas)
        
        print("✅ Color test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Color test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🎵 SpotiPi Matrix Display Test")
    print("=" * 35)
    
    print("Choose a test:")
    print("1. Matrix display test (recommended)")
    print("2. Simple color test")
    print("3. Both tests")
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled")
        return
    
    if choice == "1":
        test_matrix_display()
    elif choice == "2":
        test_simple_colors()
    elif choice == "3":
        test_matrix_display()
        print("\n" + "=" * 30)
        test_simple_colors()
    else:
        print("❌ Invalid choice. Running matrix display test...")
        test_matrix_display()

if __name__ == "__main__":
    main() 