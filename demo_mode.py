#!/usr/bin/env python3
"""
SpotiPi Demo Mode

This shows how the matrix will display images without requiring Spotify authentication.
"""

import time
import numpy as np
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def create_test_album_art():
    """Create a test album cover image."""
    # Create a 64x64 image that looks like album art
    image = np.zeros((64, 64, 3), dtype=np.uint8)
    
    # Create a colorful album cover design
    for y in range(64):
        for x in range(64):
            # Create a gradient pattern
            r = int(255 * (x / 64))
            g = int(255 * (y / 64))
            b = int(255 * ((x + y) / 128))
            
            # Add some circles to make it look like album art
            center_x, center_y = 32, 32
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            
            if distance < 20:
                # Inner circle - different color
                r = 255 - r
                g = 255 - g
                b = 255 - b
            
            image[y, x] = [r, g, b]
    
    return image

def main():
    print("🎵 SpotiPi Demo Mode")
    print("=" * 25)
    print("This will show how album art will look on your matrix!")
    print()
    
    try:
        # Configure matrix
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "regular"
        options.gpio_slowdown = 1
        options.brightness = 50
        options.drop_privileges = False
        
        print("🔧 Initializing matrix...")
        matrix = RGBMatrix(options=options)
        canvas = matrix.CreateFrameCanvas()
        print("✅ Matrix ready!")
        
        # Create test album art
        print("🎨 Creating test album art...")
        test_image = create_test_album_art()
        
        # Display the image
        print("🖼️  Displaying test album art...")
        for y in range(64):
            for x in range(64):
                r, g, b = test_image[y, x]
                canvas.SetPixel(x, y, r, g, b)
        
        canvas = matrix.SwapOnVSync(canvas)
        
        print("✅ Test album art displayed!")
        print("🎉 This is how your Spotify album covers will look!")
        print("Press Ctrl+C to stop...")
        
        # Keep it running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping demo...")
            canvas.Fill(0, 0, 0)  # Clear
            canvas = matrix.SwapOnVSync(canvas)
            print("✅ Demo stopped")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 