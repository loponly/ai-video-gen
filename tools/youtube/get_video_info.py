"""
Get YouTube video information functionality
"""

from typing import Dict, Union
from yt_dlp import YoutubeDL


def get_video_info(url: str) -> Dict[str, Union[str, int]]:
    """
    Fetches video information using yt-dlp.
    
    :param url: The URL of the YouTube video.
    :return: A dictionary containing important video information.
    Info includes fields are: id, title, description, channel, channel_id, channel_url, duration, duration_string, view_count, like_count, upload_date, uploader, webpage_url, categories, tags, age_limit, availability, language
    """
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,  # Changed to False to get full info
    }
    
    # Important fields to extract
    important_fields = [
        'id',
        'title', 
        'description',
        'channel',
        'channel_id',
        'channel_url',
        'duration',
        'duration_string',
        'view_count',
        'like_count',
        'upload_date',
        'uploader',
        'webpage_url',
        'categories',
        'tags',
        'age_limit',
        'availability',
        'language'
    ]
    
    try:
        # Attempt to fetch video information
        if not url.startswith("https://www.youtube.com/watch?v="):
            raise ValueError("Invalid YouTube URL format.")
        with YoutubeDL(ydl_opts) as ydl:
            full_info = ydl.extract_info(url, download=False)
            
        # Extract only important fields
        filtered_info = {}
        for field in important_fields:
            if field in full_info:
                filtered_info[field] = full_info[field]

    except Exception as e:
        # If an error occurs, print it and return an empty dictionary
        print(f"Error fetching video info for URL {url}: {e}")
        return {}
    
    return filtered_info
