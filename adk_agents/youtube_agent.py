from google.adk.agents import Agent

# Tools imports
from tools.youtube_tools import (
    get_transcript,
    get_video_info,
    search_videos,
    download_youtube_video,
    convert_webm_to_mp4
)
 


model_name= "gemini-2.0-flash-preview-image-generation"




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
    If you need to convert a video from webm to mp4, use the `convert_webm_to_mp4` tool.
    Make sure to handle errors gracefully and provide useful feedback to the user.
    """,
    tools=[get_transcript, get_video_info, search_videos, download_youtube_video, convert_webm_to_mp4]
)


