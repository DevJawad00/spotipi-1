#!/usr/bin/env python3
"""
Fixed Spotify Authentication Helper for SpotiPi

This script properly handles Spotify OAuth with a local callback server.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import config
import os
import time
from urllib.parse import urlparse, parse_qs
import http.server
import socketserver
import threading
import urllib.parse

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle the OAuth callback."""
        # Parse the callback URL
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/callback':
            # Extract the authorization code
            query_params = parse_qs(parsed_url.query)
            code = query_params.get('code', [None])[0]
            
            if code:
                # Store the code for the main script to use
                with open('.auth_code', 'w') as f:
                    f.write(code)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                response = """
                <html>
                <head><title>Authentication Successful</title></head>
                <body>
                <h1>✅ Authentication Successful!</h1>
                <p>You can now close this window and return to the terminal.</p>
                <script>setTimeout(function(){ window.close(); }, 2000);</script>
                </body>
                </html>
                """
                self.wfile.write(response.encode())
                
                # Signal that authentication is complete
                self.server.auth_complete = True
            else:
                # Send error response
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                response = """
                <html>
                <head><title>Authentication Failed</title></head>
                <body>
                <h1>❌ Authentication Failed</h1>
                <p>No authorization code received.</p>
                </body>
                </html>
                """
                self.wfile.write(response.encode())
        else:
            # Send 404 for other paths
            self.send_response(404)
            self.end_headers()

def start_callback_server(port=8888):
    """Start the callback server."""
    with socketserver.TCPServer(("", port), CallbackHandler) as httpd:
        httpd.auth_complete = False
        print(f"🌐 Callback server started on port {port}")
        
        # Start server in a separate thread
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        return httpd

def main():
    print("=== SpotiPi Spotify Authentication (Fixed) ===")
    print()
    
    # Check if credentials are configured
    if (config.SPOTIFY_CLIENT_ID == "your_client_id_here" or 
        config.SPOTIFY_CLIENT_SECRET == "your_client_secret_here"):
        print("❌ Spotify credentials not configured!")
        return
    
    print("✅ Spotify credentials found in config.py")
    print()
    
    # Set up OAuth scope
    scope = "user-read-currently-playing user-read-playback-state"
    
    try:
        print("🔐 Starting Spotify authentication...")
        print("This will open your browser for authentication.")
        print()
        
        # Start callback server
        server = start_callback_server()
        
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
        
        # Wait for authentication to complete
        print("⏳ Waiting for authentication...")
        while not server.auth_complete:
            time.sleep(0.1)
        
        # Get the authorization code
        if os.path.exists('.auth_code'):
            with open('.auth_code', 'r') as f:
                auth_code = f.read().strip()
            
            # Exchange code for token
            print("🔄 Exchanging code for token...")
            token_info = sp_oauth.get_access_token(auth_code)
            
            if token_info:
                print("✅ Authentication successful!")
                print("🎵 You can now run SpotiPi with: python main.py")
                print()
                print("Token will be cached for future use.")
                
                # Clean up
                if os.path.exists('.auth_code'):
                    os.remove('.auth_code')
            else:
                print("❌ Failed to get access token!")
        else:
            print("❌ No authorization code received!")
            
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        print()
        print("Troubleshooting:")
        print("- Make sure your Spotify credentials are correct")
        print("- Check that your redirect URI matches exactly")
        print("- Ensure you have a Spotify Premium account")
        print("- Try running this script again")
    finally:
        # Clean up
        if os.path.exists('.auth_code'):
            os.remove('.auth_code')

if __name__ == "__main__":
    main() 