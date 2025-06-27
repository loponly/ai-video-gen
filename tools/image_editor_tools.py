"""
Image Editor Tools
==================

A comprehensive set of tools for image editing and image-to-video conversion including:
- Image slideshow creation
- Transitions between images
- Text overlays and captions
- Audio synchronization
- Effects and filters
- Video export with customizable settings

Dependencies: moviepy, PIL/Pillow, numpy
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple, Union
from pathlib import Path
import moviepy as mp
from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip, TextClip, 
    CompositeVideoClip, concatenate_videoclips, VideoClip
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def create_slideshow_from_images(image_paths: List[str],
                                output_path: str,
                                duration_per_image: float = 3.0,
                                fps: int = 24,
                                resolution_width: int = 1920,
                                resolution_height: int = 1080,
                                transition_type: str = "fade",
                                transition_duration: float = 0.5,
                                background_color_r: int = 0,
                                background_color_g: int = 0,
                                background_color_b: int = 0,
                                fit_mode: str = "contain",
                                audio_path: Optional[str] = None,
                                text_overlays: Optional[List[Dict[str, Any]]] = None,
                                effects: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Convert a list of images to a video slideshow with transitions and effects.
    
    Args:
        image_paths: List of paths to image files
        output_path: Path where the video will be saved
        duration_per_image: Duration each image is displayed (seconds)
        fps: Frames per second for output video
        resolution_width: Output video width in pixels
        resolution_height: Output video height in pixels
        transition_type: Type of transition ("fade", "slide_left", "slide_right", "slide_up", "slide_down", "zoom", "crossfade", "none")
        transition_duration: Duration of transitions (seconds)
        background_color_r: Background red color component (0-255)
        background_color_g: Background green color component (0-255)
        background_color_b: Background blue color component (0-255)
        fit_mode: How to fit images ("contain", "cover", "stretch", "crop")
        audio_path: Optional path to audio file to add as background
        text_overlays: List of text overlay configurations
        effects: List of effects to apply
        
    Returns:
        Dict with status, message, and output info
    """
    try:
        # Convert separate parameters back to tuples for internal use
        resolution = (resolution_width, resolution_height)
        background_color = (background_color_r, background_color_g, background_color_b)
        
        # Validate input images
        if not image_paths:
            return {
                "status": "error",
                "message": "No image paths provided",
                "output_path": None
            }
        
        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
        valid_images = []
        
        for path in image_paths:
            if not os.path.exists(path):
                return {
                    "status": "error",
                    "message": f"Image file not found: {path}",
                    "output_path": None
                }
            
            file_ext = Path(path).suffix.lower()
            if file_ext not in supported_formats:
                return {
                    "status": "error", 
                    "message": f"Unsupported image format: {file_ext}",
                    "output_path": None
                }
            valid_images.append(path)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create video clips from images
        clips = []
        total_duration = 0
        
        for i, img_path in enumerate(valid_images):
            # Create image clip
            img_clip = _create_image_clip(
                img_path, 
                duration_per_image,
                resolution,
                fit_mode,
                background_color
            )
            
            # Apply text overlays if specified
            if text_overlays:
                img_clip = _add_text_overlays(img_clip, text_overlays, i, total_duration)
            
            # Apply effects if specified
            if effects:
                img_clip = _apply_effects(img_clip, effects)
            
            clips.append(img_clip)
            total_duration += duration_per_image
        
        # Add transitions between clips
        if transition_type != "none" and len(clips) > 1:
            clips = _add_transitions(clips, transition_type, transition_duration)
        
        # Concatenate all clips
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Add background audio if specified
        if audio_path and os.path.exists(audio_path):
            audio_clip = AudioFileClip(audio_path)
            # Loop or trim audio to match video duration
            video_duration = final_video.duration
            if audio_clip.duration < video_duration:
                # Loop audio
                audio_clip = audio_clip.loop(duration=video_duration)
            else:
                # Trim audio
                audio_clip = audio_clip.subclip(0, video_duration)
            
            final_video = final_video.set_audio(audio_clip)
        
        # Write final video
        final_video.write_videofile(
            output_path,
            fps=fps,
            codec='libx264',
            audio_codec='aac' if audio_path else None,
            temp_audiofile='temp-audio.m4a' if audio_path else None,
            remove_temp=True
        )
        
        # Get duration before closing
        duration = final_video.duration
        
        # Clean up
        for clip in clips:
            clip.close()
        final_video.close()
        if audio_path and os.path.exists(audio_path):
            audio_clip.close()
        
        return {
            "status": "success",
            "message": f"Successfully created slideshow video with {len(valid_images)} images",
            "output_path": output_path,
            "duration": duration,
            "resolution": resolution,
            "fps": fps,
            "images_count": len(valid_images)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating slideshow: {str(e)}",
            "output_path": None
        }


def _create_image_clip(img_path: str, duration: float, resolution: Tuple[int, int], 
                      fit_mode: str, background_color: Tuple[int, int, int]) -> ImageClip:
    """Create a video clip from an image with proper sizing and formatting"""
    
    # Load and process image
    img = Image.open(img_path)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    target_width, target_height = resolution
    img_width, img_height = img.size
    
    if fit_mode == "stretch":
        # Stretch image to fit exactly
        img = img.resize((target_width, target_height), Image.LANCZOS)
    
    elif fit_mode == "crop":
        # Crop image to fit (center crop)
        img_ratio = img_width / img_height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            # Image is wider than target
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img_height))
        else:
            # Image is taller than target
            new_height = int(img_width / target_ratio)
            top = (img_height - new_height) // 2
            img = img.crop((0, top, img_width, top + new_height))
        
        img = img.resize((target_width, target_height), Image.LANCZOS)
    
    elif fit_mode == "cover":
        # Scale to cover entire area (may crop)
        img_ratio = img_width / img_height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            # Scale by height
            scale = target_height / img_height
            new_width = int(img_width * scale)
            img = img.resize((new_width, target_height), Image.LANCZOS)
            # Center crop width
            left = (new_width - target_width) // 2
            img = img.crop((left, 0, left + target_width, target_height))
        else:
            # Scale by width
            scale = target_width / img_width
            new_height = int(img_height * scale)
            img = img.resize((target_width, new_height), Image.LANCZOS)
            # Center crop height
            top = (new_height - target_height) // 2
            img = img.crop((0, top, target_width, top + target_height))
    
    else:  # contain (default)
        # Scale to fit inside with letterboxing
        img_ratio = img_width / img_height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            # Scale by width
            new_width = target_width
            new_height = int(target_width / img_ratio)
        else:
            # Scale by height
            new_height = target_height
            new_width = int(target_height * img_ratio)
        
        img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Create background with letterboxing
        background = Image.new('RGB', (target_width, target_height), background_color)
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        background.paste(img, (paste_x, paste_y))
        img = background
    
    # Convert PIL image to numpy array for MoviePy
    img_array = np.array(img)
    
    # Create ImageClip
    clip = ImageClip(img_array, duration=duration)
    
    return clip


def _add_text_overlays(clip: ImageClip, text_overlays: List[Dict[str, Any]], 
                      image_index: int, start_time: float) -> CompositeVideoClip:
    """Add text overlays to an image clip"""
    
    text_clips = [clip]
    
    for overlay in text_overlays:
        # Check if this overlay applies to this image
        if 'image_indices' in overlay and image_index not in overlay['image_indices']:
            continue
        
        text = overlay.get('text', '')
        if not text:
            continue
        
        # Text properties
        fontsize = overlay.get('fontsize', 50)
        color = overlay.get('color', 'white')
        font = overlay.get('font', 'Arial')
        position = overlay.get('position', 'center')
        
        # Timing
        text_start = overlay.get('start_time', 0)
        text_duration = overlay.get('duration', clip.duration)
        
        # Create text clip
        text_clip = TextClip(
            text,
            fontsize=fontsize,
            color=color,
            font=font
        ).set_position(position).set_start(text_start).set_duration(text_duration)
        
        text_clips.append(text_clip)
    
    if len(text_clips) > 1:
        return CompositeVideoClip(text_clips)
    else:
        return clip


def _apply_effects(clip: ImageClip, effects: List[Dict[str, Any]]) -> VideoClip:
    """Apply various effects to an image clip"""
    
    current_clip = clip
    
    for effect in effects:
        effect_type = effect.get('type', '')
        
        if effect_type == 'fade_in':
            duration = effect.get('duration', 1.0)
            current_clip = current_clip.fadein(duration)
        
        elif effect_type == 'fade_out':
            duration = effect.get('duration', 1.0)
            current_clip = current_clip.fadeout(duration)
        
        elif effect_type == 'zoom':
            zoom_factor = effect.get('factor', 1.2)
            # Use a custom zoom implementation to avoid MoviePy's resize issue
            def zoom_image(image):
                # Create a zoomed version using PIL instead of MoviePy's resize
                h, w = image.shape[:2]
                new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
                
                # Convert numpy array to PIL Image
                pil_image = Image.fromarray(image.astype('uint8'))
                
                # Resize with PIL
                zoomed_pil = pil_image.resize((new_w, new_h), Image.LANCZOS)
                
                # Center crop back to original size
                if zoom_factor > 1.0:
                    left = (new_w - w) // 2
                    top = (new_h - h) // 2
                    zoomed_pil = zoomed_pil.crop((left, top, left + w, top + h))
                
                return np.array(zoomed_pil)
            
            current_clip = current_clip.fl_image(zoom_image)
        
        elif effect_type == 'pan':
            direction = effect.get('direction', 'right')  # 'left', 'right', 'up', 'down'
            distance = effect.get('distance', 100)
            
            if direction == 'right':
                current_clip = current_clip.set_position(lambda t: (distance * t / clip.duration, 'center'))
            elif direction == 'left':
                current_clip = current_clip.set_position(lambda t: (-distance * t / clip.duration, 'center'))
            elif direction == 'down':
                current_clip = current_clip.set_position(lambda t: ('center', distance * t / clip.duration))
            elif direction == 'up':
                current_clip = current_clip.set_position(lambda t: ('center', -distance * t / clip.duration))
        
        elif effect_type == 'rotate':
            angle = effect.get('angle', 0)
            current_clip = current_clip.rotate(angle)
        
        elif effect_type == 'brightness':
            factor = effect.get('factor', 1.0)
            current_clip = current_clip.fl_image(lambda img: np.clip(img * factor, 0, 255).astype(np.uint8))
        
        elif effect_type == 'blur':
            radius = effect.get('radius', 2)
            # Note: Blur effect would require additional image processing
            pass
    
    return current_clip


def _add_transitions(clips: List[VideoClip], transition_type: str, 
                    transition_duration: float) -> List[VideoClip]:
    """Add transitions between clips"""
    
    if len(clips) < 2:
        return clips
    
    transitioned_clips = []
    
    for i in range(len(clips)):
        clip = clips[i]
        
        if i == 0:
            # First clip - only fade out at the end if there's a next clip
            if transition_type in ['fade', 'crossfade']:
                clip = clip.fadeout(transition_duration)
            transitioned_clips.append(clip)
        
        elif i == len(clips) - 1:
            # Last clip - only fade in at the beginning
            if transition_type in ['fade', 'crossfade']:
                clip = clip.fadein(transition_duration)
                # Offset the start time to overlap with previous clip
                clip = clip.set_start(sum(c.duration for c in transitioned_clips) - transition_duration)
            else:
                clip = clip.set_start(sum(c.duration for c in transitioned_clips))
            transitioned_clips.append(clip)
        
        else:
            # Middle clips - fade in and out
            if transition_type in ['fade', 'crossfade']:
                clip = clip.fadein(transition_duration).fadeout(transition_duration)
                # Offset the start time to overlap with previous clip
                clip = clip.set_start(sum(c.duration for c in transitioned_clips) - transition_duration)
            else:
                clip = clip.set_start(sum(c.duration for c in transitioned_clips))
            transitioned_clips.append(clip)
    
    return transitioned_clips


def create_image_slideshow(image_paths: List[str],
                          output_path: str,
                          duration_per_image: float = 3.0,
                          fps: int = 24,
                          resolution_width: int = 1920,
                          resolution_height: int = 1080,
                          transition_type: str = "fade",
                          transition_duration: float = 0.5,
                          background_color_r: int = 0,
                          background_color_g: int = 0,
                          background_color_b: int = 0,
                          fit_mode: str = "contain",
                          audio_path: Optional[str] = None,
                          text_overlays: Optional[List[Dict[str, Any]]] = None,
                          effects: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Main function to convert images to video slideshow.
    
    Args:
        image_paths: List of paths to image files
        output_path: Path where the video will be saved
        duration_per_image: Duration each image is displayed (seconds)
        fps: Frames per second for output video
        resolution: Output video resolution (width, height)
        transition_type: Type of transition ("fade", "slide_left", "slide_right", "slide_up", "slide_down", "zoom", "crossfade", "none")
        transition_duration: Duration of transitions (seconds)
        background_color: RGB background color for letterboxing
        fit_mode: How to fit images ("contain", "cover", "stretch", "crop")
        audio_path: Optional path to audio file to add as background
        text_overlays: List of text overlay configurations with format:
            [
                {
                    "text": "Caption text",
                    "fontsize": 50,
                    "color": "white",
                    "font": "Arial",
                    "position": "center",  # or ('center', 'bottom'), (50, 100), etc.
                    "start_time": 0,
                    "duration": 3.0,
                    "image_indices": [0, 1]  # Optional: which images to show text on
                }
            ]
        effects: List of effects to apply with format:
            [
                {
                    "type": "fade_in",
                    "duration": 1.0
                },
                {
                    "type": "zoom",
                    "factor": 1.2
                },
                {
                    "type": "pan",
                    "direction": "right",
                    "distance": 100
                }
            ]
    
    Returns:
        Dict with status, message, and output info
    
    Example usage:
        result = create_image_slideshow(
            image_paths=["/path/to/image1.jpg", "/path/to/image2.png"],
            output_path="/path/to/output.mp4",
            duration_per_image=4.0,
            transition_type="fade",
            text_overlays=[
                {
                    "text": "Beautiful Sunset",
                    "position": "bottom",
                    "fontsize": 60,
                    "color": "yellow"
                }
            ],
            effects=[
                {"type": "fade_in", "duration": 1.0},
                {"type": "zoom", "factor": 1.1}
            ]
        )
    """
    return create_slideshow_from_images(
        image_paths=image_paths,
        output_path=output_path,
        duration_per_image=duration_per_image,
        fps=fps,
        resolution_width=resolution_width,
        resolution_height=resolution_height,
        transition_type=transition_type,
        transition_duration=transition_duration,
        background_color_r=background_color_r,
        background_color_g=background_color_g,
        background_color_b=background_color_b,
        fit_mode=fit_mode,
        audio_path=audio_path,
        text_overlays=text_overlays,
        effects=effects
    )


def create_simple_slideshow(image_paths: List[str], output_path: str, duration_per_image: float = 3.0) -> Dict[str, Any]:
    """
    Simplified function to create a basic slideshow with default settings.
    
    Args:
        image_paths: List of paths to image files
        output_path: Path where the video will be saved
        duration_per_image: Duration each image is displayed (seconds)
    
    Returns:
        Dict with status, message, and output info
    """
    return create_slideshow_from_images(
        image_paths=image_paths,
        output_path=output_path,
        duration_per_image=duration_per_image,
        transition_type="fade",
        fit_mode="contain"
    )


def add_text_to_images(image_paths: List[str], 
                      output_dir: str,
                      texts: List[str],
                      text_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Add text overlays to images and save them as new image files.
    
    Args:
        image_paths: List of paths to input images
        output_dir: Directory to save processed images
        texts: List of text strings to overlay (one per image)
        text_config: Configuration for text appearance
    
    Returns:
        Dict with status, message, and list of output files
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        if len(texts) != len(image_paths):
            return {
                "status": "error",
                "message": "Number of texts must match number of images",
                "output_files": []
            }
        
        # Default text configuration
        default_config = {
            "font_size": 48,
            "font_color": (255, 255, 255),  # White
            "position": "bottom",  # "top", "bottom", "center", or (x, y) tuple
            "margin": 50,
            "outline_color": (0, 0, 0),  # Black outline
            "outline_width": 2
        }
        
        if text_config:
            default_config.update(text_config)
        
        output_files = []
        
        for i, (img_path, text) in enumerate(zip(image_paths, texts)):
            if not os.path.exists(img_path):
                continue
                
            # Load image
            img = Image.open(img_path)
            draw = ImageDraw.Draw(img)
            
            # Try to load a font, fall back to default if not available
            try:
                font = ImageFont.truetype("Arial.ttf", default_config["font_size"])
            except:
                font = ImageFont.load_default()
            
            # Calculate text position
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            img_width, img_height = img.size
            
            if default_config["position"] == "top":
                x = (img_width - text_width) // 2
                y = default_config["margin"]
            elif default_config["position"] == "bottom":
                x = (img_width - text_width) // 2
                y = img_height - text_height - default_config["margin"]
            elif default_config["position"] == "center":
                x = (img_width - text_width) // 2
                y = (img_height - text_height) // 2
            elif isinstance(default_config["position"], tuple):
                x, y = default_config["position"]
            else:
                x = (img_width - text_width) // 2
                y = img_height - text_height - default_config["margin"]
            
            # Draw outline if specified
            if default_config["outline_width"] > 0:
                for dx in range(-default_config["outline_width"], default_config["outline_width"] + 1):
                    for dy in range(-default_config["outline_width"], default_config["outline_width"] + 1):
                        if dx != 0 or dy != 0:
                            draw.text((x + dx, y + dy), text, font=font, fill=default_config["outline_color"])
            
            # Draw main text
            draw.text((x, y), text, font=font, fill=default_config["font_color"])
            
            # Save processed image
            output_filename = f"text_overlay_{i}_{Path(img_path).name}"
            output_path = os.path.join(output_dir, output_filename)
            img.save(output_path)
            output_files.append(output_path)
        
        return {
            "status": "success",
            "message": f"Successfully added text to {len(output_files)} images",
            "output_files": output_files
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error adding text to images: {str(e)}",
            "output_files": []
        }