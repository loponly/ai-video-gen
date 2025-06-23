import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class VideoTextParameter:
    """
    Encapsulates parameters for video processing with text overlay.
    
    Attributes:
        video_path (str): Path to the video file
        start_time (str): Start time in HH:MM:SS,mmm format
        text (str): Text content to be overlaid or associated with the video segment
        duration (Optional[float]): Duration in seconds
        end_time (Optional[str]): End time in HH:MM:SS,mmm format (calculated if not provided)
        file_name (Optional[str]): Name of the source file
        movie_name (Optional[str]): Name of the movie/series
    """
    video_path: str
    start_time: str
    text: str
    duration: Optional[float] = None
    end_time: Optional[str] = None
    file_name: Optional[str] = None
    movie_name: Optional[str] = None
    
    def __post_init__(self):
        """Calculate missing values and validate video path."""
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file not found: {self.video_path}")
        
        # Handle different scenarios for duration and end_time calculation
        if self.duration is None and self.end_time is None:
            raise ValueError("Either duration or end_time must be provided")
        elif self.duration is None and self.end_time is not None:
            # Calculate duration from start_time and end_time
            self.duration = self._calculate_duration_from_times()
        elif self.duration is not None and self.end_time is None:
            # Calculate end_time from start_time and duration
            self.end_time = self._calculate_end_time()
        # If both are provided, validate they are consistent (optional validation)
        # We could add validation here to ensure the provided values are consistent
    
    def _time_to_seconds(self, time_str: str) -> float:
        """Convert 'HH:MM:SS,mmm' format to seconds."""
        time_part, ms = time_str.split(',')
        h, m, s = map(int, time_part.split(':'))
        return h * 3600 + m * 60 + s + int(ms) / 1000
    
    def _seconds_to_time(self, seconds: float) -> str:
        """Convert seconds to 'HH:MM:SS,mmm' format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"
    
    def _calculate_end_time(self) -> str:
        """Calculate end time based on start time and duration."""
        start_seconds = self._time_to_seconds(self.start_time)
        end_seconds = start_seconds + self.duration
        return self._seconds_to_time(end_seconds)
    
    def _calculate_duration_from_times(self) -> float:
        """Calculate duration from start_time and end_time."""
        start_seconds = self._time_to_seconds(self.start_time)
        end_seconds = self._time_to_seconds(self.end_time)
        return end_seconds - start_seconds
    
    def get_duration_minutes(self) -> float:
        """Get duration in minutes."""
        if self.duration is None:
            raise ValueError("Duration is not available")
        return round(self.duration / 60, 3)
    
    def to_dict(self) -> dict:
        """Convert to dictionary format."""
        duration_minutes = None
        if self.duration is not None:
            duration_minutes = self.get_duration_minutes()
        
        return {
            'video_path': self.video_path,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'text': self.text,
            'duration': self.duration,
            'duration_minutes': duration_minutes,
            'file_name': self.file_name,
            'movie_name': self.movie_name
        }
    
    @classmethod
    def from_srt_data(cls, video_path: str, srt_data: dict) -> 'VideoTextParameter':
        """
        Create instance from SRT subtitle data.
        
        Args:
            video_path (str): Path to the video file
            srt_data (dict): Dictionary containing SRT subtitle information
        
        Returns:
            VideoTextParameter: New instance with SRT data
        """
        return cls(
            video_path=video_path,
            start_time=srt_data['start'],
            text=srt_data['text'],
            duration=srt_data.get('duration_seconds'),
            end_time=srt_data.get('end'),
            file_name=srt_data.get('file_name'),
            movie_name=srt_data.get('movie_name')
        )


class VideoTextParameterManager:
    """Manager class for handling multiple VideoTextParameter instances."""
    
    def __init__(self):
        self.parameters = []
    
    def add_parameter(self, parameter: VideoTextParameter):
        """Add a video text parameter."""
        self.parameters.append(parameter)
    
    def add_from_srt_data(self, video_path: str, srt_data_list: list):
        """Add multiple parameters from SRT data list."""
        for srt_data in srt_data_list:
            parameter = VideoTextParameter.from_srt_data(video_path, srt_data)
            self.add_parameter(parameter)
    
    def get_parameters_by_duration(self, min_duration: float = None, max_duration: float = None):
        """Filter parameters by duration range."""
        filtered = self.parameters
        if min_duration is not None:
            filtered = [p for p in filtered if p.duration is not None and p.duration >= min_duration]
        if max_duration is not None:
            filtered = [p for p in filtered if p.duration is not None and p.duration <= max_duration]
        return filtered
    
    def get_parameters_by_text_length(self, min_length: int = None, max_length: int = None):
        """Filter parameters by text length."""
        filtered = self.parameters
        if min_length is not None:
            filtered = [p for p in filtered if len(p.text) >= min_length]
        if max_length is not None:
            filtered = [p for p in filtered if len(p.text) <= max_length]
        return filtered
    
    def to_dict_list(self) -> list:
        """Convert all parameters to list of dictionaries."""
        return [param.to_dict() for param in self.parameters]