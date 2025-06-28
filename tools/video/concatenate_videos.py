"""
Video concatenation functionality
"""

import os
import json
from typing import List, Dict, Any
from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array


def concatenate_videos(video_paths: List[str], output_path: str, method: str = "compose") -> Dict[str, Any]:
    """
    Concatenate multiple video clips into a single video file.
    
    Use this tool when you need to join multiple video files together end-to-end
    or stack them vertically. The tool supports two concatenation methods:
    'compose' for sequential joining and 'stack' for vertical arrangement.
    
    Args:
        video_paths: List of absolute file paths to video files that will be concatenated.
                    All videos should exist and be valid video files.
        output_path: Absolute path where the concatenated video will be saved.
                    Directory will be created if it doesn't exist.
        method: Method for concatenation. 'compose' joins videos sequentially,
               'stack' arranges videos vertically. Defaults to 'compose'.
    
    Returns:
        A dictionary containing the concatenation result:
        - status: 'success' if concatenation completed, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the created video file (None if error)
        - duration: Total duration of concatenated video in seconds (if success)
        
        Example success: {'status': 'success', 'message': 'Successfully concatenated 3 videos', 
                         'output_path': '/path/to/output.mp4', 'duration': 45.2}
        Example error: {'status': 'error', 'message': 'Video file not found: /invalid/path.mp4', 
                       'output_path': None}
    """
    try:
        # Validate method parameter
        if method not in ["compose", "stack"]:
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
