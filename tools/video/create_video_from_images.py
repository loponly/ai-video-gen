"""
Create video from images functionality
"""

from typing import List, Dict, Any


def create_video_from_images(image_paths: List[str], output_path: str, duration_per_image: float) -> Dict[str, Any]:
    """
    Create a video slideshow from a list of images.
    
    Args:
        image_paths: List of paths to image files
        output_path: Path where the video will be saved
        duration_per_image: Duration each image is displayed (seconds)
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Import the image editor tools function
        from tools.image import create_slideshow_from_images
        
        # Create slideshow with basic settings
        result = create_slideshow_from_images(
            image_paths=image_paths,
            output_path=output_path,
            duration_per_image=duration_per_image,
            fps=24,
            resolution_width=1920,
            resolution_height=1080,
            transition_type="fade",
            transition_duration=0.5,
            background_color_r=0,
            background_color_g=0,
            background_color_b=0,
            fit_mode="contain",
            audio_path=None,
            text_overlays=None,
            effects=None
        )
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create video from images: {str(e)}",
            "output_path": None,
            "details": {
                "error_type": type(e).__name__,
                "image_count": len(image_paths)
            }
        }
