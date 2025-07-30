import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import os
import time
from typing import Optional, Dict, Any
import config

class SpotifyClient:
    def __init__(self):
        """Initialize Spotify client with OAuth authentication."""
        self.sp = None
        self.current_track_id = None
        self.current_album_art = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Spotify API using OAuth."""
        scope = "user-read-currently-playing user-read-playback-state"
        
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET,
                redirect_uri=config.SPOTIFY_REDIRECT_URI,
                scope=scope,
                cache_path=".spotify_cache"
            ))
            print("Successfully authenticated with Spotify!")
        except Exception as e:
            print(f"Authentication failed: {e}")
            raise
    
    def get_current_track(self) -> Optional[Dict[str, Any]]:
        """Get information about the currently playing track."""
        try:
            current = self.sp.current_user_playing_track()
            
            if current and current['is_playing']:
                track = current['item']
                if track:
                    track_info = {
                        'id': track['id'],
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': track['album']['name'],
                        'album_art_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'duration_ms': track['duration_ms'],
                        'progress_ms': current['progress_ms']
                    }
                    return track_info
            return None
        except Exception as e:
            print(f"Error getting current track: {e}")
            return None
    
    def has_track_changed(self, track_info: Optional[Dict[str, Any]]) -> bool:
        """Check if the current track has changed."""
        if not track_info:
            return False
        
        new_track_id = track_info.get('id')
        if new_track_id != self.current_track_id:
            self.current_track_id = new_track_id
            return True
        return False
    
    def download_album_art(self, url: str, filename: str) -> str:
        """Download album art image from URL."""
        try:
            # Create cache directory if it doesn't exist
            os.makedirs(config.IMAGE_CACHE_DIR, exist_ok=True)
            
            filepath = os.path.join(config.IMAGE_CACHE_DIR, filename)
            
            # Download the image
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return filepath
        except Exception as e:
            print(f"Error downloading album art: {e}")
            return None
    
    def get_album_art_path(self, track_info: Dict[str, Any]) -> Optional[str]:
        """Get the local path to album art image."""
        if not track_info or not track_info.get('album_art_url'):
            return None
        
        # Create filename from track ID
        filename = f"{track_info['id']}.jpg"
        filepath = os.path.join(config.IMAGE_CACHE_DIR, filename)
        
        # If file doesn't exist, download it
        if not os.path.exists(filepath):
            return self.download_album_art(track_info['album_art_url'], filename)
        
        return filepath
    
    def cleanup_cache(self, max_files: int = 50):
        """Clean up old cached images to prevent disk space issues."""
        try:
            cache_dir = config.IMAGE_CACHE_DIR
            if not os.path.exists(cache_dir):
                return
            
            files = os.listdir(cache_dir)
            if len(files) <= max_files:
                return
            
            # Sort files by modification time (oldest first)
            file_paths = [os.path.join(cache_dir, f) for f in files]
            file_paths.sort(key=os.path.getmtime)
            
            # Remove oldest files
            files_to_remove = file_paths[:len(file_paths) - max_files]
            for file_path in files_to_remove:
                try:
                    os.remove(file_path)
                except OSError:
                    pass
                    
        except Exception as e:
            print(f"Error cleaning cache: {e}") 