"""Command-line interface for the characterize package."""

import argparse
import logging
from pathlib import Path
from typing import List, Optional, Tuple, Union
import sys
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
import os
from tqdm import tqdm

from .core import process_image, create_char_image_dict
from .utils import divide_image, unite_image, save_image, save_text, optimize_files
from .ranking import create_ranking

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert images to character art",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-i", "--input",
        nargs="+",
        help="Input image file paths",
        required=True
    )
    
    parser.add_argument(
        "-cr", "--char-res",
        type=int,
        help="Character resolution (1-4000)",
        default=1000
    )
    
    parser.add_argument(
        "-cl", "--complexity",
        type=int,
        help="Complexity level (1-40)",
        default=12
    )
    
    parser.add_argument(
        "-l", "--language",
        choices=[
            "ascii", "arabic", "braille", "emoji", "chinese",
            "simple", "numbers+", "roman", "numbers", "latin",
            "hiragana", "katakana", "kanji", "cyrillic", "hangul"
        ],
        default="ascii",
        help="Character set to use"
    )
    
    parser.add_argument(
        "-d", "--divide",
        action="store_true",
        help="Divide large images"
    )
    
    parser.add_argument(
        "-c", "--color",
        action="store_true",
        help="Preserve color information"
    )
    
    parser.add_argument(
        "-f", "--format",
        nargs="+",
        choices=["png", "jpg", "txt"],
        default=["png"],
        help="Output formats"
    )
    
    parser.add_argument(
        "-ec", "--empty-char",
        action="store_true",
        help="Include empty character"
    )
    
    parser.add_argument(
        "-o", "--optimize",
        action="store_true",
        help="Optimize output files"
    )
    
    parser.add_argument(
        "-tk", "--tkinter",
        action="store_true",
        help="Use tkinter GUI for file selection"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.char_res < 1 or args.char_res > 4000:
        parser.error("Character resolution must be between 1 and 4000")
        
    if args.complexity < 1 or args.complexity > 40:
        parser.error("Complexity level must be between 1 and 40")
        
    return args

def get_input_files(use_tkinter: bool = False) -> List[Path]:
    """Get input file paths."""
    if use_tkinter:
        root = tk.Tk()
        root.withdraw()
        files = filedialog.askopenfilenames(
            title="Select input images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        return [Path(f) for f in files]
    else:
        return []

def process_single_image(
    image_path: Union[str, Path],
    char_list: List[str],
    char_images: dict,
    detail_level: int,
    divide_flag: bool,
    output_format: List[str],
    color: bool,
    output_dir: Union[str, Path]
) -> List[Path]:
    """Process a single image."""
    try:
        image_path = Path(image_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load and process image
        with Image.open(image_path) as img:
            if divide_flag:
                sub_images = divide_image(img)
            else:
                sub_images = [img]
                
        # Process each sub-image
        output_files = []
        for i, sub_img in enumerate(sub_images):
            # Generate character art
            char_images_list, char_text_list = process_image(
                sub_img,
                char_list,
                char_images,
                detail_level,
                color=color
            )
            
            # Save outputs
            base_name = f"{image_path.stem}_{i}" if len(sub_images) > 1 else image_path.stem
            output_path = output_dir / base_name
            
            if any(fmt in ["png", "jpg"] for fmt in output_format):
                # Combine character images
                final_image = unite_image(
                    char_images_list,
                    len(char_images_list),
                    len(char_images_list[0]),
                    detail_level
                )
                save_image(final_image, output_format, color, output_path)
                output_files.extend([
                    output_path.with_suffix(f".{fmt}")
                    for fmt in output_format if fmt in ["png", "jpg"]
                ])
                
            if "txt" in output_format:
                save_text(char_text_list, output_path)
                output_files.append(output_path.with_suffix(".txt"))
                
        return output_files
        
    except Exception as e:
        logger.error(f"Error processing {image_path}: {str(e)}")
        raise

def main() -> None:
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_args()
        
        # Set logging level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            
        # Get input files
        input_files = args.input
        if args.tkinter:
            input_files.extend(get_input_files(True))
            
        if not input_files:
            logger.error("No input files specified")
            sys.exit(1)
            
        # Create output directory
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Create character ranking
        char_list, _ = zip(*create_ranking(
            args.char_res,
            "arial.ttf",  # TODO: Make font configurable
            args.complexity,
            include_empty=args.empty_char
        ))
        
        # Create character images
        char_images = create_char_image_dict(
            char_list,
            args.char_res,
            "arial.ttf",
            args.color
        )
        
        # Process images in parallel
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = []
            for path in input_files:
                future = executor.submit(
                    process_single_image,
                    path,
                    char_list,
                    char_images,
                    args.char_res,
                    args.divide,
                    args.format,
                    args.color,
                    output_dir
                )
                futures.append(future)
                
            # Wait for all images to be processed
            output_files = []
            for future in tqdm(
                futures,
                desc="Processing images",
                unit="image"
            ):
                output_files.extend(future.result())
                
        # Optimize output files if requested
        if args.optimize and output_files:
            optimize_files(output_files)
            
        logger.info("Processing complete!")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
