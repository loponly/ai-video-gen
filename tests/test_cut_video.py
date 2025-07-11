"""
Unit tests for the advanced video cutting tool.

Tests cover all cutting modes, error handling, and edge cases.
"""

import os
import json
import tempfile
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Import the modules to test
from tools.video.cut_video import (
    cut_video,
    cut_video_by_scenes,
    VideoCutter,
    CutSegment,
    CutConfig,
    CutMode,
    VideoQuality
)


class TestCutSegment:
    """Test CutSegment dataclass."""
    
    def test_cut_segment_creation(self):
        """Test CutSegment creation with default values."""
        segment = CutSegment(start=10.0, end=20.0)
        assert segment.start == 10.0
        assert segment.end == 20.0
        assert segment.mode == CutMode.TIME
        assert segment.label is None
    
    def test_cut_segment_with_custom_values(self):
        """Test CutSegment creation with custom values."""
        segment = CutSegment(
            start=100,
            end=200,
            mode=CutMode.FRAME,
            label="test_segment"
        )
        assert segment.start == 100
        assert segment.end == 200
        assert segment.mode == CutMode.FRAME
        assert segment.label == "test_segment"


class TestCutConfig:
    """Test CutConfig dataclass."""
    
    def test_cut_config_defaults(self):
        """Test CutConfig with default values."""
        config = CutConfig()
        assert config.quality == VideoQuality.ORIGINAL
        assert config.codec == "libx264"
        assert config.audio_codec == "aac"
        assert config.preserve_audio is True
        assert config.remove_temp_files is True
        assert config.fps is None
    
    def test_cut_config_custom_values(self):
        """Test CutConfig with custom values."""
        config = CutConfig(
            quality=VideoQuality.HIGH,
            codec="h264",
            fps=30
        )
        assert config.quality == VideoQuality.HIGH
        assert config.codec == "h264"
        assert config.fps == 30


class TestVideoCutter:
    """Test VideoCutter class."""
    
    @pytest.fixture
    def mock_video_clip(self):
        """Create a mock VideoFileClip for testing."""
        mock_clip = Mock()
        mock_clip.duration = 60.0
        mock_clip.fps = 30.0
        mock_clip.size = (1920, 1080)
        mock_clip.subclip.return_value = Mock()
        mock_clip.close.return_value = None
        return mock_clip
    
    @pytest.fixture
    def video_cutter(self):
        """Create a VideoCutter instance for testing."""
        return VideoCutter()
    
    def test_video_cutter_initialization(self):
        """Test VideoCutter initialization."""
        cutter = VideoCutter()
        assert cutter.config.quality == VideoQuality.ORIGINAL
        assert cutter.logger is not None
    
    def test_video_cutter_with_config(self):
        """Test VideoCutter initialization with custom config."""
        config = CutConfig(quality=VideoQuality.HIGH)
        cutter = VideoCutter(config)
        assert cutter.config.quality == VideoQuality.HIGH
    
    def test_get_video_info(self, video_cutter, mock_video_clip):
        """Test _get_video_info method."""
        info = video_cutter._get_video_info(mock_video_clip)
        assert info["duration"] == 60.0
        assert info["fps"] == 30.0
        assert info["size"] == (1920, 1080)
        assert info["total_frames"] == 1800  # 60 * 30
    
    def test_convert_segment_to_time_mode(self, video_cutter):
        """Test _convert_segment_to_time with TIME mode."""
        segment = CutSegment(start=10.0, end=20.0, mode=CutMode.TIME)
        video_info = {"duration": 60.0, "fps": 30.0}
        
        start_time, end_time = video_cutter._convert_segment_to_time(segment, video_info)
        assert start_time == 10.0
        assert end_time == 20.0
    
    def test_convert_segment_to_frame_mode(self, video_cutter):
        """Test _convert_segment_to_time with FRAME mode."""
        segment = CutSegment(start=300, end=600, mode=CutMode.FRAME)
        video_info = {"duration": 60.0, "fps": 30.0}
        
        start_time, end_time = video_cutter._convert_segment_to_time(segment, video_info)
        assert start_time == 10.0  # 300 / 30
        assert end_time == 20.0    # 600 / 30
    
    def test_convert_segment_to_percentage_mode(self, video_cutter):
        """Test _convert_segment_to_time with PERCENTAGE mode."""
        segment = CutSegment(start=25, end=50, mode=CutMode.PERCENTAGE)
        video_info = {"duration": 60.0, "fps": 30.0}
        
        start_time, end_time = video_cutter._convert_segment_to_time(segment, video_info)
        assert start_time == 15.0  # 25% of 60
        assert end_time == 30.0    # 50% of 60
    
    def test_convert_segment_invalid_mode(self, video_cutter):
        """Test _convert_segment_to_time with invalid mode."""
        segment = CutSegment(start=10, end=20, mode="invalid")
        video_info = {"duration": 60.0, "fps": 30.0}
        
        with pytest.raises(ValueError, match="Unsupported cut mode"):
            video_cutter._convert_segment_to_time(segment, video_info)
    
    def test_validate_inputs_missing_file(self, video_cutter):
        """Test _validate_inputs with missing video file."""
        segments = [CutSegment(start=0, end=10)]
        result = video_cutter._validate_inputs(
            "/nonexistent/file.mp4", "/output/path.mp4", segments
        )
        assert result["status"] == "error"
        assert "not found" in result["message"]
    
    def test_validate_inputs_no_segments(self, video_cutter):
        """Test _validate_inputs with no segments."""
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = video_cutter._validate_inputs(tmp_path, "/output/path.mp4", [])
            assert result["status"] == "error"
            assert "No segments provided" in result["message"]
        finally:
            os.unlink(tmp_path)
    
    def test_generate_segment_output_path(self, video_cutter):
        """Test _generate_segment_output_path method."""
        base_path = "/output/video.mp4"
        
        # Test with label
        path_with_label = video_cutter._generate_segment_output_path(
            base_path, 0, "intro"
        )
        assert path_with_label == "/output/video_intro.mp4"
        
        # Test without label
        path_without_label = video_cutter._generate_segment_output_path(
            base_path, 1, None
        )
        assert path_without_label == "/output/video_segment_001.mp4"
    
    @patch('tools.video.cut_video.VideoFileClip')
    @patch('tools.video.cut_video.os.makedirs')
    def test_cut_video_success(self, mock_makedirs, mock_video_class, video_cutter):
        """Test successful video cutting."""
        # Setup mocks
        mock_video = Mock()
        mock_video.duration = 60.0
        mock_video.fps = 30.0
        mock_video.size = (1920, 1080)
        mock_video.close.return_value = None
        
        mock_clip = Mock()
        mock_clip.close.return_value = None
        mock_clip.write_videofile.return_value = None
        mock_video.subclip.return_value = mock_clip
        
        mock_video_class.return_value = mock_video
        
        # Create test segments
        segments = [CutSegment(start=10, end=20, label="test")]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = os.path.join(tmpdir, "input.mp4")
            output_path = os.path.join(tmpdir, "output.mp4")
            
            # Create dummy input file
            Path(video_path).touch()
            
            result = video_cutter.cut_video(
                video_path=video_path,
                output_path=output_path,
                segments=segments,
                merge_segments=False
            )
            
            assert result["status"] == "success"
            assert result["segments_count"] == 1
            assert result["original_duration"] == 60.0


class TestCutVideoFunction:
    """Test the main cut_video function."""
    
    @patch('tools.video.cut_video.VideoCutter')
    def test_cut_video_time_mode(self, mock_cutter_class):
        """Test cut_video function with time mode."""
        # Setup mock
        mock_cutter = Mock()
        mock_cutter.cut_video.return_value = {
            "status": "success",
            "message": "Video cut successfully",
            "output_paths": ["/output/segment_001.mp4"],
            "segments_count": 1
        }
        mock_cutter_class.return_value = mock_cutter
        
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = cut_video(
                video_path=tmp_path,
                output_path="/output/video.mp4",
                cuts="[[10, 20]]",
                cut_mode="time"
            )
            
            assert result["status"] == "success"
            mock_cutter.cut_video.assert_called_once()
        finally:
            os.unlink(tmp_path)
    
    def test_cut_video_invalid_mode(self):
        """Test cut_video function with invalid mode."""
        result = cut_video(
            video_path="/dummy/path.mp4",
            output_path="/output/video.mp4",
            cuts="[[10, 20]]",
            cut_mode="invalid"
        )
        
        assert result["status"] == "error"
        assert "Invalid cut mode" in result["message"]
    
    def test_cut_video_invalid_quality(self):
        """Test cut_video function with invalid quality."""
        result = cut_video(
            video_path="/dummy/path.mp4",
            output_path="/output/video.mp4",
            cuts="[[10, 20]]",
            quality="invalid"
        )
        
        assert result["status"] == "error"
        assert "Invalid quality" in result["message"]
    
    def test_cut_video_invalid_json(self):
        """Test cut_video function with invalid JSON cuts."""
        result = cut_video(
            video_path="/dummy/path.mp4",
            output_path="/output/video.mp4",
            cuts="invalid json"
        )
        
        assert result["status"] == "error"
        assert "Invalid cuts JSON format" in result["message"]
    
    @patch('tools.video.cut_video.VideoCutter')
    def test_cut_video_frame_mode(self, mock_cutter_class):
        """Test cut_video function with frame mode."""
        mock_cutter = Mock()
        mock_cutter.cut_video.return_value = {"status": "success"}
        mock_cutter_class.return_value = mock_cutter
        
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = cut_video(
                video_path=tmp_path,
                output_path="/output/video.mp4",
                cuts="[[300, 600]]",
                cut_mode="frame"
            )
            
            # Verify segments were created with correct mode
            call_args = mock_cutter.cut_video.call_args
            segments = call_args[1]["segments"]
            assert segments[0].mode == CutMode.FRAME
        finally:
            os.unlink(tmp_path)
    
    @patch('tools.video.cut_video.VideoCutter')
    def test_cut_video_percentage_mode(self, mock_cutter_class):
        """Test cut_video function with percentage mode."""
        mock_cutter = Mock()
        mock_cutter.cut_video.return_value = {"status": "success"}
        mock_cutter_class.return_value = mock_cutter
        
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = cut_video(
                video_path=tmp_path,
                output_path="/output/video.mp4",
                cuts="[[25, 75]]",
                cut_mode="percentage"
            )
            
            # Verify segments were created with correct mode
            call_args = mock_cutter.cut_video.call_args
            segments = call_args[1]["segments"]
            assert segments[0].mode == CutMode.PERCENTAGE
        finally:
            os.unlink(tmp_path)


class TestCutVideoByScenes:
    """Test the scene-based cutting function."""
    
    @patch('tools.video.cut_video.VideoFileClip')
    @patch('tools.video.cut_video.VideoCutter')
    def test_cut_video_by_scenes_success(self, mock_cutter_class, mock_video_class):
        """Test successful scene-based cutting."""
        # Setup video mock
        mock_video = Mock()
        mock_video.duration = 30.0
        mock_video.close.return_value = None
        
        # Mock frame data to simulate scene changes
        frames = [
            [[100, 100, 100]] * 100,  # Frame 1
            [[150, 150, 150]] * 100,  # Frame 2 (scene change)
        ]
        mock_video.get_frame.side_effect = lambda t: frames[min(int(t), 1)]
        mock_video_class.return_value = mock_video
        
        # Setup cutter mock
        mock_cutter = Mock()
        mock_cutter.cut_video.return_value = {
            "status": "success",
            "output_paths": ["/output/scene_1.mp4", "/output/scene_2.mp4"],
            "segments_count": 2
        }
        mock_cutter_class.return_value = mock_cutter
        
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = cut_video_by_scenes(
                video_path=tmp_path,
                output_path="/output/video.mp4",
                scene_threshold=30.0
            )
            
            assert result["status"] == "success"
            assert "scenes_detected" in result
            assert "scene_boundaries" in result
        finally:
            os.unlink(tmp_path)
    
    @patch('tools.video.cut_video.VideoFileClip')
    def test_cut_video_by_scenes_error(self, mock_video_class):
        """Test scene-based cutting with error."""
        mock_video_class.side_effect = Exception("Video loading failed")
        
        result = cut_video_by_scenes(
            video_path="/dummy/path.mp4",
            output_path="/output/video.mp4"
        )
        
        assert result["status"] == "error"
        assert "Error in scene-based cutting" in result["message"]


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_cut_modes_enum(self):
        """Test CutMode enum values."""
        assert CutMode.TIME.value == "time"
        assert CutMode.FRAME.value == "frame"
        assert CutMode.PERCENTAGE.value == "percentage"
        assert CutMode.SCENE.value == "scene"
    
    def test_video_quality_enum(self):
        """Test VideoQuality enum values."""
        assert VideoQuality.HIGH.value == "high"
        assert VideoQuality.MEDIUM.value == "medium"
        assert VideoQuality.LOW.value == "low"
        assert VideoQuality.ORIGINAL.value == "original"
    
    @patch('tools.video.cut_video.VideoCutter')
    def test_cut_video_with_merge_segments(self, mock_cutter_class):
        """Test cut_video with merge_segments=True."""
        mock_cutter = Mock()
        mock_cutter.cut_video.return_value = {
            "status": "success",
            "output_path": "/output/merged.mp4",
            "duration": 20.0
        }
        mock_cutter_class.return_value = mock_cutter
        
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = cut_video(
                video_path=tmp_path,
                output_path="/output/video.mp4",
                cuts="[[10, 20], [30, 40]]",
                merge_segments=True
            )
            
            # Verify merge_segments was passed correctly
            call_args = mock_cutter.cut_video.call_args
            assert call_args[1]["merge_segments"] is True
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
