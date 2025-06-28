"""
PIL/Pillow compatibility patch for MoviePy

This module provides compatibility fixes for newer versions of Pillow
where ANTIALIAS was deprecated and removed.
"""

try:
    from PIL import Image
    
    # Fix for Pillow >= 10.0.0 where ANTIALIAS was removed
    if not hasattr(Image, 'ANTIALIAS'):
        if hasattr(Image, 'Resampling'):
            # Use the new Resampling enum
            Image.ANTIALIAS = Image.Resampling.LANCZOS
        else:
            # Fallback to LANCZOS if available
            Image.ANTIALIAS = getattr(Image, 'LANCZOS', 1)
            
except ImportError:
    # PIL/Pillow not available, nothing to fix
    pass
