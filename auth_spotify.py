#!/usr/bin/env python3
"""
Spotify Authentication Helper for SpotiPi

This script helps you authenticate with Spotify API and get the necessary tokens.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import config
import os

def main():
    print("=== SpotiPi Spotify Authentication ===")
    print()
    
    # Check if credentials are configured
    if (config.SPOTIFY_CLIENT_ID == "your_client_id_here" or 
        config.SPOTIFY_CLIENT_SECRET == "your_client_secret_here"):
        print("❌ Spotify credentials not configured!")
        print()
        print("Please follow these steps:")
        print("1. Go to https://developer.spotify.com/dashboard")
        print("2. Create a new application")
        print("3. Get your Client ID and Client Secret")
        print("4. Edit config.py and add your credentials")
        print()
        print("Example config.py:")
        print("SPOTIFY_CLIENT_ID = 'your_actual_client_id'")
        print("SPOTIFY_CLIENT_SECRET = 'your_actual_client_secret'")
        print("SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'")
        print()
        return
    
    print("✅ Spotify credentials found in config.py")
    print()
    
    # Set up OAuth scope
    scope = "user-read-currently-playing user-read-playback-state"
    
    try:
        print("🔐 Starting Spotify authentication...")
        print("This will open your browser for authentication.")
        print()
        
        # Create Spotify OAuth manager
        sp_oauth = SpotifyOAuth(
            client_id=config.SPOTIFY_CLIENT_ID,
            client_secret=config.SPOTIFY_CLIENT_SECRET,
            redirect_uri=config.SPOTIFY_REDIRECT_URI,
            scope=scope,
            cache_path=".spotify_cache"
        )
        
        # Get authorization URL
        auth_url = sp_oauth.get_authorize_url()
        
        print(f"🌐 Opening browser to: {auth_url}")
        print("Please complete the authentication in your browser.")
        print()
        
        # Open browser
        webbrowser.open(auth_url)
        
        # Wait for user to complete authentication
        input("Press Enter after you've completed the authentication in your browser...")
        
        # Get access token
        print("🔄 Getting access token...")
        token_info = sp_oauth.get_access_token()
        
        if token_info:
            print("✅ Authentication successful!")
            print("🎵 You can now run SpotiPi with: python main.py")
            print()
            print("Token will be cached for future use.")
        else:
            print("❌ Authentication failed!")
            print("Please try again.")
            
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        print()
        print("Troubleshooting:")
        print("- Make sure your Spotify credentials are correct")
        print("- Check that your redirect URI matches exactly")
        print("- Ensure you have a Spotify Premium account")
        print("- Try running this script again")

if __name__ == "__main__":
    main() 