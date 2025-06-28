"""
Audio volume adjustment functionality
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


def adjust_volume(
    audio_path: str,
    output_path: str,
    volume_change: float = 0.0,
    target_volume: float = None,
    method: str = "relative"
) -> Dict[str, Any]:
    """
    Adjust audio volume levels for optimal playback and integration.
    
    Use this tool when you need to increase or decrease audio volume,
    normalize volume levels across multiple audio files, or match audio
    levels for seamless integration with video content.
    
    Args:
        audio_path: Absolute path to the input audio file.
                   Supports common formats: mp3, wav, flac, aac, m4a.
        output_path: Absolute path where the volume-adjusted audio will be saved.
                    Directory will be created if it doesn't exist.
        volume_change: Volume change in decibels (dB). Positive values increase volume,
                      negative values decrease volume. Only used when method is 'relative'.
                      Defaults to 0.0 (no change).
        target_volume: Target volume level in dB. Used when method is 'absolute'.
                      Common values: -12dB (loud), -18dB (moderate), -24dB (quiet).
        method: Volume adjustment method. Options:
               'relative' - adjust by volume_change amount (default)
               'absolute' - set to specific target_volume level
               'normalize' - normalize to maximum level without clipping
    
    Returns:
        A dictionary containing the volume adjustment result:
        - status: 'success' if volume adjusted, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the volume-adjusted audio file (None if error)
        - original_volume: Estimated original volume level in dB
        - final_volume: Final volume level in dB after adjustment
        - volume_change_applied: Actual volume change applied in dB
        
        Example success: {'status': 'success', 'message': 'Volume increased by 6dB',
                         'output_path': '/path/to/output.mp3', 'original_volume': -18.5,
                         'final_volume': -12.5, 'volume_change_applied': 6.0}
        Example error: {'status': 'error', 'message': 'Audio file not found',
                       'output_path': None}
    """
    try:
        if not os.path.exists(audio_path):
            return {
                "status": "error",
                "message": f"Audio file not found: {audio_path}",
                "output_path": None
            }
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Try pydub first (more precise volume control)
        if PYDUB_AVAILABLE:
            try:
                audio = AudioSegment.from_file(audio_path)
                original_volume = audio.dBFS  # Get current volume in dB
                
                if method == "relative":
                    # Apply relative volume change
                    adjusted_audio = audio + volume_change
                    final_volume = original_volume + volume_change
                    volume_change_applied = volume_change
                    
                elif method == "absolute" and target_volume is not None:
                    # Set to absolute volume level
                    volume_change_applied = target_volume - original_volume
                    adjusted_audio = audio + volume_change_applied
                    final_volume = target_volume
                    
                elif method == "normalize":
                    # Normalize to maximum level without clipping
                    # Find the peak and adjust to -1dB to prevent clipping
                    target_level = -1.0
                    volume_change_applied = target_level - audio.max_dBFS
                    adjusted_audio = audio + volume_change_applied
                    final_volume = target_level
                    
                else:
                    return {
                        "status": "error",
                        "message": f"Invalid method '{method}' or missing target_volume for absolute method",
                        "output_path": None
                    }
                
                # Export adjusted audio
                format_ext = os.path.splitext(audio_path)[1].lower().replace('.', '')
                if format_ext in ['mp3', 'wav', 'flac', 'aac']:
                    export_format = format_ext
                else:
                    export_format = 'mp3'
                
                adjusted_audio.export(output_path, format=export_format)
                
                return {
                    "status": "success",
                    "message": f"Volume adjusted using {method} method",
                    "output_path": output_path,
                    "original_volume": round(original_volume, 2),
                    "final_volume": round(final_volume, 2),
                    "volume_change_applied": round(volume_change_applied, 2),
                    "method_used": method
                }
                
            except Exception as e:
                # Fallback to moviepy
                pass
        
        # Fallback to moviepy
        if MOVIEPY_AVAILABLE:
            try:
                audio_clip = AudioFileClip(audio_path)
                
                if method == "relative":
                    # Convert dB to linear scale for moviepy
                    # dB to linear: 10^(dB/20)
                    volume_factor = 10 ** (volume_change / 20)
                    adjusted_clip = audio_clip.volumex(volume_factor)
                    volume_change_applied = volume_change
                    
                elif method == "normalize":
                    # Simple normalization - increase to reasonable level
                    volume_factor = 2.0  # Roughly +6dB
                    adjusted_clip = audio_clip.volumex(volume_factor)
                    volume_change_applied = 6.0
                    
                else:
                    return {
                        "status": "error", 
                        "message": f"Method '{method}' not fully supported with moviepy. Use 'relative' or 'normalize'",
                        "output_path": None
                    }
                
                # Export adjusted audio
                adjusted_clip.write_audiofile(
                    output_path,
                    verbose=False,
                    logger=None
                )
                
                # Clean up
                audio_clip.close()
                adjusted_clip.close()
                
                return {
                    "status": "success",
                    "message": f"Volume adjusted using moviepy with {method} method",
                    "output_path": output_path,
                    "volume_change_applied": volume_change_applied,
                    "method_used": method,
                    "note": "Volume levels estimated (moviepy fallback)"
                }
                
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Volume adjustment failed with moviepy: {str(e)}",
                    "output_path": None
                }
        
        return {
            "status": "error",
            "message": "No audio processing libraries available. Install pydub or moviepy",
            "output_path": None
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Volume adjustment failed: {str(e)}",
            "output_path": None
        }
