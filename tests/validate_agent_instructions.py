#!/usr/bin/env python3
"""
Agent Instructions Validation
=============================

Validates that the Video_Editor_Agent_v1 instructions correctly reference 
all available tools and provides comprehensive coverage.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def validate_agent_instructions():
    """Validate that agent instructions match available tools"""
    
    print("🔍 Validating Video_Editor_Agent_v1 Instructions")
    print("=" * 60)
    
    # Import the agent and tools
    from adk_agents.youtube_agent import video_editor_agent
    from tools.video_editor_tools import (
        concatenate_videos,
        synchronize_audio,
        clip_videos,
        edit_video_metadata,
        add_effects,
        export_video,
        add_subtitles
    )
    
    # Available tools
    available_tools = {
        'concatenate_videos': concatenate_videos,
        'synchronize_audio': synchronize_audio,
        'clip_videos': clip_videos,
        'edit_video_metadata': edit_video_metadata,
        'add_effects': add_effects,
        'export_video': export_video,
        'add_subtitles': add_subtitles
    }
    
    # Agent's configured tools
    agent_tools = video_editor_agent.tools
    agent_tool_names = [tool.__name__ for tool in agent_tools]
    
    print(f"📊 Agent Information:")
    print(f"   Name: {video_editor_agent.name}")
    print(f"   Model: {video_editor_agent.model}")
    print(f"   Description: {video_editor_agent.description}")
    
    print(f"\n🛠️  Available Tools ({len(available_tools)}):")
    for i, tool_name in enumerate(available_tools.keys(), 1):
        print(f"   {i}. {tool_name}")
    
    print(f"\n🤖 Agent Configured Tools ({len(agent_tool_names)}):")
    for i, tool_name in enumerate(agent_tool_names, 1):
        print(f"   {i}. {tool_name}")
    
    # Validation checks
    print(f"\n✅ Validation Results:")
    
    all_tools_configured = True
    for tool_name in available_tools.keys():
        if tool_name in agent_tool_names:
            print(f"   ✅ {tool_name} - Configured correctly")
        else:
            print(f"   ❌ {tool_name} - Missing from agent configuration")
            all_tools_configured = False
    
    # Check for extra tools
    extra_tools = set(agent_tool_names) - set(available_tools.keys())
    if extra_tools:
        print(f"   ⚠️  Extra tools in agent: {', '.join(extra_tools)}")
    
    # Check instruction content
    instruction = video_editor_agent.instruction
    print(f"\n📋 Instruction Analysis:")
    
    tool_mentions = {}
    for tool_name in available_tools.keys():
        if f"`{tool_name}`" in instruction:
            tool_mentions[tool_name] = True
            print(f"   ✅ {tool_name} - Mentioned in instructions")
        else:
            tool_mentions[tool_name] = False
            print(f"   ❌ {tool_name} - Not mentioned in instructions")
    
    # Overall assessment
    tools_match = len(available_tools) == len(agent_tool_names) and all_tools_configured
    instructions_complete = all(tool_mentions.values())
    
    print(f"\n📈 Overall Assessment:")
    print(f"   Tools Configuration: {'✅ PASS' if tools_match else '❌ FAIL'}")
    print(f"   Instruction Coverage: {'✅ PASS' if instructions_complete else '❌ FAIL'}")
    print(f"   Overall Status: {'✅ VALID' if tools_match and instructions_complete else '❌ NEEDS FIXES'}")
    
    # Detailed instruction breakdown
    print(f"\n📝 Current Instructions:")
    print(f"   {instruction.strip()}")
    
    return tools_match and instructions_complete

if __name__ == "__main__":
    try:
        is_valid = validate_agent_instructions()
        exit_code = 0 if is_valid else 1
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        sys.exit(1)
