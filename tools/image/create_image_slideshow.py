"""
Image slideshow creation with comprehensive options
"""

from typing import List, Dict, Any, Optional
from .create_slideshow_from_images import create_slideshow_from_images


def create_image_slideshow(image_paths: List[str],
                          output_path: str,
                          duration_per_image: float = 3.0,
                          fps: int = 24,
                          resolution_width: int = 1920,
                          resolution_height: int = 1080,
                          transition_type: str = "fade",
                          transition_duration: float = 0.5,
                          background_color_r: int = 0,
                          background_color_g: int = 0,
                          background_color_b: int = 0,
                          fit_mode: str = "contain",
                          audio_path: Optional[str] = None,
                          text_overlays: Optional[List[Dict[str, Any]]] = None,
                          effects: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Main function to convert images to video slideshow.
    
    Args:
        image_paths: List of paths to image files
        output_path: Path where the video will be saved
        duration_per_image: Duration each image is displayed (seconds)
        fps: Frames per second for output video
        resolution_width: Output video width in pixels
        resolution_height: Output video height in pixels
        transition_type: Type of transition ("fade", "slide_left", "slide_right", "slide_up", "slide_down", "zoom", "crossfade", "none")
        transition_duration: Duration of transitions (seconds)
        background_color_r: Background red color component (0-255)
        background_color_g: Background green color component (0-255)
        background_color_b: Background blue color component (0-255)
        fit_mode: How to fit images ("contain", "cover", "stretch", "crop")
        audio_path: Optional path to audio file to add as background
        text_overlays: List of text overlay configurations with format:
            [
                {
                    "text": "Caption text",
                    "fontsize": 50,
                    "color": "white",
                    "font": "Arial",
                    "position": "center",  # or ('center', 'bottom'), (50, 100), etc.
                    "start_time": 0,
                    "duration": 3.0,
                    "image_indices": [0, 1]  # Optional: which images to show text on
                }
            ]
        effects: List of effects to apply with format:
            [
                {
                    "type": "fade_in",
                    "duration": 1.0
                },
                {
                    "type": "zoom",
                    "factor": 1.2
                },
                {
                    "type": "pan",
                    "direction": "right",
                    "distance": 100
                }
            ]
    
    Returns:
        Dict with status, message, and output info
    
    Example usage:
        result = create_image_slideshow(
            image_paths=["/path/to/image1.jpg", "/path/to/image2.png"],
            output_path="/path/to/output.mp4",
            duration_per_image=4.0,
            transition_type="fade",
            text_overlays=[
                {
                    "text": "Beautiful Sunset",
                    "position": "bottom",
                    "fontsize": 60,
                    "color": "yellow"
                }
            ],
            effects=[
                {"type": "fade_in", "duration": 1.0},
                {"type": "zoom", "factor": 1.1}
            ]
        )
    """
    return create_slideshow_from_images(
        image_paths=image_paths,
        output_path=output_path,
        duration_per_image=duration_per_image,
        fps=fps,
        resolution=(resolution_width, resolution_height),
        transition_type=transition_type,
        transition_duration=transition_duration,
        background_color=(background_color_r, background_color_g, background_color_b),
        fit_mode=fit_mode,
        audio_path=audio_path,
        text_overlays=text_overlays,
        effects=effects
    )
