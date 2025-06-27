"""
Download YouTube video functionality
"""

import os
from typing import Union
from yt_dlp import YoutubeDL


def download_youtube_video(url: str, save_dir: str = "./downloads", cookie_file: Union[str, None] = None) -> str:
    """Robustly downloads the best available version of a YouTube video."""
    
    # Validate and fix save_dir path
    if save_dir.startswith('/content/') or not os.access(os.path.dirname(save_dir) if os.path.dirname(save_dir) else '.', os.W_OK):
        # Fallback to a safe directory if the provided path is problematic
        save_dir = "./downloads"
        print(f"Warning: Using fallback directory '{save_dir}' due to permission issues")
    
    try:
        os.makedirs(save_dir, exist_ok=True)
    except OSError as e:
        # If we still can't create the directory, use current directory
        save_dir = "./downloads"
        print(f"Warning: Could not create directory, using '{save_dir}': {e}")
        os.makedirs(save_dir, exist_ok=True)

    ydl_opts = {
     #   "format": "(bv*[ext=mp4]+ba[ext=m4a])/(bv*+ba/best)/best",
        "outtmpl": os.path.join(save_dir, "%(title)s.%(ext)s"),
    }
    if cookie_file:
        ydl_opts["cookiefile"] = cookie_file

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return os.path.abspath(ydl.prepare_filename(info))
