from google.adk.agents import Agent

# Tools imports
from tools.youtube_tools import (
    get_transcript,
    get_video_info,
    search_videos,
    download_youtube_video
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
    description="An agent to edit videos, capable of concatenating video clips and synchronizing them with audio.",
    instruction="""
    You are a Video Editor Agent. You can concatenate video clips and synchronize them with audio.
    Use the tools provided to perform these tasks.
    If you need to concatenate video clips, use the `concatenate_videos` tool.
    If you need to synchronize audio with video, use the `synchronize_audio` tool.
    Make sure to handle errors gracefully and provide useful feedback to the user.
    """,
    tools=[]  # Add video editing tools here when implemented
)

