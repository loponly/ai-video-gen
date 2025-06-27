"""
Video concatenation functionality
"""

import os
import json
from typing import List, Dict, Any
from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array


def concatenate_videos(video_paths: List[str], output_path: str, method: str) -> Dict[str, Any]:
    """
    Concatenate multiple video clips into a single video.
    
    Args:
        video_paths: List of paths to video files to concatenate
        output_path: Path where the concatenated video will be saved
        method: Method for concatenation ("compose" or "stack")
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Set default method if not provided
        if not method:
            method = "compose"
            
        # Validate input files
        valid_videos = []
        for path in video_paths:
            if not os.path.exists(path):
                return {
                    "status": "error",
                    "message": f"Video file not found: {path}",
                    "output_path": None
                }
            valid_videos.append(VideoFileClip(path))
        
        if not valid_videos:
            return {
                "status": "error", 
                "message": "No valid video files provided",
                "output_path": None
            }
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Concatenate videos
        if method == "compose":
            final_video = concatenate_videoclips(valid_videos)
        elif method == "stack":
            # Stack videos vertically - use clips_array for this
            final_video = clips_array([[video] for video in valid_videos])
        else:
            return {
                "status": "error",
                "message": f"Invalid method: {method}. Use 'compose' or 'stack'",
                "output_path": None
            }
        
        # Write the final video
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Get duration before closing and convert to native Python float
        duration = float(final_video.duration)
        
        # Clean up
        for video in valid_videos:
            video.close()
        final_video.close()
        
        return {
            "status": "success",
            "message": f"Successfully concatenated {len(video_paths)} videos",
            "output_path": output_path,
            "duration": duration
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error concatenating videos: {str(e)}",
            "output_path": None
        }
