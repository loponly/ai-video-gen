"""
AI Video Generator Agents Configuration

This module defines the comprehensive agent team structure with consistent path management:
- Downloads: All downloaded content goes to 'downloads/' directory
- Outputs: All final results go to 'outputs/' directory
- Path validation is enforced through agent instructions

Agent Hierarchy:
├── video_agents_team (root orchestrator)
    ├── youtube_agent (downloads to downloads/)
    ├── video_editor_agent (outputs to outputs/)
    ├── image_to_video_agent (outputs to outputs/)
    ├── audio_processing_agent (outputs to outputs/)
    └── file_management_agent (system-wide file operations)

Capabilities:
- Video content discovery and downloading
- Comprehensive video editing and effects
- Image-to-video conversion and slideshows
- Audio processing and voice-over generation
- File management and organization
- End-to-end multimedia content creation workflows
"""

from google.adk.agents import Agent
from guards.block_keyword import block_keyword_guardrail
from google.adk.tools import agent_tool
from .path_config import PathConfig

# Tools imports
from tools.youtube import (
    get_transcript,
    get_video_info,
    search_videos,
    download_youtube_video
)

from tools.video import (
    concatenate_videos,
    synchronize_audio,
    clip_videos,
    edit_video_metadata,
    add_effects,
    export_video,
    add_subtitles,
    create_video_from_images,
    extract_audio
)
 
from tools.image import (
    create_slideshow_from_images,
    create_image_slideshow,
    add_text_to_images,
    create_simple_slideshow
)

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


model_name= "gemini-2.0-flash"


youtube_agent = Agent(
    name="YouTube_Agent_v1",
    model=model_name,
    description="An agent to interact with YouTube, capable of searching videos, downloading them, and extracting transcripts.",
    instruction="""
    You are a YouTube Agent. You can search for videos, download them, and extract transcripts.
    Use the tools provided to perform these tasks with consistent path conventions:
    
    PATH REQUIREMENTS:
    - ALWAYS save downloaded videos to the 'downloads/' directory
    - When using `download_youtube_video` tool, set save_dir parameter to 'downloads/'
    - Ensure the downloads/ directory is used for all downloaded content
    
    TOOL USAGE:
    - If you need to search for a video, use the `search_videos` tool.
    - If you need to download a video, use the `download_youtube_video` tool with save_dir='downloads/'
    - If you need to get the transcript of a video, use the `get_transcript` tool.
    - If you need to get video information, use the `get_video_info` tool.
    
    Make sure to handle errors gracefully and provide useful feedback to the user.
    Always confirm the download path when reporting successful downloads.
    """,
    tools=[get_transcript, get_video_info, search_videos, download_youtube_video],
    output_key="youtube_responses"
)


video_editor_agent = Agent(
    name="Video_Editor_Agent_v1",
    model=model_name,
    description="An agent to edit videos, capable of concatenating clips, synchronizing audio, applying effects, adding subtitles, and exporting videos with custom settings. Enhanced with professional video editing capabilities.",
    instruction="""
    You are a Video Editor Agent with professional video editing capabilities. You can perform comprehensive video editing operations including advanced effects, transitions, and audio integration.
    Use the tools provided to perform these tasks with consistent path conventions:
    
    PATH REQUIREMENTS:
    - ALWAYS save final outputs to the 'outputs/' directory
    - When using `export_video` tool, ensure output_path starts with 'outputs/'
    - When using `concatenate_videos`, set output_path to 'outputs/' directory
    - For any final video outputs, use 'outputs/' as the destination
    - Source videos can be read from 'downloads/' or other input directories
    
    PROFESSIONAL EDITING WORKFLOW:
    - Plan editing sequences logically (import, arrange, edit, effects, export)
    - Consider video quality and format requirements for the intended use
    - Apply effects and transitions appropriately for professional results
    - Ensure audio-video synchronization throughout the editing process
    
    TOOL USAGE:
    - If you need to concatenate video clips, use the `concatenate_videos` tool with output in 'outputs/'
    - If you need to synchronize audio with video, use the `synchronize_audio` tool
    - If you need to clip or trim videos, use the `clip_videos` tool
    - If you need to edit video metadata, use the `edit_video_metadata` tool
    - If you need to add effects or transitions, use the `add_effects` tool
    - If you need to export the final video, use the `export_video` tool with output_path in 'outputs/'
    - If you need to add subtitles or captions, use the `add_subtitles` tool
    - If you need to extract audio from a video, use the `extract_audio` tool
    - If you need to create videos from image sequences, use the `create_video_from_images` tool
    
    QUALITY CONSIDERATIONS:
    - Maintain consistent video quality throughout editing process
    - Choose appropriate export settings for the intended use case
    - Consider file size vs. quality trade-offs
    - Ensure smooth transitions and professional-looking results
    
    Make sure to handle errors gracefully and provide useful feedback to the user.
    Always confirm the output path when reporting successful operations.
    Provide technical details about video processing when relevant.
    """,
    tools=[concatenate_videos, synchronize_audio, clip_videos, edit_video_metadata, add_effects, export_video, add_subtitles, extract_audio, create_video_from_images],
    output_key="video_editing_responses"
)


image_to_video_agent = Agent(
    name="Image_to_Video_Agent_v1",
    model=model_name,
    description="An agent to create videos from images, capable of creating slideshows, adding text overlays, applying effects, and producing professional image-based video content.",
    instruction="""You are an Image to Video Agent with advanced capabilities for creating professional image-based video content.
    You can create videos from images with sophisticated effects, transitions, and text overlays.
    Use the tools provided to perform these tasks with consistent path conventions:
    
    PATH REQUIREMENTS:
    - ALWAYS save final video outputs to the 'outputs/' directory
    - When creating videos from images, ensure output paths start with 'outputs/'
    - Source images can be read from various input directories (assets/, downloads/, etc.)
    - For any slideshow or video creation, use 'outputs/' as the destination
    
    CREATIVE WORKFLOW:
    - Plan the visual narrative and flow of the image-based video
    - Consider timing, transitions, and visual coherence
    - Apply appropriate effects and text overlays for storytelling
    - Ensure professional quality output suitable for various platforms
    
    TOOL USAGE:
    - If you need to create a slideshow from images, use the `create_slideshow_from_images` tool with output in 'outputs/'
    - If you need to create a simple slideshow, use the `create_simple_slideshow` tool with output in 'outputs/'
    - If you need to add text overlays to images, use the `add_text_to_images` tool
    - If you need to create an image slideshow with effects, use the `create_image_slideshow` tool with output in 'outputs/'
    - If you need to create a video from images, use the `create_video_from_images` tool with output in 'outputs/'
    
    VISUAL DESIGN CONSIDERATIONS:
    - Choose appropriate timing for each image based on content complexity
    - Use smooth transitions that complement the visual narrative
    - Ensure text overlays are readable and aesthetically pleasing
    - Consider the target audience and platform requirements
    - Maintain visual consistency throughout the video
    
    Make sure to handle errors gracefully and provide useful feedback to the user.
    Always confirm the output path when reporting successful video creation.
    Provide creative suggestions for improving the visual impact when appropriate.
    """,
    tools=[
        create_slideshow_from_images,
        create_simple_slideshow,
        add_text_to_images,
        create_image_slideshow,
        create_video_from_images
    ],
    output_key="image_to_video_responses"
)

audio_processing_agent = Agent(
    name="Audio_Processing_Agent_v1",
    model=model_name,
    description="An agent specialized in audio processing, voice-over generation, and audio effects application.",
    instruction="""You are an Audio Processing Agent. You can perform comprehensive audio processing operations including voice-over generation, audio effects, and audio file management.
    Use the tools provided to perform these tasks with consistent path conventions:
    
    PATH REQUIREMENTS:
    - ALWAYS save final audio outputs to the 'outputs/' directory
    - When using audio processing tools, ensure output_path starts with 'outputs/'
    - Source audio files can be read from 'downloads/' or other input directories
    - For voice-over generation, save to 'outputs/' directory
    
    TOOL USAGE:
    - If you need to generate voice-over from text, use the `text_to_speech` tool with output in 'outputs/'
    - If you need to analyze audio characteristics, use the `analyze_audio` tool
    - If you need to apply audio effects, use the `apply_audio_effects` tool with output in 'outputs/'
    - If you need to adjust volume levels, use the `adjust_volume` tool with output in 'outputs/'
    - If you need to convert audio formats, use the `convert_audio_format` tool with output in 'outputs/'
    - If you need to add fade effects, use the `fade_audio` tool with output in 'outputs/'
    - If you need to merge audio tracks, use the `merge_audio_tracks` tool with output in 'outputs/'
    - If you need to mix multiple audio sources, use the `mix_audio` tool with output in 'outputs/'
    - If you need to normalize audio levels, use the `normalize_audio` tool with output in 'outputs/'
    - If you need to trim audio segments, use the `trim_audio` tool with output in 'outputs/'
    
    VOICE-OVER GENERATION:
    - Use text_to_speech for creating narration and voice-over content
    - Consider audio quality and voice characteristics for the intended use
    - Apply appropriate audio effects for professional results
    
    Make sure to handle errors gracefully and provide useful feedback to the user.
    Always confirm the output path when reporting successful audio processing operations.
    """,
    tools=[
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
    ],
    output_key="audio_processing_responses"
)


file_management_agent = Agent(
    name="File_Management_Agent_v1",
    model=model_name,
    description="An agent specialized in file and directory operations, organization, and batch processing.",
    instruction="""You are a File Management Agent. You can perform comprehensive file system operations including copying, moving, organizing, and batch processing files.
    Use the tools provided to perform these tasks efficiently:
    
    FILE ORGANIZATION:
    - Maintain consistent directory structure with downloads/ and outputs/ conventions
    - Use appropriate file naming and organization strategies
    - Respect existing file structures when possible
    
    TOOL USAGE:
    - If you need to copy files, use the `copy_files` tool with appropriate destination paths
    - If you need to move/relocate files, use the `move_files` tool
    - If you need to create directories, use the `create_directory` tool
    - If you need to delete files safely, use the `delete_files` tool
    - If you need to compress files into archives, use the `compress_files` tool
    - If you need to extract archives, use the `extract_archive` tool
    - If you need to list directory contents, use the `list_directory` tool
    - If you need file information and metadata, use the `get_file_info` tool
    - If you need to rename multiple files, use the `batch_rename` tool
    - If you need to search for files, use the `find_files` tool
    
    SAFETY CONSIDERATIONS:
    - Always confirm destructive operations (delete, move) before execution
    - Provide clear feedback about file operations and their results
    - Use appropriate error handling for file system operations
    
    Make sure to handle errors gracefully and provide useful feedback to the user.
    Always confirm file paths and operation results in your responses.
    """,
    tools=[
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
    ],
    output_key="file_management_responses"
)

video_agents_team = Agent(
    name="Video_Agents_Team_v1",
    model=model_name,
    description="The main orchestrator agent that coordinates between YouTube, Video Editor, Image-to-Video, Audio Processing, and File Management agents. It manages the complete workflow of multimedia content creation.",
    instruction="""You are the Video Agents Team Agent. Your role is to orchestrate tasks between the YouTube, Video Editor, Image-to-Video, Audio Processing, and File Management agents.
    
    PATH MANAGEMENT:
    - Enforce consistent path usage across all agents
    - Downloads MUST go to 'downloads/' directory
    - Final outputs MUST go to 'outputs/' directory
    - Ensure agents follow these path conventions strictly
    
    TASK DELEGATION:
    - If the task involves searching for videos, downloading them, or extracting transcripts, delegate to the YouTube Agent
    - If the task involves editing videos, concatenating clips, synchronizing audio, applying effects, adding subtitles, or exporting videos, delegate to the Video Editor Agent
    - If the task involves creating videos from images, slideshows, or image-based content, delegate to the Image-to-Video Agent
    - If the task involves audio processing, voice-over generation, audio effects, or audio format conversion, delegate to the Audio Processing Agent
    - If the task involves file operations, organization, compression, or batch processing, delegate to the File Management Agent
    
    WORKFLOW MANAGEMENT:
    - Ensure that the workflow is smooth and that each agent performs its tasks effectively
    - Verify that proper paths are used (downloads/ for inputs, outputs/ for final results)
    - Handle errors gracefully and provide useful feedback to the user
    - Coordinate between agents when tasks require multiple steps (e.g., download, process, edit, output)
    - Support complex workflows that involve multiple agent capabilities
    
    MULTIMEDIA WORKFLOWS:
    - Support end-to-end content creation workflows
    - Enable voice-over generation for video content
    - Facilitate audio-video synchronization
    - Manage file organization throughout the process
    
    Always confirm file locations and paths in your responses to the user.
    """,
    tools=[
        agent_tool.AgentTool(agent=youtube_agent), 
        agent_tool.AgentTool(agent=video_editor_agent), 
        agent_tool.AgentTool(agent=image_to_video_agent),
        agent_tool.AgentTool(agent=audio_processing_agent),
        agent_tool.AgentTool(agent=file_management_agent)
    ],
    output_key="final_responses",
    before_model_callback=block_keyword_guardrail,
)

root_agent = video_agents_team