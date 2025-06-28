"""
Text-to-speech functionality for voice-over generation
"""

import os
import tempfile
from typing import Dict, Any, Optional
from pathlib import Path

try:
    import pyttsx3
    from gtts import gTTS
    AUDIO_LIBRARIES_AVAILABLE = True
except ImportError:
    AUDIO_LIBRARIES_AVAILABLE = False


def text_to_speech(
    text: str, 
    output_path: str, 
    voice_engine: str = "gtts",
    language: str = "en",
    speed: float = 1.0,
    voice_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convert text to speech and save as audio file for voice-over generation.
    
    Use this tool when you need to generate voice-over narration from text,
    create audio commentary, or add spoken content to videos. Supports multiple
    text-to-speech engines for different voice characteristics and languages.
    
    Args:
        text: The text content to convert to speech. Should be clean text
              without special formatting or excessive punctuation.
        output_path: Absolute path where the audio file will be saved.
                    Should end with .mp3 or .wav extension.
        voice_engine: TTS engine to use. Options are 'gtts' (Google Text-to-Speech,
                     requires internet) or 'pyttsx3' (offline). Defaults to 'gtts'.
        language: Language code for speech synthesis (e.g., 'en', 'es', 'fr').
                 Used mainly with gtts engine. Defaults to 'en'.
        speed: Speech speed multiplier. 1.0 is normal speed, 0.5 is half speed,
               2.0 is double speed. Only works with pyttsx3 engine.
        voice_id: Optional voice identifier for pyttsx3 engine. If None,
                 uses system default voice.
    
    Returns:
        A dictionary containing the TTS operation result:
        - status: 'success' if audio generated, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the generated audio file (None if error)
        - duration_estimate: Estimated duration in seconds (if success)
        - engine_used: Which TTS engine was actually used
        
        Example success: {'status': 'success', 'message': 'Successfully generated speech',
                         'output_path': '/path/to/output.mp3', 'duration_estimate': 15.2,
                         'engine_used': 'gtts'}
        Example error: {'status': 'error', 'message': 'Text-to-speech libraries not available',
                       'output_path': None}
    """
    try:
        if not AUDIO_LIBRARIES_AVAILABLE:
            return {
                "status": "error",
                "message": "Text-to-speech libraries not available. Install pyttsx3 and gtts: pip install pyttsx3 gtts",
                "output_path": None
            }
        
        if not text.strip():
            return {
                "status": "error",
                "message": "Text content cannot be empty",
                "output_path": None
            }
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Estimate duration (rough calculation: ~150 words per minute)
        word_count = len(text.split())
        duration_estimate = (word_count / 150) * 60 / speed
        
        if voice_engine == "gtts":
            try:
                # Use Google Text-to-Speech
                tts = gTTS(text=text, lang=language, slow=False)
                tts.save(output_path)
                
                return {
                    "status": "success", 
                    "message": f"Successfully generated speech using Google TTS",
                    "output_path": output_path,
                    "duration_estimate": duration_estimate,
                    "engine_used": "gtts",
                    "language": language
                }
                
            except Exception as e:
                # Fallback to pyttsx3 if gtts fails
                voice_engine = "pyttsx3"
        
        if voice_engine == "pyttsx3":
            try:
                # Use offline text-to-speech
                engine = pyttsx3.init()
                
                # Set speech rate
                rate = engine.getProperty('rate')
                engine.setProperty('rate', int(rate * speed))
                
                # Set voice if specified
                if voice_id:
                    voices = engine.getProperty('voices')
                    for voice in voices:
                        if voice_id in voice.id:
                            engine.setProperty('voice', voice.id)
                            break
                
                # Generate speech
                engine.save_to_file(text, output_path)
                engine.runAndWait()
                
                return {
                    "status": "success",
                    "message": f"Successfully generated speech using offline TTS", 
                    "output_path": output_path,
                    "duration_estimate": duration_estimate,
                    "engine_used": "pyttsx3",
                    "speed": speed
                }
                
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Failed to generate speech with pyttsx3: {str(e)}",
                    "output_path": None
                }
        
        return {
            "status": "error",
            "message": f"Unsupported voice engine: {voice_engine}. Use 'gtts' or 'pyttsx3'",
            "output_path": None
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Text-to-speech generation failed: {str(e)}",
            "output_path": None
        }
