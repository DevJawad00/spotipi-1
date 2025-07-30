#!/usr/bin/env python3
"""
SpotiPi Enhanced Mode

This displays album art with basic enhancements for better appearance.
"""

import time
import signal
import sys
import os
import numpy as np
from datetime import datetime
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
            # Initialize Spotify client
            print("📡 Connecting to Spotify...")
            self.spotify_client = SpotifyClient()
            
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
    
    def create_enhanced_image(self, image_url):
        """Create an enhanced version of the album art."""
        try:
            # Download the image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Open with PIL
            img = Image.open(io.BytesIO(response.content))
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Apply basic enhancements
            img = self._enhance_image(img)
            
            # Resize to 64x64
            img = img.resize((64, 64), Image.LANCZOS)
            
            # Convert to numpy array
            img_array = np.array(img)
            
            return img_array
            
        except Exception as e:
            print(f"❌ Error creating enhanced image: {e}")
            return self._create_placeholder_image()
    
    def _enhance_image(self, img):
        """Apply basic image enhancements."""
        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Increase saturation
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)
        
        # Increase brightness slightly
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        
        return img
    
    def _create_placeholder_image(self):
        """Create a placeholder image when album art fails to load."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Create a simple gradient pattern
        for y in range(64):
            for x in range(64):
                r = int(128 + 127 * (x / 64))
                g = int(128 + 127 * (y / 64))
                b = int(128 + 127 * ((x + y) / 128))
                image[y, x] = [r, g, b]
        
        return image
    
    def run(self):
        """Main application loop."""
        if not self.initialize():
            return
        
        self.running = True
        print("🎵 SpotiPi Enhanced is running! Press Ctrl+C to stop.")
        print("📺 Monitoring Spotify playback...")
        print()
        
        while self.running:
            try:
                # Get current track info
                track_info = self.spotify_client.get_current_track()
                
                if track_info:
                    # Check if track has changed
                    if isinstance(track_info, dict) and self.spotify_client.has_track_changed(track_info):
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
        track_id = track_info.get('id') if track_info else None
        track_name = track_info.get('name', 'Unknown') if track_info else 'Unknown'
        artist_name = track_info.get('artist', 'Unknown') if track_info else 'Unknown'
        album_art_url = track_info.get('album_art_url') if track_info else None
        
        print(f"🎵 Now playing: {track_name} by {artist_name}")
        
        if album_art_url:
            print("🖼️  Creating enhanced album art...")
            enhanced_image = self.create_enhanced_image(album_art_url)
            self.matrix_display.display_image(enhanced_image, 0.1)
            print("✅ Enhanced album art displayed!")
        else:
            print("⚠️  No album art available")
            placeholder = self._create_placeholder_image()
            self.matrix_display.display_image(placeholder, 0.1)
        
        self.current_track_id = track_id
    
    def _handle_no_track(self):
        """Handle when no track is playing."""
        print("⏸️  No track currently playing")
        # Show a simple animated pattern
        idle_image = np.zeros((64, 64, 3), dtype=np.uint8)
        current_time = time.time()
        
        for y in range(64):
            for x in range(64):
                # Create a simple wave pattern
                wave = np.sin(x * 0.2 + current_time) * np.cos(y * 0.2 + current_time)
                intensity = int(128 + 127 * wave)
                
                # Simple color variation
                r = int(intensity * 0.8)
                g = int(intensity * 0.6)
                b = int(intensity)
                
                idle_image[y, x] = [r, g, b]
        
        self.matrix_display.display_image(idle_image, 0.1)
    
    def stop(self):
        """Stop the application."""
        print("🛑 Stopping SpotiPi Enhanced...")
        self.running = False
        
        if self.matrix_display:
            self.matrix_display.clear_display()
        
        print("✅ SpotiPi Enhanced stopped.")

def main():
    """Main function."""
    print("🎵 SpotiPi Enhanced Mode")
    print("=" * 30)
    print("This will display album art with basic enhancements!")
    print()
    
    app = SpotiPiEnhanced()
    app.run()

if __name__ == "__main__":
    main() 