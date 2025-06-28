"""
Audio fade effects functionality
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


def fade_audio(
    audio_path: str,
    output_path: str,
    fade_in_duration: float = 0.0,
    fade_out_duration: float = 0.0,
    fade_type: str = "linear"
) -> Dict[str, Any]:
    """
    Apply fade in and fade out effects to audio for smooth transitions.
    
    Use this tool when you need smooth audio transitions, eliminate abrupt starts/stops,
    or create professional audio transitions for video content.
    
    Args:
        audio_path: Absolute path to the input audio file.
        output_path: Absolute path where the faded audio will be saved.
        fade_in_duration: Duration of fade in effect in seconds. Defaults to 0.0.
        fade_out_duration: Duration of fade out effect in seconds. Defaults to 0.0.
        fade_type: Type of fade curve. Options: 'linear', 'exponential'.
                  Defaults to 'linear'.
    
    Returns:
        A dictionary containing the fade operation result:
        - status: 'success' if fades applied, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the faded audio file (None if error)
        - fade_in_applied: Fade in duration actually applied
        - fade_out_applied: Fade out duration actually applied
    """
    try:
        if not os.path.exists(audio_path):
            return {
                "status": "error",
                "message": f"Audio file not found: {audio_path}",
                "output_path": None
            }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if PYDUB_AVAILABLE:
            audio = AudioSegment.from_file(audio_path)
            
            if fade_in_duration > 0:
                audio = audio.fade_in(int(fade_in_duration * 1000))
            
            if fade_out_duration > 0:
                audio = audio.fade_out(int(fade_out_duration * 1000))
            
            format_ext = os.path.splitext(audio_path)[1].lower().replace('.', '')
            audio.export(output_path, format=format_ext if format_ext else 'mp3')
            
        elif MOVIEPY_AVAILABLE:
            audio_clip = AudioFileClip(audio_path)
            
            if fade_in_duration > 0:
                audio_clip = audio_clip.audio_fadein(fade_in_duration)
            
            if fade_out_duration > 0:
                audio_clip = audio_clip.audio_fadeout(fade_out_duration)
            
            audio_clip.write_audiofile(output_path, verbose=False, logger=None)
            audio_clip.close()
        else:
            return {
                "status": "error",
                "message": "No audio processing libraries available",
                "output_path": None
            }
        
        return {
            "status": "success",
            "message": f"Applied fade effects successfully",
            "output_path": output_path,
            "fade_in_applied": fade_in_duration,
            "fade_out_applied": fade_out_duration
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Fade effects failed: {str(e)}",
            "output_path": None
        }
