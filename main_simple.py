#!/usr/bin/env python3
"""
SpotiPi Simple Demo

A simplified version that shows how the matrix will work without requiring Spotify authentication.
"""

import time
import signal
import sys
import os
import numpy as np
from datetime import datetime

# Import our modules
from image_processor import ImageProcessor
from matrix_display import MatrixDisplay

class SpotiPiSimple:
    def __init__(self):
        """Initialize SpotiPi Simple application."""
        self.running = False
        self.image_processor = None
        self.matrix_display = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.stop()
    
    def initialize(self):
        """Initialize all components."""
        print("🎵 Initializing SpotiPi Simple...")
        
        try:
            # Initialize image processor
            print("🖼️  Initializing image processor...")
            self.image_processor = ImageProcessor()
            
            # Initialize matrix display
            print("📺 Initializing RGB matrix...")
            self.matrix_display = MatrixDisplay()
            
            print("✅ SpotiPi Simple initialized successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False
    
    def run(self):
        """Main application loop."""
        if not self.initialize():
            return
        
        self.running = True
        print("🎵 SpotiPi Simple is running! Press Ctrl+C to stop.")
        print("📺 Displaying demo images on matrix...")
        print()
        
        # Display startup animation
        self._display_startup_animation()
        
        # Demo loop
        demo_images = [
            self._create_album_art_1(),
            self._create_album_art_2(),
            self._create_album_art_3(),
            self._create_album_art_4()
        ]
        
        image_index = 0
        
        while self.running:
            try:
                # Display current demo image
                current_image = demo_images[image_index]
                print(f"🎨 Displaying demo image {image_index + 1}/4...")
                
                self.matrix_display.display_image(current_image, 0.1)
                
                # Wait and cycle to next image
                time.sleep(5)
                image_index = (image_index + 1) % len(demo_images)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(1)
        
        self.stop()
    
    def _display_startup_animation(self):
        """Display startup animation."""
        print("🚀 Starting up...")
        
        # Create a startup animation
        for i in range(10):
            # Create a pulsing circle
            image = np.zeros((64, 64, 3), dtype=np.uint8)
            center_x, center_y = 32, 32
            radius = 5 + i * 2
            
            for y in range(64):
                for x in range(64):
                    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                    if distance <= radius:
                        intensity = int(255 * (1 - distance / radius))
                        image[y, x] = [intensity, 0, intensity]  # Purple
            
            self.matrix_display.display_image(image, 0.1)
            time.sleep(0.1)
        
        # Clear
        black_image = np.zeros((64, 64, 3), dtype=np.uint8)
        self.matrix_display.display_image(black_image, 0.1)
    
    def _create_album_art_1(self):
        """Create demo album art 1."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Create a red gradient
        for y in range(64):
            for x in range(64):
                intensity = int(255 * (x + y) / 128)
                image[y, x] = [intensity, 0, 0]
        
        return image
    
    def _create_album_art_2(self):
        """Create demo album art 2."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Create a blue circle
        center_x, center_y = 32, 32
        radius = 25
        
        for y in range(64):
            for x in range(64):
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                if distance <= radius:
                    intensity = int(255 * (1 - distance / radius))
                    image[y, x] = [0, 0, intensity]
        
        return image
    
    def _create_album_art_3(self):
        """Create demo album art 3."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Create a green pattern
        for y in range(64):
            for x in range(64):
                if (x // 8 + y // 8) % 2 == 0:
                    image[y, x] = [0, 255, 0]
        
        return image
    
    def _create_album_art_4(self):
        """Create demo album art 4."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Create a rainbow pattern
        for y in range(64):
            for x in range(64):
                r = int(255 * (x / 64))
                g = int(255 * (y / 64))
                b = int(255 * ((x + y) / 128))
                image[y, x] = [r, g, b]
        
        return image
    
    def stop(self):
        """Stop the application."""
        print("🛑 Stopping SpotiPi Simple...")
        self.running = False
        
        if self.matrix_display:
            self.matrix_display.clear_display()
        
        print("✅ SpotiPi Simple stopped.")

def main():
    """Main function."""
    print("🎵 SpotiPi Simple Demo")
    print("=" * 25)
    print("This will show demo images on your RGB matrix!")
    print("(No Spotify authentication required)")
    print()
    
    app = SpotiPiSimple()
    app.run()

if __name__ == "__main__":
    main() 