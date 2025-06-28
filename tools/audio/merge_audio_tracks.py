"""
Audio track merging functionality
"""

import os
from typing import Dict, Any, List

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


def merge_audio_tracks(
    audio_paths: List[str],
    output_path: str,
    method: str = "sequential"
) -> Dict[str, Any]:
    """
    Merge multiple audio tracks into a single audio file.
    
    Use this tool when you need to combine multiple audio files end-to-end
    or overlay them for complex audio compositions.
    
    Args:
        audio_paths: List of absolute paths to audio files to merge.
        output_path: Absolute path where the merged audio will be saved.
        method: Merge method. Options: 'sequential' (end-to-end), 'overlay' (simultaneous).
               Defaults to 'sequential'.
    
    Returns:
        A dictionary containing the merge operation result:
        - status: 'success' if merged, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the merged audio file (None if error)
        - total_duration: Total duration of merged audio
        - tracks_merged: Number of tracks successfully merged
    """
    try:
        if not audio_paths:
            return {
                "status": "error",
                "message": "No audio files provided for merging",
                "output_path": None
            }
        
        if not PYDUB_AVAILABLE:
            return {
                "status": "error",
                "message": "Audio processing library not available",
                "output_path": None
            }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        audio_segments = []
        for path in audio_paths:
            if os.path.exists(path):
                audio_segments.append(AudioSegment.from_file(path))
        
        if not audio_segments:
            return {
                "status": "error",
                "message": "No valid audio files found",
                "output_path": None
            }
        
        if method == "sequential":
            merged_audio = audio_segments[0]
            for segment in audio_segments[1:]:
                merged_audio += segment
        elif method == "overlay":
            merged_audio = audio_segments[0]
            for segment in audio_segments[1:]:
                merged_audio = merged_audio.overlay(segment)
        
        merged_audio.export(output_path, format="mp3")
        
        return {
            "status": "success",
            "message": f"Successfully merged {len(audio_segments)} audio tracks",
            "output_path": output_path,
            "total_duration": len(merged_audio) / 1000.0,
            "tracks_merged": len(audio_segments)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Audio merging failed: {str(e)}",
            "output_path": None
        }
