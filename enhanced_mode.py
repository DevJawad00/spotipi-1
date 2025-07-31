#!/usr/bin/env python3
"""
SpotiPi Enhanced Mode

This displays album art with enhanced visual effects for better appearance.
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
        self.last_playback_state = None  # Track if playing/paused
        
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
            
            # Enhance the image
            img = self._enhance_image(img)
            
            # Resize to 64x64
            img = img.resize((64, 64), Image.LANCZOS)
            
            # Convert to numpy array
            img_array = np.array(img)
            
            # Apply color enhancement
            img_array = self._enhance_colors(img_array)
            
            return img_array
            
        except Exception as e:
            print(f"❌ Error creating enhanced image: {e}")
            return self._create_placeholder_image()
    
    def _enhance_image(self, img):
        """Apply image enhancements."""
        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.3)
        
        # Increase saturation
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.4)
        
        # Increase brightness slightly
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        
        # Apply sharpening
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)
        
        return img
    
    def _enhance_colors(self, img_array):
        """Enhance colors for better matrix display."""
        # Convert to float for processing
        img_float = img_array.astype(np.float32) / 255.0
        
        # Apply gamma correction for better color reproduction
        gamma = 0.8
        img_float = np.power(img_float, gamma)
        
        # Increase saturation
        # Convert to HSV
        hsv = self._rgb_to_hsv(img_float)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 1)  # Increase saturation
        img_float = self._hsv_to_rgb(hsv)
        
        # Convert back to uint8
        img_array = np.clip(img_float * 255, 0, 255).astype(np.uint8)
        
        return img_array
    
    def _rgb_to_hsv(self, rgb):
        """Convert RGB to HSV."""
        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
        
        max_rgb = np.maximum(np.maximum(r, g), b)
        min_rgb = np.minimum(np.minimum(r, g), b)
        diff = max_rgb - min_rgb
        
        # Hue
        h = np.zeros_like(max_rgb)
        h[max_rgb == r] = (60 * ((g[max_rgb == r] - b[max_rgb == r]) / diff[max_rgb == r]) % 360) / 360
        h[max_rgb == g] = (60 * ((b[max_rgb == g] - r[max_rgb == g]) / diff[max_rgb == g] + 2) % 360) / 360
        h[max_rgb == b] = (60 * ((r[max_rgb == b] - g[max_rgb == b]) / diff[max_rgb == b] + 4) % 360) / 360
        
        # Saturation
        s = np.where(max_rgb == 0, 0, diff / max_rgb)
        
        # Value
        v = max_rgb
        
        return np.stack([h, s, v], axis=2)
    
    def _hsv_to_rgb(self, hsv):
        """Convert HSV to RGB."""
        h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
        
        h = h * 360
        c = v * s
        x = c * (1 - np.abs((h / 60) % 2 - 1))
        m = v - c
        
        r = np.zeros_like(h)
        g = np.zeros_like(h)
        b = np.zeros_like(h)
        
        mask = (h >= 0) & (h < 60)
        r[mask] = c[mask]
        g[mask] = x[mask]
        b[mask] = 0
        
        mask = (h >= 60) & (h < 120)
        r[mask] = x[mask]
        g[mask] = c[mask]
        b[mask] = 0
        
        mask = (h >= 120) & (h < 180)
        r[mask] = 0
        g[mask] = c[mask]
        b[mask] = x[mask]
        
        mask = (h >= 180) & (h < 240)
        r[mask] = 0
        g[mask] = x[mask]
        b[mask] = c[mask]
        
        mask = (h >= 240) & (h < 300)
        r[mask] = x[mask]
        g[mask] = 0
        b[mask] = c[mask]
        
        mask = (h >= 300) & (h < 360)
        r[mask] = c[mask]
        g[mask] = 0
        b[mask] = x[mask]
        
        r = r + m
        g = g + m
        b = b + m
        
        return np.stack([r, g, b], axis=2)
    
    def _create_placeholder_image(self):
        """Create a placeholder image when album art fails to load."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        
        # Create a gradient pattern
        for y in range(64):
            for x in range(64):
                r = int(255 * (x / 64))
                g = int(255 * (y / 64))
                b = int(255 * ((x + y) / 128))
                image[y, x] = [r, g, b]
        
        return image
    
    def _has_playback_state_changed(self, track_info):
        """Check if playback state (playing/paused) has changed."""
        if not track_info:
            return False
        
        current_playing = track_info.get('is_playing', False)
        
        # If this is the first check, just store the state
        if self.last_playback_state is None:
            self.last_playback_state = current_playing
            return False
        
        # Check if state changed
        if current_playing != self.last_playback_state:
            self.last_playback_state = current_playing
            return True
        
        return False
    
    def _should_display_album_art(self, track_info):
        """Determine if we should display album art based on track info."""
        if not track_info:
            return False
        
        # If we have a track with album art, display it
        # Don't rely solely on is_playing as it can be unreliable
        album_art_url = track_info.get('album_art_url')
        track_name = track_info.get('name')
        
        return album_art_url is not None and track_name is not None
    
    def run(self):
        """Main application loop."""
        if not self.initialize():
            return
        
        self.running = True
        print("🎵 SpotiPi Enhanced is running! Press Ctrl+C to stop.")
        print("📺 Monitoring Spotify playback...")
        print("⏸️  Will detect play/pause and track changes!")
        print()
        
        # Display startup animation
        self._display_startup_animation()
        
        while self.running:
            try:
                # Get current track info
                track_info = self.spotify_client.get_current_track()
                
                if track_info:
                    # Check if track has changed OR playback state has changed
                    track_changed = isinstance(track_info, dict) and self.spotify_client.has_track_changed(track_info)
                    playback_changed = self._has_playback_state_changed(track_info)
                    
                    if track_changed or playback_changed:
                        self._handle_track_change(track_info)
                    else:
                        # Check if we should display album art (in case API was wrong before)
                        if self._should_display_album_art(track_info) and self.current_track_id != track_info.get('id'):
                            print("🔄 Re-checking track info...")
                            self._handle_track_change(track_info)
                        else:
                            # Track is still playing, just wait
                            time.sleep(2)
                else:
                    # No track playing, show idle state
                    if self.current_track_id is not None:
                        print("⏸️  No track detected, switching to idle...")
                        self.current_track_id = None
                    self._handle_no_track()
                    time.sleep(2)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(5)
        
        self.stop()
    
    def _handle_track_change(self, track_info):
        """Handle when a track changes or playback state changes."""
        track_id = track_info.get('id') if track_info else None
        track_name = track_info.get('name', 'Unknown') if track_info else 'Unknown'
        artist_name = track_info.get('artist', 'Unknown') if track_info else 'Unknown'
        album_art_url = track_info.get('album_art_url') if track_info else None
        is_playing = track_info.get('is_playing', False) if track_info else False
        
        print(f"🎵 Track: {track_name} by {artist_name}")
        print(f"▶️  Playing: {is_playing}")
        
        # If we have a track with album art, assume it's playing
        # (Spotify API sometimes incorrectly reports is_playing as false)
        if track_info and album_art_url:
            print("🖼️  Creating enhanced album art...")
            enhanced_image = self.create_enhanced_image(album_art_url)
            self.matrix_display.display_image(enhanced_image, 0.1)
            print("✅ Enhanced album art displayed!")
        elif track_info and not album_art_url:
            print("⚠️  No album art available")
            placeholder = self._create_placeholder_image()
            self.matrix_display.display_image(placeholder, 0.1)
        else:
            print("⏸️  No track detected, showing idle pattern...")
            self._handle_no_track()
        
        self.current_track_id = track_id
    
    def _handle_no_track(self):
        """Handle when no track is playing or track is paused."""
        print("⏸️  No track currently playing or paused")
        # Show a really cool animated pattern
        idle_image = self._create_cool_idle_animation()
        self.matrix_display.display_image(idle_image, 0.1)
    
    def _create_cool_idle_animation(self):
        """Create a spinning square animation with colors."""
        image = np.zeros((64, 64, 3), dtype=np.uint8)
        current_time = time.time()
        
        # Square properties
        center_x, center_y = 32, 32
        square_size = 20
        rotation_speed = 2.0
        
        # Calculate rotation angle
        angle = current_time * rotation_speed
        
        # Create spinning square
        for y in range(64):
            for x in range(64):
                # Calculate distance from center
                dx = x - center_x
                dy = y - center_y
                
                # Rotate the point
                cos_a = np.cos(angle)
                sin_a = np.sin(angle)
                rotated_x = dx * cos_a - dy * sin_a
                rotated_y = dx * sin_a + dy * cos_a
                
                # Check if point is inside the square
                if abs(rotated_x) <= square_size and abs(rotated_y) <= square_size:
                    # Create color based on position and time
                    color_phase = (current_time * 0.8) % 6  # 6 different color phases
                    
                    # Calculate intensity based on distance from center
                    distance = np.sqrt(rotated_x**2 + rotated_y**2)
                    max_distance = square_size * np.sqrt(2)
                    intensity = int(255 * (1 - distance / max_distance))
                    
                    # Apply color scheme
                    if color_phase < 1:  # Red
                        r, g, b = intensity, 0, 0
                    elif color_phase < 2:  # Orange
                        r, g, b = intensity, int(intensity * 0.5), 0
                    elif color_phase < 3:  # Yellow
                        r, g, b = intensity, intensity, 0
                    elif color_phase < 4:  # Green
                        r, g, b = 0, intensity, 0
                    elif color_phase < 5:  # Blue
                        r, g, b = 0, 0, intensity
                    else:  # Purple
                        r, g, b = int(intensity * 0.5), 0, intensity
                    
                    # Add some variation based on position
                    variation = np.sin(rotated_x * 0.2 + current_time) * np.cos(rotated_y * 0.2 + current_time)
                    brightness = 0.8 + 0.2 * variation
                    
                    r = int(r * brightness)
                    g = int(g * brightness)
                    b = int(b * brightness)
                    
                    image[y, x] = [r, g, b]
                else:
                    # Background - subtle gradient
                    bg_intensity = int(32 + 16 * np.sin(x * 0.1 + current_time * 0.5))
                    image[y, x] = [bg_intensity//4, bg_intensity//8, bg_intensity//2]
        
        return image
    
    def _display_startup_animation(self):
        """Display startup animation."""
        print("🚀 Starting up...")
        
        # Create a beautiful startup animation
        for i in range(20):
            image = np.zeros((64, 64, 3), dtype=np.uint8)
            
            # Create expanding circles
            center_x, center_y = 32, 32
            radius = 2 + i * 2
            
            for y in range(64):
                for x in range(64):
                    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                    if distance <= radius:
                        intensity = int(255 * (1 - distance / radius))
                        # Rainbow colors
                        hue = (i * 18) % 360
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
        
        # Clear
        black_image = np.zeros((64, 64, 3), dtype=np.uint8)
        self.matrix_display.display_image(black_image, 0.1)
    
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
    print("This will display album art with enhanced visual effects!")
    print("Detects play/pause and track changes!")
    print()
    
    app = SpotiPiEnhanced()
    app.run()

if __name__ == "__main__":
    main()