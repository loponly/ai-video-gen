"""
Convert WebM to MP4 functionality
"""

import os
from typing import Union
from moviepy.editor import VideoFileClip


def convert_webm_to_mp4(input_file: str, output_file: Union[str, None] = None) -> str:
    """
    Converts a .webm video to .mp4 using MoviePy.
    
    :param input_file: Path to the input .webm file.
    :param output_file: Optional path for the output .mp4 file.
    :return: The absolute path of the saved MP4.
    """
    if output_file is None:
        # Default output name if not provided
        name, _ = os.path.splitext(input_file)
        output_file = f"{name}.mp4"

    clip = VideoFileClip(input_file)
    clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    return os.path.abspath(output_file)
