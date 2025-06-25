#!/usr/bin/env python3
"""
Simple script to run video concatenation with audio synchronization.
Usage: python run_video_concatenator.py
"""

import sys
import subprocess
from pathlib import Path

def check_and_install_dependencies():
    """Check if required packages are installed and install if needed."""
    try:
        import moviepy
        print("✅ MoviePy is already installed")
        return True
    except ImportError:
        print("📦 MoviePy not found. Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
            print("✅ MoviePy installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install MoviePy: {e}")
            print("Please install manually using: pip install moviepy")
            return False

def main():
    """Main function to check dependencies and run video concatenator."""
    print("🎬 Video Concatenator with Audio Synchronization")
    print("=" * 50)
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        return
    
    # Import and run the video concatenator
    try:
        from video_concatenator import VideoProcessor
        import logging
        
        # Configuration
        script_dir = Path(__file__).parent
        video_dir = script_dir / "movie-reels/movie_2"
        audio_file = script_dir / "movie-reels/movie_2/audio.m4a"
        output_file = script_dir / "movie-reels/output/final_video.mp4"
        
        print(f"\n📁 Processing videos from: {video_dir}")
        print(f"🎵 Using audio from: {audio_file}")
        print(f"💾 Output will be saved to: {output_file}")
        print("\nProcessing... This may take a few minutes.\n")
        
        # Set up logging to be less verbose for the user
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        
        # Create processor and run
        processor = VideoProcessor(video_dir, audio_file, output_file)
        processor.process_video()
        
        print(f"\n🎉 Success! Final video saved to: {output_file}")
        print(f"📂 You can find the output in: {output_file.parent}")
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        print("Please check the logs above for more details.")

if __name__ == "__main__":
    main()
