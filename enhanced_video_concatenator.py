#!/usr/bin/env python3
"""
Enhanced Video Concatenator with Configuration File Support

This script reads settings from video_config.ini and processes videos accordingly.
"""

import configparser
from pathlib import Path
import sys
import os

# Add the main script directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent))

def load_config(config_file="video_config.ini"):
    """Load configuration from INI file."""
    config = configparser.ConfigParser()
    config_path = Path(__file__).parent / config_file
    
    if not config_path.exists():
        print(f"⚠️  Configuration file not found: {config_path}")
        print("Using default settings...")
        return None
    
    config.read(config_path)
    print(f"📋 Loaded configuration from: {config_file}")
    return config

def main():
    """Main function with configuration support."""
    print("🎬 Enhanced Video Concatenator")
    print("=" * 40)
    
    # Load configuration
    config = load_config()
    
    # Set default values
    defaults = {
        'video_directory': 'movie-reels/movie_2',
        'audio_file': 'movie-reels/movie_2/audio.m4a',
        'output_file': 'movie-reels/output/final_video.mp4',
        'fade_duration': 0.5,
        'segment_duration': 10.0,
        'verbose_logging': False,
        'use_crossfade': True
    }
    
    # Get values from config or use defaults
    if config:
        try:
            video_directory = config.get('paths', 'video_directory', fallback=defaults['video_directory'])
            audio_file = config.get('paths', 'audio_file', fallback=defaults['audio_file'])
            output_file = config.get('paths', 'output_file', fallback=defaults['output_file'])
            fade_duration = config.getfloat('video_settings', 'fade_duration', fallback=defaults['fade_duration'])
            segment_duration = config.getfloat('video_settings', 'segment_duration', fallback=defaults['segment_duration'])
            verbose_logging = config.getboolean('processing', 'verbose_logging', fallback=defaults['verbose_logging'])
            use_crossfade = config.getboolean('processing', 'use_crossfade', fallback=defaults['use_crossfade'])
        except (configparser.Error, ValueError) as e:
            print(f"⚠️  Error reading configuration: {e}")
            print("Using default settings...")
            video_directory = defaults['video_directory']
            audio_file = defaults['audio_file']
            output_file = defaults['output_file']
            fade_duration = defaults['fade_duration']
            segment_duration = defaults['segment_duration']
            verbose_logging = defaults['verbose_logging']
            use_crossfade = defaults['use_crossfade']
    else:
        # Use all defaults
        video_directory = defaults['video_directory']
        audio_file = defaults['audio_file']
        output_file = defaults['output_file']
        fade_duration = defaults['fade_duration']
        segment_duration = defaults['segment_duration']
        verbose_logging = defaults['verbose_logging']
        use_crossfade = defaults['use_crossfade']
    
    # Print configuration
    print(f"📁 Video directory: {video_directory}")
    print(f"🎵 Audio file: {audio_file}")
    print(f"💾 Output file: {output_file}")
    print(f"⏱️  Fade duration: {fade_duration}s")
    print(f"📏 Segment duration: {segment_duration}s")
    print(f"🔊 Verbose logging: {verbose_logging}")
    print(f"🎭 Use crossfade: {use_crossfade}")
    
    # Check dependencies
    try:
        from video_concatenator import VideoProcessor, MOVIEPY_AVAILABLE
        if not MOVIEPY_AVAILABLE:
            print("\n❌ MoviePy is not available. Please install it:")
            print("   pip install moviepy")
            return
    except ImportError:
        print("\n❌ Could not import video_concatenator module.")
        print("Make sure video_concatenator.py is in the same directory.")
        return
    
    # Get absolute paths
    script_dir = Path(__file__).parent
    video_dir = script_dir / video_directory
    audio_path = script_dir / audio_file
    output_path = script_dir / output_file
    
    print(f"\n🚀 Starting video processing...")
    
    try:
        # Create custom processor with configuration
        processor = VideoProcessor(video_dir, audio_path, output_path)
        
        # Apply configuration settings
        processor.fade_duration = fade_duration
        # Note: segment_duration and other settings would need to be added to VideoProcessor class
        
        # Set up logging level
        import logging
        log_level = logging.DEBUG if verbose_logging else logging.INFO
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Process the video
        processor.process_video()
        
        print(f"\n🎉 Success! Final video saved to: {output_path}")
        print(f"📂 Output location: {output_path.parent}")
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        if verbose_logging:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
