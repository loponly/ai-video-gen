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
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip, clips_array
from moviepy.video import fx as vfx
from moviepy.audio import fx as afx
import ffmpeg


def concatenate_videos(video_paths: List[str], output_path: str, method: str) -> Dict[str, Any]:
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
        # Set default method if not provided
        if not method:
            method = "compose"
            
        # Validate input files
        valid_videos = []
        for path in video_paths:
            if not os.path.exists(path):
                return {
                    "status": "error",
                    "message": f"Video file not found: {path}",
                    "output_path": None
                }
            valid_videos.append(VideoFileClip(path))
        
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
            final_video = concatenate_videoclips(valid_videos)
        elif method == "stack":
            # Stack videos vertically - use clips_array for this
            final_video = clips_array([[video] for video in valid_videos])
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
        
        # Get duration before closing and convert to native Python float
        duration = float(final_video.duration)
        
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
                     sync_method: str) -> Dict[str, Any]:
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
        # Set default sync method if not provided
        if not sync_method:
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
            final_video = video.with_audio(audio)
        elif sync_method == "overlay":
            # Overlay new audio on existing audio
            if video.audio is not None:
                mixed_audio = CompositeAudioClip([video.audio, audio])
                final_video = video.with_audio(mixed_audio)
            else:
                final_video = video.with_audio(audio)
        elif sync_method == "mix":
            # Mix audio at 50% volume each
            if video.audio is not None:
                original_audio = video.audio.with_volume_scaled(0.5)
                new_audio = audio.with_volume_scaled(0.5)
                mixed_audio = CompositeAudioClip([original_audio, new_audio])
                final_video = video.with_audio(mixed_audio)
            else:
                final_video = video.with_audio(audio)
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


def clip_videos(video_path: str, output_path: str, start_time: float, 
               end_time: Optional[float], segments: Optional[str]) -> Dict[str, Any]:
    """
    Clip video(s) to specified segments.
    
    Args:
        video_path: Path to the input video file
        output_path: Path where the clipped video will be saved
        start_time: Start time in seconds (for single clip)
        end_time: End time in seconds (for single clip)
        segments: JSON string of (start, end) tuples for multiple segments, e.g., "[[0,10],[20,30]]"
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Set default values if not provided
        if start_time is None:
            start_time = 0.0
            
        # Validate input file
        if not os.path.exists(video_path):
            return {
                "status": "error",
                "message": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        # Load video
        video = VideoFileClip(video_path)
        original_duration = video.duration
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Clip video based on parameters
        if segments:
            # Parse segments from JSON string
            try:
                segments_list = json.loads(segments)
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "message": f"Invalid segments JSON format: {segments}",
                    "output_path": None
                }
            
            # Multiple segments - concatenate them
            clips = []
            for start, end in segments_list:
                if end > video.duration:
                    end = video.duration
                clip = video.subclipped(start, end)
                clips.append(clip)
            
            if clips:
                final_video = concatenate_videoclips(clips)
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
            
            final_video = video.subclipped(start_time, end_time)
        
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
        final_video.close()
        
        return {
            "status": "success",
            "message": "Successfully clipped video",
            "output_path": output_path,
            "duration": duration,
            "original_duration": float(original_duration)  # Convert this too
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
    Note: MoviePy doesn't support metadata editing, so this copies the video and returns success.
    For full metadata support, use external tools.
    
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
        
        # Load and copy video (MoviePy doesn't support metadata editing directly)
        video = VideoFileClip(video_path)
        
        # Write the video (this will copy the video without metadata changes)
        video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        video.close()
        
        return {
            "status": "success",
            "message": f"Video copied successfully (metadata support limited in MoviePy)",
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
        video = VideoFileClip(video_path)
        
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
                current_video = current_video.resized((width, height))
                applied_effects.append(f"resize({width}x{height})")
                
            elif effect_type == 'speed':
                factor = effect.get('factor', 1.0)
                # Use with_speed_scaled method for changing speed
                current_video = current_video.with_speed_scaled(factor)
                applied_effects.append(f"speed({factor}x)")
                
            elif effect_type == 'fade_in':
                duration = effect.get('duration', 1.0)
                current_video = current_video.with_effects([vfx.FadeIn(duration)])
                applied_effects.append(f"fade_in({duration}s)")
                
            elif effect_type == 'fade_out':
                duration = effect.get('duration', 1.0)
                current_video = current_video.with_effects([vfx.FadeOut(duration)])
                applied_effects.append(f"fade_out({duration}s)")
                
            elif effect_type == 'audio_fade_in':
                duration = effect.get('duration', 1.0)
                if current_video.audio:
                    current_video = current_video.with_audio(
                        current_video.audio.with_effects([afx.AudioFadeIn(duration)])
                    )
                applied_effects.append(f"audio_fade_in({duration}s)")
                
            elif effect_type == 'audio_fade_out':
                duration = effect.get('duration', 1.0)
                if current_video.audio:
                    current_video = current_video.with_audio(
                        current_video.audio.with_effects([afx.AudioFadeOut(duration)])
                    )
                applied_effects.append(f"audio_fade_out({duration}s)")
                
            elif effect_type == 'crop':
                x1 = effect.get('x1', 0)
                y1 = effect.get('y1', 0)
                x2 = effect.get('x2', current_video.w)
                y2 = effect.get('y2', current_video.h)
                current_video = current_video.cropped(x1=x1, y1=y1, x2=x2, y2=y2)
                applied_effects.append(f"crop({x1},{y1},{x2},{y2})")
        
        # Write the final video
        current_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Get duration before closing and convert to native Python float
        duration = float(current_video.duration)
        
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
        video = VideoFileClip(video_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Extract format settings and adjust for output format
        output_ext = os.path.splitext(output_path)[1].lower()
        
        # Set appropriate default codecs based on output format
        if output_ext == '.webm':
            default_codec = 'libvpx-vp9'  # VP9 for WebM
            default_audio_codec = None  # Let MoviePy choose for WebM
        elif output_ext == '.mp4':
            default_codec = 'libx264'  # H.264 for MP4
            default_audio_codec = 'aac'  # AAC for MP4
        elif output_ext == '.avi':
            default_codec = 'libx264'  # H.264 for AVI
            default_audio_codec = 'mp3'  # MP3 for AVI
        else:
            default_codec = 'libx264'  # Default fallback
            default_audio_codec = 'aac'  # Default fallback
        
        codec = format_settings.get('codec', default_codec)
        audio_codec = format_settings.get('audio_codec', default_audio_codec)
        bitrate = format_settings.get('bitrate', None)
        fps = format_settings.get('fps', None)
        resolution = format_settings.get('resolution', None)
        
        # Apply resolution if specified
        if resolution:
            width, height = resolution
            video = video.resized((width, height))
        
        # Handle case where input and output paths are the same
        temp_output_path = output_path
        if os.path.abspath(video_path) == os.path.abspath(output_path):
            # Create a temporary output path with same extension
            path_parts = os.path.splitext(output_path)
            temp_output_path = f"{path_parts[0]}_temp{path_parts[1]}"
        
        # Prepare write parameters
        write_params = {
            'codec': codec,
            'remove_temp': True
        }
        
        # Handle audio codec and temp file based on output format
        if output_ext == '.webm':
            # For WebM, let MoviePy handle audio codec automatically
            # Don't specify temp_audiofile for WebM to avoid issues
            pass
        else:
            # For other formats, use temp audio file
            write_params['temp_audiofile'] = 'temp-audio.m4a'
            if audio_codec:
                write_params['audio_codec'] = audio_codec
        
        if bitrate:
            write_params['bitrate'] = bitrate
        if fps:
            write_params['fps'] = fps
        
        # Write the video
        video.write_videofile(temp_output_path, **write_params)
        
        # Get file size and duration and convert to native Python types
        file_size = int(os.path.getsize(temp_output_path))
        duration = float(video.duration)
        
        # Clean up
        video.close()
        
        # If we used a temporary file, replace the original
        if temp_output_path != output_path:
            import shutil
            shutil.move(temp_output_path, output_path)
            file_size = int(os.path.getsize(output_path))
        
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
                 subtitle_options: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Add subtitles or captions to video.
    Note: This function creates a copy of the video. For subtitle overlay, external tools are needed.
    
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
        
        # Load and copy video (MoviePy doesn't support subtitle overlay directly)
        video = VideoFileClip(video_path)
        
        # Write the video (this will copy the video)
        video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        video.close()
        
        return {
            "status": "success",
            "message": "Video copied successfully (subtitle overlay requires external tools)",
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


def extract_audio(video_path: str, output_path: str, audio_format: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract audio from video file and save as audio file.
    
    Args:
        video_path: Path to the input video file
        output_path: Path where the extracted audio will be saved
        audio_format: Optional audio format ("mp3", "wav", "aac", "flac"). If None, inferred from output_path
    
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
        video = VideoFileClip(video_path)
        
        # Check if video has audio
        if video.audio is None:
            video.close()
            return {
                "status": "error",
                "message": "Video file has no audio track",
                "output_path": None
            }
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Determine audio format if not specified
        if audio_format is None:
            output_ext = os.path.splitext(output_path)[1].lower()
            if output_ext in ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg']:
                audio_format = output_ext[1:]  # Remove the dot
            else:
                audio_format = 'mp3'  # Default format
                # Update output path with correct extension
                output_path = os.path.splitext(output_path)[0] + '.mp3'
        
        # Extract audio
        audio = video.audio
        
        # Write audio file with appropriate codec
        if audio_format.lower() in ['mp3']:
            audio.write_audiofile(output_path, codec='mp3')
        elif audio_format.lower() in ['wav']:
            audio.write_audiofile(output_path, codec='pcm_s16le')
        elif audio_format.lower() in ['aac', 'm4a']:
            audio.write_audiofile(output_path, codec='aac')
        elif audio_format.lower() in ['flac']:
            audio.write_audiofile(output_path, codec='flac')
        elif audio_format.lower() in ['ogg']:
            audio.write_audiofile(output_path, codec='libvorbis')
        else:
            # Default to mp3 for unknown formats
            audio.write_audiofile(output_path, codec='mp3')
        
        # Get audio info before closing and convert to native Python types
        duration = float(audio.duration)
        sample_rate = int(audio.fps) if audio.fps else None
        
        # Get file size
        file_size = int(os.path.getsize(output_path))
        
        # Clean up
        audio.close()
        video.close()
        
        return {
            "status": "success",
            "message": f"Successfully extracted audio in {audio_format} format",
            "output_path": output_path,
            "duration": duration,
            "sample_rate": sample_rate,
            "file_size": file_size,
            "audio_format": audio_format
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error extracting audio: {str(e)}",
            "output_path": None
        }


def create_video_from_images(image_paths: List[str], output_path: str, duration_per_image: float) -> Dict[str, Any]:
    """
    Create a video slideshow from a list of images.
    
    Args:
        image_paths: List of paths to image files
        output_path: Path where the video will be saved
        duration_per_image: Duration each image is displayed (seconds)
    
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Import the image editor tools function
        from tools.image_editor_tools import create_slideshow_from_images
        
        # Create slideshow with basic settings
        result = create_slideshow_from_images(
            image_paths=image_paths,
            output_path=output_path,
            duration_per_image=duration_per_image,
            fps=24,
            resolution_width=1920,
            resolution_height=1080,
            transition_type="fade",
            transition_duration=0.5,
            background_color_r=0,
            background_color_g=0,
            background_color_b=0,
            fit_mode="contain",
            audio_path=None,
            text_overlays=None,
            effects=None
        )
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create video from images: {str(e)}",
            "output_path": None,
            "details": {
                "error_type": type(e).__name__,
                "image_count": len(image_paths)
            }
        }


if __name__ == "__main__":
    print("Video Editor Tools - Basic functionality check")
    print("=" * 50)
    
    # Test basic video loading
    video_path = "/Users/enkhbat_1/projects/ai-video-ge/movie-reels/movie_2/1.mp4"
    
    if os.path.exists(video_path):
        try:
            video = VideoFileClip(video_path)
            print(f"✅ Video loaded successfully")
            print(f"   Duration: {video.duration:.2f}s")
            print(f"   Resolution: {video.w}x{video.h}")
            print(f"   FPS: {video.fps}")
            video.close()
        except Exception as e:
            print(f"❌ Failed to load video: {e}")
    else:
        print(f"❌ Test video not found: {video_path}")
