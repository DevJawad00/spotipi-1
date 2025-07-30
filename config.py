# SpotiPi Configuration

# Spotify API Configuration
SPOTIFY_CLIENT_ID = "2d7b7dfff6d748b9ac3e129565cb6adf"
SPOTIFY_CLIENT_SECRET = "03a69fc2bdbc4c5aa7e5f84dde28e76d"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

# Matrix Display Configuration
MATRIX_WIDTH = 64
MATRIX_HEIGHT = 64
MATRIX_BRIGHTNESS = 50  # 0-100
MATRIX_GPIO_MAPPING = "regular"  # or "adafruit-hat" depending on your setup

# Application Settings
UPDATE_INTERVAL = 5  # seconds between Spotify API calls
IMAGE_CACHE_DIR = "cache"
TRANSITION_DURATION = 1.0  # seconds for fade transitions

# Display Settings
DITHERING = True  # Enable dithering for better color reproduction
GAMMA_CORRECTION = True  # Enable gamma correction 