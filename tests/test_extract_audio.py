"""
Test for extract_audio function from video_editor_tools.

Tests the audio extraction functionality with various formats and scenarios.
"""

import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.video import extract_audio


class TestExtractAudio:
    """Test class for extract_audio function."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.video_path = os.path.join(self.test_dir, "test_video.mp4")
        self.audio_output_path = os.path.join(self.test_dir, "extracted_audio.mp3")
        
    def teardown_method(self):
        """Clean up test fixtures after each test method."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_extract_audio_video_not_found(self):
        """Test extract_audio with non-existent video file."""
        result = extract_audio(
            video_path="/nonexistent/video.mp4",
            output_path=self.audio_output_path
        )
        
        assert result["status"] == "error"
        assert "Video file not found" in result["message"]
        assert result["output_path"] is None
    
    @patch('tools.video.extract_audio.VideoFileClip')
    def test_extract_audio_no_audio_track(self, mock_video_clip):
        """Test extract_audio with video that has no audio track."""
        # Create a temporary video file
        Path(self.video_path).touch()
        
        # Mock VideoFileClip to return a video with no audio
        mock_video = MagicMock()
        mock_video.audio = None
        mock_video_clip.return_value = mock_video
        
        result = extract_audio(
            video_path=self.video_path,
            output_path=self.audio_output_path
        )
        
        assert result["status"] == "error"
        assert "Video file has no audio track" in result["message"]
        assert result["output_path"] is None
        mock_video.close.assert_called_once()
    
    @patch('tools.video.extract_audio.VideoFileClip')
    @patch('os.path.getsize')
    def test_extract_audio_mp3_success(self, mock_getsize, mock_video_clip):
        """Test successful audio extraction to MP3 format."""
        # Create a temporary video file
        Path(self.video_path).touch()
        
        # Mock VideoFileClip and audio
        mock_audio = MagicMock()
        mock_audio.duration = 120.5
        mock_audio.fps = 44100
        mock_audio.write_audiofile = MagicMock()
        
        mock_video = MagicMock()
        mock_video.audio = mock_audio
        mock_video_clip.return_value = mock_video
        
        # Mock file size
        mock_getsize.return_value = 2048000
        
        result = extract_audio(
            video_path=self.video_path,
            output_path=self.audio_output_path,
            audio_format="mp3"
        )
        
        assert result["status"] == "success"
        assert "Successfully extracted audio in mp3 format" in result["message"]
        assert result["output_path"] == self.audio_output_path
        assert result["duration"] == 120.5
        assert result["sample_rate"] == 44100
        assert result["file_size"] == 2048000
        assert result["audio_format"] == "mp3"
        
        # Verify audio extraction was called with correct parameters
        mock_audio.write_audiofile.assert_called_once_with(
            self.audio_output_path, 
            codec='mp3'
        )
        mock_audio.close.assert_called_once()
        mock_video.close.assert_called_once()
    
    @patch('tools.video.extract_audio.VideoFileClip')
    @patch('os.path.getsize')
    def test_extract_audio_wav_format(self, mock_getsize, mock_video_clip):
        """Test audio extraction to WAV format."""
        # Create a temporary video file
        Path(self.video_path).touch()
        wav_output_path = os.path.join(self.test_dir, "extracted_audio.wav")
        
        # Mock VideoFileClip and audio
        mock_audio = MagicMock()
        mock_audio.duration = 60.0
        mock_audio.fps = 48000
        mock_audio.write_audiofile = MagicMock()
        
        mock_video = MagicMock()
        mock_video.audio = mock_audio
        mock_video_clip.return_value = mock_video
        
        # Mock file size
        mock_getsize.return_value = 5760000
        
        result = extract_audio(
            video_path=self.video_path,
            output_path=wav_output_path,
            audio_format="wav"
        )
        
        assert result["status"] == "success"
        assert result["audio_format"] == "wav"
        
        # Verify WAV codec was used
        mock_audio.write_audiofile.assert_called_once_with(
            wav_output_path, 
            codec='pcm_s16le'
        )
    
    @patch('tools.video.extract_audio.VideoFileClip')
    @patch('os.path.getsize')
    def test_extract_audio_format_inference(self, mock_getsize, mock_video_clip):
        """Test audio format inference from output file extension."""
        # Create a temporary video file
        Path(self.video_path).touch()
        flac_output_path = os.path.join(self.test_dir, "extracted_audio.flac")
        
        # Mock VideoFileClip and audio
        mock_audio = MagicMock()
        mock_audio.duration = 180.0
        mock_audio.fps = 44100
        mock_audio.write_audiofile = MagicMock()
        
        mock_video = MagicMock()
        mock_video.audio = mock_audio
        mock_video_clip.return_value = mock_video
        
        # Mock file size
        mock_getsize.return_value = 15360000
        
        # Don't specify audio_format, let it be inferred
        result = extract_audio(
            video_path=self.video_path,
            output_path=flac_output_path
        )
        
        assert result["status"] == "success"
        assert result["audio_format"] == "flac"
        
        # Verify FLAC codec was used
        mock_audio.write_audiofile.assert_called_once_with(
            flac_output_path, 
            codec='flac'
        )
    
    @patch('tools.video.extract_audio.VideoFileClip')
    @patch('os.path.getsize')
    def test_extract_audio_unknown_format_defaults_to_mp3(self, mock_getsize, mock_video_clip):
        """Test that unknown format defaults to MP3."""
        # Create a temporary video file
        Path(self.video_path).touch()
        unknown_output_path = os.path.join(self.test_dir, "extracted_audio.xyz")
        expected_mp3_path = os.path.join(self.test_dir, "extracted_audio.mp3")
        
        # Mock VideoFileClip and audio
        mock_audio = MagicMock()
        mock_audio.duration = 90.0
        mock_audio.fps = 22050
        mock_audio.write_audiofile = MagicMock()
        
        mock_video = MagicMock()
        mock_video.audio = mock_audio
        mock_video_clip.return_value = mock_video
        
        # Mock file size
        mock_getsize.return_value = 1024000
        
        result = extract_audio(
            video_path=self.video_path,
            output_path=unknown_output_path
        )
        
        assert result["status"] == "success"
        assert result["audio_format"] == "mp3"
        assert result["output_path"] == expected_mp3_path
        
        # Verify MP3 codec was used and path was corrected
        mock_audio.write_audiofile.assert_called_once_with(
            expected_mp3_path, 
            codec='mp3'
        )
    
    @patch('tools.video.extract_audio.VideoFileClip')
    def test_extract_audio_handles_none_sample_rate(self, mock_video_clip):
        """Test extraction when audio has no fps (sample rate)."""
        # Create a temporary video file
        Path(self.video_path).touch()
        
        # Mock VideoFileClip and audio with None fps
        mock_audio = MagicMock()
        mock_audio.duration = 45.0
        mock_audio.fps = None
        mock_audio.write_audiofile = MagicMock()
        
        mock_video = MagicMock()
        mock_video.audio = mock_audio
        mock_video_clip.return_value = mock_video
        
        with patch('os.path.getsize', return_value=512000):
            result = extract_audio(
                video_path=self.video_path,
                output_path=self.audio_output_path
            )
        
        assert result["status"] == "success"
        assert result["sample_rate"] is None
        assert result["duration"] == 45.0
    
    @patch('tools.video.extract_audio.VideoFileClip')
    def test_extract_audio_exception_handling(self, mock_video_clip):
        """Test exception handling during audio extraction."""
        # Create a temporary video file
        Path(self.video_path).touch()
        
        # Mock VideoFileClip to raise an exception
        mock_video_clip.side_effect = Exception("Codec error")
        
        result = extract_audio(
            video_path=self.video_path,
            output_path=self.audio_output_path
        )
        
        assert result["status"] == "error"
        assert "Error extracting audio" in result["message"]
        assert "Codec error" in result["message"]
        assert result["output_path"] is None
    
    @patch('tools.video.extract_audio.VideoFileClip')
    @patch('os.path.getsize')
    def test_extract_audio_aac_m4a_formats(self, mock_getsize, mock_video_clip):
        """Test audio extraction to AAC and M4A formats."""
        # Create a temporary video file
        Path(self.video_path).touch()
        
        # Mock VideoFileClip and audio
        mock_audio = MagicMock()
        mock_audio.duration = 75.0
        mock_audio.fps = 44100
        mock_audio.write_audiofile = MagicMock()
        
        mock_video = MagicMock()
        mock_video.audio = mock_audio
        mock_video_clip.return_value = mock_video
        
        # Mock file size
        mock_getsize.return_value = 1536000
        
        # Test AAC format
        aac_output_path = os.path.join(self.test_dir, "extracted_audio.aac")
        result = extract_audio(
            video_path=self.video_path,
            output_path=aac_output_path,
            audio_format="aac"
        )
        
        assert result["status"] == "success"
        assert result["audio_format"] == "aac"
        
        # Verify AAC codec was used
        mock_audio.write_audiofile.assert_called_with(
            aac_output_path, 
            codec='aac'
        )
        
        # Reset mock for M4A test
        mock_audio.write_audiofile.reset_mock()
        
        # Test M4A format
        m4a_output_path = os.path.join(self.test_dir, "extracted_audio.m4a")
        result = extract_audio(
            video_path=self.video_path,
            output_path=m4a_output_path,
            audio_format="m4a"
        )
        
        assert result["status"] == "success"
        assert result["audio_format"] == "m4a"
        
        # Verify AAC codec was used for M4A
        mock_audio.write_audiofile.assert_called_with(
            m4a_output_path, 
            codec='aac'
        )


def run_manual_test():
    """
    Manual test function to test with a real video file.
    Run this separately if you have a real video file to test with.
    """
    print("Manual Test for extract_audio function")
    print("=" * 40)
    
    # Use a real video file path for manual testing
    test_video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    test_output_dir = "/Users/enkhbat_1/projects/ai-video-ge/tests/test_outputs"
    
    # Create test output directory
    os.makedirs(test_output_dir, exist_ok=True)
    
    if os.path.exists(test_video_path):
        print(f"✅ Test video found: {test_video_path}")
        
        # Test different audio formats
        formats_to_test = [
            ("mp3", "extracted_test.mp3"),
            ("wav", "extracted_test.wav"),
            ("aac", "extracted_test.aac"),
            ("flac", "extracted_test.flac"),
            ("ogg", "extracted_test.ogg")
        ]
        
        for audio_format, filename in formats_to_test:
            output_path = os.path.join(test_output_dir, filename)
            
            print(f"\n🔄 Testing {audio_format.upper()} extraction...")
            result = extract_audio(
                video_path=test_video_path,
                output_path=output_path,
                audio_format=audio_format
            )
            
            if result["status"] == "success":
                print(f"✅ {audio_format.upper()} extraction successful")
                print(f"   Output: {result['output_path']}")
                print(f"   Duration: {result['duration']:.2f}s")
                print(f"   Sample Rate: {result['sample_rate']} Hz")
                print(f"   File Size: {result['file_size'] / 1024:.1f} KB")
                
                # Verify file exists
                if os.path.exists(result['output_path']):
                    print(f"   ✅ Output file created successfully")
                else:
                    print(f"   ❌ Output file not found")
            else:
                print(f"❌ {audio_format.upper()} extraction failed: {result['message']}")
        
        # Test format inference
        print(f"\n🔄 Testing format inference...")
        inferred_output = os.path.join(test_output_dir, "inferred_format.mp3")
        result = extract_audio(
            video_path=test_video_path,
            output_path=inferred_output
        )
        
        if result["status"] == "success":
            print(f"✅ Format inference successful: {result['audio_format']}")
        else:
            print(f"❌ Format inference failed: {result['message']}")
            
    else:
        print(f"❌ Test video not found: {test_video_path}")
        print("   Please provide a valid video file path for manual testing")


if __name__ == "__main__":
    # Run manual test if called directly
    run_manual_test()
