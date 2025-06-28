"""
Video Generation Tools Package

This package contains comprehensive tools for video creation, editing, and processing:
- Image processing and slideshow creation
- Video editing and manipulation
- YouTube integration and content extraction
- Audio synchronization and processing

All tools follow ADK (Agent Development Kit) standards for:
- Comprehensive type hints
- Detailed docstrings
- Consistent return structures with status indicators
- SOLID design principles
"""

from . import image
from . import video
from . import youtube

__all__ = [
    'image',
    'video', 
    'youtube'
]
