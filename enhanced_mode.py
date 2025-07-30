#!/usr/bin/env python3
"""
SpotiPi Enhanced Demo

An enhanced version with sophisticated visual effects and animations.
"""

import time
import signal
import sys
import os
import numpy as np
from datetime import datetime
import math

# Import our modules
from image_processor import ImageProcessor
from matrix_display import MatrixDisplay

class SpotiPiEnhanced:
    def __init__(self):
        """Initialize SpotiPi Enhanced application."""
        self.running = False
        self.image_processor = None
        self.matrix_display = None
        self.start_time = time.time()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.stop()
    
    def initialize(self):
        """Initialize all components."""
        print("🎵 Initializing SpotiPi Enhanced...")
        
        try:
            # Initialize image processor
            print("🖼️  Initializing image processor...")
            self.image_processor = ImageProcessor()
            
            # Initialize matrix display
            print("📺 Initializing RGB matrix...")
            self.matrix_display = MatrixDisplay()
            
            print("✅ SpotiPi Enhanced initialized successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False
    
    def run(self):
        """Main application loop."""
        if not self.initialize():
            return
        
        self.running = True
        print("🎵 SpotiPi Enhanced is running! Press Ctrl+C to stop.")
        print("📺 Displaying enhanced visual effects on matrix...")
        print()
        
        # Display enhanced startup animation
        self._display_enhanced_startup()
        
        # Enhanced demo loop with more sophisticated effects
        demo_functions = [
            self._create_wave_pattern,
            self._create_spiral_galaxy,
            self._create_neon_city,
            self._create_fire_effect,
            self._create_matrix_rain,
            self._create_cosmic_swirl,
            self._create_neon_pulse,
            self._create_geometric_art
        ]
        
        effect_index = 0
        
        while self.running:
            try:
                # Display current enhanced effect
                current_function = demo_functions[effect_index]
                print(f"🎨 Displaying enhanced effect {effect_index + 1}/{len(demo_functions)}...")
                
                # Display animated effect for 8 seconds
                for frame in range(80):  # 80 frames at 0.1s each = 8 seconds
                    if not self.running:
                        break
                    current_image = current_function(frame * 0.1)
                    self.matrix_display.display_image(current_image, 0.1)
                
                # Cycle to next effect
                effect_index = (effect_index + 1) % len(demo_functions)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(1)
        
        self.stop()
    
    def _display_enhanced_startup(self):
        """Display enhanced startup animation."""
        print("🚀 Starting up with enhanced effects...")
        
        # Create a more sophisticated startup animation
        for i in range(20):
            image = np.zeros((64, 64, 3), dtype=np.uint8)
            
            # Create expanding rings with rainbow colors
            center_x, center_y = 32, 32
            radius = 2 + i * 1.5
            
            for y in range(64):
                for x in range(64):
                    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                    if distance <= radius:
                        # Create rainbow effect
                        hue = (i * 18 + distance * 5) % 360
                        intensity = int(255 * (1 - distance / radius))
                        
                        # Convert HSV to RGB
                        if hue < 60:
                            r, g, b = 255, intensity * hue // 60, 0
                        elif hue < 120:
                            r, g, b = 255 - intensity * (hue - 60) // 60, 255, 0
                        elif hue < 180:
                            r, g, b = 0, 255, intensity * (hue - 120) // 60
                        elif hue < 240:
                            r, g, b = 0, 255 - intensity * (hue - 180) // 60, 255
                        elif hue < 300:
                            r, g, b = intensity * (hue - 240) // 60, 0, 255
                        else:
                            r, g, b = 255, 0, 255 - intensity * (hue - 300) // 60
                        
                        image[y, x] = [r, g, b]
            
            self.matrix_display.display_image(image, 0.1)
            time.sleep(0.1)
        
        # Clear with fade
        for i in range(10):
            fade_factor = 1 - (i / 10)
            image = np.zeros((64, 64, 3), dtype=np.uint8)
            self.matrix_display.display_image(image, 0.1)
            time.sleep(0.05)
    
    def _create_wave_pattern(self, time_offset):
        """Create animated wave pattern."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        for y in range(64):
            for x in range(64):
                # Create multiple wave layers
                wave1 = np.sin(x * 0.2 + time_offset * 2) * np.cos(y * 0.2 + time_offset * 1.5)
                wave2 = np.sin(x * 0.1 + time_offset * 3) * np.cos(y * 0.1 + time_offset * 2.5)
                wave3 = np.sin((x + y) * 0.15 + time_offset * 1.8)
                
                # Combine waves
                combined_wave = (wave1 + wave2 + wave3) / 3
                intensity = int(128 + 127 * combined_wave)
                
                # Create ocean-like colors
                r = int(intensity * 0.2)
                g = int(intensity * 0.6)
                b = int(intensity)
                
                image[y, x] = [r, g, b]
        
        return image
    
    def _create_spiral_galaxy(self, time_offset):
        """Create animated spiral galaxy effect."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        center_x, center_y = 32, 32
        
        for y in range(64):
            for x in range(64):
                # Calculate distance and angle from center
                dx, dy = x - center_x, y - center_y
                distance = np.sqrt(dx*dx + dy*dy)
                angle = np.arctan2(dy, dx)
                
                # Create spiral effect
                spiral = np.sin(angle * 3 + distance * 0.1 + time_offset * 2)
                rotation = np.sin(angle + time_offset * 0.5)
                
                # Combine effects
                intensity = int(128 + 127 * (spiral + rotation) / 2)
                
                # Create galaxy colors (purple/blue)
                r = int(intensity * 0.8)
                g = int(intensity * 0.3)
                b = int(intensity)
                
                # Add distance-based fade
                fade = max(0, 1 - distance / 45)
                image[y, x] = [int(r * fade), int(g * fade), int(b * fade)]
        
        return image
    
    def _create_neon_city(self, time_offset):
        """Create animated neon city effect."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        for y in range(64):
            for x in range(64):
                # Create building-like patterns
                building_height = int(32 + 16 * np.sin(x * 0.3 + time_offset))
                if y > building_height:
                    # Sky gradient
                    sky_intensity = int(64 + 32 * (y - building_height) / (64 - building_height))
                    image[y, x] = [sky_intensity//4, sky_intensity//8, sky_intensity//2]
                else:
                    # Building with neon lights
                    neon_light = np.sin(x * 0.5 + time_offset * 3) * np.sin(y * 0.3 + time_offset * 2)
                    if abs(neon_light) > 0.7:
                        # Bright neon
                        image[y, x] = [255, 255, 255]
                    else:
                        # Building color
                        image[y, x] = [32, 32, 48]
        
        return image
    
    def _create_fire_effect(self, time_offset):
        """Create animated fire effect."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        for y in range(64):
            for x in range(64):
                # Create fire base
                fire_base = 64 - y
                if fire_base > 0:
                    # Add noise and animation
                    noise = np.sin(x * 0.3 + time_offset * 4) * np.cos(y * 0.2 + time_offset * 3)
                    fire_intensity = fire_base + noise * 20
                    
                    # Create fire colors
                    if fire_intensity > 40:
                        # Hot center (white/yellow)
                        r = min(255, int(fire_intensity * 6))
                        g = min(255, int(fire_intensity * 4))
                        b = min(255, int(fire_intensity * 2))
                    elif fire_intensity > 20:
                        # Medium heat (orange)
                        r = min(255, int(fire_intensity * 8))
                        g = min(255, int(fire_intensity * 4))
                        b = 0
                    else:
                        # Cool edges (red)
                        r = min(255, int(fire_intensity * 10))
                        g = 0
                        b = 0
                    
                    image[y, x] = [r, g, b]
        
        return image
    
    def _create_matrix_rain(self, time_offset):
        """Create Matrix-style digital rain effect."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Create multiple rain streams
        for stream in range(8):
            stream_x = (stream * 8 + int(time_offset * 10)) % 64
            
            for drop in range(10):
                drop_y = (int(time_offset * 20) + drop * 6) % 64
                
                # Create green digital rain
                if 0 <= stream_x < 64 and 0 <= drop_y < 64:
                    intensity = max(0, 255 - drop * 25)
                    image[drop_y, stream_x] = [0, intensity, 0]
                    
                    # Add trail
                    for trail in range(1, 4):
                        trail_y = (drop_y + trail) % 64
                        trail_intensity = max(0, intensity - trail * 50)
                        if trail_intensity > 0:
                            image[trail_y, stream_x] = [0, trail_intensity, 0]
        
        return image
    
    def _create_cosmic_swirl(self, time_offset):
        """Create cosmic swirl effect."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        center_x, center_y = 32, 32
        
        for y in range(64):
            for x in range(64):
                # Calculate polar coordinates
                dx, dy = x - center_x, y - center_y
                distance = np.sqrt(dx*dx + dy*dy)
                angle = np.arctan2(dy, dx)
                
                # Create swirling effect
                swirl = np.sin(angle * 2 + distance * 0.1 + time_offset * 3)
                cosmic = np.cos(angle * 3 - distance * 0.15 + time_offset * 2)
                
                # Combine effects
                intensity = int(128 + 127 * (swirl + cosmic) / 2)
                
                # Create cosmic colors (deep space)
                r = int(intensity * 0.4)
                g = int(intensity * 0.2)
                b = int(intensity * 0.8)
                
                # Add star twinkle
                twinkle = np.sin(distance * 0.5 + time_offset * 5) * np.cos(angle * 4 + time_offset * 3)
                if twinkle > 0.8:
                    r, g, b = 255, 255, 255
                
                image[y, x] = [r, g, b]
        
        return image
    
    def _create_neon_pulse(self, time_offset):
        """Create neon pulse effect."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        for y in range(64):
            for x in range(64):
                # Create pulsing circles
                center1_x, center1_y = 16, 16
                center2_x, center2_y = 48, 48
                
                dist1 = np.sqrt((x - center1_x)**2 + (y - center1_y)**2)
                dist2 = np.sqrt((x - center2_x)**2 + (y - center2_y)**2)
                
                # Pulsing effect
                pulse1 = np.sin(time_offset * 4) * 20 + 15
                pulse2 = np.sin(time_offset * 4 + np.pi) * 20 + 15
                
                # Calculate intensities
                intensity1 = max(0, 255 - dist1 * 8) if dist1 < pulse1 else 0
                intensity2 = max(0, 255 - dist2 * 8) if dist2 < pulse2 else 0
                
                # Combine with different colors
                r = min(255, intensity1)
                g = min(255, intensity2)
                b = min(255, (intensity1 + intensity2) // 2)
                
                image[y, x] = [r, g, b]
        
        return image
    
    def _create_geometric_art(self, time_offset):
        """Create geometric art pattern."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        for y in range(64):
            for x in range(64):
                # Create geometric patterns
                pattern1 = np.sin(x * 0.2 + time_offset) * np.cos(y * 0.2 + time_offset)
                pattern2 = np.sin((x + y) * 0.1 + time_offset * 2)
                pattern3 = np.cos(x * 0.3 - time_offset) * np.sin(y * 0.3 - time_offset)
                
                # Combine patterns
                combined = (pattern1 + pattern2 + pattern3) / 3
                intensity = int(128 + 127 * combined)
                
                # Create geometric color scheme
                r = int(intensity * 0.9)
                g = int(intensity * 0.7)
                b = int(intensity * 0.5)
                
                # Add geometric borders
                if x % 16 == 0 or y % 16 == 0:
                    r, g, b = 255, 255, 255
                
                image[y, x] = [r, g, b]
        
        return image
    
    def stop(self):
        """Stop the application."""
        print("🛑 Stopping SpotiPi Enhanced...")
        self.running = False
        
        if self.matrix_display:
            self.matrix_display.clear_display()
        
        print("✅ SpotiPi Enhanced stopped.")

def main():
    """Main function."""
    print("🎵 SpotiPi Enhanced Demo")
    print("=" * 30)
    print("Enhanced visual effects and animations!")
    print("(No Spotify authentication required)")
    print()
    
    app = SpotiPiEnhanced()
    app.run()

if __name__ == "__main__":
    main() 