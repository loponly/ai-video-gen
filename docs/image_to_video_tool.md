# Image-to-Video Conversion Tool

A comprehensive tool for converting images to video slideshows with advanced features including transitions, text overlays, effects, and audio synchronization.

## Features

- **Multiple Image Formats**: Support for JPG, PNG, BMP, GIF, TIFF, WebP
- **Flexible Sizing**: Multiple fit modes (contain, cover, stretch, crop)
- **Smooth Transitions**: Fade, crossfade, slide, zoom transitions
- **Text Overlays**: Customizable text with fonts, colors, and positioning
- **Visual Effects**: Fade in/out, zoom, pan, rotate, brightness adjustment
- **Audio Support**: Background music with looping and trimming
- **High Quality Output**: Customizable resolution, FPS, and codecs

## Installation

Ensure you have the required dependencies installed:

```bash
pip install moviepy Pillow numpy
```

## Basic Usage

### Simple Slideshow

```python
from tools.image_editor_tools import create_simple_slideshow

result = create_simple_slideshow(
    image_paths=[
        "/path/to/image1.jpg",
        "/path/to/image2.png",
        "/path/to/image3.jpg"
    ],
    output_path="/path/to/output.mp4",
    duration_per_image=3.0
)

print(result)
```

### Advanced Slideshow

```python
from tools.image_editor_tools import create_image_slideshow

# Define text overlays
text_overlays = [
    {
        "text": "Beautiful Sunset",
        "fontsize": 60,
        "color": "white",
        "position": ("center", "bottom"),
        "duration": 3.0,
        "image_indices": [0]  # Show on first image only
    },
    {
        "text": "Mountain View",
        "fontsize": 50,
        "color": "yellow",
        "position": "center",
        "duration": 3.0,
        "image_indices": [1]  # Show on second image only
    }
]

# Define effects
effects = [
    {"type": "fade_in", "duration": 1.0},
    {"type": "fade_out", "duration": 1.0},
    {"type": "zoom", "factor": 1.1}
]

result = create_image_slideshow(
    image_paths=[
        "/path/to/image1.jpg",
        "/path/to/image2.png",
        "/path/to/image3.jpg"
    ],
    output_path="/path/to/slideshow.mp4",
    duration_per_image=4.0,
    fps=30,
    resolution=(1920, 1080),
    transition_type="fade",
    transition_duration=0.5,
    background_color=(0, 0, 0),
    fit_mode="contain",
    audio_path="/path/to/background_music.mp3",
    text_overlays=text_overlays,
    effects=effects
)
```

## Parameters

### Main Function: `create_image_slideshow()`

- **image_paths** (List[str]): List of paths to image files
- **output_path** (str): Path where the video will be saved
- **duration_per_image** (float): Duration each image is displayed (seconds) [default: 3.0]
- **fps** (int): Frames per second for output video [default: 24]
- **resolution** (Tuple[int, int]): Output video resolution (width, height) [default: (1920, 1080)]
- **transition_type** (str): Type of transition [default: "fade"]
- **transition_duration** (float): Duration of transitions (seconds) [default: 0.5]
- **background_color** (Tuple[int, int, int]): RGB background color [default: (0, 0, 0)]
- **fit_mode** (str): How to fit images [default: "contain"]
- **audio_path** (Optional[str]): Path to audio file for background music
- **text_overlays** (Optional[List[Dict]]): List of text overlay configurations
- **effects** (Optional[List[Dict]]): List of effects to apply

### Transition Types

- `"fade"`: Cross-fade between images
- `"crossfade"`: Smooth crossfade transition
- `"slide_left"`: Slide from right to left
- `"slide_right"`: Slide from left to right
- `"slide_up"`: Slide from bottom to top
- `"slide_down"`: Slide from top to bottom
- `"zoom"`: Zoom transition effect
- `"none"`: No transition (hard cuts)

### Fit Modes

- `"contain"`: Scale to fit inside with letterboxing (preserves aspect ratio)
- `"cover"`: Scale to cover entire area (may crop, preserves aspect ratio)
- `"stretch"`: Stretch to fit exactly (may distort)
- `"crop"`: Center crop to fit exactly

### Text Overlay Configuration

```python
{
    "text": "Your caption text",
    "fontsize": 50,                    # Font size in pixels
    "color": "white",                  # Font color (name or hex)
    "font": "Arial",                   # Font family name
    "position": "center",              # Position: "top", "bottom", "center", or (x, y) tuple
    "start_time": 0,                   # When to start showing text (seconds)
    "duration": 3.0,                   # How long to show text (seconds)
    "image_indices": [0, 1]            # Optional: which images to show text on
}
```

### Effects Configuration

```python
# Fade in effect
{"type": "fade_in", "duration": 1.0}

# Fade out effect  
{"type": "fade_out", "duration": 1.0}

# Zoom effect
{"type": "zoom", "factor": 1.2}

# Pan effect
{
    "type": "pan", 
    "direction": "right",  # "left", "right", "up", "down"
    "distance": 100
}

# Rotate effect
{"type": "rotate", "angle": 15}

# Brightness adjustment
{"type": "brightness", "factor": 1.2}
```

## Output Format

The function returns a dictionary with the following structure:

```python
{
    "status": "success" | "error",
    "message": "Descriptive message",
    "output_path": "/path/to/output.mp4" | None,
    "duration": 12.0,              # Total video duration in seconds
    "resolution": (1920, 1080),    # Output resolution
    "fps": 30,                     # Frames per second
    "images_count": 4              # Number of images processed
}
```

## Error Handling

The tool includes comprehensive error handling for:

- Missing or invalid image files
- Unsupported image formats
- Invalid parameters
- File I/O errors
- Video encoding errors

All errors are returned in the result dictionary with `"status": "error"` and a descriptive message.

## Examples

### Example 1: Travel Photo Slideshow

```python
result = create_image_slideshow(
    image_paths=[
        "photos/paris.jpg",
        "photos/london.jpg", 
        "photos/rome.jpg"
    ],
    output_path="travel_slideshow.mp4",
    duration_per_image=5.0,
    transition_type="fade",
    transition_duration=1.0,
    text_overlays=[
        {"text": "Paris, France", "position": "bottom", "fontsize": 48, "image_indices": [0]},
        {"text": "London, UK", "position": "bottom", "fontsize": 48, "image_indices": [1]},
        {"text": "Rome, Italy", "position": "bottom", "fontsize": 48, "image_indices": [2]}
    ],
    effects=[
        {"type": "fade_in", "duration": 0.5},
        {"type": "zoom", "factor": 1.05}
    ],
    audio_path="background_music.mp3"
)
```

### Example 2: Product Showcase

```python
result = create_image_slideshow(
    image_paths=[
        "products/product1.png",
        "products/product2.png",
        "products/product3.png"
    ],
    output_path="product_showcase.mp4",
    duration_per_image=3.0,
    resolution=(1280, 720),
    fit_mode="contain",
    background_color=(255, 255, 255),  # White background
    transition_type="slide_left",
    text_overlays=[
        {"text": "New Product Line", "position": "top", "fontsize": 60, "color": "blue"}
    ]
)
```

## Tips and Best Practices

1. **Image Quality**: Use high-resolution images for better output quality
2. **Consistent Aspect Ratios**: Use images with similar aspect ratios for better visual flow
3. **Audio Synchronization**: Ensure audio duration matches or exceeds video duration
4. **Text Readability**: Use contrasting colors and appropriate font sizes for text overlays
5. **Transition Timing**: Keep transitions short (0.3-1.0 seconds) for professional look
6. **File Formats**: PNG files provide better quality for graphics, JPG for photographs
7. **Performance**: Reduce resolution for faster processing during development, increase for final output
