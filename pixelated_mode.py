#!/usr/bin/env python3
"""
SpotiPi Pixelated Mode

This displays album art at a lower resolution for a more retro, pixelated look.
"""

import time
import signal
import sys
import os
import numpy as np
from datetime import datetime
import requests
from PIL import Image
import io

# Import our modules
from spotify_client import SpotifyClient
from image_processor import ImageProcessor
from matrix_display import MatrixDisplay

class SpotiPiPixelated:
    def __init__(self, resolution=16):
        """Initialize SpotiPi Pixelated application."""
        self.running = False
        self.spotify_client = None
        self.image_processor = None
        self.matrix_display = None
        self.current_track_id = None
        self.resolution = resolution  # 16x16, 32x32, etc.
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.stop()
    
    def initialize(self):
        """Initialize all components."""
        print("🎵 Initializing SpotiPi Pixelated...")
        print(f"📺 Resolution: {self.resolution}x{self.resolution}")
        
        try:
            # Initialize Spotify client
            print("📡 Connecting to Spotify...")
            self.spotify_client = SpotifyClient()
            
            # Initialize image processor
            print("🖼️  Initializing image processor...")
            self.image_processor = ImageProcessor()
            
            # Initialize matrix display
            print("📺 Initializing RGB matrix...")
            self.matrix_display = MatrixDisplay()
            
            print("✅ SpotiPi Pixelated initialized successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False
    
    def create_pixelated_image(self, image_url):
        """Create a pixelated version of the album art."""
        try:
            # Download the image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Open with PIL
            img = Image.open(io.BytesIO(response.content))
            
            # Resize to our target resolution (this creates the pixelated effect)
            img = img.resize((self.resolution, self.resolution), Image.NEAREST)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert to numpy array
            img_array = np.array(img)
            
            # Scale up to 64x64 for the matrix (each pixel becomes a block)
            block_size = 64 // self.resolution
            final_image = np.zeros((64, 64, 3), dtype=np.uint8)
            
            for y in range(self.resolution):
                for x in range(self.resolution):
                    # Get the pixel color
                    r, g, b = img_array[y, x]
                    
                    # Create a block of this color
                    start_y = y * block_size
                    end_y = (y + 1) * block_size
                    start_x = x * block_size
                    end_x = (x + 1) * block_size
                    
                    final_image[start_y:end_y, start_x:end_x] = [r, g, b]
            
            return final_image
            
        except Exception as e:
            print(f"❌ Error creating pixelated image: {e}")
            return self._create_placeholder_image()
    
    def _create_placeholder_image(self):
        """Create a placeholder image when album art fails to load."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Create a simple pattern
        for y in range(64):
            for x in range(64):
                if (x // 8 + y // 8) % 2 == 0:
                    image[y, x] = [255, 0, 0]  # Red
                else:
                    image[y, x] = [0, 0, 255]  # Blue
        
        return image
    
    def run(self):
        """Main application loop."""
        if not self.initialize():
            return
        
        self.running = True
        print("🎵 SpotiPi Pixelated is running! Press Ctrl+C to stop.")
        print("📺 Monitoring Spotify playback...")
        print()
        
        # Display startup animation
        self._display_startup_animation()
        
        while self.running:
            try:
                # Get current track info
                track_info = self.spotify_client.get_current_track()
                
                if track_info:
                    # Check if track has changed
                    if self.spotify_client.has_track_changed(track_info):
                        self._handle_track_change(track_info)
                    else:
                        # Track is still playing, just wait
                        time.sleep(5)
                else:
                    # No track playing, show idle state
                    self._handle_no_track()
                    time.sleep(5)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(5)
        
        self.stop()
    
    def _handle_track_change(self, track_info):
        """Handle when a track changes."""
        track_id = track_info.get('id')
        track_name = track_info.get('name', 'Unknown')
        artist_name = track_info.get('artists', [{}])[0].get('name', 'Unknown')
        album_art_url = track_info.get('album', {}).get('images', [{}])[0].get('url')
        
        print(f"🎵 Now playing: {track_name} by {artist_name}")
        
        if album_art_url:
            print("🖼️  Creating pixelated album art...")
            pixelated_image = self.create_pixelated_image(album_art_url)
            self.matrix_display.display_image(pixelated_image, 0.1)
            print("✅ Pixelated album art displayed!")
        else:
            print("⚠️  No album art available")
            placeholder = self._create_placeholder_image()
            self.matrix_display.display_image(placeholder, 0.1)
        
        self.current_track_id = track_id
    
    def _handle_no_track(self):
        """Handle when no track is playing."""
        print("⏸️  No track currently playing")
        # Show a simple idle pattern
        idle_image = np.zeros((64, 64, 3), dtype=np.uint8)
        for y in range(64):
            for x in range(64):
                if (x + y) % 16 < 8:
                    idle_image[y, x] = [0, 255, 0]  # Green
        self.matrix_display.display_image(idle_image, 0.1)
    
    def _display_startup_animation(self):
        """Display startup animation."""
        print("🚀 Starting up...")
        
        # Create a pixelated startup animation
        for i in range(8):
            image = np.zeros((64, 64, 3), dtype=np.uint8)
            
            # Create a simple pixelated pattern
            block_size = 8
            for y in range(0, 64, block_size):
                for x in range(0, 64, block_size):
                    if (x // block_size + y // block_size + i) % 2 == 0:
                        image[y:y+block_size, x:x+block_size] = [255, 0, 255]  # Magenta
            
            self.matrix_display.display_image(image, 0.1)
            time.sleep(0.2)
        
        # Clear
        black_image = np.zeros((64, 64, 3), dtype=np.uint8)
        self.matrix_display.display_image(black_image, 0.1)
    
    def stop(self):
        """Stop the application."""
        print("🛑 Stopping SpotiPi Pixelated...")
        self.running = False
        
        if self.matrix_display:
            self.matrix_display.clear_display()
        
        print("✅ SpotiPi Pixelated stopped.")

def main():
    """Main function."""
    print("🎵 SpotiPi Pixelated Mode")
    print("=" * 30)
    print("Choose resolution:")
    print("1. 16x16 (very pixelated)")
    print("2. 32x32 (medium pixelated)")
    print("3. 48x48 (slightly pixelated)")
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            resolution = 16
        elif choice == "2":
            resolution = 32
        elif choice == "3":
            resolution = 48
        else:
            print("Invalid choice, using 16x16")
            resolution = 16
    except KeyboardInterrupt:
        print("\n🛑 Cancelled")
        return
    
    print(f"🎨 Using {resolution}x{resolution} resolution")
    print()
    
    app = SpotiPiPixelated(resolution)
    app.run()

if __name__ == "__main__":
    main() 