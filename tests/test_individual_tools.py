#!/usr/bin/env python3
"""
Individual Tool Tests for Video Editor
=====================================

Test each video editing tool separately to verify functionality
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from tools.video_editor_tools import (
    concatenate_videos,
    synchronize_audio,
    clip_videos,
    edit_video_metadata,
    add_effects,
    export_video,
    add_subtitles
)


def test_clip_videos():
    """Test video clipping"""
    print("\n🎬 Testing clip_videos tool...")
    
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_clipped.mp4"
    
    if not os.path.exists(video_path):
        print(f"❌ Test video not found: {video_path}")
        return False
    
    print(f"   Input: {video_path}")
    print(f"   Output: {output_path}")
    print("   Clipping first 5 seconds...")
    
    result = clip_videos(video_path, output_path, start_time=0, end_time=5)
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        print(f"   Duration: {result['duration']:.2f}s (original: {result['original_duration']:.2f}s)")
        return True
    else:
        print(f"❌ {result['message']}")
        return False


def test_add_effects():
    """Test adding effects to video"""
    print("\n✨ Testing add_effects tool...")
    
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
    
    print(f"   Input: {video_path}")
    print(f"   Output: {output_path}")
    print(f"   Effects: {[e['type'] for e in effects]}")
    
    result = add_effects(video_path, output_path, effects)
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        print(f"   Applied: {', '.join(result['effects_applied'])}")
        return True
    else:
        print(f"❌ {result['message']}")
        return False


def test_export_video():
    """Test video export with different settings"""
    print("\n📦 Testing export_video tool...")
    
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
    
    print(f"   Input: {video_path}")
    print(f"   Output: {output_path}")
    print(f"   Settings: {format_settings}")
    
    result = export_video(video_path, output_path, format_settings)
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        print(f"   File size: {result['file_size'] / (1024*1024):.2f} MB")
        return True
    else:
        print(f"❌ {result['message']}")
        return False


def test_concatenate_videos():
    """Test video concatenation"""
    print("\n🔗 Testing concatenate_videos tool...")
    
    video1 = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    video2 = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/2.mp4"
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_concatenated.mp4"
    
    videos = [video1, video2]
    
    print(f"   Inputs: {videos}")
    print(f"   Output: {output_path}")
    
    result = concatenate_videos(videos, output_path)
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        print(f"   Duration: {result['duration']:.2f}s")
        return True
    else:
        print(f"❌ {result['message']}")
        return False


def test_synchronize_audio():
    """Test audio synchronization"""
    print("\n🔊 Testing synchronize_audio tool...")
    
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    audio_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/audio.m4a"
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_sync_audio.mp4"
    
    if not os.path.exists(audio_path):
        print(f"❌ Test audio not found: {audio_path}")
        return False
    
    print(f"   Video: {video_path}")
    print(f"   Audio: {audio_path}")
    print(f"   Output: {output_path}")
    
    result = synchronize_audio(video_path, audio_path, output_path)
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        print(f"   Duration: {result['duration']:.2f}s")
        return True
    else:
        print(f"❌ {result['message']}")
        return False


def test_edit_metadata():
    """Test metadata editing"""
    print("\n📝 Testing edit_video_metadata tool...")
    
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_metadata.mp4"
    
    metadata = {
        "title": "Test Video",
        "artist": "AI Video Generator",
        "description": "Generated by video editor tools",
        "date": "2025"
    }
    
    print(f"   Input: {video_path}")
    print(f"   Output: {output_path}")
    print(f"   Metadata: {metadata}")
    
    result = edit_video_metadata(video_path, output_path, metadata)
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        print(f"   Updated: {', '.join(result['metadata_updated'])}")
        return True
    else:
        print(f"❌ {result['message']}")
        return False


def test_add_subtitles():
    """Test subtitle addition"""
    print("\n📋 Testing add_subtitles tool...")
    
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    
    # Find SRT files
    srt_dir = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/srt_files"
    srt_files = [f for f in os.listdir(srt_dir) if f.endswith('.srt')]
    
    if not srt_files:
        print(f"❌ No SRT files found in {srt_dir}")
        return False
    
    subtitle_path = os.path.join(srt_dir, srt_files[0])
    output_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output/test_subtitles.mp4"
    
    print(f"   Video: {video_path}")
    print(f"   Subtitles: {subtitle_path}")
    print(f"   Output: {output_path}")
    
    result = add_subtitles(video_path, subtitle_path, output_path)
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        return True
    else:
        print(f"❌ {result['message']}")
        return False


def main():
    """Run all tests"""
    print("🚀 Video Editor Tools - Individual Tests")
    print("=" * 50)
    
    # Ensure output directory exists
    output_dir = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Test functions to run
    tests = [
        ("Clip Videos", test_clip_videos),
        ("Add Effects", test_add_effects),
        ("Export Video", test_export_video),
        ("Edit Metadata", test_edit_metadata),
        ("Concatenate Videos", test_concatenate_videos),
        ("Synchronize Audio", test_synchronize_audio),
        ("Add Subtitles", test_add_subtitles),
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
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Video editor tools are working correctly.")
    else:
        print(f"⚠️  {total - passed} tests failed. Check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    main()
