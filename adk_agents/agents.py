"""
AI Video Generator Agents Configuration

This module defines the agent team structure with consistent path management:
- Downloads: All downloaded content goes to 'downloads/' directory
- Outputs: All final results go to 'outputs/' directory
- Path validation is enforced through agent instructions

Agent Hierarchy:
├── video_agents_team (root orchestrator)
    ├── youtube_agent (downloads to downloads/)
    ├── video_editor_agent (outputs to outputs/)
    └── image_to_video_agent (outputs to outputs/)
"""

from google.adk.agents import Agent
from guards.block_keyword import block_keyword_guardrail
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
    description="An agent to edit videos, capable of concatenating clips, synchronizing audio, applying effects, adding subtitles, and exporting videos with custom settings.",
    instruction="""
    You are a Video Editor Agent. You can perform comprehensive video editing operations.
    Use the tools provided to perform these tasks with consistent path conventions:
    
    PATH REQUIREMENTS:
    - ALWAYS save final outputs to the 'outputs/' directory
    - When using `export_video` tool, ensure output_path starts with 'outputs/'
    - When using `concatenate_videos`, set output_path to 'outputs/' directory
    - For any final video outputs, use 'outputs/' as the destination
    - Source videos can be read from 'downloads/' or other input directories
    
    TOOL USAGE:
    - If you need to concatenate video clips, use the `concatenate_videos` tool with output in 'outputs/'
    - If you need to synchronize audio with video, use the `synchronize_audio` tool
    - If you need to clip videos, use the `clip_videos` tool
    - If you need to edit video metadata, use the `edit_video_metadata` tool
    - If you need to add effects or transitions, use the `add_effects` tool
    - If you need to export the final video, use the `export_video` tool with output_path in 'outputs/'
    - If you need to add subtitles or captions, use the `add_subtitles` tool
    - If you need to extract audio from a video, use the `extract_audio` tool
    
    Make sure to handle errors gracefully and provide useful feedback to the user.
    Always confirm the output path when reporting successful operations.
    """,
    tools=[concatenate_videos, synchronize_audio, clip_videos, edit_video_metadata, add_effects, export_video, add_subtitles, extract_audio],
    output_key="video_editing_responses"
)


image_to_video_agent = Agent(
    name="Image_to_Video_Agent_v1",
    model=model_name,
    description="An agent to create videos from images, capable of creating slideshows, adding text overlays, and applying effects.",
    instruction="""You are an Image to Video Agent. You can create videos from images.
    Use the tools provided to perform these tasks with consistent path conventions:
    
    PATH REQUIREMENTS:
    - ALWAYS save final video outputs to the 'outputs/' directory
    - When creating videos from images, ensure output paths start with 'outputs/'
    - Source images can be read from various input directories (assets/, downloads/, etc.)
    - For any slideshow or video creation, use 'outputs/' as the destination
    
    TOOL USAGE:
    - If you need to create a slideshow from images, use the `create_slideshow_from_images` tool with output in 'outputs/'
    - If you need to create a simple slideshow, use the `create_simple_slideshow` tool with output in 'outputs/'
    - If you need to add text overlays to images, use the `add_text_to_images` tool
    - If you need to create an image slideshow with effects, use the `create_image_slideshow` tool with output in 'outputs/'
    - If you need to create a video from images, use the `create_video_from_images` tool with output in 'outputs/'
    
    Make sure to handle errors gracefully and provide useful feedback to the user.
    Always confirm the output path when reporting successful video creation.
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

video_agents_team = Agent(
    name="Video_Agents_Team_v1",
    model=model_name,
    description="The main orchestrator agent that coordinates between YouTube and Video Editor agents. It also manages the workflow of agent interactions.",
    instruction="""You are the Video Agents Team Agent. Your role is to orchestrate tasks between the YouTube, Video Editor, and Image-to-Video agents.
    
    PATH MANAGEMENT:
    - Enforce consistent path usage across all agents
    - Downloads MUST go to 'downloads/' directory
    - Final outputs MUST go to 'outputs/' directory
    - Ensure agents follow these path conventions strictly
    
    TASK DELEGATION:
    - If the task involves searching for videos, downloading them, or extracting transcripts, delegate to the YouTube Agent
    - If the task involves editing videos, concatenating clips, synchronizing audio, applying effects, adding subtitles, or exporting videos, delegate to the Video Editor Agent
    - If the task involves creating videos from images, slideshows, or image-based content, delegate to the Image-to-Video Agent
    
    WORKFLOW MANAGEMENT:
    - Ensure that the workflow is smooth and that each agent performs its tasks effectively
    - Verify that proper paths are used (downloads/ for inputs, outputs/ for final results)
    - Handle errors gracefully and provide useful feedback to the user
    - Coordinate between agents when tasks require multiple steps (e.g., download then edit)
    
    Always confirm file locations and paths in your responses to the user.
    """,
    sub_agents=[youtube_agent, video_editor_agent,image_to_video_agent],
    output_key="final_responses",
    before_model_callback=block_keyword_guardrail,
)

root_agent = video_agents_team