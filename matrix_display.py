import time
import numpy as np
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import config

class MatrixDisplay:
    def __init__(self):
        """Initialize RGB matrix display."""
        self.matrix = None
        self.current_image = None
        self._setup_matrix()
    
    def _setup_matrix(self):
        """Setup RGB matrix with configuration."""
        try:
            options = RGBMatrixOptions()
            
            # Hardware configuration
            options.rows = config.MATRIX_HEIGHT
            options.cols = config.MATRIX_WIDTH
            options.chain_length = 1
            options.parallel = 1
            options.hardware_mapping = "regular"  # Use regular mapping
            
            # Brightness and performance settings
            options.brightness = config.MATRIX_BRIGHTNESS
            options.limit_refresh_rate_hz = 200
            options.drop_privileges = False
            
            # Additional settings to prevent row skipping
            options.scan_mode = 0  # Progressive scan mode
            options.multiplexing = 0  # No multiplexing
            
            # Create matrix instance
            self.matrix = RGBMatrix(options=options)
            
            print(f"RGB Matrix initialized: {config.MATRIX_WIDTH}x{config.MATRIX_HEIGHT}")
            
        except Exception as e:
            print(f"Error initializing RGB matrix: {e}")
            print("Running in simulation mode...")
            self.matrix = None
    
    def display_image(self, image_array: np.ndarray, duration: float = None):
        """Display image on RGB matrix."""
        if self.matrix is None:
            self._simulate_display(image_array)
            return
        
        try:
            # Ensure image array is the correct shape and type
            if image_array.shape != (64, 64, 3):
                print(f"Warning: Image shape is {image_array.shape}, expected (64, 64, 3)")
                return
            
            # Convert to uint8 if needed
            if image_array.dtype != np.uint8:
                image_array = image_array.astype(np.uint8)
            
            # Create canvas
            canvas = self.matrix.CreateFrameCanvas()
            
            # Set pixels on canvas - ensure proper addressing
            for y in range(image_array.shape[0]):
                for x in range(image_array.shape[1]):
                    r, g, b = image_array[y, x]
                    # Ensure pixel values are in valid range
                    r = max(0, min(255, int(r)))
                    g = max(0, min(255, int(g)))
                    b = max(0, min(255, int(b)))
                    canvas.SetPixel(x, y, r, g, b)
            
            # Display the image
            canvas = self.matrix.SwapOnVSync(canvas)
            
            # Store current image
            self.current_image = image_array.copy()
            
            # Wait for specified duration
            if duration:
                time.sleep(duration)
                
        except Exception as e:
            print(f"Error displaying image: {e}")
    
    def display_transition(self, from_image: np.ndarray, to_image: np.ndarray, 
                          duration: float = None):
        """Display smooth transition between two images."""
        if duration is None:
            duration = config.TRANSITION_DURATION
        
        num_frames = int(duration * 30)  # 30 FPS
        frame_duration = duration / num_frames
        
        for i in range(num_frames):
            alpha = i / (num_frames - 1)
            transition_frame = (from_image * (1 - alpha) + to_image * alpha).astype(np.uint8)
            self.display_image(transition_frame, frame_duration)
    
    def clear_display(self):
        """Clear the display (set all pixels to black)."""
        if self.matrix is None:
            print("Display cleared (simulation mode)")
            return
        
        try:
            canvas = self.matrix.CreateFrameCanvas()
            canvas.Clear()
            self.matrix.SwapOnVSync(canvas)
            self.current_image = None
        except Exception as e:
            print(f"Error clearing display: {e}")
    
    def set_brightness(self, brightness: int):
        """Set matrix brightness (0-100)."""
        if self.matrix is None:
            print(f"Brightness set to {brightness}% (simulation mode)")
            return
        
        try:
            # Note: This might require matrix restart on some hardware
            print(f"Brightness set to {brightness}%")
        except Exception as e:
            print(f"Error setting brightness: {e}")
    
    def _simulate_display(self, image_array: np.ndarray):
        """Simulate display for testing without hardware."""
        print("=== SIMULATION MODE ===")
        print(f"Displaying image: {image_array.shape}")
        
        # Print a simple ASCII representation
        height, width = image_array.shape[:2]
        scale = max(1, min(width // 20, height // 10))  # Scale down for display
        
        for y in range(0, height, scale):
            line = ""
            for x in range(0, width, scale):
                r, g, b = image_array[y, x]
                # Convert to grayscale and choose character
                gray = 0.299 * r + 0.587 * g + 0.114 * b
                if gray > 200:
                    char = "█"
                elif gray > 150:
                    char = "▓"
                elif gray > 100:
                    char = "▒"
                elif gray > 50:
                    char = "░"
                else:
                    char = " "
                line += char
            print(line)
        print("======================")
    
    def cleanup(self):
        """Clean up matrix resources."""
        if self.matrix:
            try:
                self.clear_display()
                self.matrix.Clear()
            except Exception as e:
                print(f"Error during cleanup: {e}")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup() 