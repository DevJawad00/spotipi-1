#!/usr/bin/env python3
"""
SpotiPi - Spotify Album Art Display

Main application that monitors Spotify playback and displays album art
on a 64x64 RGB LED matrix.
"""

import time
import signal
import sys
import os
import numpy as np
from datetime import datetime
import config

# Import our modules
from spotify_client import SpotifyClient
from image_processor import ImageProcessor
from matrix_display import MatrixDisplay

class SpotiPi:
    def __init__(self):
        """Initialize SpotiPi application."""
        self.running = False
        self.spotify_client = None
        self.image_processor = None
        self.matrix_display = None
        self.current_track_id = None
        self.current_image = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.stop()
    
    def initialize(self):
        """Initialize all components."""
        print("🎵 Initializing SpotiPi...")
        
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
            
            print("✅ SpotiPi initialized successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False
    
    def run(self):
        """Main application loop."""
        if not self.initialize():
            return
        
        self.running = True
        print("🎵 SpotiPi is running! Press Ctrl+C to stop.")
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
                        time.sleep(config.UPDATE_INTERVAL)
                else:
                    # No track playing, show idle state
                    self._handle_no_track()
                    time.sleep(config.UPDATE_INTERVAL)
                
                # Periodic cleanup
                if datetime.now().second % 60 == 0:  # Every minute
                    self.spotify_client.cleanup_cache()
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(config.UPDATE_INTERVAL)
        
        self.stop()
    
    def _handle_track_change(self, track_info):
        """Handle when a new track starts playing."""
        print(f"🎵 Now playing: {track_info['name']} - {track_info['artist']}")
        
        # Get album art path
        album_art_path = self.spotify_client.get_album_art_path(track_info)
        
        if album_art_path:
            # Process and display the image
            new_image = self.image_processor.load_and_process_image(album_art_path)
            
            if self.current_image is not None:
                # Display transition
                print("🔄 Transitioning to new album art...")
                self.matrix_display.display_transition(self.current_image, new_image)
            else:
                # First image, display directly
                self.matrix_display.display_image(new_image)
            
            self.current_image = new_image
            print("✅ Album art displayed!")
        else:
            print("⚠️  No album art available")
            self._display_placeholder()
    
    def _handle_no_track(self):
        """Handle when no track is playing."""
        if self.current_track_id is not None:
            print("⏸️  No track currently playing")
            self.current_track_id = None
            self._display_idle_animation()
    
    def _display_startup_animation(self):
        """Display startup animation on the matrix."""
        print("🚀 Displaying startup animation...")
        
        # Create a simple startup pattern
        startup_image = self.image_processor._create_placeholder_image()
        
        # Add some animation frames
        for i in range(10):
            # Create pulsing effect
            brightness = int(128 + 127 * (i % 2))
            frame = startup_image.copy()
            frame = (frame * brightness // 255).astype(np.uint8)
            self.matrix_display.display_image(frame, 0.1)
        
        print("✅ Startup complete!")
    
    def _display_placeholder(self):
        """Display placeholder when no album art is available."""
        placeholder = self.image_processor._create_placeholder_image()
        self.matrix_display.display_image(placeholder)
    
    def _display_idle_animation(self):
        """Display idle animation when no track is playing."""
        print("💤 Displaying idle animation...")
        
        # Create a simple breathing animation
        for i in range(20):
            brightness = int(50 + 30 * (i % 10) / 10)
            frame = self.current_image.copy() if self.current_image is not None else self.image_processor._create_placeholder_image()
            frame = (frame * brightness // 100).astype(np.uint8)
            self.matrix_display.display_image(frame, 0.2)
    
    def stop(self):
        """Stop the application and cleanup."""
        print("🛑 Stopping SpotiPi...")
        self.running = False
        
        if self.matrix_display:
            self.matrix_display.clear_display()
            self.matrix_display.cleanup()
        
        print("✅ SpotiPi stopped. Goodbye! 👋")

def main():
    """Main entry point."""
    print("🎵 SpotiPi - Spotify Album Art Display")
    print("=" * 40)
    
    # Check if running on Raspberry Pi
    if not os.path.exists('/proc/cpuinfo') or 'Raspberry Pi' not in open('/proc/cpuinfo').read():
        print("⚠️  Warning: This appears to be running on a non-Raspberry Pi system.")
        print("   The RGB matrix will run in simulation mode.")
        print()
    
    # Create and run SpotiPi
    spotipi = SpotiPi()
    spotipi.run()

if __name__ == "__main__":
    main() 