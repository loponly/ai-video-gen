"""
Audio analysis functionality for extracting audio characteristics
"""

import os
from typing import Dict, Any, Optional
import wave
import json

try:
    import librosa
    import numpy as np
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

try:
    from moviepy.editor import AudioFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False


def analyze_audio(
    audio_path: str,
    analysis_type: str = "basic",
    output_format: str = "json"
) -> Dict[str, Any]:
    """
    Analyze audio file properties and characteristics for audio processing decisions.
    
    Use this tool when you need to understand audio file properties before processing,
    determine optimal settings for audio effects, or extract metadata for audio editing.
    Provides detailed analysis including duration, sample rate, channels, and advanced
    features like tempo, pitch, and spectral characteristics.
    
    Args:
        audio_path: Absolute path to the audio file to analyze.
                   Supports common formats: mp3, wav, flac, aac, m4a.
        analysis_type: Type of analysis to perform. Options:
                      'basic' - duration, sample rate, channels, bitrate
                      'advanced' - includes tempo, pitch, spectral analysis
                      'full' - comprehensive analysis with detailed features
                      Defaults to 'basic'.
        output_format: Format for detailed analysis data. Options are 'json'
                      or 'summary'. Defaults to 'json'.
    
    Returns:
        A dictionary containing the audio analysis results:
        - status: 'success' if analysis completed, 'error' if failed
        - message: Descriptive message about the operation result
        - file_path: Path to the analyzed audio file
        - properties: Dictionary with audio properties (duration, sample_rate, etc.)
        - analysis_data: Detailed analysis results based on analysis_type
        
        Example success: {'status': 'success', 'message': 'Audio analysis completed',
                         'file_path': '/path/to/audio.mp3', 
                         'properties': {'duration': 45.2, 'sample_rate': 44100, 'channels': 2},
                         'analysis_data': {...}}
        Example error: {'status': 'error', 'message': 'Audio file not found',
                       'file_path': audio_path}
    """
    try:
        if not os.path.exists(audio_path):
            return {
                "status": "error",
                "message": f"Audio file not found: {audio_path}",
                "file_path": audio_path
            }
        
        # Basic properties using moviepy (more reliable for various formats)
        properties = {}
        analysis_data = {}
        
        if MOVIEPY_AVAILABLE:
            try:
                audio_clip = AudioFileClip(audio_path)
                properties = {
                    "duration": float(audio_clip.duration),
                    "fps": int(audio_clip.fps) if audio_clip.fps else None,
                    "channels": 2 if audio_clip.nchannels == 2 else 1,  # Simplified channel detection
                    "file_size": os.path.getsize(audio_path)
                }
                audio_clip.close()
            except Exception as e:
                # Fallback to basic file info
                properties = {
                    "file_size": os.path.getsize(audio_path),
                    "file_extension": os.path.splitext(audio_path)[1].lower()
                }
        
        # Advanced analysis using librosa if available
        if analysis_type in ["advanced", "full"] and LIBROSA_AVAILABLE:
            try:
                y, sr = librosa.load(audio_path)
                
                # Tempo and beat tracking
                tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
                
                # Spectral features
                spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
                spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
                
                # MFCC features
                mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                
                # Zero crossing rate
                zcr = librosa.feature.zero_crossing_rate(y)[0]
                
                analysis_data = {
                    "sample_rate": int(sr),
                    "tempo": float(tempo),
                    "beats_count": int(len(beats)),
                    "spectral_centroid_mean": float(np.mean(spectral_centroids)),
                    "spectral_rolloff_mean": float(np.mean(spectral_rolloff)),
                    "mfcc_mean": [float(x) for x in np.mean(mfccs, axis=1)],
                    "zero_crossing_rate_mean": float(np.mean(zcr)),
                    "rms_energy": float(np.mean(librosa.feature.rms(y=y)[0]))
                }
                
                if analysis_type == "full":
                    # Additional detailed features
                    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
                    tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
                    
                    analysis_data.update({
                        "chroma_mean": [float(x) for x in np.mean(chroma, axis=1)],
                        "tonnetz_mean": [float(x) for x in np.mean(tonnetz, axis=1)],
                        "spectral_bandwidth_mean": float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)[0])),
                        "spectral_contrast_mean": [float(x) for x in np.mean(librosa.feature.spectral_contrast(y=y, sr=sr), axis=1)]
                    })
                    
            except Exception as e:
                analysis_data["librosa_error"] = f"Advanced analysis failed: {str(e)}"
        
        # Format output
        if output_format == "summary" and analysis_data:
            # Create human-readable summary
            summary_parts = []
            if "duration" in properties:
                summary_parts.append(f"Duration: {properties['duration']:.1f}s")
            if "tempo" in analysis_data:
                summary_parts.append(f"Tempo: {analysis_data['tempo']:.1f} BPM")
            if "sample_rate" in analysis_data:
                summary_parts.append(f"Sample Rate: {analysis_data['sample_rate']} Hz")
            
            analysis_data["summary"] = ", ".join(summary_parts)
        
        return {
            "status": "success",
            "message": f"Audio analysis completed using {analysis_type} method",
            "file_path": audio_path,
            "properties": properties,
            "analysis_data": analysis_data,
            "libraries_used": {
                "moviepy": MOVIEPY_AVAILABLE,
                "librosa": LIBROSA_AVAILABLE
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Audio analysis failed: {str(e)}",
            "file_path": audio_path
        }
