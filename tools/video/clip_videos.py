"""
Video clipping functionality
"""

import os
import json
from typing import Dict, Any, Optional
from moviepy.editor import VideoFileClip, concatenate_videoclips


def clip_videos(video_path: str, output_path: str, start_time: float, 
               end_time: Optional[float], segments: Optional[str]) -> Dict[str, Any]:
    """
    Clip video(s) to specified segments.
    
    Args:
        video_path: Path to the input video file
        output_path: Path where the clipped video will be saved
        start_time: Start time in seconds (for single clip)
        end_time: End time in seconds (for single clip)
        segments: JSON string of (start, end) tuples for multiple segments, e.g., "[[0,10],[20,30]]"
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Set default values if not provided
        if start_time is None:
            start_time = 0.0
            
        # Validate input file
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        # Load video
        video = VideoFileClip(video_path)
        original_duration = video.duration
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Clip video based on parameters
        if segments:
            # Parse segments from JSON string
            try:
                segments_list = json.loads(segments)
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "message": f"Invalid segments JSON format: {segments}",
                    "output_path": None
                }
            
            # Multiple segments - concatenate them
            clips = []
            for start, end in segments_list:
                if end > video.duration:
                    end = video.duration
                clip = video.subclipped(start, end)
                clips.append(clip)
            
            if clips:
                final_video = concatenate_videoclips(clips)
            else:
                return {
                    "status": "error",
                    "message": "No valid segments provided",
                    "output_path": None
                }
        else:
            # Single segment
            if end_time is None:
                end_time = video.duration
            elif end_time > video.duration:
                end_time = video.duration
            
            final_video = video.subclipped(start_time, end_time)
        
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
        video.close()
        final_video.close()
        
        return {
            "status": "success",
            "message": "Successfully clipped video",
            "output_path": output_path,
            "duration": duration,
            "original_duration": float(original_duration)  # Convert this too
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error clipping video: {str(e)}",
            "output_path": None
        }
