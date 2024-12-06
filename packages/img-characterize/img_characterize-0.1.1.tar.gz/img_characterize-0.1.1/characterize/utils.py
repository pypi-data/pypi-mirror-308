"""Utility functions for image processing and file operations."""

from typing import List, Union, Optional
from pathlib import Path
import logging
from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
from tqdm import tqdm

logger = logging.getLogger(__name__)

def divide_image(
    image: Image.Image,
    min_size: int = 1000000
) -> List[Image.Image]:
    """
    Divide a large image into smaller parts.
    
    Args:
        image: Input PIL Image
        min_size: Minimum size threshold for division
        
    Returns:
        List of smaller PIL Images
    """
    try:
        image_list = [image]
        current_size = image.size[0] * image.size[1]
        
        while current_size >= min_size:
            temp_list = []
            for img in image_list:
                # Divide image into quarters
                w, h = img.size
                temp_list.extend([
                    img.crop((0, 0, w//2, h//2)),
                    img.crop((w//2, 0, w, h//2)),
                    img.crop((0, h//2, w//2, h)),
                    img.crop((w//2, h//2, w, h))
                ])
            image_list = temp_list
            current_size = image_list[0].size[0] * image_list[0].size[1]
            
        return image_list
        
    except Exception as e:
        logger.error(f"Error dividing image: {str(e)}")
        raise

def unite_image(
    char_images: List[List[Image.Image]],
    width: int,
    height: int,
    detail_level: int
) -> Image.Image:
    """
    Combine character images into a single image.
    
    Args:
        char_images: 2D list of character images
        width: Original image width
        height: Original image height
        detail_level: Size of each character image
        
    Returns:
        Combined PIL Image
    """
    try:
        # Create new transparent image
        new_image = Image.new(
            "RGBA",
            (detail_level * width, detail_level * height),
            (0, 0, 0, 0)
        )
        
        # Paste each character image
        for i in range(width):
            for j in range(height):
                char_img = char_images[i][j].convert("RGBA")
                new_image.paste(
                    char_img,
                    (i * detail_level, j * detail_level),
                    char_img
                )
                
        return new_image
        
    except Exception as e:
        logger.error(f"Error uniting images: {str(e)}")
        raise

def save_image(
    image: Image.Image,
    output_format: str,
    use_color: bool,
    filename: Union[str, Path],
    max_attempts: int = 10
) -> None:
    """
    Save image with retry mechanism and format fallback.
    
    Args:
        image: PIL Image to save
        output_format: Desired output format (png or jpg)
        use_color: Whether to preserve color
        filename: Output filename
        max_attempts: Maximum number of save attempts
    """
    save_options = {
        "png": {"format": "PNG", "compress_level": 9},
        "jpg": {"format": "JPEG", "quality": 95}
    }
    
    try:
        filename = Path(filename)
        
        for fmt in ["png", "jpg"]:
            if fmt in output_format:
                for attempt in range(max_attempts):
                    try:
                        # Ensure correct color mode
                        if image.mode != "RGB":
                            image = image.convert("RGB")
                            
                        # Apply color optimization
                        if use_color and fmt == "png":
                            image = image.quantize(colors=256)
                            
                        # Save with current format
                        output_path = filename.with_suffix(f".{fmt}")
                        image.save(output_path, **save_options[fmt])
                        
                        # Verify saved image
                        with Image.open(output_path) as img:
                            img.verify()
                            
                        logger.info(f"Successfully saved image as {output_path}")
                        break
                        
                    except Exception as e:
                        if attempt == max_attempts - 1:
                            # Try backup format
                            backup_fmt = "jpg" if fmt == "png" else "png"
                            backup_path = filename.with_suffix(f"_backup.{backup_fmt}")
                            image.save(backup_path, **save_options[backup_fmt])
                            logger.warning(
                                f"Failed to save as {fmt}, saved backup as {backup_path}"
                            )
                        else:
                            logger.warning(
                                f"Save attempt {attempt + 1} failed: {str(e)}"
                            )
                            
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        raise

def save_text(
    characters: List[List[str]],
    filename: Union[str, Path]
) -> None:
    """
    Save character art as text file.
    
    Args:
        characters: 2D list of characters
        filename: Output filename
    """
    try:
        filename = Path(filename)
        with open(filename.with_suffix(".txt"), "w", encoding="utf-8") as f:
            for line in characters:
                f.write(" ".join(line) + "\n")
        logger.info(f"Successfully saved text file as {filename}")
        
    except Exception as e:
        logger.error(f"Error saving text file: {str(e)}")
        raise

def optimize_file(filepath: Union[str, Path]) -> None:
    """
    Optimize file size using FileOptimizer.
    
    Args:
        filepath: Path to file to optimize
    """
    try:
        optimizer_path = Path("C:/Program Files/FileOptimizer/FileOptimizer64.exe")
        if not optimizer_path.exists():
            logger.warning("FileOptimizer not found, skipping optimization")
            return
            
        subprocess.run(
            [str(optimizer_path), str(filepath)],
            check=True,
            capture_output=True
        )
        logger.info(f"Successfully optimized {filepath}")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error optimizing file: {str(e)}")
        raise

def optimize_files(
    files: List[Union[str, Path]],
    num_threads: Optional[int] = None
) -> None:
    """
    Optimize multiple files in parallel.
    
    Args:
        files: List of file paths to optimize
        num_threads: Number of threads to use
    """
    if not num_threads:
        num_threads = os.cpu_count() or 1
        
    try:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            list(tqdm(
                executor.map(optimize_file, files),
                total=len(files),
                desc="Optimizing files"
            ))
            
    except Exception as e:
        logger.error(f"Error in parallel file optimization: {str(e)}")
        raise
