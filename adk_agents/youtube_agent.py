from google.adk.agents import Agent

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
    tools=[get_transcript, get_video_info, search_videos, download_youtube_video]
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
    tools=[concatenate_videos, synchronize_audio, clip_videos, edit_video_metadata, add_effects, export_video, add_subtitles]
)

