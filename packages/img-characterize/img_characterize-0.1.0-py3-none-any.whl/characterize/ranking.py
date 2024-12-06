"""Functions for character ranking and selection."""

from typing import List, Tuple, Optional
import logging
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

def create_ranking(
    detail: int,
    font_path: str,
    list_size: int = 12,
    allowed_chars: Optional[str] = None,
    include_empty: bool = False
) -> List[Tuple[str, float]]:
    """
    Create a ranking of characters based on their brightness levels.
    
    Args:
        detail: Size of character images
        font_path: Path to font file
        list_size: Number of characters to select
        allowed_chars: String of allowed characters
        include_empty: Whether to include empty space character
        
    Returns:
        List of tuples (character, brightness_value)
    """
    try:
        if allowed_chars is None:
            allowed_chars = (
                "0123456789"
                "abcdefghijklmnñopqrstuvwxyz"
                "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
            )
            
        if include_empty:
            allowed_chars += " "
            
        # Calculate brightness for each character
        char_values = []
        for char in allowed_chars:
            brightness = char_image_colors(char, detail, font_path)
            char_values.append((char, brightness))
            
        # Sort by brightness
        ranking = sorted(char_values, key=lambda x: x[1])
        
        # Filter to get optimal distribution
        return _filter_ranking(ranking, list_size)
        
    except Exception as e:
        logger.error(f"Error creating character ranking: {str(e)}")
        raise

def char_image_colors(
    character: str,
    detail: int,
    font_path: str
) -> float:
    """
    Calculate the brightness value for a character.
    
    Args:
        character: Character to analyze
        detail: Size of character image
        font_path: Path to font file
        
    Returns:
        Brightness value between 0 and 1
    """
    try:
        # Handle empty character
        if character.strip() == "":
            return 0.0
            
        # Create character image
        img = Image.new("L", (detail, detail), color=0)
        font = ImageFont.truetype(font_path, detail)
        draw = ImageDraw.Draw(img)
        
        # Draw character
        draw.text(
            (detail/2, detail/2),
            character,
            font=font,
            fill=255,
            anchor="mm"
        )
        
        # Calculate average brightness
        return float(np.mean(img)) / 255
        
    except Exception as e:
        logger.error(f"Error calculating character brightness: {str(e)}")
        raise

def _filter_ranking(
    rank_list: List[Tuple[str, float]],
    selected_size: int
) -> List[Tuple[str, float]]:
    """
    Filter ranking to get optimal character distribution.
    
    Args:
        rank_list: List of (character, brightness) tuples
        selected_size: Number of characters to select
        
    Returns:
        Filtered list of (character, brightness) tuples
    """
    try:
        if not rank_list:
            raise ValueError("Empty ranking list")
            
        if len(rank_list) < selected_size:
            selected_size = len(rank_list)
            
        # Handle empty character separately
        empty_char = None
        if (" ", 0.0) in rank_list:
            empty_char = (" ", 0.0)
            rank_list = [c for c in rank_list if c != (" ", 0.0)]
            selected_size -= 1
            
        # Calculate target brightness values
        min_brightness = rank_list[0][1]
        max_brightness = rank_list[-1][1]
        step = (max_brightness - min_brightness) / (selected_size - 1)
        target_values = [min_brightness + i * step for i in range(selected_size)]
        
        # Select characters closest to target values
        selected = []
        for target in target_values:
            closest = min(rank_list, key=lambda x: abs(x[1] - target))
            selected.append(closest)
            rank_list.remove(closest)
            
        # Add empty character back if needed
        if empty_char:
            selected = [empty_char] + selected
            
        # Calculate quality metrics
        brightness_range = selected[-1][1] - selected[0][1]
        step_sizes = [b2[1] - b1[1] for b1, b2 in zip(selected[:-1], selected[1:])]
        dissimilarity = np.median(step_sizes) / brightness_range if step_sizes else 0
        
        logger.info(
            f"Character ranking stats: "
            f"range={brightness_range:.3f}, "
            f"dissimilarity={dissimilarity:.3f}"
        )
        
        return sorted(selected, key=lambda x: x[1])
        
    except Exception as e:
        logger.error(f"Error filtering character ranking: {str(e)}")
        raise

def _decimal_range(
    start: float,
    stop: float,
    length: int
) -> List[float]:
    """Generate evenly spaced decimal values."""
    if length < 2:
        return [start]
    step = (stop - start) / (length - 1)
    return [start + i * step for i in range(length)]
