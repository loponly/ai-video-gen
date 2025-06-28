"""
Get YouTube video information functionality
"""

from typing import Dict, Any
from yt_dlp import YoutubeDL


def get_video_info(url: str) -> Dict[str, Any]:
    """
    Fetch comprehensive information about a YouTube video using its URL.
    
    Use this tool when you need to extract metadata about a YouTube video
    including title, description, duration, view counts, and channel information.
    
    Args:
        url: The complete YouTube video URL (e.g., 'https://www.youtube.com/watch?v=dQw4w9WgXcQ').
             Must be a valid YouTube watch URL format.
    
    Returns:
        A dictionary containing the video information retrieval result:
        - status: 'success' if info retrieved, 'error' if failed
        - message: Descriptive message about the operation result
        - video_info: Dictionary with video metadata fields (if success)
        - url: The original URL that was processed (if success)
        
        Video info includes: id, title, description, channel, channel_id, channel_url,
        duration, duration_string, view_count, like_count, upload_date, uploader,
        webpage_url, categories, tags, age_limit, availability, language
        
        Example success: {'status': 'success', 'message': 'Successfully retrieved video info',
                         'video_info': {'id': 'dQw4w9WgXcQ', 'title': 'Sample Video'},
                         'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
        Example error: {'status': 'error', 'message': 'Invalid YouTube URL format',
                       'url': 'invalid_url'}
    """
    try:
        # Validate URL format
        if not url.startswith("https://www.youtube.com/watch?v="):
            return {
                "status": "error",
                "message": "Invalid YouTube URL format. Must be https://www.youtube.com/watch?v=VIDEO_ID",
                "url": url
            }
        
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        # Important fields to extract
        important_fields = [
            'id', 'title', 'description', 'channel', 'channel_id', 'channel_url',
            'duration', 'duration_string', 'view_count', 'like_count', 'upload_date',
            'uploader', 'webpage_url', 'categories', 'tags', 'age_limit', 
            'availability', 'language'
        ]
        
        # Extract video information
        with YoutubeDL(ydl_opts) as ydl:
            full_info = ydl.extract_info(url, download=False)
            
        # Filter to important fields only
        filtered_info = {}
        for field in important_fields:
            if field in full_info:
                filtered_info[field] = full_info[field]
        
        return {
            "status": "success",
            "message": "Successfully retrieved video information",
            "video_info": filtered_info,
            "url": url
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to retrieve video info: {str(e)}",
            "url": url
        }
