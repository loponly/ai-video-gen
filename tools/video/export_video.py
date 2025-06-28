"""
Video export functionality
"""

import os
import shutil
from typing import Dict, Any

# Import PIL compatibility patch first
from . import pil_compat

from moviepy.editor import VideoFileClip


def export_video(video_path: str, output_path: str, format_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export video with specific format settings and codec options.
    
    Use this tool when you need to convert video to different formats or apply
    specific encoding settings like resolution, bitrate, or codec changes.
    
    Args:
        video_path: Absolute path to the input video file to be exported.
        output_path: Absolute path where the exported video will be saved.
                    File extension determines output format (.mp4, .webm, .avi).
                    Directory will be created if it doesn't exist.
        format_settings: Dictionary with export configuration options.
                        Supported keys: 'codec', 'audio_codec', 'bitrate', 
                        'resolution', 'fps'. If None, uses format-appropriate defaults.
    
    Returns:
        A dictionary containing the export result:
        - status: 'success' if export completed, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the exported video file (None if error)
        - duration: Duration of exported video in seconds (if success)
        - format: Output format/extension used (if success)
        - settings_used: The export settings that were applied (if success)
        
        Example success: {'status': 'success', 'message': 'Successfully exported video',
                         'output_path': '/path/to/exported.mp4', 'duration': 75.2,
                         'format': 'mp4', 'settings_used': {'codec': 'libx264'}}
        Example error: {'status': 'error', 'message': 'Video file not found: /invalid/path.mp4',
                       'output_path': None}
    """
    try:
        # Set default format settings if not provided
        if format_settings is None:
            format_settings = {}
        # Validate input file
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        # Load video
        video = VideoFileClip(video_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Extract format settings and adjust for output format
        output_ext = os.path.splitext(output_path)[1].lower()
        
        # Set appropriate default codecs based on output format
        if output_ext == '.webm':
            default_codec = 'libvpx-vp9'  # VP9 for WebM
            default_audio_codec = None  # Let MoviePy choose for WebM
        elif output_ext == '.mp4':
            default_codec = 'libx264'  # H.264 for MP4
            default_audio_codec = 'aac'  # AAC for MP4
        elif output_ext == '.avi':
            default_codec = 'libx264'  # H.264 for AVI
            default_audio_codec = 'mp3'  # MP3 for AVI
        else:
            default_codec = 'libx264'  # Default fallback
            default_audio_codec = 'aac'  # Default fallback
        
        codec = format_settings.get('codec', default_codec)
        audio_codec = format_settings.get('audio_codec', default_audio_codec)
        bitrate = format_settings.get('bitrate', None)
        fps = format_settings.get('fps', None)
        resolution = format_settings.get('resolution', None)
        
        # Apply resolution if specified
        if resolution:
            width, height = resolution
            video = video.resize((width, height))
        
        # Handle case where input and output paths are the same
        temp_output_path = output_path
        if os.path.abspath(video_path) == os.path.abspath(output_path):
            # Create a temporary output path with same extension
            path_parts = os.path.splitext(output_path)
            temp_output_path = f"{path_parts[0]}_temp{path_parts[1]}"
        
        # Prepare write parameters
        write_params = {
            'codec': codec,
            'remove_temp': True
        }
        
        # Handle audio codec and temp file based on output format
        if output_ext == '.webm':
            # For WebM, let MoviePy handle audio codec automatically
            # Don't specify temp_audiofile for WebM to avoid issues
            pass
        else:
            # For other formats, use temp audio file
            write_params['temp_audiofile'] = 'temp-audio.m4a'
            if audio_codec:
                write_params['audio_codec'] = audio_codec
        
        if bitrate:
            write_params['bitrate'] = bitrate
        if fps:
            write_params['fps'] = fps
        
        # Write the video
        video.write_videofile(temp_output_path, **write_params)
        
        # Get file size and duration and convert to native Python types
        file_size = int(os.path.getsize(temp_output_path))
        duration = float(video.duration)
        
        # Clean up
        video.close()
        
        # If we used a temporary file, replace the original
        if temp_output_path != output_path:
            shutil.move(temp_output_path, output_path)
            file_size = int(os.path.getsize(output_path))
        
        return {
            "status": "success",
            "message": "Successfully exported video",
            "output_path": output_path,
            "file_size": file_size,
            "settings_used": format_settings,
            "duration": duration
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error exporting video: {str(e)}",
            "output_path": None
        }
