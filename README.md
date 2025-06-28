# AI Video Generator (ai-video-ge)

A comprehensive AI-powered video creation platform that transforms content from various sources into professional videos. Create engaging videos from YouTube content, images, text, or audio using sophisticated AI agents and automated workflows.

## 🎯 Core Features

### Multi-Agent AI System
- **Orchestration Agent**: Coordinates complex multi-step workflows
- **YouTube Agent**: Download videos, extract transcripts, get video information
- **Video Editor Agent**: Professional video editing with effects and transitions
- **Image-to-Video Agent**: Create stunning slideshows and image-based videos
- **Audio Processing Agent**: Voice-over generation and audio effects
- **File Management Agent**: Automated file organization and batch operations

### Video Processing Capabilities
- **Smart Video Concatenation**: Automatically merge MP4 files with smooth transitions
- **Audio Synchronization**: Perfect audio-video sync with intelligent extension
- **Professional Effects**: Fade transitions, cross-dissolve, zoom, and custom effects
- **Subtitle Management**: Add captions and subtitles with customizable styling
- **Format Conversion**: Support for multiple video and audio formats

### Content Creation Tools
- **YouTube Integration**: Download videos, extract transcripts, search content
- **Image Slideshows**: Transform image collections into professional videos
- **Text-to-Speech**: Generate voice-overs in multiple languages
- **Audio Processing**: Effects, normalization, mixing, and format conversion
- **Batch Processing**: Handle multiple files efficiently

## 🚀 Quick Start

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Add your API keys to .env file
   ```

### Basic Usage

1. **Run the AI agent system**:
   ```bash
   python agent_runner.py
   ```

2. **Interactive demo**:
   ```bash
   python demo_agent_runner.py
   ```

3. **Test functionality**:
   ```bash
   pytest tests/ -v
   ```

## 📁 Project Structure
```
ai-video-ge/
├── 📁 adk_agents/              # AI Agent System
│   ├── agents.py               # Multi-agent orchestration
│   ├── path_config.py          # Centralized path management
│   └── __init__.py
├── 📁 tools/                   # Comprehensive Tool Library
│   ├── 🎬 video/              # Video editing and processing
│   ├── 🖼️ image/              # Image-to-video conversion
│   ├── 🎵 audio/              # Audio processing and TTS
│   ├── 📺 youtube/            # YouTube integration
│   └── 📂 file/               # File management utilities
├── 📁 tests/                   # Comprehensive test suite
├── 📁 docs/                    # Documentation and guides
├── 📁 downloads/               # Downloaded content storage
├── 📁 outputs/                 # Generated content output
├── 📁 content/                 # Sample content files
├── 📁 movie-reels/            # Video project workspace
├── agent_runner.py             # Main application entry
├── demo_agent_runner.py        # Interactive demo
├── requirements.txt            # Dependencies
└── video_config.ini           # Configuration settings
```

## 🛠️ Available Tools

### YouTube Tools
- **Download Videos**: High-quality video downloads with format options
- **Extract Transcripts**: Automatic transcript extraction with timestamps
- **Video Information**: Metadata, thumbnails, and video details
- **Search Videos**: Find content by keywords and filters

### Video Editing Tools
- **Concatenate Videos**: Merge multiple videos with transitions
- **Audio Synchronization**: Perfect audio-video alignment
- **Video Effects**: Fade, zoom, speed, resize effects
- **Clip Management**: Trim, split, and arrange video segments
- **Subtitle Addition**: Add captions with custom styling
- **Format Export**: Multiple output formats and quality settings
- **Metadata Editing**: Update video information and properties

### Image-to-Video Tools
- **Slideshow Creation**: Transform images into professional videos
- **Text Overlays**: Add captions and titles to images
- **Transition Effects**: Smooth transitions between images
- **Audio Integration**: Sync background music with slideshows
- **Custom Timing**: Control display duration per image

### Audio Processing Tools
- **Text-to-Speech**: Generate voice-overs in multiple languages
- **Audio Effects**: Fade, normalize, compress, and filter
- **Format Conversion**: Convert between audio formats
- **Volume Control**: Adjust and normalize audio levels
- **Audio Mixing**: Combine multiple audio tracks
- **Trim & Edit**: Cut and arrange audio segments

### File Management Tools
- **Batch Operations**: Process multiple files simultaneously
- **Directory Management**: Create and organize folder structures
- **File Compression**: Create and extract archives
- **Search & Find**: Locate files by pattern and type
- **Copy & Move**: Relocate files with structure preservation

## 🎯 Use Cases

### Content Creation
- Transform YouTube videos into short-form content
- Create educational slideshows with voice-over
- Generate social media videos from images
- Compile video highlights with effects

### Educational Content
- Extract and save video transcripts for study
- Create presentation videos from slides
- Generate audio content from text materials
- Organize multimedia learning resources

### Marketing & Social Media
- Create promotional videos from product images
- Generate video content with branded overlays
- Compile customer testimonials with effects
- Transform blog content into video format

## ⚙️ Configuration

### Video Processing Settings
Edit `video_config.ini` to customize:
```ini
[video_settings]
fade_duration = 0.5          # Transition duration
segment_duration = 10.0      # Extension segment length
video_codec = libx264        # Output codec
audio_codec = aac            # Audio codec

[paths]
video_directory = movie-reels/movie_2
audio_file = movie-reels/movie_2/audio.m4a
output_file = movie-reels/output/final_video.mp4
```

### Environment Variables
Create `.env` file with your API keys:
```env
GOOGLE_API_KEY=your_gemini_api_key
YOUTUBE_API_KEY=your_youtube_api_key
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Run all tests
pytest tests/ -v

# Test specific functionality
pytest tests/test_video_editor_tools.py
pytest tests/test_image_to_video.py
pytest tests/test_agent_evaluation.py

# Integration tests
pytest tests/test_adk_compatible_evaluation.py
```

## 📖 Documentation

Detailed guides available in the `docs/` folder:
- **Agent Development**: How to extend the AI agent system
- **Tool Integration**: Adding new processing capabilities
- **Evaluation Framework**: Testing and quality assurance
- **Path Configuration**: File organization best practices

## 🔧 Advanced Usage

### Custom Workflows
```python
from adk_agents import root_agent
from google.adk.runners import Runner

# Create custom processing pipeline
async def process_youtube_to_slideshow(video_url, images_dir):
    runner = await create_runner()
    
    # Download and extract transcript
    result = await runner.run(
        f"Download video from {video_url} and extract transcript"
    )
    
    # Create slideshow with voice-over
    result = await runner.run(
        f"Create slideshow from {images_dir} with extracted audio"
    )
    
    return result
```

### Batch Processing
```python
# Process multiple videos
video_urls = [
    "https://youtube.com/watch?v=...",
    "https://youtube.com/watch?v=...",
]

for url in video_urls:
    await runner.run(f"Download and process {url}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Follow the coding guidelines in the project documentation
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Projects

- [MoviePy](https://github.com/Zulko/moviepy) - Video editing library
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube download tool
- [Google ADK](https://ai.google.dev/adk) - Agent Development Kit

---

**Made with ❤️ for content creators and AI enthusiasts**
processor = VideoProcessor(
    video_dir="path/to/videos",
    audio_file="path/to/audio.m4a", 
    output_file="path/to/output.mp4"
)
processor.process_video()
```

### Configuration Options

- **Fade Duration**: Adjust transition length by modifying `fade_duration` in `VideoProcessor`
- **Extension Segments**: Control how video is extended by adjusting `segment_duration`
- **Output Quality**: Modify codec settings in the `write_videofile` call

### Troubleshooting

- **MoviePy Import Error**: Install with `pip install moviepy`
- **FFmpeg Not Found**: Install FFmpeg on your system
- **Memory Issues**: For large videos, ensure sufficient RAM or process in smaller batches
- **File Not Found**: Run `test_video_setup.py` to verify all files exist
