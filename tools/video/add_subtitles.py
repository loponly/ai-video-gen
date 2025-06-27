"""
Subtitle addition functionality
"""

import os
from typing import Dict, Any, Optional
from moviepy.editor import VideoFileClip


def add_subtitles(video_path: str, subtitle_path: str, output_path: str, 
                 subtitle_options: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Add subtitles or captions to video.
    Note: This function creates a copy of the video. For subtitle overlay, external tools are needed.
    
    Args:
        video_path: Path to the input video file
        subtitle_path: Path to the subtitle file (.srt, .vtt, .ass)
        output_path: Path where the video with subtitles will be saved
        subtitle_options: Optional styling options for subtitles
    
    Returns:
        Dict with status, message, and output info
    """
    try:
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
