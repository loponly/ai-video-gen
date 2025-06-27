# Agent Path Configuration Guide

## Overview

The AI Video Generator agents have been configured with persistent path management to ensure consistent file organization across all operations.

## Path Conventions

### Downloads Directory (`downloads/`)
- **Purpose**: All downloaded content from external sources
- **Used by**: YouTube Agent
- **Examples**:
  - Downloaded YouTube videos
  - External media files
  - Temporary downloads

### Outputs Directory (`outputs/`)
- **Purpose**: All final processed results and exports
- **Used by**: Video Editor Agent, Image-to-Video Agent
- **Examples**:
  - Edited videos
  - Concatenated clips
  - Generated slideshows
  - Exported final products

### Other Directories
- **`assets/`**: Static assets and resources
- **`content/`**: Existing content and media files
- **`cache-models/`**: Cached AI models and temporary data

## Agent Behavior

### YouTube Agent (`YouTube_Agent_v1`)
- **Download Path**: Always saves to `downloads/` directory
- **Instruction**: Uses `save_dir='downloads/'` parameter
- **Validation**: Confirms download location in responses

### Video Editor Agent (`Video_Editor_Agent_v1`)
- **Output Path**: Always saves to `outputs/` directory
- **Instruction**: Uses `output_path` starting with `outputs/`
- **Operations**: Concatenation, effects, exports all go to `outputs/`

### Image-to-Video Agent (`Image_to_Video_Agent_v1`)
- **Output Path**: Always saves to `outputs/` directory
- **Instruction**: All video creation outputs go to `outputs/`
- **Operations**: Slideshows, video generation to `outputs/`

### Orchestrator Agent (`Video_Agents_Team_v1`)
- **Role**: Enforces path conventions across all sub-agents
- **Validation**: Verifies proper path usage
- **Coordination**: Manages workflow with consistent paths

## Usage Examples

### Downloading a Video
```python
# The agent will automatically use downloads/ directory
"Download this YouTube video: https://youtube.com/watch?v=example"
# Result: downloads/Video_Title.mp4
```

### Editing and Exporting
```python
# The agent will automatically output to outputs/ directory
"Edit the downloaded video and add subtitles"
# Input: downloads/Video_Title.mp4
# Result: outputs/Video_Title_edited.mp4
```

### Creating Slideshow
```python
# The agent will automatically output to outputs/ directory
"Create a slideshow from images in assets/images/"
# Input: assets/images/*.jpg
# Result: outputs/slideshow.mp4
```

## Path Configuration Module

The `adk_agents/path_config.py` module provides:

### PathConfig Class Methods
- `get_download_path(filename=None)`: Returns download directory path
- `get_output_path(filename=None)`: Returns output directory path
- `validate_download_path(path)`: Validates download path
- `validate_output_path(path)`: Validates output path
- `ensure_directories()`: Creates required directories

### Example Usage
```python
from adk_agents.path_config import PathConfig

# Get standardized paths
download_path = PathConfig.get_download_path("video.mp4")
output_path = PathConfig.get_output_path("edited_video.mp4")

# Validate paths
is_valid_download = PathConfig.validate_download_path(some_path)
is_valid_output = PathConfig.validate_output_path(some_path)
```

## Benefits

1. **Consistency**: All agents follow the same path conventions
2. **Organization**: Clear separation between downloads and outputs
3. **Validation**: Built-in path validation to prevent errors
4. **Maintainability**: Centralized path management
5. **User Experience**: Predictable file locations

## File Structure After Operations

```
ai-video-ge/
├── downloads/          # All downloaded content
│   ├── video1.mp4
│   ├── video2.webm
│   └── ...
├── outputs/           # All final results
│   ├── edited_video.mp4
│   ├── slideshow.mp4
│   ├── concatenated.mp4
│   └── ...
├── assets/            # Static resources
├── content/           # Existing content
└── ...
```

## Testing

Run the path configuration tests:

```bash
python tests/test_agent_path_config.py
```

This validates:
- Directory creation
- Agent instruction compliance
- Path validation functions
- Tool configuration
- Agent hierarchy

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure write permissions for `downloads/` and `outputs/`
2. **Path Not Found**: The PathConfig automatically creates directories
3. **Wrong Directory**: Check agent instructions in `adk_agents/agents.py`

### Debugging

Enable verbose logging to see path usage:
- Check agent responses for confirmed paths
- Validate using `PathConfig.validate_*_path()` methods
- Review agent instructions for path requirements

## Migration Guide

If you have existing code that uses different paths:

1. **Update tool calls**: Use PathConfig methods for path generation
2. **Modify workflows**: Ensure downloads go to `downloads/`, outputs to `outputs/`
3. **Test thoroughly**: Run the test suite to validate changes
4. **Update documentation**: Keep path references current

This configuration ensures that your AI Video Generator maintains organized, predictable file management across all operations.
