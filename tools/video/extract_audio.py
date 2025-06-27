"""
Audio extraction functionality
"""

import os
from typing import Dict, Any, Optional
from moviepy.editor import VideoFileClip


def extract_audio(video_path: str, output_path: str, audio_format: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract audio from video file and save as audio file.
    
    Args:
        video_path: Path to the input video file
        output_path: Path where the extracted audio will be saved
        audio_format: Optional audio format ("mp3", "wav", "aac", "flac"). If None, inferred from output_path
    
    Returns:
        Dict with status, message, and output info
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
        
        # Check if video has audio
        if video.audio is None:
            video.close()
            return {
                "status": "error",
                "message": "Video file has no audio track",
                "output_path": None
            }
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Determine audio format if not specified
        if audio_format is None:
            output_ext = os.path.splitext(output_path)[1].lower()
            if output_ext in ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg']:
                audio_format = output_ext[1:]  # Remove the dot
            else:
                audio_format = 'mp3'  # Default format
                # Update output path with correct extension
                output_path = os.path.splitext(output_path)[0] + '.mp3'
        
        # Extract audio
        audio = video.audio
        
        # Write audio file with appropriate codec
        if audio_format.lower() in ['mp3']:
            audio.write_audiofile(output_path, codec='mp3')
        elif audio_format.lower() in ['wav']:
            audio.write_audiofile(output_path, codec='pcm_s16le')
        elif audio_format.lower() in ['aac', 'm4a']:
            audio.write_audiofile(output_path, codec='aac')
        elif audio_format.lower() in ['flac']:
            audio.write_audiofile(output_path, codec='flac')
        elif audio_format.lower() in ['ogg']:
            audio.write_audiofile(output_path, codec='libvorbis')
        else:
            # Default to mp3 for unknown formats
            audio.write_audiofile(output_path, codec='mp3')
        
        # Get audio info before closing and convert to native Python types
        duration = float(audio.duration)
        sample_rate = int(audio.fps) if audio.fps else None
        
        # Get file size
        file_size = int(os.path.getsize(output_path))
        
        # Clean up
        audio.close()
        video.close()
        
        return {
            "status": "success",
            "message": f"Successfully extracted audio in {audio_format} format",
            "output_path": output_path,
            "duration": duration,
            "sample_rate": sample_rate,
            "file_size": file_size,
            "audio_format": audio_format
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error extracting audio: {str(e)}",
            "output_path": None
        }
