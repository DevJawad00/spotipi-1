#!/usr/bin/env python3
"""
SpotiPi Enhanced Mode

Simple and stable album art display for Spotify.
"""

import time
import signal
import sys
import os
import numpy as np
import requests
from PIL import Image, ImageEnhance
import io

# Import our modules
from spotify_client import SpotifyClient
from image_processor import ImageProcessor
from matrix_display import MatrixDisplay

class SpotiPiEnhanced:
    def __init__(self):
        """Initialize SpotiPi Enhanced application."""
        self.running = False
        self.spotify_client = None
        self.image_processor = None
        self.matrix_display = None
        self.current_track_id = None
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\n🛑 Shutting down...")
        self.stop()
    
    def initialize(self):
        """Initialize all components."""
        print("🎵 Initializing SpotiPi Enhanced...")
        
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
            
            print("✅ Initialization complete!")
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False
    
    def process_album_art(self, image_url):
        """Process album art for display."""
        try:
            # Download image
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Open with PIL
            img = Image.open(io.BytesIO(response.content))
            
            # Convert to RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Apply basic enhancements
            img = self._apply_enhancements(img)
            
            # Resize to 64x64
            img = img.resize((64, 64), Image.Resampling.LANCZOS)
            
            # Convert to numpy array
            img_array = np.array(img, dtype=np.uint8)
            
            return img_array
            
        except Exception as e:
            print(f"❌ Error processing image: {e}")
            return self._create_placeholder()
    
    def _apply_enhancements(self, img):
        """Apply basic image enhancements."""
        try:
            # Moderate contrast increase
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            # Moderate saturation increase
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.3)
            
            # Slight brightness increase
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.1)
            
            return img
        except Exception as e:
            print(f"Enhancement failed: {e}")
            return img
    
    def _create_placeholder(self):
        """Create a placeholder image."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Simple gradient pattern
        for y in range(64):
            for x in range(64):
                r = int(64 + 64 * (x / 64))
                g = int(64 + 64 * (y / 64))
                b = int(128 + 64 * ((x + y) / 128))
                image[y, x] = [r, g, b]
        
        return image
    
    def _create_idle_pattern(self):
        """Create an idle pattern."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        current_time = time.time()
        
        for y in range(64):
            for x in range(64):
                # Simple wave pattern
                wave = np.sin(x * 0.1 + current_time * 0.5) * np.cos(y * 0.1 + current_time * 0.3)
                intensity = int(64 + 64 * wave)
                
                # Blue-tinted pattern
                r = int(intensity * 0.3)
                g = int(intensity * 0.5)
                b = int(intensity)
                
                image[y, x] = [r, g, b]
        
        return image
    
    def run(self):
        """Main application loop."""
        if not self.initialize():
            return
        
        self.running = True
        print("🎵 SpotiPi Enhanced is running!")
        print("📺 Monitoring Spotify playback...")
        print()
        
        # Show initial idle pattern
        idle_image = self._create_idle_pattern()
        self.matrix_display.display_image(idle_image, 0.1)
        
        while self.running:
            try:
                # Get current track info
                track_info = self.spotify_client.get_current_track()
                
                if track_info:
                    # Check if track changed
                    if isinstance(track_info, dict) and self.spotify_client.has_track_changed(track_info):
                        self._handle_track_change(track_info)
                    else:
                        # Update idle pattern occasionally
                        time.sleep(2)
                        idle_image = self._create_idle_pattern()
                        self.matrix_display.display_image(idle_image, 0.1)
                else:
                    # No track playing
                    time.sleep(2)
                    idle_image = self._create_idle_pattern()
                    self.matrix_display.display_image(idle_image, 0.1)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(5)
        
        self.stop()
    
    def _handle_track_change(self, track_info):
        """Handle track changes."""
        try:
            track_id = track_info.get('id')
            track_name = track_info.get('name', 'Unknown')
            artist_name = track_info.get('artist', 'Unknown')
            album_art_url = track_info.get('album_art_url')
            
            print(f"🎵 Now playing: {track_name} by {artist_name}")
            
            if album_art_url:
                print("🖼️  Processing album art...")
                processed_image = self.process_album_art(album_art_url)
                self.matrix_display.display_image(processed_image, 0.1)
                print("✅ Album art displayed!")
            else:
                print("⚠️  No album art available")
                placeholder = self._create_placeholder()
                self.matrix_display.display_image(placeholder, 0.1)
            
            self.current_track_id = track_id
            
        except Exception as e:
            print(f"❌ Error handling track change: {e}")
            placeholder = self._create_placeholder()
            self.matrix_display.display_image(placeholder, 0.1)
    
    def stop(self):
        """Stop the application."""
        print("🛑 Stopping SpotiPi Enhanced...")
        self.running = False
        
        if self.matrix_display:
            try:
                self.matrix_display.clear_display()
            except Exception as e:
                print(f"Error clearing display: {e}")
        
        print("✅ SpotiPi Enhanced stopped.")

def main():
    """Main function."""
    print("🎵 SpotiPi Enhanced Mode")
    print("=" * 30)
    print("Simple and stable album art display")
    print()
    
    app = SpotiPiEnhanced()
    app.run()

if __name__ == "__main__":
    main()