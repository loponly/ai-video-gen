from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

from google.genai import types

from typing import Optional


def block_keyword_guardrail(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """
    Inspects the latest user message for 'BLOCK'. If found, blocks the LLM call
    and returns a predefined LlmResponse. Otherwise, returns None to proceed.
    """
    agent_name = callback_context.agent_name
    print(f"Calling guardrail for agent: {agent_name}")

    # Extract the latest user message
    latest_user_message = "" # Default to empty string if no messages are present

    if llm_request.contents:
        # Find the recent message from the user
        for content in reversed(llm_request.contents):
            if content.role == "user":
                if content.parts[0].text:
                    latest_user_message = content.parts[0].text
                    break # Found the latest user message
    print(f"--- Callback: Inspecting last user message: '{latest_user_message[:100]}...' ---") # Log first 100 chars

    keyword_to_block = "BLOCK"
    if keyword_to_block in latest_user_message.upper():
        print(f"--- Callback: Blocking LLM call due to keyword '{keyword_to_block}' found in user message ---")
        # Create a predefined response indicating the block
        return LlmResponse(content=types.Content(
                    role= "model",
                    parts=[types.Part(text=f"Your request contains the keyword '{keyword_to_block}'. This action is blocked for security reasons. Please rephrase your request without this keyword.")]
                )            
        )
    else:
        print(f"--- Callback: No blocking keyword found. Proceeding with LLM call ---")
        # Return None to indicate no blocking, allowing the LLM call to proceed
        return None