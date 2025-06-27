"""
Simple slideshow creation with basic settings
"""

from typing import List, Dict, Any
from .create_slideshow_from_images import create_slideshow_from_images


def create_simple_slideshow(image_paths: List[str], output_path: str, duration_per_image: float = 3.0) -> Dict[str, Any]:
    """
    Simplified function to create a basic slideshow with default settings.
    
    Args:
        image_paths: List of paths to image files
        output_path: Path where the video will be saved
        duration_per_image: Duration each image is displayed (seconds)
    
    Returns:
        Dict with status, message, and output info
    """
    return create_slideshow_from_images(
        image_paths=image_paths,
        output_path=output_path,
        duration_per_image=duration_per_image,
        transition_type="fade",
        fit_mode="contain"
    )
