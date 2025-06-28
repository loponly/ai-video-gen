"""
Audio synchronization functionality
"""

import os
from typing import Dict, Any
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


def synchronize_audio(video_path: str, audio_path: str, output_path: str, 
                     sync_method: str = "replace") -> Dict[str, Any]:
    """
    Synchronize audio with video using different mixing methods.
    
    Use this tool when you need to replace, overlay, or mix audio tracks with video.
    The tool supports three synchronization methods for different use cases.
    
    Args:
        video_path: Absolute path to the input video file.
        audio_path: Absolute path to the audio file to synchronize with video.
        output_path: Absolute path where the synchronized video will be saved.
                    Directory will be created if it doesn't exist.
        sync_method: Method for audio synchronization. Options:
                    - "replace": Replace original audio with new audio track
                    - "overlay": Layer new audio over existing audio
                    - "mix": Blend new audio with existing audio
                    Defaults to "replace".
    
    Returns:
        A dictionary containing the synchronization result:
        - status: 'success' if synchronization completed, 'error' if failed
        - message: Descriptive message about the operation result
        - output_path: Path to the created video file (None if error)
        - duration: Duration of output video in seconds (if success)
        - sync_method: The synchronization method used (if success)
        
        Example success: {'status': 'success', 'message': 'Successfully synchronized audio',
                         'output_path': '/path/to/synced.mp4', 'duration': 120.5,
                         'sync_method': 'replace'}
        Example error: {'status': 'error', 'message': 'Video file not found: /invalid/path.mp4',
                       'output_path': None}
    """
    try:
        # Validate sync method
        if sync_method not in ["replace", "overlay", "mix"]:
            sync_method = "replace"
            
        # Validate input files
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        if not os.path.exists(audio_path):
            return {
                "status": "error",
                "message": f"Audio file not found: {audio_path}",
                "output_path": None
            }
        
        # Load video and audio
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Synchronize based on method
        if sync_method == "replace":
            # Replace video audio with new audio
            final_video = video.set_audio(audio)
        elif sync_method == "overlay":
            # Overlay new audio on existing audio
            if video.audio is not None:
                mixed_audio = CompositeAudioClip([video.audio, audio])
                final_video = video.set_audio(mixed_audio)
            else:
                final_video = video.set_audio(audio)
        elif sync_method == "mix":
            # Mix audio at 50% volume each
            if video.audio is not None:
                original_audio = video.audio.volumex(0.5)
                new_audio = audio.volumex(0.5)
                mixed_audio = CompositeAudioClip([original_audio, new_audio])
                final_video = video.set_audio(mixed_audio)
            else:
                final_video = video.set_audio(audio)
        else:
            return {
                "status": "error",
                "message": f"Invalid sync method: {sync_method}",
                "output_path": None
            }
        
        # Write the final video
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Get duration before closing and convert to native Python float
        duration = float(final_video.duration)
        
        # Clean up
        video.close()
        audio.close()
        final_video.close()
        
        return {
            "status": "success",
            "message": f"Successfully synchronized audio using {sync_method} method",
            "output_path": output_path,
            "duration": duration
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error synchronizing audio: {str(e)}",
            "output_path": None
        }
