"""
Convert WebM to MP4 functionality
"""

import os
from typing import Optional, Dict, Any
from moviepy.editor import VideoFileClip


def convert_webm_to_mp4(input_file: str, output_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Convert a WebM video file to MP4 format using H.264 codec.
    
    Use this tool when you need to convert WebM videos (commonly downloaded from web sources)
    to the more widely compatible MP4 format. The conversion maintains video quality while
    ensuring compatibility across different platforms and players.
    
    Args:
        input_file: Absolute path to the input WebM video file to be converted.
        output_file: Optional absolute path for the output MP4 file.
                    If None, uses the same filename with .mp4 extension.
                    Directory will be created if it doesn't exist.
    
    Returns:
        A dictionary containing the conversion result:
        - status: 'success' if conversion completed, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Absolute path to the converted MP4 file (None if error)
        - input_path: Path to the original WebM file (if success)
        - duration: Duration of converted video in seconds (if success)
        - file_size: Size of output file in bytes (if success)
        
        Example success: {'status': 'success', 'message': 'Successfully converted WebM to MP4',
                         'output_path': '/path/to/video.mp4', 'input_path': '/path/to/video.webm',
                         'duration': 120.5, 'file_size': 25165824}
        Example error: {'status': 'error', 'message': 'Input file not found: /invalid/path.webm',
                       'output_path': None}
    """
    try:
        # Validate input file
        if not os.path.exists(input_file):
            return {
                "status": "error",
                "message": f"Input file not found: {input_file}",
                "output_path": None
            }
        
        # Validate file extension
        if not input_file.lower().endswith('.webm'):
            return {
                "status": "error",
                "message": f"Input file must be a WebM file (.webm extension required)",
                "output_path": None
            }
        
        # Set default output file if not provided
        if output_file is None:
            name, _ = os.path.splitext(input_file)
            output_file = f"{name}.mp4"
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Load and convert video
        clip = VideoFileClip(input_file)
        clip.write_videofile(
            output_file, 
            codec="libx264", 
            audio_codec="aac",
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Get output file info
        output_path = os.path.abspath(output_file)
        duration = float(clip.duration)
        
        # Clean up
        clip.close()
        
        # Get file size
        file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
        
        return {
            "status": "success",
            "message": "Successfully converted WebM to MP4",
            "output_path": output_path,
            "input_path": input_file,
            "duration": duration,
            "file_size": file_size
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to convert WebM to MP4: {str(e)}",
            "output_path": None
        }
