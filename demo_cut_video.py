#!/usr/bin/env python3
"""
Demonstration script for the advanced video cutting tool.

This script shows how to use the new cut_video tool with different cutting modes
and features. It provides examples for all supported cutting modes.
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tools.video.cut_video import cut_video, cut_video_by_scenes


def demo_time_based_cutting():
    """Demonstrate time-based video cutting."""
    print("🎬 Time-based Video Cutting Demo")
    print("=" * 50)
    
    # Example: Cut video from 10-20 seconds and 30-40 seconds
    cuts = json.dumps([[10, 20], [30, 40]])
    
    # Create dummy paths for demonstration
    input_video = "/path/to/your/input_video.mp4"
    output_video = "/path/to/output/cut_video.mp4"
    
    print(f"Input: {input_video}")
    print(f"Cuts: {cuts} (time in seconds)")
    print(f"Output: {output_video}")
    print()
    
    # This would be the actual function call:
    # result = cut_video(
    #     video_path=input_video,
    #     output_path=output_video,
    #     cuts=cuts,
    #     cut_mode="time",
    #     merge_segments=False
    # )
    
    print("Expected result:")
    print("- video_segment_001.mp4 (10s clip from 10-20s)")
    print("- video_segment_002.mp4 (10s clip from 30-40s)")
    print()


def demo_frame_based_cutting():
    """Demonstrate frame-based video cutting."""
    print("🎞️ Frame-based Video Cutting Demo")
    print("=" * 50)
    
    # Example: Cut from frame 300-600 and 900-1200 (assuming 30fps)
    cuts = json.dumps([[300, 600], [900, 1200]])
    
    input_video = "/path/to/your/input_video.mp4"
    output_video = "/path/to/output/frame_cut_video.mp4"
    
    print(f"Input: {input_video}")
    print(f"Cuts: {cuts} (frame numbers)")
    print(f"Output: {output_video}")
    print()
    
    # This would be the actual function call:
    # result = cut_video(
    #     video_path=input_video,
    #     output_path=output_video,
    #     cuts=cuts,
    #     cut_mode="frame",
    #     merge_segments=False
    # )
    
    print("Expected result (assuming 30fps):")
    print("- video_segment_001.mp4 (10s clip from frames 300-600)")
    print("- video_segment_002.mp4 (10s clip from frames 900-1200)")
    print()


def demo_percentage_based_cutting():
    """Demonstrate percentage-based video cutting."""
    print("📊 Percentage-based Video Cutting Demo")
    print("=" * 50)
    
    # Example: Cut first 25% and middle 50% of video
    cuts = json.dumps([[0, 25], [25, 75]])
    
    input_video = "/path/to/your/input_video.mp4"
    output_video = "/path/to/output/percentage_cut_video.mp4"
    
    print(f"Input: {input_video}")
    print(f"Cuts: {cuts} (percentages)")
    print(f"Output: {output_video}")
    print()
    
    # This would be the actual function call:
    # result = cut_video(
    #     video_path=input_video,
    #     output_path=output_video,
    #     cuts=cuts,
    #     cut_mode="percentage",
    #     merge_segments=False
    # )
    
    print("Expected result (for 60s video):")
    print("- video_segment_001.mp4 (15s clip from 0-25%)")
    print("- video_segment_002.mp4 (30s clip from 25-75%)")
    print()


def demo_merged_cutting():
    """Demonstrate cutting with merged output."""
    print("🔗 Merged Video Cutting Demo")
    print("=" * 50)
    
    # Example: Cut multiple segments and merge them
    cuts = json.dumps([[10, 20], [40, 50], [70, 80]])
    
    input_video = "/path/to/your/input_video.mp4"
    output_video = "/path/to/output/merged_highlights.mp4"
    
    print(f"Input: {input_video}")
    print(f"Cuts: {cuts} (time in seconds)")
    print(f"Output: {output_video}")
    print("Merge segments: True")
    print()
    
    # This would be the actual function call:
    # result = cut_video(
    #     video_path=input_video,
    #     output_path=output_video,
    #     cuts=cuts,
    #     cut_mode="time",
    #     merge_segments=True
    # )
    
    print("Expected result:")
    print("- merged_highlights.mp4 (30s video with all segments combined)")
    print()


def demo_quality_settings():
    """Demonstrate different quality settings."""
    print("⚙️ Quality Settings Demo")
    print("=" * 50)
    
    cuts = json.dumps([[10, 30]])
    input_video = "/path/to/your/input_video.mp4"
    
    qualities = ["original", "high", "medium", "low"]
    
    for quality in qualities:
        output_video = f"/path/to/output/video_{quality}_quality.mp4"
        
        print(f"Quality: {quality}")
        print(f"Output: {output_video}")
        
        # This would be the actual function call:
        # result = cut_video(
        #     video_path=input_video,
        #     output_path=output_video,
        #     cuts=cuts,
        #     cut_mode="time",
        #     quality=quality
        # )
        
        print(f"- Optimized for {quality} quality")
        print()


def demo_scene_detection():
    """Demonstrate automatic scene detection cutting."""
    print("🎭 Scene Detection Cutting Demo")
    print("=" * 50)
    
    input_video = "/path/to/your/input_video.mp4"
    output_base = "/path/to/output/scene_"
    
    print(f"Input: {input_video}")
    print(f"Output base: {output_base}")
    print("Scene detection: Automatic")
    print()
    
    # This would be the actual function call:
    # result = cut_video_by_scenes(
    #     video_path=input_video,
    #     output_path=output_base + "auto.mp4",
    #     scene_threshold=30.0,
    #     min_scene_length=2.0,
    #     max_scenes=10
    # )
    
    print("Expected result:")
    print("- scene_auto_scene_1.mp4")
    print("- scene_auto_scene_2.mp4")
    print("- scene_auto_scene_3.mp4")
    print("- ... (up to 10 scenes)")
    print()


def demo_error_handling():
    """Demonstrate error handling examples."""
    print("❌ Error Handling Examples")
    print("=" * 50)
    
    print("1. Invalid cut mode:")
    result = cut_video(
        video_path="/dummy/path.mp4",
        output_path="/output/video.mp4",
        cuts="[[10, 20]]",
        cut_mode="invalid_mode"
    )
    print(f"Result: {result}")
    print()
    
    print("2. Invalid JSON cuts:")
    result = cut_video(
        video_path="/dummy/path.mp4",
        output_path="/output/video.mp4",
        cuts="invalid json",
        cut_mode="time"
    )
    print(f"Result: {result}")
    print()
    
    print("3. Invalid quality setting:")
    result = cut_video(
        video_path="/dummy/path.mp4",
        output_path="/output/video.mp4",
        cuts="[[10, 20]]",
        cut_mode="time",
        quality="invalid_quality"
    )
    print(f"Result: {result}")
    print()


def demo_practical_examples():
    """Show practical real-world examples."""
    print("🌟 Practical Examples")
    print("=" * 50)
    
    print("Example 1: Extract highlights from a sports video")
    print("- Cut key moments: goals, saves, etc.")
    cuts = json.dumps([[120, 135], [480, 495], [1200, 1220]])  # 15s clips
    print(f"Cuts: {cuts}")
    print("Use case: Create highlight reel")
    print()
    
    print("Example 2: Remove commercials from TV recording")
    print("- Keep content, skip ads")
    cuts = json.dumps([[0, 600], [720, 1320], [1440, 2040]])  # Skip 2min ads
    print(f"Cuts: {cuts}")
    print("Use case: Clean TV show recording")
    print()
    
    print("Example 3: Create intro/outro for YouTube video")
    print("- Extract first and last 30 seconds")
    cuts = json.dumps([[0, 30], [1770, 1800]])  # 30min video
    print(f"Cuts: {cuts}")
    print("Use case: Template creation")
    print()
    
    print("Example 4: Split long lecture into chapters")
    print("- 10-minute segments")
    cuts = json.dumps([[0, 600], [600, 1200], [1200, 1800], [1800, 2400]])
    print(f"Cuts: {cuts}")
    print("Use case: Educational content organization")
    print()


def main():
    """Run all demonstrations."""
    print("🎬 Advanced Video Cutting Tool - Demonstration")
    print("=" * 60)
    print("This demo shows various features of the new video cutting tool.")
    print()
    
    # Run all demos
    demo_time_based_cutting()
    demo_frame_based_cutting()
    demo_percentage_based_cutting()
    demo_merged_cutting()
    demo_quality_settings()
    demo_scene_detection()
    demo_error_handling()
    demo_practical_examples()
    
    print("🎉 Demo Complete!")
    print("=" * 60)
    print("To use the tool in your code:")
    print()
    print("from tools.video.cut_video import cut_video, cut_video_by_scenes")
    print()
    print("# Basic usage:")
    print('result = cut_video(')
    print('    video_path="/path/to/video.mp4",')
    print('    output_path="/path/to/output.mp4",')
    print('    cuts="[[10, 20], [30, 40]]",')
    print('    cut_mode="time"')
    print(')')
    print()
    print("For more examples, see the test file: tests/test_cut_video.py")


if __name__ == "__main__":
    main()
