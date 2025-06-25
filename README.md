# ai-video-ge
AI Video Gen lets you effortlessly create engaging videos from text, subtitles, or scripts. Turn movie clips, reels, or ideas into stunning 15-sec videos using AI-powered scene selection, editing, and voiceover – perfect for content creators.

## Video Concatenation and Audio Synchronization

### Features
- **Smart Video Concatenation**: Automatically finds and concatenates all MP4 files in numerical order
- **Audio Synchronization**: Adds audio track and ensures perfect sync
- **Intelligent Video Extension**: If video is shorter than audio, extends it by repeating scenes with smooth transitions
- **Professional Transitions**: Adds fade-in/fade-out and cross-dissolve effects for seamless viewing
- **Automated Processing**: One-click solution for complex video editing tasks

### Quick Start

1. **Check your setup**:
   ```bash
   python test_video_setup.py
   ```

2. **Run the video concatenator**:
   ```bash
   python run_video_concatenator.py
   ```

3. **Or use the main script directly**:
   ```bash
   python video_concatenator.py
   ```

### File Structure
```
movie-reels/movie_2/
├── 1.mp4          # Video files (will be concatenated in order)
├── 2.mp4
├── 3.mp4
├── 4.mp4
├── 5.mp4
└── audio.m4a      # Audio track to be added

movie-reels/output/
└── final_video.mp4 # Generated output
```

### How It Works

1. **Discovery**: Scans `movie-reels/movie_2/` for all `.mp4` files
2. **Sorting**: Orders files numerically (1.mp4, 2.mp4, etc.)
3. **Concatenation**: Combines videos with smooth fade transitions
4. **Audio Integration**: Adds the audio track from `audio.m4a`
5. **Extension Logic**: If video duration < audio duration:
   - Repeats video segments with cross-fade transitions
   - Ensures total video matches audio length exactly
6. **Export**: Saves final video as `movie-reels/output/final_video.mp4`

### Requirements

The script requires MoviePy for video processing:
```bash
pip install moviepy
# or
pip install -r requirements.txt
```

### Advanced Usage

```python
from video_concatenator import VideoProcessor

# Custom configuration
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
