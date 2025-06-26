#!/usr/bin/env python3
"""
Simple test to check basic MoviePy functionality
"""

import os

try:
    import moviepy as mp
    print("✅ MoviePy import successful")
    
    # Test basic functionality
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    
    if os.path.exists(video_path):
        print(f"✅ Test video found: {video_path}")
        
        # Try to load video
        video = mp.VideoFileClip(video_path)
        print(f"✅ Video loaded successfully")
        print(f"   Duration: {video.duration:.2f}s")
        print(f"   Resolution: {video.w}x{video.h}")
        print(f"   FPS: {video.fps}")
        
        video.close()
    else:
        print(f"❌ Test video not found: {video_path}")
        
except Exception as e:
    print(f"❌ Error: {e}")
