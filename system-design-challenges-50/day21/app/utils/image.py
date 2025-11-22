from typing import List, Optional
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)


def resize_image(image_data: bytes, max_width: int = 1024, max_height: int = 1024) -> bytes:
    """Resize an image to fit within specified dimensions"""
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_data))
        
        # Calculate new dimensions while maintaining aspect ratio
        width, height = image.size
        if width <= max_width and height <= max_height:
            # Image is already within limits
            output = io.BytesIO()
            image.save(output, format=image.format)
            return output.getvalue()
        
        # Calculate scaling factor
        scale = min(max_width / width, max_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resize image
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save to bytes
        output = io.BytesIO()
        resized_image.save(output, format=image.format)
        return output.getvalue()
    except Exception as e:
        logger.error(f"Error resizing image: {e}")
        raise


def generate_thumbnail(image_data: bytes, size: tuple = (128, 128)) -> bytes:
    """Generate a thumbnail of specified size"""
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_data))
        
        # Create thumbnail
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save to bytes
        output = io.BytesIO()
        thumbnail.save(output, format=image.format)
        return output.getvalue()
    except Exception as e:
        logger.error(f"Error generating thumbnail: {e}")
        raise


def get_image_info(image_data: bytes) -> dict:
    """Get image information (format, size, mode)"""
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_data))
        
        return {
            "format": image.format,
            "size": image.size,
            "mode": image.mode
        }
    except Exception as e:
        logger.error(f"Error getting image info: {e}")
        raise