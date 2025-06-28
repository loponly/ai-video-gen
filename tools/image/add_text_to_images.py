"""
Add text overlays to images functionality
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def add_text_to_images(image_paths: List[str], 
                      output_dir: str,
                      texts: List[str],
                      text_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Add text overlays to images and save them as new image files.
    
    Use this tool when you need to add captions, titles, or annotations to images.
    The tool supports customizable text styling including font size, color, position,
    and outline effects for better readability.
    
    Args:
        image_paths: List of absolute paths to input image files.
                    Supported formats: JPG, PNG, BMP, TIFF.
        output_dir: Absolute path to directory where processed images will be saved.
                   Directory will be created if it doesn't exist.
        texts: List of text strings to overlay on images.
              Must have same length as image_paths (one text per image).
        text_config: Optional configuration for text appearance.
                    Supported options: 'font_size', 'font_color', 'position',
                    'margin', 'outline_color', 'outline_width'.
                    If None, uses default styling.
    
    Returns:
        A dictionary containing the text overlay result:
        - status: 'success' if all images processed, 'error' if failed
        - message: Descriptive message about the operation result
        - output_files: List of paths to created image files (empty if error)
        - images_processed: Number of images successfully processed (if success)
        
        Example success: {'status': 'success', 'message': 'Successfully added text to 3 images',
                         'output_files': ['/path/to/image1_text.jpg'], 'images_processed': 3}
        Example error: {'status': 'error', 'message': 'Number of texts must match number of images',
                       'output_files': []}
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
