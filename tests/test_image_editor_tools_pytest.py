#!/usr/bin/env python3
"""
Pytest Test Suite for Image Editor Tools
========================================

Tests all functions in image_editor_tools.py using pytest framework.
Run with: pytest tests/test_image_editor_tools_pytest.py -v
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import pytest

# Add the tools and project directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from tools.image_editor_tools import (
    create_slideshow_from_images,
    create_image_slideshow,
    create_simple_slideshow,
    add_text_to_images,
    _create_image_clip,
    _add_text_overlays,
    _apply_effects,
    _add_transitions
)


@pytest.fixture
def test_environment():
    """Pytest fixture to create test environment with sample images"""
    # Create temporary directory
    test_dir = tempfile.mkdtemp(prefix="image_editor_test_")
    
    # Create sample images
    test_images = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow
    
    for i, color in enumerate(colors):
        # Create a simple colored image
        img = Image.new('RGB', (640, 480), color)
        img_path = os.path.join(test_dir, f"test_image_{i+1}.jpg")
        img.save(img_path)
        test_images.append(img_path)
    
    yield {
        'test_dir': test_dir,
        'test_images': test_images
    }
    
    # Cleanup
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


class TestImageEditorTools:
    """Test class for image editor tools using pytest"""
    
    def test_create_slideshow_from_images_basic(self, test_environment):
        """Test basic slideshow creation"""
        test_data = test_environment
        output_path = os.path.join(test_data['test_dir'], "test_slideshow_basic.mp4")
        
        result = create_slideshow_from_images(
            image_paths=test_data['test_images'][:2],
            output_path=output_path,
            duration_per_image=2.0,
            fps=24,
            resolution=(1280, 720),
            transition_type="none"
        )
        
        assert result["status"] == "success"
        assert os.path.exists(output_path)
        assert result["images_count"] == 2
        assert result["duration"] > 0
        assert result["resolution"] == (1280, 720)
        assert result["fps"] == 24
    
    def test_create_slideshow_with_transitions(self, test_environment):
        """Test slideshow with fade transitions"""
        test_data = test_environment
        output_path = os.path.join(test_data['test_dir'], "test_slideshow_transitions.mp4")
        
        result = create_slideshow_from_images(
            image_paths=test_data['test_images'][:3],
            output_path=output_path,
            duration_per_image=2.0,
            transition_type="fade",
            transition_duration=0.5
        )
        
        assert result["status"] == "success"
        assert os.path.exists(output_path)
        assert result["images_count"] == 3
    
    def test_create_slideshow_with_text_overlays(self, test_environment):
        """Test slideshow with text overlays"""
        test_data = test_environment
        output_path = os.path.join(test_data['test_dir'], "test_slideshow_text.mp4")
        
        text_overlays = [
            {
                "text": "Image 1: Red",
                "fontsize": 48,
                "color": "white",
                "position": "bottom",
                "image_indices": [0]
            },
            {
                "text": "Image 2: Green", 
                "fontsize": 48,
                "color": "black",
                "position": "top",
                "image_indices": [1]
            }
        ]
        
        result = create_slideshow_from_images(
            image_paths=test_data['test_images'][:2],
            output_path=output_path,
            duration_per_image=3.0,
            text_overlays=text_overlays
        )
        
        assert result["status"] == "success"
        assert os.path.exists(output_path)
    
    def test_create_slideshow_with_effects(self, test_environment):
        """Test slideshow with effects"""
        test_data = test_environment
        output_path = os.path.join(test_data['test_dir'], "test_slideshow_effects.mp4")
        
        effects = [
            {"type": "fade_in", "duration": 0.5},
            {"type": "fade_out", "duration": 0.5},
            {"type": "zoom", "factor": 1.1}
        ]
        
        result = create_slideshow_from_images(
            image_paths=test_data['test_images'][:2],
            output_path=output_path,
            duration_per_image=3.0,
            effects=effects
        )
        
        assert result["status"] == "success"
        assert os.path.exists(output_path)
    
    @pytest.mark.parametrize("fit_mode", ["contain", "cover", "stretch", "crop"])
    def test_different_fit_modes(self, test_environment, fit_mode):
        """Test different image fitting modes"""
        test_data = test_environment
        output_path = os.path.join(test_data['test_dir'], f"test_slideshow_{fit_mode}.mp4")
        
        result = create_slideshow_from_images(
            image_paths=test_data['test_images'][:2],
            output_path=output_path,
            duration_per_image=2.0,
            fit_mode=fit_mode
        )
        
        assert result["status"] == "success"
        assert os.path.exists(output_path)
    
    def test_create_image_slideshow_wrapper(self, test_environment):
        """Test the main wrapper function"""
        test_data = test_environment
        output_path = os.path.join(test_data['test_dir'], "test_wrapper_slideshow.mp4")
        
        result = create_image_slideshow(
            image_paths=test_data['test_images'][:2],
            output_path=output_path,
            duration_per_image=2.0,
            transition_type="fade"
        )
        
        assert result["status"] == "success"
        assert os.path.exists(output_path)
    
    def test_create_simple_slideshow(self, test_environment):
        """Test simple slideshow function"""
        test_data = test_environment
        output_path = os.path.join(test_data['test_dir'], "test_simple_slideshow.mp4")
        
        result = create_simple_slideshow(
            image_paths=test_data['test_images'][:2],
            output_path=output_path,
            duration_per_image=2.0
        )
        
        assert result["status"] == "success"
        assert os.path.exists(output_path)
    
    def test_add_text_to_images(self, test_environment):
        """Test adding text to images"""
        test_data = test_environment
        output_dir = os.path.join(test_data['test_dir'], "text_overlay_images")
        texts = ["Red Image", "Green Image"]
        
        text_config = {
            "font_size": 36,
            "font_color": (255, 255, 255),
            "position": "bottom",
            "margin": 30
        }
        
        result = add_text_to_images(
            image_paths=test_data['test_images'][:2],
            output_dir=output_dir,
            texts=texts,
            text_config=text_config
        )
        
        assert result["status"] == "success"
        assert len(result["output_files"]) == 2
        
        # Check that output files exist
        for output_file in result["output_files"]:
            assert os.path.exists(output_file)
    
    def test_error_non_existent_image(self, test_environment):
        """Test error handling for non-existent images"""
        test_data = test_environment
        
        result = create_slideshow_from_images(
            image_paths=["/nonexistent/path/image.jpg"],
            output_path=os.path.join(test_data['test_dir'], "error_test.mp4")
        )
        
        assert result["status"] == "error"
        assert "not found" in result["message"]
    
    def test_error_empty_image_list(self, test_environment):
        """Test error handling for empty image list"""
        test_data = test_environment
        
        result = create_slideshow_from_images(
            image_paths=[],
            output_path=os.path.join(test_data['test_dir'], "error_test.mp4")
        )
        
        assert result["status"] == "error"
        assert "No image paths provided" in result["message"]
    
    def test_error_mismatched_text_lists(self, test_environment):
        """Test error handling for mismatched text lists"""
        test_data = test_environment
        
        result = add_text_to_images(
            image_paths=test_data['test_images'][:2],
            output_dir=os.path.join(test_data['test_dir'], "error_text"),
            texts=["Only one text"]  # Mismatch: 2 images, 1 text
        )
        
        assert result["status"] == "error"
        assert "must match" in result["message"]
    
    def test_helper_create_image_clip(self, test_environment):
        """Test _create_image_clip helper function"""
        test_data = test_environment
        
        try:
            clip = _create_image_clip(
                img_path=test_data['test_images'][0],
                duration=2.0,
                resolution=(640, 480),
                fit_mode="contain",
                background_color=(0, 0, 0)
            )
            
            assert clip is not None
            assert clip.duration == 2.0
            clip.close()
            
        except Exception as e:
            pytest.fail(f"_create_image_clip failed: {e}")
    
    def test_comprehensive_slideshow_all_features(self, test_environment):
        """Test slideshow with all features combined"""
        test_data = test_environment
        output_path = os.path.join(test_data['test_dir'], "test_comprehensive.mp4")
        
        text_overlays = [
            {
                "text": "Comprehensive Test",
                "fontsize": 60,
                "color": "white",
                "position": "center"
            }
        ]
        
        effects = [
            {"type": "fade_in", "duration": 0.5},
            {"type": "fade_out", "duration": 0.5}
        ]
        
        result = create_slideshow_from_images(
            image_paths=test_data['test_images'],
            output_path=output_path,
            duration_per_image=2.0,
            fps=30,
            resolution=(1920, 1080),
            transition_type="fade",
            transition_duration=0.5,
            background_color=(255, 255, 255),
            fit_mode="contain",
            text_overlays=text_overlays,
            effects=effects
        )
        
        assert result["status"] == "success"
        assert os.path.exists(output_path)
        assert result["images_count"] == 4
        assert result["resolution"] == (1920, 1080)
        assert result["fps"] == 30


# Additional test functions for specific scenarios
def test_module_imports():
    """Test that all required modules can be imported"""
    try:
        from tools.image_editor_tools import (
            create_slideshow_from_images,
            create_image_slideshow,
            create_simple_slideshow,
            add_text_to_images
        )
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required modules: {e}")


if __name__ == "__main__":
    # Run tests directly if script is executed
    pytest.main([__file__, "-v"])
