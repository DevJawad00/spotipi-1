from PIL import Image, ImageEnhance
import numpy as np
import config

class ImageProcessor:
    def __init__(self):
        """Initialize image processor with matrix dimensions."""
        self.width = config.MATRIX_WIDTH
        self.height = config.MATRIX_HEIGHT
    
    def load_and_process_image(self, image_path: str) -> np.ndarray:
        """Load and process image for RGB matrix display."""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Process the image
            processed_image = self._process_image(image)
            
            return processed_image
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return self._create_placeholder_image()
    
    def _process_image(self, image: Image.Image) -> np.ndarray:
        """Process image for optimal display on RGB matrix."""
        # Resize image to fit matrix dimensions
        resized_image = self._resize_image(image)
        
        # Apply enhancements
        enhanced_image = self._enhance_image(resized_image)
        
        # Convert to numpy array
        image_array = np.array(enhanced_image)
        
        # Apply dithering if enabled
        if config.DITHERING:
            image_array = self._apply_dithering(image_array)
        
        # Apply gamma correction if enabled
        if config.GAMMA_CORRECTION:
            image_array = self._apply_gamma_correction(image_array)
        
        return image_array
    
    def _resize_image(self, image: Image.Image) -> Image.Image:
        """Resize image to matrix dimensions while maintaining aspect ratio."""
        # Calculate aspect ratios
        img_aspect = image.width / image.height
        matrix_aspect = self.width / self.height
        
        if img_aspect > matrix_aspect:
            # Image is wider than matrix
            new_width = self.width
            new_height = int(self.width / img_aspect)
        else:
            # Image is taller than matrix
            new_height = self.height
            new_width = int(self.height * img_aspect)
        
        # Resize image
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create new image with matrix dimensions and black background
        final_image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        
        # Calculate position to center the image
        x_offset = (self.width - new_width) // 2
        y_offset = (self.height - new_height) // 2
        
        # Paste the resized image onto the background
        final_image.paste(resized, (x_offset, y_offset))
        
        return final_image
    
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """Apply image enhancements for better display."""
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Enhance brightness
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.1)
        
        # Enhance saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)
        
        return image
    
    def _apply_dithering(self, image_array: np.ndarray) -> np.ndarray:
        """Apply Floyd-Steinberg dithering for better color reproduction."""
        # Convert to float for processing
        img_float = image_array.astype(np.float32) / 255.0
        
        # Apply dithering to each channel
        dithered = np.zeros_like(img_float)
        
        for channel in range(3):
            dithered[:, :, channel] = self._floyd_steinberg_dither(img_float[:, :, channel])
        
        # Convert back to uint8
        return (dithered * 255).astype(np.uint8)
    
    def _floyd_steinberg_dither(self, channel: np.ndarray) -> np.ndarray:
        """Apply Floyd-Steinberg dithering to a single channel."""
        height, width = channel.shape
        result = channel.copy()
        
        for y in range(height):
            for x in range(width):
                old_pixel = result[y, x]
                new_pixel = 1.0 if old_pixel > 0.5 else 0.0
                result[y, x] = new_pixel
                
                error = old_pixel - new_pixel
                
                # Distribute error to neighboring pixels
                if x + 1 < width:
                    result[y, x + 1] += error * 7 / 16
                if x - 1 >= 0 and y + 1 < height:
                    result[y + 1, x - 1] += error * 3 / 16
                if y + 1 < height:
                    result[y + 1, x] += error * 5 / 16
                if x + 1 < width and y + 1 < height:
                    result[y + 1, x + 1] += error * 1 / 16
        
        return result
    
    def _apply_gamma_correction(self, image_array: np.ndarray) -> np.ndarray:
        """Apply gamma correction for better color accuracy."""
        gamma = 2.2
        corrected = np.power(image_array.astype(np.float32) / 255.0, 1/gamma)
        return (corrected * 255).astype(np.uint8)
    
    def _create_placeholder_image(self) -> np.ndarray:
        """Create a placeholder image when processing fails."""
        # Create a simple gradient pattern
        placeholder = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        for y in range(self.height):
            for x in range(self.width):
                r = int((x / self.width) * 255)
                g = int((y / self.height) * 255)
                b = 128
                placeholder[y, x] = [r, g, b]
        
        return placeholder
    
    def create_transition_frames(self, from_image: np.ndarray, to_image: np.ndarray, 
                                num_frames: int = 10) -> list:
        """Create transition frames between two images."""
        frames = []
        
        for i in range(num_frames):
            alpha = i / (num_frames - 1)
            transition_frame = (from_image * (1 - alpha) + to_image * alpha).astype(np.uint8)
            frames.append(transition_frame)
        
        return frames 