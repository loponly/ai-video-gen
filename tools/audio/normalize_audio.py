"""Audio normalization functionality"""
import os
from typing import Dict, Any

try:
    from pydub import AudioSegment
    from pydub.effects import normalize
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

def normalize_audio(audio_path: str, output_path: str, target_db: float = -20.0) -> Dict[str, Any]:
    """Normalize audio to target dB level."""
    try:
        if not PYDUB_AVAILABLE:
            return {"status": "error", "message": "Pydub not available", "output_path": None}
        
        if not os.path.exists(audio_path):
            return {"status": "error", "message": "Audio file not found", "output_path": None}
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        audio = AudioSegment.from_file(audio_path)
        normalized = normalize(audio, headroom=abs(target_db))
        normalized.export(output_path, format="mp3")
        
        return {
            "status": "success",
            "message": f"Normalized audio to {target_db}dB",
            "output_path": output_path,
            "target_db": target_db
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "output_path": None}
