"""Audio mixing functionality"""
import os
from typing import Dict, Any, List

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

def mix_audio(audio_paths: List[str], output_path: str, volumes: List[float] = None) -> Dict[str, Any]:
    """Mix multiple audio tracks with volume control."""
    try:
        if not PYDUB_AVAILABLE:
            return {"status": "error", "message": "Pydub not available", "output_path": None}
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        audio_segments = [AudioSegment.from_file(path) for path in audio_paths if os.path.exists(path)]
        
        if not audio_segments:
            return {"status": "error", "message": "No valid audio files", "output_path": None}
        
        mixed = audio_segments[0]
        for i, segment in enumerate(audio_segments[1:], 1):
            volume = volumes[i] if volumes and i < len(volumes) else 1.0
            mixed = mixed.overlay(segment + (20 * np.log10(volume) if volume > 0 else -60))
        
        mixed.export(output_path, format="mp3")
        
        return {
            "status": "success",
            "message": f"Mixed {len(audio_segments)} tracks",
            "output_path": output_path,
            "duration": len(mixed) / 1000.0
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "output_path": None}
