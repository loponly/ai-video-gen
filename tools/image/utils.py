"""
Utility functions for image processing and video creation
"""

from typing import List, Dict, Any, Tuple
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, VideoClip
from PIL import Image
import numpy as np


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
