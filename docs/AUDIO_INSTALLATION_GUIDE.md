# Installation Guide for Enhanced Audio Features

## Audio Dependencies Installation

To enable full audio processing capabilities including voice-over generation, install the following dependencies:

### Method 1: Install Individual Packages
```bash
pip install pydub>=0.25.0
pip install librosa>=0.10.0
pip install pyttsx3>=2.90
pip install gTTS>=2.3.0
```

### Method 2: Install from Requirements
```bash
pip install -r requirements.txt
```

### Additional System Dependencies

#### For macOS:
```bash
# For audio processing
brew install ffmpeg
brew install portaudio

# For pyttsx3 (text-to-speech)
# Usually works out of the box on macOS
```

#### For Ubuntu/Debian:
```bash
# For audio processing
sudo apt update
sudo apt install ffmpeg
sudo apt install portaudio19-dev python3-pyaudio

# For pyttsx3
sudo apt install espeak espeak-data libespeak-dev
```

#### For Windows:
```bash
# Install chocolatey first, then:
choco install ffmpeg

# For pyttsx3, additional setup may be needed
# See: https://pyttsx3.readthedocs.io/en/latest/
```

## Verification

Test audio functionality:

```python
# Test text-to-speech
from tools.audio import text_to_speech
result = text_to_speech("Hello world", "test_output.mp3")
print(f"TTS Status: {result['status']}")

# Test audio analysis
from tools.audio import analyze_audio
# Will show error if no audio file exists (expected)
result = analyze_audio("nonexistent.mp3")
print(f"Analysis Status: {result['status']}")
```

## Troubleshooting

### Common Issues:

1. **"No module named 'pydub'"**
   - Solution: `pip install pydub`

2. **"ffmpeg not found"**
   - Solution: Install ffmpeg system-wide
   - macOS: `brew install ffmpeg`
   - Ubuntu: `sudo apt install ffmpeg`

3. **"pyttsx3 init() failed"**
   - Solution: Install system TTS engine
   - macOS: Usually works out of the box
   - Ubuntu: `sudo apt install espeak`

4. **"librosa import error"**
   - Solution: `pip install librosa numba`
   - May require additional audio libraries

### Fallback Behavior:

All audio tools gracefully handle missing dependencies:
- Return descriptive error messages
- Suggest installation commands
- Don't break the overall system
- Allow other functionality to continue working

## Testing Installation

Run the enhanced features demo:
```bash
cd /path/to/ai-video-ge
python demo_enhanced_features.py
```

This will show which audio libraries are available and working.
