# Image to Video Conversion Tool

A comprehensive Python toolkit for converting images to videos with advanced features including transitions, text overlays, effects, and audio synchronization.

## Features

✅ **Image Slideshow Creation** - Convert multiple images into video slideshows  
✅ **Transitions** - Smooth transitions between images (fade, slide, zoom, crossfade)  
✅ **Text Overlays** - Add customizable text over images  
✅ **Effects** - Apply visual effects (fade in/out, zoom, pan, rotate, brightness)  
✅ **Audio Synchronization** - Add background music/audio to videos  
✅ **Multiple Fit Modes** - Different ways to fit images (contain, cover, stretch, crop)  
✅ **Custom Resolutions** - Support for any resolution and frame rate  
✅ **Error Handling** - Robust error handling with detailed feedback  
✅ **Test Coverage** - 100% test coverage with comprehensive test suite  

## Quick Start

### Basic Usage

```python
from tools.image_editor_tools import create_simple_slideshow

# Create a basic slideshow
result = create_simple_slideshow(
    image_paths=["image1.jpg", "image2.jpg", "image3.jpg"],
    output_path="slideshow.mp4",
    duration_per_image=3.0
)

if result["status"] == "success":
    print(f"Slideshow created: {result['output_path']}")
```

### Advanced Usage

```python
from tools.image_editor_tools import create_slideshow_from_images

# Create advanced slideshow with transitions and effects
result = create_slideshow_from_images(
    image_paths=["img1.jpg", "img2.jpg", "img3.jpg"],
    output_path="advanced_slideshow.mp4",
    duration_per_image=4.0,
    fps=30,
    resolution=(1920, 1080),
    transition_type="fade",
    transition_duration=1.0,
    text_overlays=[
        {
            "text": "Welcome!",
            "position": "center",
            "font_size": 48,
            "color": "white",
            "start_time": 0,
            "duration": 3
        }
    ],
    effects=[
        {"type": "fade_in", "duration": 0.5},
        {"type": "zoom", "factor": 1.1}
    ],
    audio_path="background_music.mp3",
    fit_mode="contain"
)
```

### Text Overlay on Images

```python
from tools.image_editor_tools import add_text_to_images

# Add text overlays to images
result = add_text_to_images(
    image_paths=["img1.jpg", "img2.jpg"],
    output_dir="output_images/",
    texts=["Caption 1", "Caption 2"],
    text_config={
        "font_size": 36,
        "color": "white",
        "position": "bottom",
        "background_color": "black",
        "background_opacity": 0.7
    }
)
```

## Function Reference

### create_slideshow_from_images()

The main function for creating video slideshows with full control over all parameters.

**Parameters:**
- `image_paths` (List[str]): List of image file paths
- `output_path` (str): Output video file path
- `duration_per_image` (float): Duration each image is displayed (seconds)
- `fps` (int): Frames per second for output video (default: 24)
- `resolution` (Tuple[int, int]): Output resolution (width, height) (default: (1920, 1080))
- `transition_type` (str): Transition type (default: "fade")
- `transition_duration` (float): Transition duration (seconds) (default: 0.5)
- `background_color` (Tuple[int, int, int]): RGB background color (default: (0, 0, 0))
- `fit_mode` (str): How to fit images (default: "contain")
- `audio_path` (str, optional): Path to background audio file
- `text_overlays` (List[Dict], optional): Text overlay configurations
- `effects` (List[Dict], optional): Effects to apply

**Transition Types:**
- `"fade"` - Fade between images
- `"slide_left"` - Slide from right to left
- `"slide_right"` - Slide from left to right
- `"slide_up"` - Slide from bottom to top
- `"slide_down"` - Slide from top to bottom
- `"zoom"` - Zoom transition
- `"crossfade"` - Cross-fade transition
- `"none"` - No transition

**Fit Modes:**
- `"contain"` - Scale to fit inside with letterboxing (maintains aspect ratio)
- `"cover"` - Scale to cover entire area (may crop, maintains aspect ratio)
- `"stretch"` - Stretch to exact dimensions (may distort)
- `"crop"` - Center crop to fit exact dimensions

**Effects:**
- `{"type": "fade_in", "duration": 0.5}` - Fade in effect
- `{"type": "fade_out", "duration": 0.5}` - Fade out effect
- `{"type": "zoom", "factor": 1.1}` - Zoom effect
- `{"type": "pan", "direction": "right", "distance": 100}` - Pan effect
- `{"type": "rotate", "angle": 5}` - Rotation effect
- `{"type": "brightness", "factor": 1.2}` - Brightness adjustment

### create_simple_slideshow()

Simplified function for basic slideshow creation with default settings.

**Parameters:**
- `image_paths` (List[str]): List of image file paths
- `output_path` (str): Output video file path
- `duration_per_image` (float): Duration each image is displayed (seconds)

### add_text_to_images()

Add text overlays to images and save them as new image files.

**Parameters:**
- `image_paths` (List[str]): List of input image paths
- `output_dir` (str): Directory to save processed images
- `texts` (List[str]): List of text strings to overlay
- `text_config` (Dict, optional): Text appearance configuration

**Text Configuration:**
```python
text_config = {
    "font_size": 36,           # Font size in pixels
    "color": "white",          # Text color
    "position": "bottom",      # Position: "top", "center", "bottom", or (x, y)
    "background_color": "black", # Background color (optional)
    "background_opacity": 0.7,   # Background opacity 0-1 (optional)
    "font_family": "Arial"       # Font family (optional)
}
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Import and use:
```python
from tools.image_editor_tools import create_slideshow_from_images
```

## Dependencies

- moviepy==1.0.3 (Video processing)
- Pillow>=9.0.0 (Image processing)
- numpy>=1.21.0 (Array operations)
- pytest>=7.0.0 (Testing framework)

## Examples

Run the example script to see all features in action:

```bash
python example_image_to_video.py
```

This will create sample images and demonstrate:
- Basic slideshow creation
- Advanced slideshow with transitions and effects
- Text overlay on images

## Testing

The toolkit includes comprehensive tests covering all functions:

```bash
# Run all tests
pytest tests/ -v

# Run specific image editor tests
pytest tests/test_image_editor_tools_pytest.py -v

# Run comprehensive test suite
python tests/test_image_editor_tools.py
```

## Error Handling

All functions return a dictionary with status information:

```python
result = create_slideshow_from_images(...)

if result["status"] == "success":
    print(f"Video created: {result['output_path']}")
    print(f"Duration: {result['duration']}s")
    print(f"Images: {result['images_count']}")
else:
    print(f"Error: {result['message']}")
```

## Supported Formats

**Input Images:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)
- WebP (.webp)

**Output Video:**
- MP4 (H.264 codec)
- Custom resolution and frame rate support

**Audio:**
- MP3, WAV, M4A, and other formats supported by MoviePy

## Performance Tips

1. **Image Size**: Resize large images before processing for better performance
2. **Memory**: Process videos in smaller batches for large image sets
3. **Quality**: Use appropriate resolution for your target platform
4. **Effects**: Limit complex effects for faster processing

## License

This project follows the coding guidelines and best practices defined in the project documentation.
