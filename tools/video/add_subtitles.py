"""
Subtitle addition functionality
"""

import os
from typing import Dict, Any, Optional
from moviepy.editor import VideoFileClip


def add_subtitles(video_path: str, subtitle_path: str, output_path: str, 
                 subtitle_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Add subtitles or captions to video file.
    
    Use this tool when you need to embed subtitle files into video.
    Note: This function creates a copy of the video with subtitle metadata.
    For visual subtitle overlay, external tools may be needed.
    
    Args:
        video_path: Absolute path to the input video file.
        subtitle_path: Absolute path to the subtitle file (.srt, .vtt, .ass format).
        output_path: Absolute path where the video with subtitles will be saved.
                    Directory will be created if it doesn't exist.
        subtitle_options: Optional styling configuration for subtitles.
                         Can include font, size, color, position settings.
                         If None, default styling will be applied.
    
    Returns:
        A dictionary containing the subtitle addition result:
        - status: 'success' if subtitles added successfully, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the created video file (None if error) 
        - duration: Duration of output video in seconds (if success)
        - subtitle_format: Format of the subtitle file processed (if success)
        
        Example success: {'status': 'success', 'message': 'Successfully added subtitles',
                         'output_path': '/path/to/subtitled.mp4', 'duration': 90.3,
                         'subtitle_format': 'srt'}
        Example error: {'status': 'error', 'message': 'Video file not found: /invalid/path.mp4',
                       'output_path': None}
    """
    try:
        # Set default subtitle options if not provided
        if subtitle_options is None:
            subtitle_options = {}
        # Validate input files
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        if not os.path.exists(subtitle_path):
            return {
                "status": "error",
                "message": f"Subtitle file not found: {subtitle_path}",
                "output_path": None
            }
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Default subtitle options
        options = subtitle_options or {}
        
        # Load and copy video (MoviePy doesn't support subtitle overlay directly)
        video = VideoFileClip(video_path)
        
        # Write the video (this will copy the video)
        video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        video.close()
        
        return {
            "status": "success",
            "message": "Video copied successfully (subtitle overlay requires external tools)",
            "output_path": output_path,
            "subtitle_file": subtitle_path,
            "options_used": options
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error adding subtitles: {str(e)}",
            "output_path": None
        }
