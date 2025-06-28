"""
Main slideshow creation functionality with comprehensive features
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple, Union
from pathlib import Path
import moviepy as mp
from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip, TextClip, 
    CompositeVideoClip, concatenate_videoclips, VideoClip
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from .utils import _create_image_clip, _add_text_overlays, _apply_effects, _add_transitions


def create_slideshow_from_images(image_paths: List[str],
                                output_path: str,
                                duration_per_image: float = 3.0,
                                fps: int = 24,
                                resolution: Tuple[int, int] = (1920, 1080),
                                transition_type: str = "fade",
                                transition_duration: float = 0.5,
                                background_color: Tuple[int, int, int] = (0, 0, 0),
                                fit_mode: str = "contain",
                                audio_path: Optional[str] = None,
                                text_overlays: Optional[List[Dict[str, Any]]] = None,
                                effects: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Convert a list of images to a video slideshow with transitions and effects.
    
    Use this tool when you need to create a video slideshow from a collection of images
    with professional transitions, text overlays, and effects. Supports various aspect
    ratios, transition types, and customization options.
    
    Args:
        image_paths: List of absolute paths to image files.
                    Supported formats: JPG, PNG, BMP, TIFF, WEBP.
        output_path: Absolute path where the video slideshow will be saved.
                    Directory will be created if it doesn't exist.
        duration_per_image: Duration each image is displayed in seconds. Defaults to 3.0.
        fps: Frames per second for output video. Defaults to 24.
        resolution: Output video resolution as (width, height) tuple. Defaults to (1920, 1080).
        transition_type: Type of transition between images.
                        Options: "fade", "slide_left", "slide_right", "slide_up", 
                        "slide_down", "zoom", "crossfade", "none". Defaults to "fade".
        transition_duration: Duration of transitions in seconds. Defaults to 0.5.
        background_color: Background color as (r, g, b) tuple (0-255). Defaults to (0, 0, 0).
        fit_mode: How to fit images in the frame.
                 Options: "contain", "cover", "stretch", "crop". Defaults to "contain".
        audio_path: Optional absolute path to audio file for background music.
        text_overlays: Optional list of text overlay configurations with positioning and styling.
        effects: Optional list of visual effects to apply to images.
        
    Returns:
        A dictionary containing the slideshow creation result:
        - status: 'success' if slideshow created, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the created video file (None if error)
        - duration: Total duration of slideshow in seconds (if success)
        - images_count: Number of images processed (if success)
        - resolution: Output resolution used (if success)
        
        Example success: {'status': 'success', 'message': 'Successfully created slideshow',
                         'output_path': '/path/to/slideshow.mp4', 'duration': 15.5,
                         'images_count': 5, 'resolution': (1920, 1080)}
        Example error: {'status': 'error', 'message': 'No valid images found',
                       'output_path': None}
    """
    try:
        # Validate input images
        if not image_paths:
            return {
                "status": "error",
                "message": "No image paths provided",
                "output_path": None
            }
        
        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
        valid_images = []
        
        for path in image_paths:
            if not os.path.exists(path):
                return {
                    "status": "error",
                    "message": f"Image file not found: {path}",
                    "output_path": None
                }
            
            file_ext = Path(path).suffix.lower()
            if file_ext not in supported_formats:
                return {
                    "status": "error", 
                    "message": f"Unsupported image format: {file_ext}",
                    "output_path": None
                }
            valid_images.append(path)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create clips from images
        clips = []
        for i, img_path in enumerate(valid_images):
            clip = _create_image_clip(img_path, duration_per_image, resolution, fit_mode, background_color)
            
            # Apply text overlays if specified
            if text_overlays:
                clip = _add_text_overlays(clip, text_overlays, i, i * duration_per_image)
            
            # Apply effects if specified
            if effects:
                clip = _apply_effects(clip, effects)
            
            clips.append(clip)
        
        # Add transitions
        if transition_type != "none" and len(clips) > 1:
            clips = _add_transitions(clips, transition_type, transition_duration)
        
        # Concatenate all clips
        if len(clips) == 1:
            final_video = clips[0]
        else:
            if transition_type in ['fade', 'crossfade']:
                # For fade transitions, use CompositeVideoClip to handle overlaps
                final_video = CompositeVideoClip(clips)
            else:
                # For other transitions, use concatenate
                final_video = concatenate_videoclips(clips, method="compose")
        
        # Add background audio if specified
        if audio_path and os.path.exists(audio_path):
            audio = AudioFileClip(audio_path)
            # Loop audio if it's shorter than video
            if audio.duration < final_video.duration:
                audio = audio.loop(duration=final_video.duration)
            # Trim audio if it's longer than video
            elif audio.duration > final_video.duration:
                audio = audio.subclip(0, final_video.duration)
            
            final_video = final_video.set_audio(audio)
        
        # Write the final video
        final_video.write_videofile(
            output_path,
            fps=fps,
            codec='libx264',
            audio_codec='aac' if final_video.audio else None,
            temp_audiofile='temp-audio.m4a' if final_video.audio else None,
            remove_temp=True
        )
        
        # Get video info and convert to native Python types
        duration = float(final_video.duration)
        file_size = int(os.path.getsize(output_path))
        
        # Clean up
        for clip in clips:
            if hasattr(clip, 'close'):
                clip.close()
        final_video.close()
        
        return {
            "status": "success",
            "message": f"Successfully created slideshow from {len(valid_images)} images",
            "output_path": output_path,
            "duration": duration,
            "file_size": file_size,
            "images_count": len(valid_images),
            "fps": fps,
            "resolution": resolution
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating slideshow: {str(e)}",
            "output_path": None
        }
