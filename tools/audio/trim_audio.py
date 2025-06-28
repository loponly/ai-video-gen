"""Audio trimming functionality"""
import os
from typing import Dict, Any

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

def trim_audio(audio_path: str, output_path: str, start_time: float = 0.0, end_time: float = None) -> Dict[str, Any]:
    """Trim audio to specified time range."""
    try:
        if not PYDUB_AVAILABLE:
            return {"status": "error", "message": "Pydub not available", "output_path": None}
        
        if not os.path.exists(audio_path):
            return {"status": "error", "message": "Audio file not found", "output_path": None}
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        audio = AudioSegment.from_file(audio_path)
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000) if end_time else len(audio)
        
        trimmed = audio[start_ms:end_ms]
        trimmed.export(output_path, format="mp3")
        
        return {
            "status": "success",
            "message": f"Trimmed audio from {start_time}s to {end_time or len(audio)/1000}s",
            "output_path": output_path,
            "duration": len(trimmed) / 1000.0
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "output_path": None}
