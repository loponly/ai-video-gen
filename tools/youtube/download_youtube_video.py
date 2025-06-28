"""
Download YouTube video functionality
"""

import os
from typing import Optional, Dict, Any
from yt_dlp import YoutubeDL


def download_youtube_video(url: str, save_dir: str = "./downloads", cookie_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Download the best available version of a YouTube video to local storage.
    
    Use this tool when you need to download YouTube videos for offline processing,
    analysis, or storage. The tool automatically selects the best quality available
    and handles various video formats.
    
    Args:
        url: The complete YouTube video URL (e.g., 'https://www.youtube.com/watch?v=VIDEO_ID').
        save_dir: Absolute path to directory where video will be saved. 
                 Defaults to "./downloads". Directory will be created if it doesn't exist.
        cookie_file: Optional path to cookie file for authentication if required
                    for age-restricted or private videos.
    
    Returns:
        A dictionary containing the download result:
        - status: 'success' if download completed, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Absolute path to the downloaded video file (None if error)
        - title: Title of the downloaded video (if success)
        - duration: Duration of video in seconds (if success)
        - file_size: Size of downloaded file in bytes (if success)
        
        Example success: {'status': 'success', 'message': 'Successfully downloaded video',
                         'output_path': '/downloads/Sample Video.mp4', 'title': 'Sample Video',
                         'duration': 180.5, 'file_size': 15728640}
        Example error: {'status': 'error', 'message': 'Invalid YouTube URL format',
                       'output_path': None}
    """
    try:
        # Validate URL format
        if not url or not url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
            return {
                "status": "error",
                "message": "Invalid YouTube URL format",
                "output_path": None
            }
        
        # Validate and fix save_dir path
        if save_dir.startswith('/content/') or not os.access(os.path.dirname(save_dir) if os.path.dirname(save_dir) else '.', os.W_OK):
            # Fallback to a safe directory if the provided path is problematic
            save_dir = "./downloads"
        
        try:
            os.makedirs(save_dir, exist_ok=True)
        except OSError:
            # If we still can't create the directory, use current directory
            save_dir = "./downloads"
            os.makedirs(save_dir, exist_ok=True)

        ydl_opts = {
            "format": "best[ext=mp4]/best",
            "outtmpl": os.path.join(save_dir, "%(title)s.%(ext)s"),
        }
        if cookie_file:
            ydl_opts["cookiefile"] = cookie_file

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            output_path = os.path.abspath(ydl.prepare_filename(info))
            
            # Get file size
            file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
            
            return {
                "status": "success",
                "message": "Successfully downloaded video",
                "output_path": output_path,
                "title": info.get("title", "Unknown"),
                "duration": float(info.get("duration", 0)) if info.get("duration") else None,
                "file_size": file_size
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to download video: {str(e)}",
            "output_path": None
        }
