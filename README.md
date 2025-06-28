# AI Video Generator (ai-video-ge)

🚀 **Create Viral Reels in Seconds**
Transform any text, blog post, or long video into engaging short-form content. AI handles the script, voiceover, visuals, and editing automatically.

## 🎯 Why This Tool Exists

In today's content landscape, **viral short-form content is king**. Whether it's YouTube Shorts, TikTok, Instagram Reels, or any platform - the demand for quick, engaging content has never been higher. This tool automates the entire process:

✨ **From Idea to Viral Reel in Minutes**  
📝 **AI Script Generation** → 🎤 **Voice-over Creation** → 🎬 **Professional Editing** → 📱 **Ready-to-Post Content**

## 🔥 Core Features

### 🤖 Complete AI Automation Pipeline
- **Script Generator**: AI creates engaging scripts from any input (text, articles, concepts)
- **Voice-over Engine**: Text-to-speech with natural-sounding voices in multiple languages
- **Visual Content Creator**: Generates videos from images, text overlays, and effects
- **Auto-Editor**: Applies transitions, effects, and timing optimization for maximum engagement
- **Viral Optimization**: Built-in hooks, retention tactics, and platform-specific formatting

### 🎯 Multi-Agent AI System
- **Orchestration Agent**: Coordinates the entire content creation workflow
- **YouTube Agent**: Download viral content, extract transcripts, analyze trending topics
- **Video Editor Agent**: Professional editing with viral-focused effects and transitions
- **Image-to-Video Agent**: Transform static content into dynamic visual experiences
- **Audio Processing Agent**: Voice-over generation and audio effects optimization
- **File Management Agent**: Automated organization and batch content production

### 📱 Viral Reel Creation
- **Short-Form Focus**: Optimized for YouTube Shorts, TikTok, Instagram Reels
- **Engagement Hooks**: AI-generated attention-grabbing openings and CTAs
- **Retention Optimization**: Smart pacing and visual elements to maximize watch time
- **Trend Analysis**: Identify viral content patterns and apply them automatically
- **Platform Adaptation**: Automatic formatting for different social media platforms

### 🎬 Advanced Video Processing
- **Smart Video Concatenation**: Automatically merge MP4 files with smooth transitions
- **Audio Synchronization**: Perfect audio-video sync with intelligent extension
- **Professional Effects**: Fade transitions, cross-dissolve, zoom, and custom effects
- **Subtitle Management**: Add captions and subtitles with viral-style formatting
- **Format Conversion**: Support for multiple video and audio formats optimized for social media

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

### Viral Content Creation
- **AI-Powered Scripts**: Generate engaging scripts for trending topics and viral formats
- **Rapid Reel Production**: Create multiple short-form videos from single inputs
- **Trending Topic Analysis**: Transform YouTube videos into viral short-form content
- **Cross-Platform Optimization**: Automatically adapt content for different social platforms

### Automated Workflows
- **Text-to-Reel Pipeline**: Transform blog posts, articles, or ideas into viral videos
- **Batch Content Creation**: Generate multiple reels from image collections with AI voiceovers
- **Template-Based Production**: Use proven viral formats for consistent engagement
- **One-Click Publishing**: Complete automation from concept to ready-to-post content

### Content Creator Tools
- **Voice-over Generation**: Professional AI narration in multiple languages and styles
- **Visual Enhancement**: Dynamic transitions, effects, and text overlays for maximum impact
- **Trend Integration**: Apply viral video patterns and engagement tactics automatically
- **Analytics-Driven**: Optimize content based on successful viral reel characteristics

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
