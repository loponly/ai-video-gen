#!/usr/bin/env python3
"""
Test script for image-to-video conversion tool
"""

import os
import sys
from pathlib import Path

# Add the tools directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from tools.image import create_image_slideshow, create_simple_slideshow


def test_basic_slideshow():
    """Test basic slideshow creation with images from movie-reels/images"""
    
    # Get image paths from movie-reels/images directory
    images_dir = Path(__file__).parent / "movie-reels" / "images"
    if not images_dir.exists():
        print(f"Images directory not found: {images_dir}")
        return
    
    # Get the first few image files
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png']:
        image_files.extend(list(images_dir.glob(f"*{ext}")))
    
    if len(image_files) < 2:
        print("Need at least 2 images to create a slideshow")
        return
    
    # Use first 3 images for testing
    image_paths = [str(f) for f in sorted(image_files)[:3]]
    print(f"Using images: {[f.name for f in sorted(image_files)[:3]]}")
    
    # Create output directory
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    output_path = str(output_dir / "test_slideshow.mp4")
    
    print("Creating basic slideshow...")
    result = create_simple_slideshow(
        image_paths=image_paths,
        output_path=output_path,
        duration_per_image=2.0
    )
    
    print(f"Result: {result}")


def test_advanced_slideshow():
    """Test advanced slideshow with transitions, text, and effects"""
    
    # Get image paths from movie-reels/images directory
    images_dir = Path(__file__).parent / "movie-reels" / "images"
    if not images_dir.exists():
        print(f"Images directory not found: {images_dir}")
        return
    
    # Get the first few image files
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png']:
        image_files.extend(list(images_dir.glob(f"*{ext}")))
    
    if len(image_files) < 2:
        print("Need at least 2 images to create a slideshow")
        return
    
    # Use first 3 images for testing
    image_paths = [str(f) for f in sorted(image_files)[:3]]
    print(f"Using images: {[f.name for f in sorted(image_files)[:3]]}")
    
    # Create output directory
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    output_path = str(output_dir / "test_advanced_slideshow.mp4")
    
    # Define text overlays
    text_overlays = [
        {
            "text": "Image 1: Beautiful Scene",
            "fontsize": 60,
            "color": "white",
            "position": ("center", "bottom"),
            "duration": 3.0,
            "image_indices": [0]
        },
        {
            "text": "Image 2: Another View",
            "fontsize": 60,
            "color": "yellow",
            "position": ("center", "bottom"),
            "duration": 3.0,
            "image_indices": [1]
        },
        {
            "text": "Image 3: Final Shot",
            "fontsize": 60,
            "color": "cyan",
            "position": ("center", "bottom"),
            "duration": 3.0,
            "image_indices": [2]
        }
    ]
    
    # Define effects
    effects = [
        {"type": "fade_in", "duration": 0.5},
        {"type": "fade_out", "duration": 0.5}
    ]
    
    print("Creating advanced slideshow with transitions, text, and effects...")
    result = create_image_slideshow(
        image_paths=image_paths,
        output_path=output_path,
        duration_per_image=3.0,
        fps=30,
        resolution=(1920, 1080),
        transition_type="fade",
        transition_duration=0.7,
        background_color=(0, 0, 0),
        fit_mode="contain",
        text_overlays=text_overlays,
        effects=effects
    )
    
    print(f"Result: {result}")


if __name__ == "__main__":
    print("Testing image-to-video conversion tools...")
    print("=" * 50)
    
    print("\n1. Testing basic slideshow...")
    test_basic_slideshow()
    
    print("\n2. Testing advanced slideshow...")
    test_advanced_slideshow()
    
    print("\nTests completed!")
