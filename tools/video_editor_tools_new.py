"""
Video Editor Tools
=================

A comprehensive set of tools for video editing operations including:
- Video concatenation
- Audio synchronization  
- Video clipping
- Metadata editing
- Effects and transitions
- Video export
- Subtitle/caption management

Dependencies: moviepy, ffmpeg-python
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import moviepy as mp
import ffmpeg


def concatenate_videos(video_paths: List[str], output_path: str, method: str = "compose") -> Dict[str, Any]:
    """
    Concatenate multiple video clips into a single video.
    
    Args:
        video_paths: List of paths to video files to concatenate
        output_path: Path where the concatenated video will be saved
        method: Method for concatenation ("compose" or "stack")
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Validate input files
        valid_videos = []
        for path in video_paths:
            if not os.path.exists(path):
                return {
                    "status": "error",
                    "message": f"Video file not found: {path}",
                    "output_path": None
                }
            valid_videos.append(mp.VideoFileClip(path))
        
        if not valid_videos:
            return {
                "status": "error", 
                "message": "No valid video files provided",
                "output_path": None
            }
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Concatenate videos
        if method == "compose":
            final_video = mp.concatenate_videoclips(valid_videos)
        elif method == "stack":
            # Stack videos vertically - use clips_array for this
            final_video = mp.clips_array([[video] for video in valid_videos])
        else:
            return {
                "status": "error",
                "message": f"Invalid method: {method}. Use 'compose' or 'stack'",
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
        
        # Get duration before closing
        duration = final_video.duration
        
        # Clean up
        for video in valid_videos:
            video.close()
        final_video.close()
        
        return {
            "status": "success",
            "message": f"Successfully concatenated {len(video_paths)} videos",
            "output_path": output_path,
            "duration": duration
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error concatenating videos: {str(e)}",
            "output_path": None
        }


def synchronize_audio(video_path: str, audio_path: str, output_path: str, 
                     sync_method: str = "replace") -> Dict[str, Any]:
    """
    Synchronize audio with video.
    
    Args:
        video_path: Path to the video file
        audio_path: Path to the audio file
        output_path: Path where the synchronized video will be saved
        sync_method: "replace", "overlay", or "mix"
    
    Returns:
        Dict with status, message, and output info
    """
    try:
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
        video = mp.VideoFileClip(video_path)
        audio = mp.AudioFileClip(audio_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Synchronize based on method
        if sync_method == "replace":
            # Replace video audio with new audio
            final_video = video.set_audio(audio)
        elif sync_method == "overlay":
            # Overlay new audio on existing audio
            if video.audio is not None:
                mixed_audio = mp.CompositeAudioClip([video.audio, audio])
                final_video = video.set_audio(mixed_audio)
            else:
                final_video = video.set_audio(audio)
        elif sync_method == "mix":
            # Mix audio at 50% volume each
            if video.audio is not None:
                original_audio = video.audio.volumex(0.5)
                new_audio = audio.volumex(0.5)
                mixed_audio = mp.CompositeAudioClip([original_audio, new_audio])
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
        
        # Get duration before closing
        duration = final_video.duration
        
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


def clip_videos(video_path: str, output_path: str, start_time: float = 0, 
               end_time: Optional[float] = None, segments: Optional[List[Tuple[float, float]]] = None) -> Dict[str, Any]:
    """
    Clip video(s) to specified segments.
    
    Args:
        video_path: Path to the input video file
        output_path: Path where the clipped video will be saved
        start_time: Start time in seconds (for single clip)
        end_time: End time in seconds (for single clip)
        segments: List of (start, end) tuples for multiple segments
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Validate input file
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        # Load video
        video = mp.VideoFileClip(video_path)
        original_duration = video.duration
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Clip video based on parameters
        if segments:
            # Multiple segments - concatenate them
            clips = []
            for start, end in segments:
                if end > video.duration:
                    end = video.duration
                clip = video.subclip(start, end)
                clips.append(clip)
            
            if clips:
                final_video = mp.concatenate_videoclips(clips)
            else:
                return {
                    "status": "error",
                    "message": "No valid segments provided",
                    "output_path": None
                }
        else:
            # Single segment
            if end_time is None:
                end_time = video.duration
            elif end_time > video.duration:
                end_time = video.duration
            
            final_video = video.subclip(start_time, end_time)
        
        # Write the final video
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Get duration before closing
        duration = final_video.duration
        
        # Clean up
        video.close()
        final_video.close()
        
        return {
            "status": "success",
            "message": "Successfully clipped video",
            "output_path": output_path,
            "duration": duration,
            "original_duration": original_duration
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error clipping video: {str(e)}",
            "output_path": None
        }


def edit_video_metadata(video_path: str, output_path: str, metadata: Dict[str, str]) -> Dict[str, Any]:
    """
    Edit video metadata (title, description, author, etc.).
    
    Args:
        video_path: Path to the input video file
        output_path: Path where the video with new metadata will be saved
        metadata: Dictionary of metadata fields to update
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Validate input file
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Use ffmpeg to add metadata
        input_stream = ffmpeg.input(video_path)
        
        # Prepare metadata options
        metadata_options = {}
        for key, value in metadata.items():
            if key in ['title', 'artist', 'album', 'date', 'genre', 'comment', 'description']:
                metadata_options[f'metadata:{key}'] = value
        
        # Output with metadata
        output_stream = ffmpeg.output(input_stream, output_path, **metadata_options)
        
        # Run the ffmpeg command
        ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
        
        return {
            "status": "success",
            "message": f"Successfully updated metadata for video",
            "output_path": output_path,
            "metadata_updated": list(metadata.keys())
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error editing video metadata: {str(e)}",
            "output_path": None
        }


def add_effects(video_path: str, output_path: str, effects: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Add effects and transitions to video.
    
    Args:
        video_path: Path to the input video file
        output_path: Path where the video with effects will be saved
        effects: List of effect dictionaries with type and parameters
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Validate input file
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        # Load video
        video = mp.VideoFileClip(video_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Apply effects
        current_video = video
        applied_effects = []
        
        for effect in effects:
            effect_type = effect.get('type', '')
            
            if effect_type == 'resize':
                width = effect.get('width', current_video.w)
                height = effect.get('height', current_video.h)
                current_video = current_video.resize((width, height))
                applied_effects.append(f"resize({width}x{height})")
                
            elif effect_type == 'speed':
                factor = effect.get('factor', 1.0)
                # Use speedx method for changing speed
                current_video = current_video.fx(mp.vfx.speedx, factor)
                applied_effects.append(f"speed({factor}x)")
                
            elif effect_type == 'fade_in':
                duration = effect.get('duration', 1.0)
                current_video = current_video.fadein(duration)
                applied_effects.append(f"fade_in({duration}s)")
                
            elif effect_type == 'fade_out':
                duration = effect.get('duration', 1.0)
                current_video = current_video.fadeout(duration)
                applied_effects.append(f"fade_out({duration}s)")
                
            elif effect_type == 'audio_fade_in':
                duration = effect.get('duration', 1.0)
                if current_video.audio:
                    current_video = current_video.set_audio(
                        current_video.audio.fx(mp.afx.audio_fadein, duration)
                    )
                applied_effects.append(f"audio_fade_in({duration}s)")
                
            elif effect_type == 'audio_fade_out':
                duration = effect.get('duration', 1.0)
                if current_video.audio:
                    current_video = current_video.set_audio(
                        current_video.audio.fx(mp.afx.audio_fadeout, duration)
                    )
                applied_effects.append(f"audio_fade_out({duration}s)")
                
            elif effect_type == 'crop':
                x1 = effect.get('x1', 0)
                y1 = effect.get('y1', 0)
                x2 = effect.get('x2', current_video.w)
                y2 = effect.get('y2', current_video.h)
                current_video = current_video.crop(x1=x1, y1=y1, x2=x2, y2=y2)
                applied_effects.append(f"crop({x1},{y1},{x2},{y2})")
        
        # Write the final video
        current_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Get duration before closing
        duration = current_video.duration
        
        # Clean up
        video.close()
        current_video.close()
        
        return {
            "status": "success",
            "message": f"Successfully applied {len(applied_effects)} effects",
            "output_path": output_path,
            "effects_applied": applied_effects,
            "duration": duration
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error adding effects: {str(e)}",
            "output_path": None
        }


def export_video(video_path: str, output_path: str, format_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export video with specific format settings.
    
    Args:
        video_path: Path to the input video file
        output_path: Path where the exported video will be saved
        format_settings: Dictionary with export settings (codec, bitrate, resolution, etc.)
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Validate input file
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        # Load video
        video = mp.VideoFileClip(video_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Extract format settings
        codec = format_settings.get('codec', 'libx264')
        audio_codec = format_settings.get('audio_codec', 'aac')
        bitrate = format_settings.get('bitrate', None)
        fps = format_settings.get('fps', None)
        resolution = format_settings.get('resolution', None)
        
        # Apply resolution if specified
        if resolution:
            width, height = resolution
            video = video.resize((width, height))
        
        # Prepare write parameters
        write_params = {
            'codec': codec,
            'audio_codec': audio_codec,
            'temp_audiofile': 'temp-audio.m4a',
            'remove_temp': True
        }
        
        if bitrate:
            write_params['bitrate'] = bitrate
        if fps:
            write_params['fps'] = fps
        
        # Write the video
        video.write_videofile(output_path, **write_params)
        
        # Get file size and duration
        file_size = os.path.getsize(output_path)
        duration = video.duration
        
        # Clean up
        video.close()
        
        return {
            "status": "success",
            "message": "Successfully exported video",
            "output_path": output_path,
            "file_size": file_size,
            "settings_used": format_settings,
            "duration": duration
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error exporting video: {str(e)}",
            "output_path": None
        }


def add_subtitles(video_path: str, subtitle_path: str, output_path: str, 
                 subtitle_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Add subtitles or captions to video.
    
    Args:
        video_path: Path to the input video file
        subtitle_path: Path to the subtitle file (.srt, .vtt, .ass)
        output_path: Path where the video with subtitles will be saved
        subtitle_options: Optional styling options for subtitles
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Validate input files
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        if not os.path.exists(subtitle_path):
            return {
                "status": "error",
                "message": f"Subtitle file not found: {subtitle_path}",
                "output_path": None
            }
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Default subtitle options
        options = subtitle_options or {}
        font_size = options.get('font_size', 24)
        font_color = options.get('font_color', 'white')
        
        # Use ffmpeg to add subtitles
        input_video = ffmpeg.input(video_path)
        
        # Create subtitle filter
        subtitle_filter = f"subtitles={subtitle_path}:force_style='FontSize={font_size},PrimaryColour={font_color}'"
        
        output = ffmpeg.output(
            input_video,
            output_path,
            vf=subtitle_filter,
            codec='libx264',
            acodec='aac'
        )
        
        # Run ffmpeg
        ffmpeg.run(output, overwrite_output=True, quiet=True)
        
        return {
            "status": "success",
            "message": "Successfully added subtitles to video",
            "output_path": output_path,
            "subtitle_file": subtitle_path,
            "options_used": options
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error adding subtitles: {str(e)}",
            "output_path": None
        }


if __name__ == "__main__":
    print("Video Editor Tools - Basic functionality check")
    print("=" * 50)
    
    # Test basic video loading
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    
    if os.path.exists(video_path):
        try:
            video = mp.VideoFileClip(video_path)
            print(f"✅ Video loaded successfully")
            print(f"   Duration: {video.duration:.2f}s")
            print(f"   Resolution: {video.w}x{video.h}")
            print(f"   FPS: {video.fps}")
            video.close()
        except Exception as e:
            print(f"❌ Failed to load video: {e}")
    else:
        print(f"❌ Test video not found: {video_path}")
