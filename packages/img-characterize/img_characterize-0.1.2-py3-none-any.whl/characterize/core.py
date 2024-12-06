"""Core functionality for image to character art conversion."""

from typing import Dict, List, Tuple, Union, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path

from .utils import divide_image, unite_image, save_image, save_text

logger = logging.getLogger(__name__)

def process_image(
    image: Image.Image,
    char_list: List[str],
    char_images: Dict[str, Image.Image],
    detail_level: int,
    divide_image_flag: bool = False,
    output_format: str = "png",
    resize: Optional[Tuple[int, int]] = None,
    color: bool = False,
    output_folder: Union[str, Path] = "output",
    use_tkinter: bool = False,
) -> Tuple[List[List[Image.Image]], List[List[str]]]:
    """
    Process an image to convert it into character art.
    
    Args:
        image: Input PIL Image
        char_list: List of characters to use for conversion
        char_images: Dictionary mapping characters to their image representations
        detail_level: Level of detail for character conversion
        divide_image_flag: Whether to divide large images
        output_format: Output format (png, jpg, or txt)
        resize: Optional tuple of (width, height) to resize the image
        color: Whether to preserve color information
        output_folder: Folder to save output files
        use_tkinter: Whether to use tkinter for display
        
    Returns:
        Tuple of (character images list, character text list)
    """
    try:
        # Resize image if requested
        if resize:
            image = image.resize(resize, Image.Resampling.LANCZOS)
            
        # Convert image to grayscale for processing
        pixels = image.convert("L").load()
        width, height = image.size
        
        # Calculate color levels
        color_levels = _calculate_color_levels(pixels, width, height, len(char_list), color)
        
        # Create character representations
        char_images_list = []
        char_text_list = []
        
        for i in range(width):
            char_row = []
            text_row = []
            for j in range(height):
                level = color_levels[i][j]
                char = char_list[level]
                char_img = char_images[char]
                char_row.append(char_img)
                text_row.append(char)
            char_images_list.append(char_row)
            char_text_list.append(text_row)
            
        return char_images_list, char_text_list
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise

def create_char_image_dict(
    characters: List[str],
    detail: int,
    font_path: Union[str, Path],
    color: bool = False
) -> Dict[str, Image.Image]:
    """
    Create a dictionary mapping characters to their image representations.
    
    Args:
        characters: List of characters to create images for
        detail: Size of character images
        font_path: Path to font file
        color: Whether to use color
        
    Returns:
        Dictionary mapping characters to PIL Images
    """
    try:
        char_images = {}
        font = ImageFont.truetype(str(font_path), detail)
        
        for char in characters:
            char_images[char] = _create_char_image(char, detail, font, color)
            
        return char_images
        
    except Exception as e:
        logger.error(f"Error creating character images: {str(e)}")
        raise

def _calculate_color_levels(
    pixels: Image.Image,
    width: int,
    height: int,
    num_chars: int,
    use_color: bool
) -> List[List[int]]:
    """Calculate color levels for each pixel."""
    color_levels = [[pixels[i, j] / 255 for j in range(height)] for i in range(width)]
    
    if not use_color:
        # Calculate threshold for better black and white contrast
        all_levels = [level for row in color_levels for level in row]
        threshold = np.percentile(all_levels, 90)
        
        # Amplify differences
        for i, row in enumerate(color_levels):
            color_levels[i] = _amplify_differences(row, threshold)
            
    # Convert to character indices
    return [[int(level * (num_chars - 1)) for level in row] for row in color_levels]

def _create_char_image(
    char: str,
    size: int,
    font: ImageFont.FreeTypeFont,
    use_color: bool
) -> Image.Image:
    """Create an image representation of a character."""
    mode = "RGBA" if use_color else "L"
    color = (0, 0, 0, 0) if use_color else 0
    fill = (255, 255, 255, 255) if use_color else 255
    
    img = Image.new(mode, (size, size), color=color)
    draw = ImageDraw.Draw(img)
    draw.text(
        (size/2, size/2),
        char,
        font=font,
        fill=fill,
        anchor="mm"
    )
    return img

def _amplify_differences(values: List[float], threshold: float) -> List[float]:
    """Amplify differences in color values for better contrast."""
    values = np.array(values)
    deviations = np.abs(values - threshold)
    
    # Apply different amplification based on threshold
    amplification = np.where(
        values >= threshold,
        1 + deviations,  # Amplify bright areas
        1 - deviations   # Reduce dark areas
    )
    
    # Apply amplification and clip to valid range
    return np.clip(values * amplification, 0, 1)
