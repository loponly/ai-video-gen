import os
import asyncio
import warnings

from dotenv import load_dotenv

from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.runners import Runner

from google.genai import types

from adk_agents.agents import root_agent


# InMemorySessionService is simple, non-persistent storage for this tutorial.
session_service = InMemorySessionService()

# Load environment variables from .env file
load_dotenv()
# Ignore all warnings
warnings.filterwarnings("ignore")


APP_NAME = "Content Creator Agents"
USER_ID =  "user-12345"  # Replace with your user ID
SESSION_ID = "session-1234"  # Replace with your session ID

async def create_runner():
    """
    Create a Runner instance for the YouTube agent.
    
    :return: A Runner instance configured with the YouTube agent and session service.
    """
    await session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state={
        "user_preferences": {
            "language": "en",
            "video_quality": "720p",
            "transcript_format": "srt",
        },
    }
    )
  # Ensure the session service is initialized
    return Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )


async def call_agent_async(prompt: str,runner: Runner,user_id: str, session_id: str) -> str:
    """
    Call the agent asynchronously with the given prompt.
    
    :param prompt: The input prompt for the agent.
    :param runner: The Runner instance to execute the agent.
    :param user_id: The user ID for session tracking.
    :param session_id: The session ID for session tracking.
    :return: The response from the agent.
    """
    content = types.Content(role='user', parts=[types.Part(text=prompt)])
    
    final_response_text = "Agent did not respond." # Default response if no content is returned
    async for event in runner.run_async(new_message=content, user_id=user_id, session_id=session_id):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                # Add more checks here if needed (e.g., specific error codes)
            break # Stop processing events once the final response is found
        
    print(f"<<< Agent Response: {final_response_text}")
    return final_response_text


async def run_conversation():
    """
    Run a conversation with the agent.
    
    This function will prompt the user for input and call the agent asynchronously.
    """
    runner = await create_runner()
    await call_agent_async(""" BLOCK What is information about this video  https://www.youtube.com/watch?v=pdwp6S1lrP0.
                           Download the video and add effects. The effect should fade in and out Then concatenate 10 seconds of the video""",
                                       runner=runner,
                                       user_id=USER_ID,
                                       session_id=SESSION_ID)
    
    
    

if __name__ == "__main__":
    print(f"👋 Welcome to {APP_NAME}!")

    asyncio.run(run_conversation())
