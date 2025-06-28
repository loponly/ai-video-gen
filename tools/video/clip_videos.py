"""
Video clipping functionality
"""

import os
import json
from typing import Dict, Any, Optional
from moviepy.editor import VideoFileClip, concatenate_videoclips


def clip_videos(video_path: str, output_path: str, start_time: float = 0.0, 
               end_time: Optional[float] = None, segments: Optional[str] = None) -> Dict[str, Any]:
    """
    Clip video to specified segments or time range.
    
    Use this tool when you need to extract specific portions of a video.
    You can either clip a single segment using start_time and end_time,
    or extract multiple segments using the segments parameter.
    
    Args:
        video_path: Absolute path to the input video file to be clipped.
        output_path: Absolute path where the clipped video will be saved.
                    Directory will be created if it doesn't exist.
        start_time: Start time in seconds for single clip extraction. Defaults to 0.0.
        end_time: End time in seconds for single clip. If None, clips to end of video.
        segments: JSON string of (start, end) time pairs for multiple segments.
                 Format: "[[0,10],[20,30]]" for clips from 0-10s and 20-30s.
                 If provided, start_time and end_time are ignored.
    
    Returns:
        A dictionary containing the clipping result:
        - status: 'success' if clipping completed, 'error' if failed
        - message: Descriptive message about the operation result  
        - output_path: Path to the created video file (None if error)
        - duration: Duration of clipped video in seconds (if success)
        - original_duration: Duration of original video in seconds (if success)
        
        Example success: {'status': 'success', 'message': 'Successfully clipped video',
                         'output_path': '/path/to/clipped.mp4', 'duration': 10.5, 
                         'original_duration': 60.0}
        Example error: {'status': 'error', 'message': 'Video file not found: /invalid/path.mp4',
                       'output_path': None}
    """
    try:
            
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
                clip = video.subclip(start, end)
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
            
            final_video = video.subclip(start_time, end_time)
        
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
