#!/usr/bin/env python3
"""
Video Concatenation and Audio Synchronization Script

This script:
1. Finds all .mp4 files in movie-reels/movie_2/
2. Concatenates them in numerical order
3. Adds audio from audio.m4a
4. Extends video if shorter than audio by repeating scenes with transitions
5. Outputs final synchronized video
"""

import os
import re
import glob
from pathlib import Path
from typing import List, Tuple, Union, Any
import logging

# Try to import MoviePy components
try:
    from moviepy import (
        VideoFileClip, AudioFileClip, concatenate_videoclips,
        CompositeVideoClip, vfx
    )
    # Import effects from vfx
    fadein = vfx.FadeIn
    fadeout = vfx.FadeOut
    crossfadein = vfx.CrossFadeIn
    crossfadeout = vfx.CrossFadeOut
    
    MOVIEPY_AVAILABLE = True
    
    # Type hints for when MoviePy is available
    VideoClipType = VideoFileClip
    AudioClipType = AudioFileClip
    
except ImportError as e:
    print(f"MoviePy import error: {e}")
    print("Please install it using: pip install moviepy")
    print("Or run: pip install -r requirements.txt")
    MOVIEPY_AVAILABLE = False
    
    # Type hints for when MoviePy is not available
    VideoClipType = Any
    AudioClipType = Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VideoProcessor:
    """Handles video concatenation, audio synchronization, and extension."""
    
    def __init__(self, video_dir: str, audio_file: str, output_file: str):
        self.video_dir = Path(video_dir)
        self.audio_file = Path(audio_file)
        self.output_file = Path(output_file)
        self.fade_duration = 0.5  # Duration for fade transitions
        
    def find_video_files(self) -> List[Path]:
        """Find all .mp4 files in the directory and sort them numerically."""
        video_files = list(self.video_dir.glob("*.mp4"))
        
        # Sort numerically (1.mp4, 2.mp4, etc.)
        def numerical_sort_key(file_path):
            # Extract number from filename
            match = re.search(r'(\d+)', file_path.stem)
            return int(match.group(1)) if match else 0
        
        video_files.sort(key=numerical_sort_key)
        logger.info(f"Found {len(video_files)} video files: {[f.name for f in video_files]}")
        return video_files
    
    def load_video_clips(self, video_files: List[Path]):
        """Load video clips from file paths."""
        if not MOVIEPY_AVAILABLE:
            raise ImportError("MoviePy is required but not available")
            
        clips = []
        for video_file in video_files:
            try:
                clip = VideoFileClip(str(video_file))
                clips.append(clip)
                logger.info(f"Loaded {video_file.name}: {clip.duration:.2f}s")
            except Exception as e:
                logger.error(f"Error loading {video_file}: {e}")
                continue
        return clips
    
    def concatenate_videos(self, clips):
        """Concatenate video clips with smooth transitions."""
        if not MOVIEPY_AVAILABLE:
            raise ImportError("MoviePy is required but not available")
            
        if not clips:
            raise ValueError("No video clips to concatenate")
        
        # Add fade transitions between clips
        processed_clips = []
        for i, clip in enumerate(clips):
            if i == 0:
                # First clip: fade in at the beginning
                processed_clip = clip.with_effects([fadein(self.fade_duration)])
            elif i == len(clips) - 1:
                # Last clip: fade out at the end
                processed_clip = clip.with_effects([fadeout(self.fade_duration)])
            else:
                # Middle clips: no special effects for now
                processed_clip = clip
            
            processed_clips.append(processed_clip)
        
        # Concatenate all clips
        final_video = concatenate_videoclips(processed_clips, method="compose")
        logger.info(f"Concatenated video duration: {final_video.duration:.2f}s")
        return final_video
    
    def extend_video_to_match_audio(self, video, audio_duration: float):
        """Extend video by repeating scenes with transitions to match audio duration."""
        if not MOVIEPY_AVAILABLE:
            raise ImportError("MoviePy is required but not available")
            
        video_duration = video.duration
        
        if video_duration >= audio_duration:
            logger.info("Video is already longer than or equal to audio duration")
            return video.subclipped(0, audio_duration)
        
        logger.info(f"Extending video from {video_duration:.2f}s to {audio_duration:.2f}s")
        
        # Calculate how much additional content we need
        additional_duration_needed = audio_duration - video_duration
        
        # Create extension by repeating parts of the original video
        extension_clips = []
        current_extension_duration = 0
        
        # We'll repeat the video in segments with cross-fade transitions
        segment_duration = min(video_duration, 10.0)  # Use 10-second segments or full video if shorter
        
        while current_extension_duration < additional_duration_needed:
            # Calculate remaining time needed
            remaining_time = additional_duration_needed - current_extension_duration
            clip_duration = min(segment_duration, remaining_time)
            
            # Create a segment from a random part of the original video
            start_time = (len(extension_clips) * 3) % max(1, video_duration - clip_duration)
            segment = video.subclipped(start_time, min(start_time + clip_duration, video_duration))
            
            # Add cross-fade effect for smooth transitions
            if extension_clips:
                segment = segment.with_effects([crossfadein(self.fade_duration)])
            
            extension_clips.append(segment)
            current_extension_duration += segment.duration
        
        # Combine original video with extensions
        if extension_clips:
            # Add cross-fade to the first extension clip
            extension_clips[0] = extension_clips[0].with_effects([crossfadein(self.fade_duration)])
            all_clips = [video] + extension_clips
            extended_video = concatenate_videoclips(all_clips, method="compose")
        else:
            extended_video = video
        
        # Trim to exact audio duration
        final_video = extended_video.subclipped(0, audio_duration)
        logger.info(f"Final video duration: {final_video.duration:.2f}s")
        return final_video
    
    def process_video(self) -> None:
        """Main processing function to create the final video with audio."""
        try:
            # Step 1: Find and load video files
            video_files = self.find_video_files()
            if not video_files:
                raise ValueError(f"No .mp4 files found in {self.video_dir}")
            
            clips = self.load_video_clips(video_files)
            if not clips:
                raise ValueError("No valid video clips could be loaded")
            
            # Step 2: Concatenate videos
            concatenated_video = self.concatenate_videos(clips)
            
            # Step 3: Load audio
            if not self.audio_file.exists():
                raise FileNotFoundError(f"Audio file not found: {self.audio_file}")
            
            audio = AudioFileClip(str(self.audio_file))
            logger.info(f"Audio duration: {audio.duration:.2f}s")
            
            # Step 4: Extend video if necessary
            final_video = self.extend_video_to_match_audio(concatenated_video, audio.duration)
            
            # Step 5: Add audio to video
            final_video_with_audio = final_video.with_audio(audio)
            
            # Step 6: Export final video
            logger.info(f"Exporting final video to: {self.output_file}")
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            
            final_video_with_audio.write_videofile(
                str(self.output_file),
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger=None  # Disable progress bar for cleaner output
            )
            
            logger.info("Video processing completed successfully!")
            
            # Clean up
            for clip in clips:
                clip.close()
            concatenated_video.close()
            final_video.close()
            final_video_with_audio.close()
            audio.close()
            
        except Exception as e:
            logger.error(f"Error during video processing: {e}")
            raise


def main():
    """Main function to run the video processing."""
    # Check if MoviePy is available
    if not MOVIEPY_AVAILABLE:
        print("\n❌ Error: MoviePy is required but not installed.")
        print("Please install it using one of these commands:")
        print("  pip install moviepy")
        print("  pip install -r requirements.txt")
        return
    
    # Configuration
    video_directory = "movie-reels/movie_2"
    audio_file = "movie-reels/movie_2/audio.m4a"
    output_file = "movie-reels/output/final_video.mp4"
    
    # Get absolute paths
    script_dir = Path(__file__).parent
    video_dir = script_dir / video_directory
    audio_path = script_dir / audio_file
    output_path = script_dir / output_file
    
    logger.info("Starting video concatenation and audio synchronization process...")
    logger.info(f"Video directory: {video_dir}")
    logger.info(f"Audio file: {audio_path}")
    logger.info(f"Output file: {output_path}")
    
    # Create processor and run
    processor = VideoProcessor(video_dir, audio_path, output_path)
    processor.process_video()
    
    print(f"\n✅ Success! Final video saved to: {output_path}")
    print(f"📁 Check the output in: {output_path.parent}")


if __name__ == "__main__":
    main()
