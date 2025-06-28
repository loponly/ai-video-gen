"""
Video effects functionality
"""

import os
from typing import List, Dict, Any

# Import PIL compatibility patch first
from . import pil_compat

from moviepy.editor import VideoFileClip
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.resize import resize
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout


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
                current_video = current_video.resize((width, height))
                applied_effects.append(f"resize({width}x{height})")
                
            elif effect_type == 'speed':
                factor = effect.get('factor', 1.0)
                # Use fx for changing speed
                current_video = current_video.fx(speedx, factor)
                applied_effects.append(f"speed({factor}x)")
                
            elif effect_type == 'fade_in':
                duration = effect.get('duration', 1.0)
                current_video = current_video.fx(fadein, duration)
                applied_effects.append(f"fade_in({duration}s)")
                
            elif effect_type == 'fade_out':
                duration = effect.get('duration', 1.0)
                current_video = current_video.fx(fadeout, duration)
                applied_effects.append(f"fade_out({duration}s)")
                
            elif effect_type == 'audio_fade_in':
                duration = effect.get('duration', 1.0)
                if current_video.audio:
                    current_video = current_video.set_audio(
                        current_video.audio.fx(audio_fadein, duration)
                    )
                applied_effects.append(f"audio_fade_in({duration}s)")
                
            elif effect_type == 'audio_fade_out':
                duration = effect.get('duration', 1.0)
                if current_video.audio:
                    current_video = current_video.set_audio(
                        current_video.audio.fx(audio_fadeout, duration)
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
