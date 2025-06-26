#!/usr/bin/env python3
"""
Test script to verify video files and audio before processing.
"""

import os
from pathlib import Path
import sys

def check_files():
    """Check if all required files exist."""
    script_dir = Path(__file__).parent
    video_dir = script_dir / "movie-reels/movie_2"
    audio_file = script_dir / "movie-reels/movie_2/audio.m4a"
    
    print("🔍 Checking files...")
    print("=" * 40)
    
    # Check video directory
    if not video_dir.exists():
        print(f"❌ Video directory not found: {video_dir}")
        return False
    
    # Find MP4 files
    mp4_files = list(video_dir.glob("*.mp4"))
    mp4_files.sort(key=lambda x: int(x.stem) if x.stem.isdigit() else 0)
    
    print(f"📁 Video directory: {video_dir}")
    print(f"🎬 Found {len(mp4_files)} MP4 files:")
    for i, file in enumerate(mp4_files, 1):
        file_size = file.stat().st_size / (1024 * 1024)  # MB
        print(f"   {i}. {file.name} ({file_size:.1f} MB)")
    
    # Check audio file
    print(f"\n🎵 Audio file: {audio_file}")
    if audio_file.exists():
        audio_size = audio_file.stat().st_size / (1024 * 1024)  # MB
        print(f"   ✅ Found: {audio_file.name} ({audio_size:.1f} MB)")
    else:
        print(f"   ❌ Not found: {audio_file}")
        return False
    
    # Check output directory
    output_dir = script_dir / "movie-reels/output"
    print(f"\n💾 Output directory: {output_dir}")
    if not output_dir.exists():
        print("   📁 Creating output directory...")
        output_dir.mkdir(parents=True, exist_ok=True)
        print("   ✅ Created successfully")
    else:
        print("   ✅ Already exists")
    
    if len(mp4_files) == 0:
        print("\n❌ No MP4 files found to process!")
        return False
    
    print(f"\n✅ All checks passed! Ready to process {len(mp4_files)} video files.")
    return True

def get_video_info():
    """Get basic information about video files using ffprobe if available."""
    try:
        import subprocess
        script_dir = Path(__file__).parent
        video_dir = script_dir / "movie-reels/movie_2"
        mp4_files = sorted(video_dir.glob("*.mp4"), key=lambda x: int(x.stem) if x.stem.isdigit() else 0)
        
        print("\n📊 Video Information (using ffprobe):")
        print("=" * 50)
        
        total_duration = 0
        for file in mp4_files:
            try:
                # Get video duration using ffprobe
                cmd = [
                    'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1', str(file)
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    duration = float(result.stdout.strip())
                    total_duration += duration
                    print(f"   {file.name}: {duration:.2f} seconds")
                else:
                    print(f"   {file.name}: Unable to get duration")
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
                print(f"   {file.name}: Unable to get duration (ffprobe error)")
        
        # Check audio duration
        audio_file = script_dir / "movie-reels/movie_2/audio.m4a"
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_file)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                audio_duration = float(result.stdout.strip())
                print(f"\n🎵 Audio duration: {audio_duration:.2f} seconds")
                print(f"🎬 Total video duration: {total_duration:.2f} seconds")
                
                if total_duration < audio_duration:
                    extension_needed = audio_duration - total_duration
                    print(f"⚠️  Video is {extension_needed:.2f} seconds shorter than audio")
                    print("   The script will extend the video to match the audio length.")
                elif total_duration > audio_duration:
                    print("✅ Video is longer than audio - will be trimmed to match")
                else:
                    print("✅ Video and audio durations match perfectly!")
        except:
            print("\n🎵 Audio duration: Unable to determine (ffprobe error)")
            
    except FileNotFoundError:
        print("\n📊 ffprobe not found - install ffmpeg for detailed video information")
    except Exception as e:
        print(f"\n📊 Error getting video information: {e}")

def main():
    """Main test function."""
    print("🧪 Video Concatenator - File Check")
    print("=" * 40)
    
    if check_files():
        get_video_info()
        print("\n🚀 Ready to run video concatenation!")
        print("Execute: python run_video_concatenator.py")
    else:
        print("\n❌ Please fix the issues above before running the concatenator.")
        sys.exit(1)

if __name__ == "__main__":
    main()
