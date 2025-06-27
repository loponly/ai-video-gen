"""
Test Agent Runner
================

Unit tests for the agent_runner.py module, testing the updated functionality
with command line arguments and test scenarios.

This module tests:
- Command line argument parsing
- Test scenario management
- Agent runner functionality
- Query processing
"""

import pytest
import asyncio
import tempfile
import os
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

# Import the functions we want to test
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_runner import (
    create_test_queries,
    parse_arguments,
    run_conversation,
    create_runner,
    APP_NAME,
    USER_ID,
    SESSION_ID
)


class TestAgentRunner:
    """Test cases for the agent runner functionality."""
    
    def test_create_test_queries(self):
        """Test that test queries are created with expected keys."""
        queries = create_test_queries()
        
        # Check that all expected test scenarios exist
        expected_keys = [
            "image_to_video_basic",
            "image_to_video_advanced", 
            "youtube_search",
            "video_editing",
            "general"
        ]
        
        for key in expected_keys:
            assert key in queries, f"Expected test query '{key}' not found"
            assert isinstance(queries[key], str), f"Query '{key}' should be a string"
            assert len(queries[key]) > 0, f"Query '{key}' should not be empty"
    
    def test_parse_arguments_query(self):
        """Test parsing command line arguments for query option."""
        with patch('sys.argv', ['agent_runner.py', '--query', 'test query']):
            args = parse_arguments()
            assert args.query == 'test query'
            assert args.test is None
            assert args.test_all is False
            assert args.list_tests is False
    
    def test_parse_arguments_test(self):
        """Test parsing command line arguments for test option."""
        with patch('sys.argv', ['agent_runner.py', '--test', 'image_to_video_basic']):
            args = parse_arguments()
            assert args.test == 'image_to_video_basic'
            assert args.query is None
            assert args.test_all is False
            assert args.list_tests is False
    
    def test_parse_arguments_test_all(self):
        """Test parsing command line arguments for test-all option."""
        with patch('sys.argv', ['agent_runner.py', '--test-all']):
            args = parse_arguments()
            assert args.test_all is True
            assert args.query is None
            assert args.test is None
            assert args.list_tests is False
    
    def test_parse_arguments_list_tests(self):
        """Test parsing command line arguments for list-tests option."""
        with patch('sys.argv', ['agent_runner.py', '--list-tests']):
            args = parse_arguments()
            assert args.list_tests is True
            assert args.query is None
            assert args.test is None
            assert args.test_all is False
    
    def test_image_to_video_query_content(self):
        """Test that image-to-video queries contain expected content."""
        queries = create_test_queries()
        
        basic_query = queries["image_to_video_basic"]
        assert "slideshow" in basic_query.lower()
        assert "images" in basic_query.lower()
        assert "movie-reels/images" in basic_query
        
        advanced_query = queries["image_to_video_advanced"]
        assert "slideshow" in advanced_query.lower()
        assert "slide_left" in advanced_query
        assert "text overlay" in advanced_query.lower()
        assert "movie-reels/output" in advanced_query
    
    @pytest.mark.asyncio
    async def test_run_conversation_with_query(self):
        """Test run_conversation with a specific query."""
        test_query = "Test query"
        
        # Mock the agent runner and response
        with patch('agent_runner.create_runner') as mock_create_runner, \
             patch('agent_runner.call_agent_async') as mock_call_agent:
            
            mock_runner = AsyncMock()
            mock_create_runner.return_value = mock_runner
            mock_call_agent.return_value = "Test response"
            
            response = await run_conversation(test_query)
            
            # Verify the mocks were called correctly
            mock_create_runner.assert_called_once()
            mock_call_agent.assert_called_once_with(
                test_query,
                runner=mock_runner,
                user_id=USER_ID,
                session_id=SESSION_ID
            )
            
            assert response == "Test response"
    
    @pytest.mark.asyncio 
    async def test_run_conversation_default_query(self):
        """Test run_conversation with default query when None is provided."""
        with patch('agent_runner.create_runner') as mock_create_runner, \
             patch('agent_runner.call_agent_async') as mock_call_agent:
            
            mock_runner = AsyncMock()
            mock_create_runner.return_value = mock_runner
            mock_call_agent.return_value = "Default response"
            
            response = await run_conversation(None)
            
            # Should call with default query
            mock_call_agent.assert_called_once()
            call_args = mock_call_agent.call_args[0]
            assert call_args[0] == "Please help me understand what you can do."
            
            assert response == "Default response"
    
    def test_constants(self):
        """Test that required constants are defined."""
        assert APP_NAME == "Content Creator Agents"
        assert USER_ID == "user-12345"
        assert SESSION_ID == "session-1234"
    
    def test_query_formatting(self):
        """Test that queries are properly formatted for different scenarios."""
        queries = create_test_queries()
        
        # Test that queries contain proper instructions
        for query_name, query_text in queries.items():
            assert len(query_text.strip()) > 10, f"Query '{query_name}' seems too short"
            
            # Image-to-video queries should mention specific paths or requirements
            if "image_to_video" in query_name:
                assert ("images" in query_text.lower() or 
                       "slideshow" in query_text.lower()), \
                       f"Image-to-video query '{query_name}' should mention images or slideshow"


@pytest.mark.integration
class TestAgentRunnerIntegration:
    """Integration tests for agent runner that require actual image files."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.images_dir = os.path.join(self.temp_dir, "images")
        self.output_dir = os.path.join(self.temp_dir, "output")
        
        os.makedirs(self.images_dir)
        os.makedirs(self.output_dir)
        
        # Create some dummy image files for testing
        from PIL import Image
        import numpy as np
        
        for i in range(3):
            # Create a simple colored image
            img_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
            img = Image.fromarray(img_array)
            img.save(os.path.join(self.images_dir, f"test_image_{i}.jpg"))
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_image_paths_exist(self):
        """Test that we can create test image files."""
        image_files = os.listdir(self.images_dir)
        assert len(image_files) == 3
        
        for i in range(3):
            expected_file = f"test_image_{i}.jpg"
            assert expected_file in image_files
            
            file_path = os.path.join(self.images_dir, expected_file)
            assert os.path.isfile(file_path)
            assert os.path.getsize(file_path) > 0


if __name__ == "__main__":
    pytest.main([__file__])
