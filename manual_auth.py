#!/usr/bin/env python3
"""
Manual Spotify Authentication

This script will help you authenticate with Spotify manually.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
import json
import os

def main():
    print("🎵 Manual Spotify Authentication")
    print("=" * 35)
    print()
    
    # Check credentials
    if (config.SPOTIFY_CLIENT_ID == "your_client_id_here" or 
        config.SPOTIFY_CLIENT_SECRET == "your_client_secret_here"):
        print("❌ Spotify credentials not configured!")
        print("Please edit config.py with your credentials first.")
        return
    
    print("✅ Spotify credentials found")
    print()
    
    # Create OAuth manager
    scope = "user-read-currently-playing user-read-playback-state"
    
    sp_oauth = SpotifyOAuth(
        client_id=config.SPOTIFY_CLIENT_ID,
        client_secret=config.SPOTIFY_CLIENT_SECRET,
        redirect_uri=config.SPOTIFY_REDIRECT_URI,
        scope=scope,
        cache_path=".spotify_cache"
    )
    
    # Get authorization URL
    auth_url = sp_oauth.get_authorize_url()
    
    print("🔐 Follow these steps to authenticate:")
    print()
    print("1. Open this URL in your browser:")
    print(f"   {auth_url}")
    print()
    print("2. Log in to Spotify and authorize the application")
    print()
    print("3. You'll be redirected to a URL that looks like:")
    print("   http://localhost:8888/callback?code=AQDUQPWwkCaX5ECnMQg-NPCMKAHh80NFJB9Amuf6kwhBLg0Q_66yxJI26K0pml6vmgKk4XCMw...")
    print()
    print("4. Copy the ENTIRE URL from your browser's address bar")
    print()
    
    # Get the callback URL from user
    callback_url = input("Paste the callback URL here: ").strip()
    
    if not callback_url:
        print("❌ No URL provided")
        return
    
    # Extract the authorization code
    try:
        # Parse the URL to get the code
        if "code=" in callback_url:
            code = callback_url.split("code=")[1].split("&")[0]
            print(f"✅ Authorization code extracted: {code[:20]}...")
        else:
            print("❌ No authorization code found in URL")
            return
        
        # Exchange code for token
        print("🔄 Exchanging code for token...")
        token_info = sp_oauth.get_access_token(code)
        
        if token_info:
            print("✅ Authentication successful!")
            print("🎵 You can now run SpotiPi with: python main.py")
            print()
            print("Token will be cached for future use.")
            
            # Test the connection
            print("🧪 Testing Spotify connection...")
            sp = spotipy.Spotify(auth=token_info['access_token'])
            
            try:
                current = sp.current_user_playing_track()
                if current:
                    track = current['item']
                    print(f"✅ Connected! Currently playing: {track['name']} by {track['artists'][0]['name']}")
                else:
                    print("✅ Connected! No track currently playing")
            except Exception as e:
                print(f"⚠️  Connected but couldn't get current track: {e}")
            
        else:
            print("❌ Failed to get access token!")
            print("Please try again.")
            
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        print("Please check the URL and try again.")

if __name__ == "__main__":
    main() 