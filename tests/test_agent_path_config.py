"""
Test Agent Path Configuration

This module tests the agent configuration to ensure proper path persistence
for downloads/ and outputs/ directories.
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from adk_agents.agents import (
    youtube_agent,
    video_editor_agent,
    image_to_video_agent,
    video_agents_team
)
from adk_agents.path_config import PathConfig


class TestAgentPathConfiguration:
    """Test suite for agent path configuration."""
    
    def test_path_config_initialization(self):
        """Test that PathConfig initializes correctly."""
        assert PathConfig.PROJECT_ROOT.exists()
        assert PathConfig.DOWNLOADS_DIR.exists()
        assert PathConfig.OUTPUTS_DIR.exists()
    
    def test_downloads_directory_exists(self):
        """Test that downloads directory is created."""
        downloads_path = PathConfig.get_download_path()
        assert os.path.exists(downloads_path)
        assert downloads_path.endswith('downloads')
    
    def test_outputs_directory_exists(self):
        """Test that outputs directory is created."""
        outputs_path = PathConfig.get_output_path()
        assert os.path.exists(outputs_path)
        assert outputs_path.endswith('outputs')
    
    def test_youtube_agent_has_download_instructions(self):
        """Test that YouTube agent has proper download path instructions."""
        instruction = youtube_agent.instruction
        assert 'downloads/' in instruction
        assert 'save_dir' in instruction
        assert 'downloads/ directory' in instruction
    
    def test_video_editor_agent_has_output_instructions(self):
        """Test that Video Editor agent has proper output path instructions."""
        instruction = video_editor_agent.instruction
        assert 'outputs/' in instruction
        assert 'output_path' in instruction
        assert "'outputs/' directory" in instruction
    
    def test_image_to_video_agent_has_output_instructions(self):
        """Test that Image-to-Video agent has proper output path instructions."""
        instruction = image_to_video_agent.instruction
        assert 'outputs/' in instruction
        assert "'outputs/' as the destination" in instruction
    
    def test_orchestrator_agent_has_path_management(self):
        """Test that orchestrator agent has path management instructions."""
        instruction = video_agents_team.instruction
        assert 'downloads/' in instruction
        assert 'outputs/' in instruction
        assert 'PATH MANAGEMENT' in instruction
    
    def test_path_validation_functions(self):
        """Test path validation functions."""
        # Test download path validation
        valid_download = str(PathConfig.DOWNLOADS_DIR / "test.mp4")
        invalid_download = "/tmp/test.mp4"
        
        assert PathConfig.validate_download_path(valid_download)
        assert not PathConfig.validate_download_path(invalid_download)
        
        # Test output path validation
        valid_output = str(PathConfig.OUTPUTS_DIR / "test.mp4")
        invalid_output = "/tmp/test.mp4"
        
        assert PathConfig.validate_output_path(valid_output)
        assert not PathConfig.validate_output_path(invalid_output)
    
    def test_get_path_methods(self):
        """Test path getter methods."""
        # Test download path methods
        download_dir = PathConfig.get_download_path()
        download_file = PathConfig.get_download_path("test.mp4")
        
        assert download_dir.endswith('downloads')
        assert download_file.endswith('downloads/test.mp4')
        
        # Test output path methods
        output_dir = PathConfig.get_output_path()
        output_file = PathConfig.get_output_path("test.mp4")
        
        assert output_dir.endswith('outputs')
        assert output_file.endswith('outputs/test.mp4')
    
    def test_agent_tools_configuration(self):
        """Test that agents have the correct tools configured."""
        # YouTube agent tools
        youtube_tools = [tool.__name__ for tool in youtube_agent.tools]
        expected_youtube_tools = [
            'get_transcript', 'get_video_info', 'search_videos', 'download_youtube_video'
        ]
        for tool in expected_youtube_tools:
            assert tool in youtube_tools
        
        # Video editor tools
        video_tools = [tool.__name__ for tool in video_editor_agent.tools]
        expected_video_tools = [
            'concatenate_videos', 'synchronize_audio', 'clip_videos',
            'edit_video_metadata', 'add_effects', 'export_video',
            'add_subtitles', 'extract_audio'
        ]
        for tool in expected_video_tools:
            assert tool in video_tools
        
        # Image to video tools
        image_tools = [tool.__name__ for tool in image_to_video_agent.tools]
        expected_image_tools = [
            'create_slideshow_from_images', 'create_simple_slideshow',
            'add_text_to_images', 'create_image_slideshow', 'create_video_from_images'
        ]
        for tool in expected_image_tools:
            assert tool in image_tools


def test_agent_hierarchy():
    """Test that agent hierarchy is properly configured."""
    # Test that video_agents_team has the correct sub-agents
    sub_agents = video_agents_team.sub_agents
    assert len(sub_agents) == 3
    
    sub_agent_names = [agent.name for agent in sub_agents]
    expected_names = [
        "YouTube_Agent_v1", 
        "Video_Editor_Agent_v1", 
        "Image_to_Video_Agent_v1"
    ]
    
    for name in expected_names:
        assert name in sub_agent_names


def test_path_config_relative_paths():
    """Test relative path functionality."""
    # Test relative path generation
    test_abs_path = PathConfig.PROJECT_ROOT / "downloads" / "test.mp4"
    relative_path = PathConfig.get_relative_path(test_abs_path)
    assert relative_path == "downloads/test.mp4"


if __name__ == "__main__":
    # Run basic tests
    test_config = TestAgentPathConfiguration()
    
    print("Testing agent path configuration...")
    
    try:
        test_config.test_path_config_initialization()
        print("✓ Path config initialization test passed")
        
        test_config.test_downloads_directory_exists()
        print("✓ Downloads directory test passed")
        
        test_config.test_outputs_directory_exists()
        print("✓ Outputs directory test passed")
        
        test_config.test_youtube_agent_has_download_instructions()
        print("✓ YouTube agent download instructions test passed")
        
        test_config.test_video_editor_agent_has_output_instructions()
        print("✓ Video editor agent output instructions test passed")
        
        test_config.test_image_to_video_agent_has_output_instructions()
        print("✓ Image-to-video agent output instructions test passed")
        
        test_config.test_orchestrator_agent_has_path_management()
        print("✓ Orchestrator agent path management test passed")
        
        test_config.test_path_validation_functions()
        print("✓ Path validation functions test passed")
        
        test_config.test_get_path_methods()
        print("✓ Path getter methods test passed")
        
        test_config.test_agent_tools_configuration()
        print("✓ Agent tools configuration test passed")
        
        test_agent_hierarchy()
        print("✓ Agent hierarchy test passed")
        
        test_path_config_relative_paths()
        print("✓ Path config relative paths test passed")
        
        print("\n✅ All agent path configuration tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
