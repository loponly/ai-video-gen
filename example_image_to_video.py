#!/usr/bin/env python3
"""
Image to Video Conversion Example
=================================

This script demonstrates how to use the image_editor_tools module to create
video slideshows from images with various features like transitions, text
overlays, and effects.

Usage:
    python example_image_to_video.py

Make sure to have some sample images in a folder before running this script.
"""

import os
import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent / "tools"))

try:
    from image_editor_tools import (
        create_slideshow_from_images,
        create_simple_slideshow,
        add_text_to_images
    )
    from PIL import Image
    import tempfile
    print("✅ All required modules imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure to install requirements: pip install -r requirements.txt")
    sys.exit(1)


def create_sample_images():
    """Create sample images for demonstration"""
    temp_dir = tempfile.mkdtemp(prefix="image_video_demo_")
    print(f"📁 Creating sample images in: {temp_dir}")
    
    sample_images = []
    colors = [
        (255, 100, 100, "Red Sky"),
        (100, 255, 100, "Green Fields"),
        (100, 100, 255, "Blue Ocean"),
        (255, 255, 100, "Golden Sunset")
    ]
    
    for i, (r, g, b, name) in enumerate(colors):
        # Create a gradient image
        img = Image.new('RGB', (800, 600), (r, g, b))
        
        # Add some visual interest with gradient
        pixels = img.load()
        for x in range(800):
            for y in range(600):
                # Simple gradient effect
                factor = (x + y) / (800 + 600)
                new_r = int(r * (0.5 + 0.5 * factor))
                new_g = int(g * (0.5 + 0.5 * factor))
                new_b = int(b * (0.5 + 0.5 * factor))
                pixels[x, y] = (new_r, new_g, new_b)
        
        img_path = os.path.join(temp_dir, f"sample_{i+1}_{name.lower().replace(' ', '_')}.jpg")
        img.save(img_path, quality=95)
        sample_images.append(img_path)
        print(f"  ✅ Created: {name} -> {os.path.basename(img_path)}")
    
    return temp_dir, sample_images


def demo_basic_slideshow(images, output_dir):
    """Demonstrate basic slideshow creation"""
    print("\n🎬 Creating basic slideshow...")
    
    output_path = os.path.join(output_dir, "basic_slideshow.mp4")
    
    result = create_simple_slideshow(
        image_paths=images,
        output_path=output_path,
        duration_per_image=2.0
    )
    
    if result["status"] == "success":
        print(f"  ✅ Basic slideshow created: {output_path}")
        print(f"  📊 Duration: {result['duration']:.1f}s, Images: {result['images_count']}")
    else:
        print(f"  ❌ Error: {result['message']}")
    
    return result


def demo_advanced_slideshow(images, output_dir):
    """Demonstrate advanced slideshow with transitions and effects"""
    print("\n🎬 Creating advanced slideshow with transitions and effects...")
    
    output_path = os.path.join(output_dir, "advanced_slideshow.mp4")
    
    # Define text overlays for each image
    text_overlays = [
        {
            "text": "Beautiful Red Sky",
            "position": "center",
            "font_size": 48,
            "color": "white",
            "start_time": 0,
            "duration": 3
        },
        {
            "text": "Peaceful Green Fields", 
            "position": "bottom",
            "font_size": 36,
            "color": "yellow",
            "start_time": 0,
            "duration": 3
        }
    ]
    
    # Define effects
    effects = [
        {"type": "fade_in", "duration": 0.5},
        {"type": "fade_out", "duration": 0.5},
        {"type": "zoom", "factor": 1.1}
    ]
    
    result = create_slideshow_from_images(
        image_paths=images[:2],  # Use first 2 images for demo
        output_path=output_path,
        duration_per_image=3.0,
        fps=30,
        resolution=(1920, 1080),
        transition_type="fade",
        transition_duration=1.0,
        text_overlays=text_overlays,
        effects=effects,
        fit_mode="contain"
    )
    
    if result["status"] == "success":
        print(f"  ✅ Advanced slideshow created: {output_path}")
        print(f"  📊 Duration: {result['duration']:.1f}s, Resolution: {result['resolution']}")
        print(f"  🎨 Features: transitions, text overlays, effects")
    else:
        print(f"  ❌ Error: {result['message']}")
    
    return result


def demo_text_overlay_images(images, output_dir):
    """Demonstrate adding text overlays to images"""
    print("\n🎨 Adding text overlays to images...")
    
    texts = [
        "Sample Image 1",
        "Sample Image 2", 
        "Sample Image 3",
        "Sample Image 4"
    ]
    
    result = add_text_to_images(
        image_paths=images,
        output_dir=os.path.join(output_dir, "text_overlay_images"),
        texts=texts,
        text_config={
            "font_size": 36,
            "color": "white",
            "position": "bottom"
        }
    )
    
    if result["status"] == "success":
        print(f"  ✅ Text overlay images created in: text_overlay_images/")
        print(f"  📁 Files: {len(result['output_files'])} images with text")
    else:
        print(f"  ❌ Error: {result['message']}")
    
    return result


def main():
    """Main demonstration function"""
    print("🎥 IMAGE TO VIDEO CONVERSION DEMO")
    print("=" * 50)
    
    # Create sample images
    temp_dir, sample_images = create_sample_images()
    
    try:
        # Demo 1: Basic slideshow
        demo_basic_slideshow(sample_images, temp_dir)
        
        # Demo 2: Advanced slideshow
        demo_advanced_slideshow(sample_images, temp_dir)
        
        # Demo 3: Text overlay on images
        demo_text_overlay_images(sample_images, temp_dir)
        
        print("\n🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"📁 Output files saved in: {temp_dir}")
        print("\n📝 Generated files:")
        for file in os.listdir(temp_dir):
            if file.endswith(('.mp4', '.jpg')):
                print(f"  - {file}")
        
        # Check for subdirectory
        text_dir = os.path.join(temp_dir, "text_overlay_images")
        if os.path.exists(text_dir):
            print("  - text_overlay_images/")
            for file in os.listdir(text_dir):
                print(f"    - {file}")
        
        print(f"\n💡 You can view the videos using any video player")
        print(f"💡 Temporary files location: {temp_dir}")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    return temp_dir


if __name__ == "__main__":
    output_dir = main()
    print(f"\n🔗 Demo files available at: {output_dir}")
