"""
Audio Tools Package

This package contains tools for audio manipulation including:
- Text-to-speech conversion
- Audio analysis
- Audio effects and processing
- Volume adjustment
- Audio format conversion
- Audio mixing and merging
- Audio trimming and normalization
"""

from .text_to_speech import text_to_speech
from .analyze_audio import analyze_audio
from .apply_audio_effects import apply_audio_effects
from .adjust_volume import adjust_volume
from .convert_audio_format import convert_audio_format
from .fade_audio import fade_audio
from .merge_audio_tracks import merge_audio_tracks
from .mix_audio import mix_audio
from .normalize_audio import normalize_audio
from .trim_audio import trim_audio

__all__ = [
    'text_to_speech',
    'analyze_audio', 
    'apply_audio_effects',
    'adjust_volume',
    'convert_audio_format',
    'fade_audio',
    'merge_audio_tracks',
    'mix_audio',
    'normalize_audio',
    'trim_audio'
]
