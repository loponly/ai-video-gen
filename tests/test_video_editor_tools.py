#!/usr/bin/env python3
"""
Test Video Editor Tools
======================

Individual tests for each video editing tool to ensure they work correctly.
Run this script to test all video editing functions.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path so we can import our tools
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from tools.video import (
    concatenate_videos,
    synchronize_audio,
    clip_videos,
    edit_video_metadata,
    add_effects,
    export_video,
    add_subtitles
)


def test_clip_videos():
    """Test the clip_videos function with a real video file"""
    print("\n🎬 Testing clip_videos...")
    
    # Use an existing video file from the project
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_clipped.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Test video not found: {video_path}")
        return False
    
    # Test clipping first 5 seconds
    result = clip_videos(video_path, output_path, start_time=0, end_time=5)
    
    if result["status"] == "success":
        print(f"✅ Successfully clipped video: {result['message']}")
        print(f"   Output: {result['output_path']}")
        print(f"   Duration: {result['duration']:.2f}s")
        return True
    else:
        print(f"❌ Failed to clip video: {result['message']}")
        return False


def test_add_effects():
    """Test the add_effects function"""
    print("\n✨ Testing add_effects...")
    
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_effects.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Test video not found: {video_path}")
        return False
    
    effects = [
        {"type": "fade_in", "duration": 1.0},
        {"type": "fade_out", "duration": 1.0},
        {"type": "resize", "width": 640, "height": 480}
    ]
    
    result = add_effects(video_path, output_path, effects)
    
    if result["status"] == "success":
        print(f"✅ Successfully added effects: {result['message']}")
        print(f"   Effects applied: {', '.join(result['effects_applied'])}")
        print(f"   Output: {result['output_path']}")
        return True
    else:
        print(f"❌ Failed to add effects: {result['message']}")
        return False


def test_export_video():
    """Test the export_video function"""
    print("\n📦 Testing export_video...")
    
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_export.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Test video not found: {video_path}")
        return False
    
    format_settings = {
        "codec": "libx264",
        "audio_codec": "aac",
        "bitrate": "1000k",
        "resolution": (720, 480)
    }
    
    result = export_video(video_path, output_path, format_settings)
    
    if result["status"] == "success":
        print(f"✅ Successfully exported video: {result['message']}")
        print(f"   File size: {result['file_size'] / (1024*1024):.2f} MB")
        print(f"   Output: {result['output_path']}")
        return True
    else:
        print(f"❌ Failed to export video: {result['message']}")
        return False


def test_concatenate_videos():
    """Test the concatenate_videos function"""
    print("\n🔗 Testing concatenate_videos...")
    
    # Check if we have at least 2 video files to concatenate
    video_dir = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2"
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    
    if len(video_files) < 2:
        print(f"❌ Need at least 2 video files in {video_dir}")
        return False
    
    test_videos = [
        os.path.join(video_dir, video_files[0]),
        os.path.join(video_dir, video_files[1])
    ]
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_concatenated.mp4"
    
    result = concatenate_videos(test_videos, output_path)
    
    if result["status"] == "success":
        print(f"✅ Successfully concatenated videos: {result['message']}")
        print(f"   Duration: {result['duration']:.2f}s")
        print(f"   Output: {result['output_path']}")
        return True
    else:
        print(f"❌ Failed to concatenate videos: {result['message']}")
        return False


def test_synchronize_audio():
    """Test the synchronize_audio function"""
    print("\n🔊 Testing synchronize_audio...")
    
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    audio_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/audio.m4a"
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_sync_audio.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Test video not found: {video_path}")
        return False
    
    if not os.path.exists(audio_path):
        print(f"❌ Test audio not found: {audio_path}")
        return False
    
    result = synchronize_audio(video_path, audio_path, output_path)
    
    if result["status"] == "success":
        print(f"✅ Successfully synchronized audio: {result['message']}")
        print(f"   Duration: {result['duration']:.2f}s")
        print(f"   Output: {result['output_path']}")
        return True
    else:
        print(f"❌ Failed to synchronize audio: {result['message']}")
        return False


def test_edit_video_metadata():
    """Test the edit_video_metadata function"""
    print("\n📝 Testing edit_video_metadata...")
    
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_metadata.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Test video not found: {video_path}")
        return False
    
    metadata = {
        "title": "Test Video",
        "artist": "AI Video Generator",
        "description": "This is a test video with metadata",
        "date": "2025"
    }
    
    result = edit_video_metadata(video_path, output_path, metadata)
    
    if result["status"] == "success":
        print(f"✅ Successfully updated metadata: {result['message']}")
        print(f"   Metadata updated: {', '.join(result['metadata_updated'])}")
        print(f"   Output: {result['output_path']}")
        return True
    else:
        print(f"❌ Failed to update metadata: {result['message']}")
        return False


def test_add_subtitles():
    """Test the add_subtitles function"""
    print("\n📋 Testing add_subtitles...")
    
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    
    # Check for SRT files in the project
    srt_dir = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/srt_files"
    srt_files = [f for f in os.listdir(srt_dir) if f.endswith('.srt')]
    
    if not srt_files:
        print(f"❌ No SRT files found in {srt_dir}")
        return False
    
    subtitle_path = os.path.join(srt_dir, srt_files[0])
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_subtitles.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Test video not found: {video_path}")
        return False
    
    subtitle_options = {
        "font_size": 20,
        "font_color": "white"
    }
    
    result = add_subtitles(video_path, subtitle_path, output_path, subtitle_options)
    
    if result["status"] == "success":
        print(f"✅ Successfully added subtitles: {result['message']}")
        print(f"   Subtitle file: {result['subtitle_file']}")
        print(f"   Output: {result['output_path']}")
        return True
    else:
        print(f"❌ Failed to add subtitles: {result['message']}")
        return False


def main():
    """Run all tests"""
    print("🚀 Video Editor Tools - Test Suite")
    print("=" * 50)
    
    # Ensure output directory exists
    output_dir = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output"
    os.makedirs(output_dir, exist_ok=True)
    
    # List of test functions
    tests = [
        ("Clip Videos", test_clip_videos),
        ("Add Effects", test_add_effects),
        ("Export Video", test_export_video),
        ("Edit Metadata", test_edit_video_metadata),
        ("Concatenate Videos", test_concatenate_videos),
        ("Synchronize Audio", test_synchronize_audio),
        ("Add Subtitles", test_add_subtitles)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
        
        print("-" * 50)
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} tests failed")


if __name__ == "__main__":
    main()
