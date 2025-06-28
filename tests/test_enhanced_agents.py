"""
Comprehensive test suite for the enhanced AI Video Generator agents
Tests all audio processing, file management, and enhanced video/image capabilities
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path

# Test the new audio tools
from tools.audio import (
    text_to_speech,
    analyze_audio,
    apply_audio_effects,
    adjust_volume,
    convert_audio_format,
    fade_audio,
    merge_audio_tracks,
    mix_audio,
    normalize_audio,
    trim_audio
)

# Test the new file tools
from tools.file import (
    copy_files,
    move_files,
    create_directory,
    delete_files,
    compress_files,
    extract_archive,
    list_directory,
    get_file_info,
    batch_rename,
    find_files
)

class TestAudioTools:
    """Test suite for audio processing tools"""
    
    def setup_method(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, "outputs")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def teardown_method(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_text_to_speech(self):
        """Test text-to-speech functionality"""
        output_path = os.path.join(self.output_dir, "test_speech.mp3")
        
        result = text_to_speech(
            text="Hello, this is a test of the text-to-speech system.",
            output_path=output_path,
            voice_engine="gtts",
            language="en"
        )
        
        # Should return proper structure even if libraries not available
        assert "status" in result
        assert "message" in result
        assert "output_path" in result
        
        if result["status"] == "error":
            # Expected if libraries not installed
            assert "not available" in result["message"]
        else:
            # Should succeed if libraries available
            assert result["status"] == "success"
            assert result["output_path"] == output_path
    
    def test_analyze_audio_missing_file(self):
        """Test audio analysis with missing file"""
        result = analyze_audio("/nonexistent/audio.mp3")
        
        assert result["status"] == "error"
        assert "not found" in result["message"]
    
    def test_audio_effects_missing_file(self):
        """Test audio effects with missing file"""
        output_path = os.path.join(self.output_dir, "processed.mp3")
        
        result = apply_audio_effects(
            audio_path="/nonexistent/audio.mp3",
            output_path=output_path,
            effects=[{"type": "normalize", "parameters": {"headroom": 0.1}}]
        )
        
        assert result["status"] == "error"
        assert "not found" in result["message"]
    
    def test_volume_adjustment_missing_file(self):
        """Test volume adjustment with missing file"""
        output_path = os.path.join(self.output_dir, "adjusted.mp3")
        
        result = adjust_volume(
            audio_path="/nonexistent/audio.mp3",
            output_path=output_path,
            volume_change=6.0
        )
        
        assert result["status"] == "error"
        assert "not found" in result["message"]


class TestFileTools:
    """Test suite for file management tools"""
    
    def setup_method(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source")
        self.dest_dir = os.path.join(self.test_dir, "dest")
        os.makedirs(self.source_dir, exist_ok=True)
        
        # Create test files
        self.test_files = []
        for i in range(3):
            file_path = os.path.join(self.source_dir, f"test_file_{i}.txt")
            with open(file_path, 'w') as f:
                f.write(f"Test content {i}")
            self.test_files.append(file_path)
    
    def teardown_method(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_create_directory(self):
        """Test directory creation"""
        new_dir = os.path.join(self.test_dir, "new_directory")
        
        result = create_directory(new_dir)
        
        assert result["status"] == "success"
        assert result["directory_path"] == new_dir
        assert os.path.exists(new_dir)
    
    def test_copy_files(self):
        """Test file copying"""
        result = copy_files(
            source_paths=self.test_files,
            destination_path=self.dest_dir,
            preserve_structure=True,
            overwrite=False
        )
        
        assert result["status"] == "success"
        assert result["files_copied"] == 3
        assert result["files_failed"] == 0
        assert os.path.exists(self.dest_dir)
        
        # Check files were copied
        for file_path in self.test_files:
            dest_file = os.path.join(self.dest_dir, os.path.basename(file_path))
            assert os.path.exists(dest_file)
    
    def test_move_files(self):
        """Test file moving"""
        # Copy files first so we don't destroy originals
        temp_files = []
        for i, source_file in enumerate(self.test_files):
            temp_file = os.path.join(self.source_dir, f"temp_file_{i}.txt")
            shutil.copy2(source_file, temp_file)
            temp_files.append(temp_file)
        
        result = move_files(
            source_paths=temp_files,
            destination_path=self.dest_dir,
            overwrite=False
        )
        
        assert result["status"] == "success"
        assert result["files_moved"] == 3
        assert result["files_failed"] == 0
        
        # Check files were moved (no longer in source)
        for temp_file in temp_files:
            assert not os.path.exists(temp_file)
        
        # Check files exist in destination
        for temp_file in temp_files:
            dest_file = os.path.join(self.dest_dir, os.path.basename(temp_file))
            assert os.path.exists(dest_file)
    
    def test_list_directory(self):
        """Test directory listing"""
        result = list_directory(self.source_dir)
        
        assert result["status"] == "success"
        assert result["total_items"] == 3
        assert len(result["items"]) == 3
        
        # Check item structure
        for item in result["items"]:
            assert "name" in item
            assert "path" in item
            assert "type" in item
            assert item["type"] == "file"
    
    def test_get_file_info(self):
        """Test file information retrieval"""
        test_file = self.test_files[0]
        
        result = get_file_info(test_file)
        
        assert result["status"] == "success"
        assert result["file_path"] == test_file
        assert result["type"] == "file"
        assert "size" in result
        assert "created" in result
        assert "modified" in result
    
    def test_find_files(self):
        """Test file search functionality"""
        result = find_files(
            search_directory=self.source_dir,
            pattern="*.txt",
            file_type="file"
        )
        
        assert result["status"] == "success"
        assert result["total_found"] == 3
        assert len(result["found_files"]) == 3
        
        # Check found file structure
        for found_file in result["found_files"]:
            assert "name" in found_file
            assert "path" in found_file
            assert "type" in found_file
            assert found_file["name"].endswith(".txt")
    
    def test_compress_files(self):
        """Test file compression"""
        archive_path = os.path.join(self.test_dir, "test_archive.zip")
        
        result = compress_files(
            file_paths=self.test_files,
            archive_path=archive_path,
            format_type="zip"
        )
        
        assert result["status"] == "success"
        assert result["archive_path"] == archive_path
        assert os.path.exists(archive_path)
        assert result["archive_size"] > 0
    
    def test_extract_archive(self):
        """Test archive extraction"""
        # First create an archive
        archive_path = os.path.join(self.test_dir, "test_archive.zip")
        compress_result = compress_files(
            file_paths=self.test_files,
            archive_path=archive_path,
            format_type="zip"
        )
        
        assert compress_result["status"] == "success"
        
        # Now extract it
        extract_dir = os.path.join(self.test_dir, "extracted")
        result = extract_archive(
            archive_path=archive_path,
            destination_path=extract_dir
        )
        
        assert result["status"] == "success"
        assert result["destination_path"] == extract_dir
        assert os.path.exists(extract_dir)
        assert result["extracted_files"] >= 3
    
    def test_batch_rename(self):
        """Test batch file renaming"""
        # Copy files to avoid affecting original tests
        temp_files = []
        for i, source_file in enumerate(self.test_files):
            temp_file = os.path.join(self.source_dir, f"rename_test_{i}.txt")
            shutil.copy2(source_file, temp_file)
            temp_files.append(temp_file)
        
        result = batch_rename(
            file_paths=temp_files,
            naming_pattern="renamed_file_{number:03d}",
            start_number=1
        )
        
        assert result["status"] == "success"
        assert result["files_renamed"] == 3
        assert result["files_failed"] == 0
        
        # Check renamed files exist
        for i in range(3):
            expected_path = os.path.join(self.source_dir, f"renamed_file_{i+1:03d}.txt")
            assert os.path.exists(expected_path)
    
    def test_delete_files(self):
        """Test file deletion"""
        # Create temporary files for deletion
        temp_files = []
        for i in range(2):
            temp_file = os.path.join(self.source_dir, f"delete_test_{i}.txt")
            with open(temp_file, 'w') as f:
                f.write(f"Delete test {i}")
            temp_files.append(temp_file)
        
        result = delete_files(
            file_paths=temp_files,
            force=False
        )
        
        assert result["status"] == "success"
        assert result["files_deleted"] == 2
        assert result["files_failed"] == 0
        
        # Check files were deleted
        for temp_file in temp_files:
            assert not os.path.exists(temp_file)


class TestAgentIntegration:
    """Test agent integration and workflow"""
    
    def test_agent_imports(self):
        """Test that all agents can be imported successfully"""
        from adk_agents.agents import (
            youtube_agent,
            video_editor_agent,
            image_to_video_agent,
            audio_processing_agent,
            file_management_agent,
            video_agents_team,
            root_agent
        )
        
        # Check all agents are properly defined
        assert youtube_agent is not None
        assert video_editor_agent is not None
        assert image_to_video_agent is not None
        assert audio_processing_agent is not None
        assert file_management_agent is not None
        assert video_agents_team is not None
        assert root_agent is not None
        
        # Check agent names
        assert youtube_agent.name == "YouTube_Agent_v1"
        assert video_editor_agent.name == "Video_Editor_Agent_v1"
        assert image_to_video_agent.name == "Image_to_Video_Agent_v1"
        assert audio_processing_agent.name == "Audio_Processing_Agent_v1"
        assert file_management_agent.name == "File_Management_Agent_v1"
        assert video_agents_team.name == "Video_Agents_Team_v1"
    
    def test_agent_tools_assignment(self):
        """Test that agents have the correct tools assigned"""
        from adk_agents.agents import (
            audio_processing_agent,
            file_management_agent
        )
        
        # Check audio agent has audio tools
        audio_tool_names = [tool.__name__ for tool in audio_processing_agent.tools]
        expected_audio_tools = [
            'text_to_speech', 'analyze_audio', 'apply_audio_effects',
            'adjust_volume', 'convert_audio_format', 'fade_audio',
            'merge_audio_tracks', 'mix_audio', 'normalize_audio', 'trim_audio'
        ]
        
        for expected_tool in expected_audio_tools:
            assert expected_tool in audio_tool_names
        
        # Check file agent has file tools
        file_tool_names = [tool.__name__ for tool in file_management_agent.tools]
        expected_file_tools = [
            'copy_files', 'move_files', 'create_directory', 'delete_files',
            'compress_files', 'extract_archive', 'list_directory', 'get_file_info',
            'batch_rename', 'find_files'
        ]
        
        for expected_tool in expected_file_tools:
            assert expected_tool in file_tool_names


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])
