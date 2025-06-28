#!/usr/bin/env python3
"""
Quick Functional Test for Newly Fixed Tools
==========================================

Tests the newly updated tools to ensure they work correctly
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from tools.youtube import download_youtube_video, convert_webm_to_mp4


def test_download_youtube_video():
    """Test download_youtube_video function with invalid inputs"""
    print("🔍 Testing download_youtube_video...")
    
    # Test with invalid URL
    result = download_youtube_video("invalid_url")
    assert result["status"] == "error"
    assert "Invalid YouTube URL format" in result["message"]
    print("  ✅ Handles invalid URL correctly")
    
    # Test with empty URL
    result = download_youtube_video("")
    assert result["status"] == "error"
    print("  ✅ Handles empty URL correctly")
    
    print("  📊 download_youtube_video tests passed!")


def test_convert_webm_to_mp4():
    """Test convert_webm_to_mp4 function with invalid inputs"""
    print("\n🔍 Testing convert_webm_to_mp4...")
    
    # Test with non-existent file
    result = convert_webm_to_mp4("nonexistent.webm")
    assert result["status"] == "error"
    assert "Input file not found" in result["message"]
    print("  ✅ Handles non-existent file correctly")
    
    # Create a temporary file with wrong extension to test extension validation
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        temp_file.write(b"test")
        temp_file_path = temp_file.name
    
    try:
        result = convert_webm_to_mp4(temp_file_path)
        assert result["status"] == "error" 
        assert "WebM file" in result["message"]
        print("  ✅ Handles wrong file extension correctly")
    finally:
        os.unlink(temp_file_path)
    
    print("  📊 convert_webm_to_mp4 tests passed!")


if __name__ == "__main__":
    print("🧪 FUNCTIONAL TESTS FOR NEWLY FIXED TOOLS")
    print("=" * 45)
    
    test_download_youtube_video()
    test_convert_webm_to_mp4()
    
    print("\n🏆 All functional tests passed!")
    print("✅ Newly fixed tools are working correctly")
