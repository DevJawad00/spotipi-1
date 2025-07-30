# SpotiPi - Spotify Album Art Display

A Raspberry Pi project that displays the currently playing Spotify album cover art on a 64x64 RGB LED matrix.

## Features

- Real-time Spotify track monitoring
- Album cover art display on 64x64 RGB matrix
- Automatic image scaling and optimization
- Smooth transitions between tracks
- Background service for continuous operation

## Hardware Requirements

- Raspberry Pi (3B+ or 4 recommended)
- 64x64 RGB LED Matrix
- RGB Matrix HAT or compatible controller
- Power supply for the matrix

## Software Requirements

- Python 3.7+
- Spotify Developer Account
- Required Python packages (see requirements.txt)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Get your Client ID and Client Secret
4. Add your redirect URI (e.g., `http://localhost:8888/callback`)

### 3. Configuration

1. Copy `config.example.py` to `config.py`
2. Fill in your Spotify credentials:
   ```python
   SPOTIFY_CLIENT_ID = "your_client_id"
   SPOTIFY_CLIENT_SECRET = "your_client_secret"
   SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
   ```

### 4. Authentication

Run the authentication script:
```bash
python auth_spotify.py
```

Follow the prompts to authenticate with Spotify.

### 5. Run the Application

```bash
python main.py
```

## Project Structure

```
spotipi/
├── main.py              # Main application entry point
├── spotify_client.py    # Spotify API client
├── matrix_display.py    # RGB matrix display controller
├── image_processor.py   # Image processing utilities
├── config.py           # Configuration file
├── auth_spotify.py     # Spotify authentication helper
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Usage

The application will:
1. Monitor your currently playing Spotify track
2. Download the album cover art
3. Scale and optimize the image for the 64x64 matrix
4. Display the image with smooth transitions

## Troubleshooting

- Ensure your Raspberry Pi has sufficient power for the RGB matrix
- Check that all GPIO connections are secure
- Verify Spotify credentials are correct
- Make sure you have an active Spotify Premium account

## License

MIT License - see LICENSE file for details 