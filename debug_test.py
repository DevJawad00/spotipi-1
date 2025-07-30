#!/usr/bin/env python3
"""
Debug Matrix Test

This will show us exactly what's happening step by step.
"""

import time
import sys
import os

def main():
    print("🔍 Debug Matrix Test")
    print("=" * 30)
    
    # Step 1: Check Python version
    print(f"Python version: {sys.version}")
    
    # Step 2: Check if we're running as root
    print(f"Running as root: {os.geteuid() == 0}")
    
    # Step 3: Try to import rgbmatrix
    try:
        print("🔍 Trying to import rgbmatrix...")
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
        print("✅ rgbmatrix imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import rgbmatrix: {e}")
        return
    
    # Step 4: Create options
    try:
        print("🔍 Creating RGBMatrixOptions...")
        options = RGBMatrixOptions()
        print("✅ RGBMatrixOptions created")
        
        # Set options
        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "adafruit-hat"
        options.gpio_slowdown = 1
        options.brightness = 50
        options.drop_privileges = False
        
        print("✅ Options configured")
        print(f"   - Hardware mapping: {options.hardware_mapping}")
        print(f"   - Brightness: {options.brightness}")
        
    except Exception as e:
        print(f"❌ Error creating options: {e}")
        return
    
    # Step 5: Create matrix
    try:
        print("🔍 Creating RGBMatrix...")
        matrix = RGBMatrix(options=options)
        print("✅ RGBMatrix created")
    except Exception as e:
        print(f"❌ Error creating matrix: {e}")
        return
    
    # Step 6: Create canvas
    try:
        print("🔍 Creating canvas...")
        canvas = matrix.CreateFrameCanvas()
        print("✅ Canvas created")
    except Exception as e:
        print(f"❌ Error creating canvas: {e}")
        return
    
    # Step 7: Test red
    try:
        print("🔴 Testing RED...")
        print("   - Filling canvas with red...")
        canvas.Fill(255, 0, 0)
        print("   - Swapping canvas...")
        canvas = matrix.SwapOnVSync(canvas)
        print("   - Waiting 3 seconds...")
        time.sleep(3)
        print("✅ Red test completed")
    except Exception as e:
        print(f"❌ Error during red test: {e}")
        return
    
    # Step 8: Test green
    try:
        print("🟢 Testing GREEN...")
        canvas.Fill(0, 255, 0)
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(3)
        print("✅ Green test completed")
    except Exception as e:
        print(f"❌ Error during green test: {e}")
        return
    
    # Step 9: Test blue
    try:
        print("🔵 Testing BLUE...")
        canvas.Fill(0, 0, 255)
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(3)
        print("✅ Blue test completed")
    except Exception as e:
        print(f"❌ Error during blue test: {e}")
        return
    
    # Step 10: Clear
    try:
        print("⬛ Clearing...")
        canvas.Fill(0, 0, 0)
        canvas = matrix.SwapOnVSync(canvas)
        print("✅ Clear completed")
    except Exception as e:
        print(f"❌ Error during clear: {e}")
        return
    
    print("🎉 All tests completed successfully!")
    print("If you didn't see anything on the matrix, there might be a hardware issue.")

if __name__ == "__main__":
    main() 