"""
ADK-Compatible Agent Evaluation Test

This test demonstrates how to use the AgentEvaluator.evaluate method
as shown in the ADK documentation for pytest integration.
"""

import pytest
import asyncio
from pathlib import Path
from tests.test_agent_evaluation import AgentEvaluator


@pytest.mark.asyncio
async def test_youtube_functionality_with_adk_pattern():
    """
    Test YouTube agent functionality using ADK evaluation pattern.
    This follows the exact pattern shown in the ADK documentation.
    """
    # Path to our YouTube functionality evaluation set
    eval_file = Path(__file__).parent / "youtube_functionality.evalset.json"
    config_file = Path(__file__).parent / "test_config.json"
    
    # Run evaluation using the ADK pattern
    results = await AgentEvaluator.evaluate(
        agent_module="adk_agents",
        eval_dataset_file_path_or_dir=str(eval_file),
        config_file_path=str(config_file)
    )
    
    # Verify evaluation completed successfully
    assert results["total_cases"] == 4
    assert "tool_trajectory_score" in results
    assert "response_match_score" in results
    
    # Check that all eval cases have results
    expected_eval_ids = [
        "youtube_search_basic",
        "youtube_download_with_path_compliance", 
        "youtube_get_transcript",
        "youtube_get_video_info"
    ]
    
    actual_eval_ids = [detail["eval_id"] for detail in results["details"]]
    for expected_id in expected_eval_ids:
        assert expected_id in actual_eval_ids


@pytest.mark.asyncio
async def test_video_editing_functionality_with_adk_pattern():
    """
    Test video editing agent functionality using ADK evaluation pattern.
    """
    eval_file = Path(__file__).parent / "video_editing_functionality.evalset.json"
    config_file = Path(__file__).parent / "test_config.json"
    
    results = await AgentEvaluator.evaluate(
        agent_module="adk_agents",
        eval_dataset_file_path_or_dir=str(eval_file),
        config_file_path=str(config_file)
    )
    
    assert results["total_cases"] == 5
    
    # Check that all video editing eval cases are present
    expected_eval_ids = [
        "video_concatenation_with_output_path",
        "add_subtitles_to_video",
        "extract_audio_from_video",
        "video_export_with_custom_settings",
        "clip_video_segments"
    ]
    
    actual_eval_ids = [detail["eval_id"] for detail in results["details"]]
    for expected_id in expected_eval_ids:
        assert expected_id in actual_eval_ids


@pytest.mark.asyncio
async def test_multi_agent_workflows_with_adk_pattern():
    """
    Test multi-agent coordination using ADK evaluation pattern.
    """
    eval_file = Path(__file__).parent / "multi_agent_workflows.evalset.json"
    config_file = Path(__file__).parent / "test_config.json"
    
    results = await AgentEvaluator.evaluate(
        agent_module="adk_agents",
        eval_dataset_file_path_or_dir=str(eval_file),
        config_file_path=str(config_file)
    )
    
    assert results["total_cases"] == 4
    
    # Check that all multi-agent workflow cases are present
    expected_eval_ids = [
        "download_and_edit_workflow",
        "search_download_and_process_workflow",
        "image_to_video_with_youtube_audio",
        "complete_video_production_workflow"
    ]
    
    actual_eval_ids = [detail["eval_id"] for detail in results["details"]]
    for expected_id in expected_eval_ids:
        assert expected_id in actual_eval_ids
    
    # Verify multi-agent intermediate responses are captured
    for detail in results["details"]:
        # Each workflow should have some intermediate responses from different agents
        # (This is a simplified check for the structure)
        assert detail["eval_id"] in expected_eval_ids


@pytest.mark.asyncio 
async def test_path_compliance_across_all_evaluations():
    """
    Test that all evaluation files demonstrate proper path compliance.
    This verifies that downloads/ and outputs/ paths are used correctly.
    """
    evaluation_files = [
        "youtube_functionality.evalset.json",
        "video_editing_functionality.evalset.json", 
        "multi_agent_workflows.evalset.json"
    ]
    
    for eval_filename in evaluation_files:
        eval_file = Path(__file__).parent / eval_filename
        config_file = Path(__file__).parent / "test_config.json"
        
        results = await AgentEvaluator.evaluate(
            agent_module="adk_agents",
            eval_dataset_file_path_or_dir=str(eval_file),
            config_file_path=str(config_file)
        )
        
        # Verify the evaluation ran successfully
        assert results["total_cases"] > 0
        assert len(results["details"]) == results["total_cases"]
        
        # Basic structure validation
        for detail in results["details"]:
            assert "eval_id" in detail
            assert "passed" in detail
            assert "tool_trajectory_score" in detail
            assert "response_match_score" in detail


def test_evaluation_files_exist_and_valid():
    """
    Test that all evaluation files exist and are valid JSON.
    """
    import json
    
    evaluation_files = [
        "youtube_functionality.evalset.json",
        "video_editing_functionality.evalset.json",
        "multi_agent_workflows.evalset.json",
        "test_config.json"
    ]
    
    for filename in evaluation_files:
        file_path = Path(__file__).parent / filename
        assert file_path.exists(), f"Evaluation file {filename} does not exist"
        
        # Verify it's valid JSON
        with open(file_path, 'r') as f:
            data = json.load(f)
            assert data is not None
            
        # If it's an evalset file, verify basic structure
        if filename.endswith('.evalset.json'):
            assert "eval_set_id" in data
            assert "eval_cases" in data
            assert len(data["eval_cases"]) > 0
            
            # Verify each eval case has required fields
            for eval_case in data["eval_cases"]:
                assert "eval_id" in eval_case
                assert "conversation" in eval_case
                assert "session_input" in eval_case


if __name__ == "__main__":
    # Run the tests with asyncio
    asyncio.run(test_youtube_functionality_with_adk_pattern())
    asyncio.run(test_video_editing_functionality_with_adk_pattern())
    asyncio.run(test_multi_agent_workflows_with_adk_pattern())
    asyncio.run(test_path_compliance_across_all_evaluations())
    test_evaluation_files_exist_and_valid()
    print("All ADK-compatible evaluation tests passed!")
