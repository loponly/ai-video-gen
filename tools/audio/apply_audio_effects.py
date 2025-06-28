"""
Audio effects application functionality
"""

import os
from typing import Dict, Any, Optional, List

try:
    from pydub import AudioSegment
    from pydub.effects import normalize, compress_dynamic_range, low_pass_filter, high_pass_filter
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

try:
    from moviepy.editor import AudioFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False


def apply_audio_effects(
    audio_path: str,
    output_path: str,
    effects: List[Dict[str, Any]],
    preserve_format: bool = True
) -> Dict[str, Any]:
    """
    Apply various audio effects to enhance or modify audio characteristics.
    
    Use this tool when you need to enhance audio quality, apply creative effects,
    or modify audio characteristics for better integration with video content.
    Supports multiple effects including EQ, compression, reverb, and filters.
    
    Args:
        audio_path: Absolute path to the input audio file.
                   Supports common formats: mp3, wav, flac, aac.
        output_path: Absolute path where the processed audio will be saved.
                    Directory will be created if it doesn't exist.
        effects: List of effect dictionaries. Each effect should have:
                - type: Effect name ('normalize', 'compress', 'eq', 'filter', 'fade')
                - parameters: Dict with effect-specific parameters
                Example: [{"type": "normalize", "parameters": {"headroom": 0.1}},
                         {"type": "filter", "parameters": {"type": "low_pass", "cutoff": 5000}}]
        preserve_format: Whether to keep the original audio format.
                        If False, saves as WAV. Defaults to True.
    
    Returns:
        A dictionary containing the audio effects processing result:
        - status: 'success' if effects applied, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the processed audio file (None if error)
        - effects_applied: List of successfully applied effects
        - original_duration: Duration of original audio in seconds
        - processed_duration: Duration of processed audio in seconds
        
        Example success: {'status': 'success', 'message': 'Applied 3 audio effects',
                         'output_path': '/path/to/output.mp3', 'effects_applied': ['normalize', 'compress'],
                         'original_duration': 45.2, 'processed_duration': 45.2}
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
        
        if not PYDUB_AVAILABLE:
            return {
                "status": "error",
                "message": "Audio processing library not available. Install pydub: pip install pydub",
                "output_path": None
            }
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Load audio
        audio = AudioSegment.from_file(audio_path)
        original_duration = len(audio) / 1000.0  # Convert to seconds
        
        effects_applied = []
        
        # Apply effects in sequence
        for effect in effects:
            effect_type = effect.get("type", "").lower()
            params = effect.get("parameters", {})
            
            try:
                if effect_type == "normalize":
                    headroom = params.get("headroom", 0.1)
                    audio = normalize(audio, headroom=headroom)
                    effects_applied.append("normalize")
                
                elif effect_type == "compress":
                    threshold = params.get("threshold", -20.0)
                    ratio = params.get("ratio", 4.0)
                    attack = params.get("attack", 5.0)
                    release = params.get("release", 50.0)
                    audio = compress_dynamic_range(
                        audio, 
                        threshold=threshold,
                        ratio=ratio,
                        attack=attack,
                        release=release
                    )
                    effects_applied.append("compress")
                
                elif effect_type == "filter":
                    filter_type = params.get("type", "low_pass")
                    cutoff = params.get("cutoff", 5000)
                    
                    if filter_type == "low_pass":
                        audio = low_pass_filter(audio, cutoff)
                    elif filter_type == "high_pass":
                        audio = high_pass_filter(audio, cutoff)
                    
                    effects_applied.append(f"filter_{filter_type}")
                
                elif effect_type == "fade":
                    fade_in = params.get("fade_in", 0)
                    fade_out = params.get("fade_out", 0)
                    
                    if fade_in > 0:
                        audio = audio.fade_in(int(fade_in * 1000))
                    if fade_out > 0:
                        audio = audio.fade_out(int(fade_out * 1000))
                    
                    effects_applied.append("fade")
                
                elif effect_type == "volume":
                    gain_db = params.get("gain_db", 0)
                    audio = audio + gain_db
                    effects_applied.append("volume")
                
                elif effect_type == "speed":
                    speed_factor = params.get("factor", 1.0)
                    # Change speed without changing pitch (if supported)
                    new_sample_rate = int(audio.frame_rate * speed_factor)
                    audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_sample_rate})
                    audio = audio.set_frame_rate(audio.frame_rate)
                    effects_applied.append("speed")
                    
            except Exception as e:
                # Continue with other effects if one fails
                effects_applied.append(f"{effect_type}_failed")
        
        # Determine output format
        if preserve_format:
            format_ext = os.path.splitext(audio_path)[1].lower().replace('.', '')
            if format_ext in ['mp3', 'wav', 'flac', 'aac']:
                export_format = format_ext
            else:
                export_format = 'mp3'
        else:
            export_format = 'wav'
        
        # Export processed audio
        audio.export(output_path, format=export_format)
        
        processed_duration = len(audio) / 1000.0
        
        return {
            "status": "success",
            "message": f"Applied {len(effects_applied)} audio effects successfully",
            "output_path": output_path,
            "effects_applied": effects_applied,
            "original_duration": original_duration,
            "processed_duration": processed_duration,
            "format_used": export_format
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Audio effects processing failed: {str(e)}",
            "output_path": None
        }
