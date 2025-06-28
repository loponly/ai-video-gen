"""
Get YouTube video transcript functionality
"""

from youtube_transcript_api import YouTubeTranscriptApi
from typing import Dict, Any


def get_transcript(video_id: str) -> Dict[str, Any]:
    """
    Fetch the transcript for a YouTube video using its video ID.
    
    Use this tool when you need to extract the spoken content or captions
    from a YouTube video for analysis, summarization, or content processing.
    
    Args:
        video_id: The unique YouTube video identifier (e.g., 'dQw4w9WgXcQ').
                 This is the part after 'watch?v=' in a YouTube URL.
    
    Returns:
        A dictionary containing the transcript retrieval result:
        - status: 'success' if transcript retrieved, 'error' if failed
        - message: Descriptive message about the operation result
        - transcript: List of transcript segments with text and timing (if success)
        - video_id: The video ID that was processed (if success)
        - total_segments: Number of transcript segments found (if success)
        
        Example success: {'status': 'success', 'message': 'Successfully retrieved transcript',
                         'transcript': [{'text': 'Hello world', 'start': 0.0, 'duration': 2.5}],
                         'video_id': 'dQw4w9WgXcQ', 'total_segments': 156}
        Example error: {'status': 'error', 'message': 'Transcript not available for video',
                       'video_id': 'invalid_id'}
    """
    try:
        # Fetch the transcript from YouTube
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        
        return {
            "status": "success",
            "message": "Successfully retrieved transcript",
            "transcript": transcript_data,
            "video_id": video_id,
            "total_segments": len(transcript_data)
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Failed to retrieve transcript: {str(e)}",
            "video_id": video_id
        }
