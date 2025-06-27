# Agent Runner - Enhanced Version

## Overview

The `agent_runner.py` has been enhanced with command-line argument support and comprehensive testing capabilities for the AI Video Generation project, with special focus on testing the `image_to_video_agent`.

## Features

### Command Line Interface
- **Query Mode**: Run custom queries directly
- **Test Scenarios**: Pre-defined test cases for different functionalities
- **Batch Testing**: Run all test scenarios at once
- **Help System**: Comprehensive help and usage examples

### Test Scenarios

1. **image_to_video_basic**: Basic slideshow creation from images
2. **image_to_video_advanced**: Advanced slideshow with custom settings
3. **youtube_search**: YouTube video search functionality
4. **video_editing**: Video editing capabilities
5. **general**: General agent capabilities overview

## Usage

### Basic Usage
```bash
# Run with a custom query
python agent_runner.py --query "Create a slideshow from my images"

# Run a specific test scenario
python agent_runner.py --test image_to_video_basic

# List all available tests
python agent_runner.py --list-tests

# Run all test scenarios
python agent_runner.py --test-all

# Show help
python agent_runner.py --help
```

### Image-to-Video Agent Testing

The enhanced agent runner specifically supports testing the `image_to_video_agent` with:

- **Slideshow Creation**: Convert images to video slideshows
- **Transition Effects**: Support for fade, slide, and other transitions
- **Custom Settings**: Duration, resolution, effects, and more
- **File Management**: Automatic output directory creation

#### Example Image-to-Video Usage
```bash
# Basic slideshow test
python agent_runner.py --test image_to_video_basic

# Advanced slideshow with custom parameters
python agent_runner.py --test image_to_video_advanced

# Custom query with specific images
python agent_runner.py --query "Create a slideshow using images from movie-reels/images/ folder"
```

## Technical Details

### Function Signature Improvements
- Fixed complex type annotations that caused ADK parsing issues
- Simplified function parameters for better compatibility
- Maintained functionality while improving usability

### Test Coverage
- Comprehensive unit tests in `tests/test_agent_runner.py`
- Integration tests for file operations
- Mock-based testing for async operations
- Command-line argument validation

### Error Handling
- Graceful handling of ADK serialization warnings
- Proper error messages for missing files
- Timeout handling for long-running operations

## Files Modified/Created

1. **agent_runner.py**: Enhanced with CLI support and test scenarios
2. **tests/test_agent_runner.py**: Comprehensive test suite
3. **tools/image_editor_tools.py**: Fixed function signatures for ADK compatibility
4. **demo_agent_runner.py**: Demonstration script

## Installation

Ensure you have the required dependencies:

```bash
pip install pytest-asyncio  # For async test support
```

## Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/test_agent_runner.py -v

# Run with coverage
python -m pytest tests/test_agent_runner.py --cov=agent_runner

# Run integration tests
python -m pytest tests/test_agent_runner.py::TestAgentRunnerIntegration -v
```

## Examples

### Successful Test Output
```
🧪 Running test scenario: image_to_video_basic
==================================================
>>> User Query: I want to create a simple slideshow video from images...
Moviepy - Building video /path/to/output/slideshow.mp4
Moviepy - Done!
✅ Test scenario 'image_to_video_basic' completed.
```

### Agent Capabilities Response
```
I am the Video Agents Team Agent, designed to orchestrate tasks between specialized agents for YouTube and video editing. I can help you with:
- YouTube video search, download, and transcript extraction
- Video editing including concatenation, effects, and subtitles
- Image-to-video conversion with slideshows and transitions
```

## Troubleshooting

### Common Issues

1. **Function Signature Errors**: Ensure complex types are simplified for ADK compatibility
2. **Image Not Found**: Verify image paths exist and are accessible
3. **Permission Errors**: Check write permissions for output directories
4. **Timeout Issues**: Some operations may take time, especially video processing

### Debug Mode
Add `--verbose` or check log outputs for detailed information about agent operations.

## Contributing

When adding new test scenarios:

1. Add entries to `create_test_queries()` function
2. Create corresponding unit tests
3. Update this documentation
4. Test with various input scenarios

## License

This project follows the same license as the main AI Video Generation project.
