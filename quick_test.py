#!/usr/bin/env python3
"""
Quick Matrix Test

This will immediately show something on the matrix without any authentication.
"""

import time
import numpy as np
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def main():
    print("🎯 Quick Matrix Test")
    print("=" * 25)
    
    try:
        # Configure matrix (using the working settings)
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "regular"  # Use the working mapping
        options.gpio_slowdown = 1
        options.brightness = 50
        options.drop_privileges = False
        
        print("🔧 Creating matrix...")
        matrix = RGBMatrix(options=options)
        canvas = matrix.CreateFrameCanvas()
        print("✅ Matrix ready!")
        
        # Create a simple test pattern
        print("🎨 Creating test pattern...")
        
        # Create a colorful pattern
        for y in range(64):
            for x in range(64):
                # Create a rainbow pattern
                r = int(255 * (x / 64))
                g = int(255 * (y / 64))
                b = int(255 * ((x + y) / 128))
                canvas.SetPixel(x, y, r, g, b)
        
        print("🖼️  Displaying pattern...")
        canvas = matrix.SwapOnVSync(canvas)
        
        print("✅ Pattern displayed!")
        print("🎉 Matrix is working!")
        print("Press Ctrl+C to stop...")
        
        # Keep it running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
            canvas.Fill(0, 0, 0)  # Clear
            canvas = matrix.SwapOnVSync(canvas)
            print("✅ Display cleared")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 