"""
Advanced video cutting tool with multiple cutting modes and precision options.

This tool provides comprehensive video cutting capabilities including:
- Time-based cutting
- Frame-based cutting
- Percentage-based cutting
- Scene detection cutting
- Batch operations
- Quality preservation
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
    import numpy as np
except ImportError as e:
    raise ImportError(
        f"Required dependencies not found: {e}. "
        "Please install moviepy and numpy: pip install moviepy numpy"
    )


class CutMode(Enum):
    """Enumeration of available cutting modes."""
    TIME = "time"
    FRAME = "frame"
    PERCENTAGE = "percentage"
    SCENE = "scene"


class VideoQuality(Enum):
    """Video quality presets for output."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    ORIGINAL = "original"


@dataclass
class CutSegment:
    """Represents a single cut segment."""
    start: Union[float, int]
    end: Union[float, int]
    mode: CutMode = CutMode.TIME
    label: Optional[str] = None


@dataclass
class CutConfig:
    """Configuration for video cutting operation."""
    quality: VideoQuality = VideoQuality.ORIGINAL
    codec: str = "libx264"
    audio_codec: str = "aac"
    preserve_audio: bool = True
    remove_temp_files: bool = True
    fps: Optional[int] = None


class VideoCutter:
    """
    Advanced video cutting tool with multiple cutting modes.
    
    This class provides comprehensive video cutting capabilities following
    SOLID principles and design patterns.
    """
    
    def __init__(self, config: Optional[CutConfig] = None):
        """
        Initialize the VideoCutter with optional configuration.
        
        Args:
            config: Configuration object for cutting operations
        """
        self.config = config or CutConfig()
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logger for the video cutter."""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def cut_video(
        self,
        video_path: str,
        output_path: str,
        segments: List[CutSegment],
        merge_segments: bool = False
    ) -> Dict[str, Any]:
        """
        Cut video according to specified segments.
        
        Args:
            video_path: Path to input video file
            output_path: Path for output video file(s)
            segments: List of CutSegment objects defining cuts
            merge_segments: Whether to merge all segments into one video
            
        Returns:
            Dictionary containing operation results
        """
        try:
            self.logger.info(f"Starting video cutting: {video_path}")
            
            # Validate inputs
            validation_result = self._validate_inputs(video_path, output_path, segments)
            if validation_result["status"] == "error":
                return validation_result
            
            # Load video
            video = VideoFileClip(video_path)
            video_info = self._get_video_info(video)
            
            # Process segments
            cut_clips = []
            output_paths = []
            
            for i, segment in enumerate(segments):
                clip_result = self._cut_single_segment(
                    video, segment, video_info, i, output_path, merge_segments
                )
                
                if clip_result["status"] == "error":
                    video.close()
                    return clip_result
                
                cut_clips.append(clip_result["clip"])
                if not merge_segments:
                    output_paths.append(clip_result["output_path"])
            
            # Handle output
            if merge_segments:
                merged_result = self._merge_segments(cut_clips, output_path)
                video.close()
                return merged_result
            else:
                # Clean up clips
                for clip in cut_clips:
                    clip.close()
                video.close()
                
                return {
                    "status": "success",
                    "message": f"Successfully cut video into {len(segments)} segments",
                    "output_paths": output_paths,
                    "segments_count": len(segments),
                    "original_duration": video_info["duration"]
                }
                
        except Exception as e:
            self.logger.error(f"Error cutting video: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to cut video: {str(e)}",
                "output_path": None
            }
    
    def _validate_inputs(
        self, 
        video_path: str, 
        output_path: str, 
        segments: List[CutSegment]
    ) -> Dict[str, Any]:
        """Validate input parameters."""
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        if not segments:
            return {
                "status": "error",
                "message": "No segments provided for cutting",
                "output_path": None
            }
        
        # Create output directory
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        return {"status": "success"}
    
    def _get_video_info(self, video: VideoFileClip) -> Dict[str, Any]:
        """Extract video information."""
        return {
            "duration": video.duration,
            "fps": video.fps,
            "size": video.size,
            "total_frames": int(video.fps * video.duration) if video.fps else 0
        }
    
    def _cut_single_segment(
        self,
        video: VideoFileClip,
        segment: CutSegment,
        video_info: Dict[str, Any],
        segment_index: int,
        base_output_path: str,
        merge_segments: bool
    ) -> Dict[str, Any]:
        """Cut a single segment from the video."""
        try:
            # Convert segment coordinates based on mode
            start_time, end_time = self._convert_segment_to_time(
                segment, video_info
            )
            
            # Validate segment bounds
            if start_time < 0:
                start_time = 0
            if end_time > video_info["duration"]:
                end_time = video_info["duration"]
            
            if start_time >= end_time:
                return {
                    "status": "error",
                    "message": f"Invalid segment: start ({start_time}) >= end ({end_time})"
                }
            
            # Create clip
            clip = video.subclip(start_time, end_time)
            
            # Generate output path for individual segments
            if not merge_segments:
                output_path = self._generate_segment_output_path(
                    base_output_path, segment_index, segment.label
                )
                
                # Write individual segment
                self._write_video_clip(clip, output_path)
                
                return {
                    "status": "success",
                    "clip": clip,
                    "output_path": output_path,
                    "start_time": start_time,
                    "end_time": end_time
                }
            else:
                return {
                    "status": "success",
                    "clip": clip,
                    "start_time": start_time,
                    "end_time": end_time
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error cutting segment {segment_index}: {str(e)}"
            }
    
    def _convert_segment_to_time(
        self, 
        segment: CutSegment, 
        video_info: Dict[str, Any]
    ) -> Tuple[float, float]:
        """Convert segment coordinates to time based on the mode."""
        if segment.mode == CutMode.TIME:
            return float(segment.start), float(segment.end)
        
        elif segment.mode == CutMode.FRAME:
            fps = video_info["fps"]
            if not fps:
                raise ValueError("Cannot use frame mode: video FPS not available")
            return segment.start / fps, segment.end / fps
        
        elif segment.mode == CutMode.PERCENTAGE:
            duration = video_info["duration"]
            return (
                (segment.start / 100.0) * duration,
                (segment.end / 100.0) * duration
            )
        
        else:
            raise ValueError(f"Unsupported cut mode: {segment.mode}")
    
    def _generate_segment_output_path(
        self, 
        base_path: str, 
        index: int, 
        label: Optional[str]
    ) -> str:
        """Generate output path for individual segment."""
        path_obj = Path(base_path)
        stem = path_obj.stem
        suffix = path_obj.suffix
        parent = path_obj.parent
        
        if label:
            filename = f"{stem}_{label}{suffix}"
        else:
            filename = f"{stem}_segment_{index:03d}{suffix}"
        
        return str(parent / filename)
    
    def _write_video_clip(self, clip: VideoFileClip, output_path: str) -> None:
        """Write video clip to file with configured quality settings."""
        write_params = {
            "codec": self.config.codec,
            "audio_codec": self.config.audio_codec if self.config.preserve_audio else None,
            "temp_audiofile": "temp-audio.m4a",
            "remove_temp": self.config.remove_temp_files
        }
        
        # Add FPS if specified
        if self.config.fps:
            write_params["fps"] = self.config.fps
        
        # Quality-specific settings
        if self.config.quality == VideoQuality.HIGH:
            write_params.update({"bitrate": "8000k", "audio_bitrate": "320k"})
        elif self.config.quality == VideoQuality.MEDIUM:
            write_params.update({"bitrate": "4000k", "audio_bitrate": "192k"})
        elif self.config.quality == VideoQuality.LOW:
            write_params.update({"bitrate": "1000k", "audio_bitrate": "128k"})
        
        clip.write_videofile(output_path, **write_params)
    
    def _merge_segments(
        self, 
        clips: List[VideoFileClip], 
        output_path: str
    ) -> Dict[str, Any]:
        """Merge multiple clips into a single video."""
        try:
            if not clips:
                return {
                    "status": "error",
                    "message": "No clips to merge",
                    "output_path": None
                }
            
            # Concatenate clips
            final_video = concatenate_videoclips(clips)
            
            # Write merged video
            self._write_video_clip(final_video, output_path)
            
            duration = float(final_video.duration)
            
            # Clean up
            for clip in clips:
                clip.close()
            final_video.close()
            
            return {
                "status": "success",
                "message": f"Successfully merged {len(clips)} segments",
                "output_path": output_path,
                "duration": duration,
                "segments_count": len(clips)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error merging segments: {str(e)}",
                "output_path": None
            }


def cut_video(
    video_path: str,
    output_path: str,
    cuts: str,
    cut_mode: str = "time",
    merge_segments: bool = False,
    quality: str = "original",
    preserve_audio: bool = True
) -> Dict[str, Any]:
    """
    Cut video using advanced cutting tool with multiple modes.
    
    This is the main interface function that provides comprehensive video cutting
    capabilities with multiple cutting modes and quality options.
    
    Args:
        video_path: Absolute path to the input video file
        output_path: Absolute path for output video file(s)
        cuts: JSON string defining cut segments. Format depends on cut_mode:
              - time: "[[0,10],[20,30]]" (seconds)
              - frame: "[[0,300],[600,900]]" (frame numbers)
              - percentage: "[[0,25],[50,75]]" (percentages)
        cut_mode: Cutting mode - "time", "frame", "percentage"
        merge_segments: Whether to merge all segments into one output file
        quality: Output quality - "original", "high", "medium", "low"
        preserve_audio: Whether to preserve audio tracks
    
    Returns:
        Dictionary containing operation results:
        - status: 'success' or 'error'
        - message: Descriptive message
        - output_path(s): Path(s) to created video file(s)
        - segments_count: Number of segments created
        - original_duration: Duration of original video
        
        Example success (individual segments):
        {
            'status': 'success',
            'message': 'Successfully cut video into 2 segments',
            'output_paths': ['/path/to/video_segment_001.mp4', '/path/to/video_segment_002.mp4'],
            'segments_count': 2,
            'original_duration': 120.5
        }
        
        Example success (merged):
        {
            'status': 'success', 
            'message': 'Successfully merged 2 segments',
            'output_path': '/path/to/merged_video.mp4',
            'duration': 20.0,
            'segments_count': 2
        }
    """
    try:
        # Parse cut mode
        try:
            mode = CutMode(cut_mode.lower())
        except ValueError:
            return {
                "status": "error",
                "message": f"Invalid cut mode: {cut_mode}. Use 'time', 'frame', or 'percentage'",
                "output_path": None
            }
        
        # Parse quality
        try:
            quality_enum = VideoQuality(quality.lower())
        except ValueError:
            return {
                "status": "error",
                "message": f"Invalid quality: {quality}. Use 'original', 'high', 'medium', or 'low'",
                "output_path": None
            }
        
        # Parse cuts
        try:
            cuts_list = json.loads(cuts)
            if not isinstance(cuts_list, list):
                raise ValueError("Cuts must be a list of [start, end] pairs")
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"Invalid cuts JSON format: {str(e)}",
                "output_path": None
            }
        
        # Create cut segments
        segments = []
        for i, (start, end) in enumerate(cuts_list):
            segments.append(CutSegment(
                start=start,
                end=end,
                mode=mode,
                label=f"seg_{i+1}"
            ))
        
        # Create configuration
        config = CutConfig(
            quality=quality_enum,
            preserve_audio=preserve_audio
        )
        
        # Create cutter and perform cutting
        cutter = VideoCutter(config)
        result = cutter.cut_video(
            video_path=video_path,
            output_path=output_path,
            segments=segments,
            merge_segments=merge_segments
        )
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error in cut_video: {str(e)}",
            "output_path": None
        }


def cut_video_by_scenes(
    video_path: str,
    output_path: str,
    scene_threshold: float = 30.0,
    min_scene_length: float = 1.0,
    max_scenes: Optional[int] = None
) -> Dict[str, Any]:
    """
    Cut video automatically based on scene detection.
    
    This function analyzes the video to detect scene changes and cuts
    the video at those points, creating separate clips for each scene.
    
    Args:
        video_path: Absolute path to input video file
        output_path: Base path for output files
        scene_threshold: Threshold for scene change detection (0-100)
        min_scene_length: Minimum length for a scene in seconds
        max_scenes: Maximum number of scenes to extract (None for all)
    
    Returns:
        Dictionary with cutting results including detected scenes
    """
    try:
        # Load video
        video = VideoFileClip(video_path)
        duration = video.duration
        
        # Simple scene detection based on frame differences
        # This is a basic implementation - in production, you might want
        # to use more sophisticated scene detection algorithms
        scenes = []
        current_time = 0.0
        sample_interval = 1.0  # Sample every second
        
        prev_frame = None
        scene_start = 0.0
        
        while current_time < duration:
            try:
                frame = video.get_frame(current_time)
                
                if prev_frame is not None:
                    # Calculate frame difference (simplified)
                    diff = np.mean(np.abs(frame.astype(float) - prev_frame.astype(float)))
                    
                    # If difference exceeds threshold, mark as scene boundary
                    if diff > scene_threshold and (current_time - scene_start) >= min_scene_length:
                        scenes.append((scene_start, current_time))
                        scene_start = current_time
                
                prev_frame = frame
                current_time += sample_interval
                
            except Exception:
                # Skip problematic frames
                current_time += sample_interval
                continue
        
        # Add final scene
        if scene_start < duration:
            scenes.append((scene_start, duration))
        
        # Limit number of scenes if specified
        if max_scenes and len(scenes) > max_scenes:
            scenes = scenes[:max_scenes]
        
        video.close()
        
        # Convert to cut segments
        segments = [
            CutSegment(start=start, end=end, mode=CutMode.TIME, label=f"scene_{i+1}")
            for i, (start, end) in enumerate(scenes)
        ]
        
        # Perform cutting
        config = CutConfig(quality=VideoQuality.ORIGINAL)
        cutter = VideoCutter(config)
        
        result = cutter.cut_video(
            video_path=video_path,
            output_path=output_path,
            segments=segments,
            merge_segments=False
        )
        
        if result["status"] == "success":
            result["scenes_detected"] = len(scenes)
            result["scene_boundaries"] = scenes
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error in scene-based cutting: {str(e)}",
            "output_path": None
        }
