import os
import sys
import asyncio
import warnings
import argparse
from pathlib import Path
from typing import Dict

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


async def run_conversation(query: str = None):
    """
    Run a conversation with the agent.
    
    This function will prompt the user for input and call the agent asynchronously.
    
    Args:
        query: The query to send to the agent. If None, will use a default test query.
    """
    if query is None:
        query = "Please help me understand what you can do."
    
    print(f">>> User Query: {query}")
    runner = await create_runner()
    response = await call_agent_async(query,
                                    runner=runner,
                                    user_id=USER_ID,
                                    session_id=SESSION_ID)
    return response


def create_test_queries() -> Dict[str, str]:
    """
    Create a set of test queries for different agents.
    
    Returns:
        Dictionary of test queries for different scenarios.
    """
    return {
        "image_to_video_basic": """I want to create a simple slideshow video from images. 
                                   Please create a slideshow using the images in the movie-reels/images/ folder. 
                                   Make each image display for 3 seconds with fade transitions.""",
        
        "image_to_video_advanced": """Create an advanced slideshow video with the following specs:
                                     - Use images from movie-reels/images/ folder
                                     - Each image should display for 4 seconds
                                     - Add slide_left transitions between images
                                     - Add text overlay saying 'Sample Slideshow' at the top
                                     - Export to movie-reels/output/test_slideshow.mp4""",
        
        "youtube_search": "Search for videos about 'Python programming tutorial' and show me the top 3 results.",
        
        "video_editing": "Help me concatenate multiple video files and add subtitles to the final video.",
        
        "general": "What can you help me with? Please explain your capabilities."
    }


async def run_test_scenario(test_name: str):
    """
    Run a specific test scenario.
    
    Args:
        test_name: Name of the test scenario to run.
    """
    test_queries = create_test_queries()
    
    if test_name not in test_queries:
        print(f"❌ Test scenario '{test_name}' not found.")
        print(f"Available tests: {', '.join(test_queries.keys())}")
        return
    
    print(f"🧪 Running test scenario: {test_name}")
    print("=" * 50)
    
    query = test_queries[test_name]
    response = await run_conversation(query)
    
    print("=" * 50)
    print(f"✅ Test scenario '{test_name}' completed.")
    return response

def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="AI Video Generation Agent Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent_runner.py --query "Create a slideshow from my images"
  python agent_runner.py --test image_to_video_basic
  python agent_runner.py --test-all
  python agent_runner.py --list-tests
        """
    )
    
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Query to send to the agent"
    )
    
    parser.add_argument(
        "--test", "-t",
        type=str,
        help="Run a specific test scenario"
    )
    
    parser.add_argument(
        "--test-all",
        action="store_true",
        help="Run all test scenarios"
    )
    
    parser.add_argument(
        "--list-tests",
        action="store_true",
        help="List all available test scenarios"
    )
    
    return parser.parse_args()


async def main():
    """
    Main function to handle command line arguments and run the appropriate action.
    """
    args = parse_arguments()
    
    # List available tests
    if args.list_tests:
        test_queries = create_test_queries()
        print("📋 Available test scenarios:")
        for test_name, description in test_queries.items():
            print(f"  • {test_name}: {description[:80]}{'...' if len(description) > 80 else ''}")
        return
    
    # Run all tests
    if args.test_all:
        test_queries = create_test_queries()
        print(f"🚀 Running all {len(test_queries)} test scenarios...")
        
        for test_name in test_queries.keys():
            await run_test_scenario(test_name)
            print("\n" + "="*60 + "\n")
        
        print("🎉 All tests completed!")
        return
    
    # Run specific test
    if args.test:
        await run_test_scenario(args.test)
        return
    
    # Run with custom query
    if args.query:
        await run_conversation(args.query)
        return
    
    # Interactive mode
    print(f"👋 Welcome to {APP_NAME}!")
    print("💡 Tip: Use --help to see command line options")
    
    # Run with default query if no arguments provided
    await run_conversation()
    
    
    

if __name__ == "__main__":
    asyncio.run(main())
