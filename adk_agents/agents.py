from google.adk.agents import Agent
from guards.block_keyword import block_keyword_guardrail

# Tools imports
from tools.youtube_tools import (
    get_transcript,
    get_video_info,
    search_videos,
    download_youtube_video
)

from tools.video_editor_tools import (
    concatenate_videos,
    synchronize_audio,
    clip_videos,
    edit_video_metadata,
    add_effects,
    export_video,
    add_subtitles
)
 
from tools.image_editor_tools import (
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
    Use the tools provided to perform these tasks. 
    If you need to search for a video, use the `search_videos` tool.
    If you need to download a video, use the `download_youtube_video` tool.
    If you need to get the transcript of a video, use the `get_transcript` tool.
    If you need to get video information, use the `get_video_info` tool.
    Make sure to handle errors gracefully and provide useful feedback to the user.
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
    Use the tools provided to perform these tasks.
    If you need to concatenate video clips, use the `concatenate_videos` tool.
    If you need to synchronize audio with video, use the `synchronize_audio` tool.
    If you need to clip videos, use the `clip_videos` tool.
    If you need to edit video metadata, use the `edit_video_metadata` tool.
    If you need to add effects or transitions, use the `add_effects` tool.
    If you need to export the final video, use the `export_video` tool.
    If you need to add subtitles or captions, use the `add_subtitles` tool.
    Make sure to handle errors gracefully and provide useful feedback to the user.
    """,
    tools=[concatenate_videos, synchronize_audio, clip_videos, edit_video_metadata, add_effects, export_video, add_subtitles],
    output_key="video_editing_responses"
)


image_to_video_agent = Agent(
    name="Image_to_Video_Agent_v1",
    model=model_name,
    description="An agent to create videos from images, capable of creating slideshows, adding text overlays, and applying effects.",
    instruction="""    You are an Image to Video Agent. You can create videos from images.
    Use the tools provided to perform these tasks.
    If you need to create a slideshow from images, use the `create_slideshow_from_images` tool.
    If you need to create a simple slideshow, use the `create_simple_slideshow` tool.
    If you need to add text overlays to images, use the `add_text_to_images` tool.
    If you need to create an image slideshow with effects, use the `create_image_slideshow` tool.
    Make sure to handle errors gracefully and provide useful feedback to the user.
    """,
    tools=[
        create_slideshow_from_images,
        create_simple_slideshow,
        add_text_to_images,
        create_image_slideshow
    ],
    output_key="image_to_video_responses"
)

video_agents_team = Agent(
    name="Video_Agents_Team_v1",
    model=model_name,
    description="The main orchestrator agent that coordinates between YouTube and Video Editor agents. It also manages the workflow of agent interactions.",
    instruction="""You are the Video Agents Team Agent. Your role is to orchestrate tasks between the YouTube and Video Editor agents.
    You will delegate tasks to the appropriate agent based on the user's request.
    If the task involves searching for videos, downloading them, or extracting transcripts, delegate to the YouTube Agent.
    If the task involves editing videos, concatenating clips, synchronizing audio,
    applying effects, adding subtitles, or exporting videos, delegate to the Video Editor Agent.
    Ensure that the workflow is smooth and that each agent performs its tasks effectively.
    Handle errors gracefully and provide useful feedback to the user.
    """,
    sub_agents=[youtube_agent, video_editor_agent,image_to_video_agent],
    output_key="final_responses",
    before_model_callback=block_keyword_guardrail,
)

root_agent = video_agents_team