"""
Audio format conversion functionality
"""

import os
from typing import Dict, Any

try:
    from moviepy.editor import AudioFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


def convert_audio_format(
    audio_path: str,
    output_path: str,
    target_format: str = "mp3",
    quality: str = "medium",
    sample_rate: int = None
) -> Dict[str, Any]:
    """
    Convert audio files between different formats and quality settings.
    
    Use this tool when you need to convert audio to specific formats for compatibility,
    reduce file size, or change quality settings for different use cases.
    
    Args:
        audio_path: Absolute path to the input audio file.
        output_path: Absolute path where the converted audio will be saved.
        target_format: Target format. Options: 'mp3', 'wav', 'flac', 'aac', 'm4a'.
                      Defaults to 'mp3'.
        quality: Quality preset. Options: 'low', 'medium', 'high', 'lossless'.
                Defaults to 'medium'.
        sample_rate: Target sample rate in Hz (e.g., 44100, 48000). 
                    If None, keeps original sample rate.
    
    Returns:
        A dictionary containing the conversion result:
        - status: 'success' if converted, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the converted audio file (None if error)
        - original_format: Original audio format
        - target_format: Target format used
        - file_size_reduction: Percentage reduction in file size (if applicable)
    """
    try:
        if not os.path.exists(audio_path):
            return {
                "status": "error",
                "message": f"Audio file not found: {audio_path}",
                "output_path": None
            }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        original_size = os.path.getsize(audio_path)
        original_format = os.path.splitext(audio_path)[1].lower().replace('.', '')
        
        if PYDUB_AVAILABLE:
            audio = AudioSegment.from_file(audio_path)
            
            # Quality settings
            export_params = {}
            if target_format == "mp3":
                if quality == "low":
                    export_params["bitrate"] = "128k"
                elif quality == "medium":
                    export_params["bitrate"] = "192k" 
                elif quality == "high":
                    export_params["bitrate"] = "320k"
            
            # Sample rate conversion
            if sample_rate and sample_rate != audio.frame_rate:
                audio = audio.set_frame_rate(sample_rate)
            
            audio.export(output_path, format=target_format, **export_params)
            
        elif MOVIEPY_AVAILABLE:
            audio_clip = AudioFileClip(audio_path)
            audio_clip.write_audiofile(output_path, verbose=False, logger=None)
            audio_clip.close()
        else:
            return {
                "status": "error",
                "message": "No audio conversion libraries available",
                "output_path": None
            }
        
        new_size = os.path.getsize(output_path)
        reduction = ((original_size - new_size) / original_size) * 100 if original_size > 0 else 0
        
        return {
            "status": "success",
            "message": f"Successfully converted {original_format} to {target_format}",
            "output_path": output_path,
            "original_format": original_format,
            "target_format": target_format,
            "file_size_reduction": round(reduction, 2)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Audio conversion failed: {str(e)}",
            "output_path": None
        }
