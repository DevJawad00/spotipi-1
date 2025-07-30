#!/usr/bin/env python3
"""
GPIO Mapping Test

This tests different GPIO mappings to find the right one.
"""

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def test_mapping(mapping_name):
    """Test a specific GPIO mapping."""
    print(f"🔍 Testing GPIO mapping: {mapping_name}")
    
    try:
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = mapping_name
        options.gpio_slowdown = 1
        options.brightness = 50
        options.drop_privileges = False
        
        matrix = RGBMatrix(options=options)
        canvas = matrix.CreateFrameCanvas()
        
        print(f"✅ {mapping_name} - Matrix created successfully")
        
        # Test red
        print(f"🔴 {mapping_name} - Testing RED...")
        canvas.Fill(255, 0, 0)
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(2)
        
        # Test green
        print(f"🟢 {mapping_name} - Testing GREEN...")
        canvas.Fill(0, 255, 0)
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(2)
        
        # Clear
        canvas.Fill(0, 0, 0)
        canvas = matrix.SwapOnVSync(canvas)
        
        print(f"✅ {mapping_name} - Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ {mapping_name} - Failed: {e}")
        return False

def main():
    print("🎯 GPIO Mapping Test")
    print("=" * 30)
    
    # List of mappings to try
    mappings = [
        "regular",
        "adafruit-hat",
        "adafruit-hat-pwm",
        "compute-module",
        "compute-module-pwm"
    ]
    
    working_mappings = []
    
    for mapping in mappings:
        print(f"\n{'='*20}")
        if test_mapping(mapping):
            working_mappings.append(mapping)
        print(f"{'='*20}\n")
    
    print("📊 Results:")
    if working_mappings:
        print(f"✅ Working mappings: {', '.join(working_mappings)}")
        print(f"🎉 Use the first working mapping: {working_mappings[0]}")
    else:
        print("❌ No working mappings found")
        print("   This might indicate a hardware issue")

if __name__ == "__main__":
    main() 