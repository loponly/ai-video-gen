"""
Get YouTube video transcript functionality
"""

from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict, Union


def get_transcript(video_id: str) -> Union[List[Dict[str, str]], None]:
    """
    Fetches the transcript for a given YouTube video ID.
    
    :param video_id: The ID of the YouTube video.
    :return: A list of dictionaries containing the transcript.
    """

    try:
        # Attempt to fetch the transcript
        return YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        # If an error occurs, print it and return an empty list
        print(f"Error fetching transcript for video ID {video_id}: {e}")
    return None
