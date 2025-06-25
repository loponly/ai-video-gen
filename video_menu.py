#!/usr/bin/env python3
"""
Video Concatenator - Main Entry Point

Choose from multiple ways to run the video concatenation:
1. Quick run with defaults
2. Enhanced run with configuration file
3. Test setup only
4. Custom parameters
"""

import sys
from pathlib import Path

def show_menu():
    """Display the main menu options."""
    print("🎬 Video Concatenator Suite")
    print("=" * 40)
    print("Choose an option:")
    print("1. Quick Run (default settings)")
    print("2. Enhanced Run (with config file)")
    print("3. Test Setup Only")
    print("4. Show File Information")
    print("5. Help")
    print("6. Exit")
    print("-" * 40)

def quick_run():
    """Run with default settings."""
    print("\n🚀 Running Quick Video Concatenation...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "run_video_concatenator.py"], cwd=Path(__file__).parent)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def enhanced_run():
    """Run with configuration file."""
    print("\n🚀 Running Enhanced Video Concatenation...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "enhanced_video_concatenator.py"], cwd=Path(__file__).parent)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_setup():
    """Run setup test."""
    print("\n🧪 Testing Setup...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_video_setup.py"], cwd=Path(__file__).parent)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_info():
    """Show file information."""
    script_dir = Path(__file__).parent
    video_dir = script_dir / "movie-reels/movie_2"
    
    print("\n📊 Current Setup Information")
    print("=" * 40)
    
    if video_dir.exists():
        mp4_files = list(video_dir.glob("*.mp4"))
        print(f"📁 Video directory: {video_dir}")
        print(f"🎬 MP4 files found: {len(mp4_files)}")
        for i, file in enumerate(sorted(mp4_files, key=lambda x: int(x.stem) if x.stem.isdigit() else 0), 1):
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"   {i}. {file.name} ({size_mb:.1f} MB)")
    else:
        print(f"❌ Video directory not found: {video_dir}")
    
    audio_file = video_dir / "audio.m4a"
    if audio_file.exists():
        size_mb = audio_file.stat().st_size / (1024 * 1024)
        print(f"\n🎵 Audio file: audio.m4a ({size_mb:.1f} MB)")
    else:
        print(f"\n❌ Audio file not found: {audio_file}")
    
    output_dir = script_dir / "movie-reels/output"
    print(f"\n💾 Output directory: {output_dir}")
    if output_dir.exists():
        existing_files = list(output_dir.glob("*.mp4"))
        if existing_files:
            print(f"   📼 Existing output files: {len(existing_files)}")
            for file in existing_files:
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"      - {file.name} ({size_mb:.1f} MB)")
        else:
            print("   📁 Directory exists but no output files yet")
    else:
        print("   📁 Will be created when needed")

def show_help():
    """Show help information."""
    print("\n📖 Help - Video Concatenator")
    print("=" * 40)
    print("This tool concatenates MP4 videos and synchronizes them with audio.")
    print()
    print("🎯 What it does:")
    print("  • Finds all .mp4 files in movie-reels/movie_2/")
    print("  • Concatenates them in numerical order (1.mp4, 2.mp4, etc.)")
    print("  • Adds audio from movie-reels/movie_2/audio.m4a")
    print("  • Extends video length to match audio if needed")
    print("  • Saves result to movie-reels/output/final_video.mp4")
    print()
    print("🛠️  Requirements:")
    print("  • Python 3.6+")
    print("  • MoviePy library (pip install moviepy)")
    print("  • FFmpeg (usually installed with MoviePy)")
    print()
    print("📁 File Structure:")
    print("  movie-reels/movie_2/")
    print("  ├── 1.mp4, 2.mp4, 3.mp4, etc.  # Video files")
    print("  └── audio.m4a                   # Audio track")
    print()
    print("⚙️  Configuration:")
    print("  • Edit video_config.ini for custom settings")
    print("  • Adjust fade duration, video quality, etc.")
    print()
    print("🚨 Troubleshooting:")
    print("  • Run option 3 (Test Setup) to check files")
    print("  • Ensure all video files are present")
    print("  • Check that audio.m4a exists")
    print("  • Verify MoviePy installation")

def main():
    """Main menu loop."""
    while True:
        show_menu()
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                success = quick_run()
                if success:
                    print("\n✅ Quick run completed successfully!")
                else:
                    print("\n❌ Quick run failed. Check the errors above.")
                    
            elif choice == "2":
                success = enhanced_run()
                if success:
                    print("\n✅ Enhanced run completed successfully!")
                else:
                    print("\n❌ Enhanced run failed. Check the errors above.")
                    
            elif choice == "3":
                test_setup()
                
            elif choice == "4":
                show_info()
                
            elif choice == "5":
                show_help()
                
            elif choice == "6":
                print("\n👋 Goodbye!")
                break
                
            else:
                print("\n❌ Invalid choice. Please enter 1-6.")
            
            if choice in ["1", "2", "3", "4", "5"]:
                input("\nPress Enter to continue...")
                print("\n" * 2)  # Clear screen space
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
