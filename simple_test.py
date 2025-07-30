#!/usr/bin/env python3
"""
Very Simple Matrix Test

This uses the exact same settings as the working C++ examples.
"""

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def main():
    print("🎯 Very Simple Matrix Test")
    print("=" * 30)
    
    try:
        # Use the exact same settings as the C++ examples
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "regular"
        options.gpio_slowdown = 1
        options.brightness = 50
        options.drop_privileges = False
        
        print("🔧 Matrix configuration:")
        print(f"   - Size: {options.rows}x{options.cols}")
        print(f"   - Hardware mapping: {options.hardware_mapping}")
        print(f"   - Brightness: {options.brightness}")
        
        # Create matrix
        matrix = RGBMatrix(options=options)
        print("✅ Matrix created")
        
        # Create canvas
        canvas = matrix.CreateFrameCanvas()
        print("✅ Canvas created")
        
        # Test 1: Red
        print("🔴 Testing RED...")
        canvas.Fill(255, 0, 0)
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(3)
        
        # Test 2: Green
        print("🟢 Testing GREEN...")
        canvas.Fill(0, 255, 0)
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(3)
        
        # Test 3: Blue
        print("🔵 Testing BLUE...")
        canvas.Fill(0, 0, 255)
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(3)
        
        # Test 4: White
        print("⚪ Testing WHITE...")
        canvas.Fill(255, 255, 255)
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(3)
        
        # Clear
        print("⬛ Clearing...")
        canvas.Fill(0, 0, 0)
        canvas = matrix.SwapOnVSync(canvas)
        
        print("✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 