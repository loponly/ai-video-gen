# Test script to verify the VideoTextParameter functionality
import sys
import os

# Add the parent directory to the path to import the module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test.video_text_parameters import VideoTextParameter

def test_duration_calculation():
    """Test calculation of duration from start and end times."""
    print("Testing duration calculation from start and end times...")
    
    # Create a dummy video file for testing (we'll skip the file existence check for this test)
    test_video_path = "/path/to/dummy/video.mp4"
    
    # Mock the file existence check by temporarily modifying the __post_init__ method
    original_post_init = VideoTextParameter.__post_init__
    
    def mock_post_init(self):
        # Skip file existence check for testing
        # Handle different scenarios for duration and end_time calculation
        if self.duration is None and self.end_time is None:
            raise ValueError("Either duration or end_time must be provided")
        elif self.duration is None and self.end_time is not None:
            # Calculate duration from start_time and end_time
            self.duration = self._calculate_duration_from_times()
        elif self.duration is not None and self.end_time is None:
            # Calculate end_time from start_time and duration
            self.end_time = self._calculate_end_time()
    
    VideoTextParameter.__post_init__ = mock_post_init
    
    try:
        # Test 1: Calculate duration from start and end times
        param1 = VideoTextParameter(
            video_path=test_video_path,
            start_time="00:01:30,000",  # 1 minute 30 seconds
            end_time="00:02:45,500",    # 2 minutes 45.5 seconds
            text="Test subtitle 1"
        )
        expected_duration = 75.5  # 75.5 seconds difference
        print(f"Test 1 - Duration calculated: {param1.duration} seconds (expected: {expected_duration})")
        assert abs(param1.duration - expected_duration) < 0.001, f"Expected {expected_duration}, got {param1.duration}"
        
        # Test 2: Calculate end time from start time and duration
        param2 = VideoTextParameter(
            video_path=test_video_path,
            start_time="00:01:30,000",  # 1 minute 30 seconds
            duration=75.5,              # 75.5 seconds
            text="Test subtitle 2"
        )
        expected_end_time = "00:02:45,500"
        print(f"Test 2 - End time calculated: {param2.end_time} (expected: {expected_end_time})")
        assert param2.end_time == expected_end_time, f"Expected {expected_end_time}, got {param2.end_time}"
        
        # Test 3: Error when neither duration nor end_time is provided
        try:
            param3 = VideoTextParameter(
                video_path=test_video_path,
                start_time="00:01:30,000",
                text="Test subtitle 3"
            )
            print("Test 3 - ERROR: Should have raised ValueError")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            print(f"Test 3 - Correctly raised ValueError: {e}")
        
        print("All tests passed!")
        
    finally:
        # Restore original __post_init__ method
        VideoTextParameter.__post_init__ = original_post_init

if __name__ == "__main__":
    test_duration_calculation()
