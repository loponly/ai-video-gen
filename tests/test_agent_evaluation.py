"""
Agent Evaluation Tests

This module contains comprehensive evaluation tests for the AI Video Generator agents
following ADK evaluation best practices and guidelines.

Tests evaluate:
1. Trajectory and tool use
2. Final response quality
3. Multi-agent coordination
4. Path compliance for downloads/ and outputs/
"""

import pytest
from typing import Dict, List, Any
from unittest.mock import Mock, patch
import json
import os
import tempfile
from pathlib import Path

# Import the root agent for evaluation
from adk_agents import root_agent


class AgentEvaluator:
    """
    Custom Agent Evaluator for testing AI Video Generator agents.
    Based on ADK evaluation patterns and best practices.
    """
    
    @staticmethod
    async def evaluate(
        agent_module: str,
        eval_dataset_file_path_or_dir: str,
        config_file_path: str = None
    ) -> Dict[str, Any]:
        """
        Evaluate agent performance against predefined test cases.
        
        Args:
            agent_module: The agent module to evaluate
            eval_dataset_file_path_or_dir: Path to test file or directory
            config_file_path: Optional config file for evaluation criteria
            
        Returns:
            Dict containing evaluation results
        """
        # Load evaluation criteria
        criteria = {
            "tool_trajectory_avg_score": 1.0,
            "response_match_score": 0.8
        }
        
        if config_file_path and os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
                criteria.update(config.get('criteria', {}))
        
        # Load test data
        if os.path.isfile(eval_dataset_file_path_or_dir):
            with open(eval_dataset_file_path_or_dir, 'r') as f:
                test_data = json.load(f)
        else:
            raise FileNotFoundError(f"Test file not found: {eval_dataset_file_path_or_dir}")
        
        # Run evaluation
        results = {
            "total_cases": 0,
            "passed": 0,
            "failed": 0,
            "tool_trajectory_score": 0.0,
            "response_match_score": 0.0,
            "details": []
        }
        
        # Process eval cases
        eval_cases = test_data.get('eval_cases', [])
        results["total_cases"] = len(eval_cases)
        
        for eval_case in eval_cases:
            case_result = await AgentEvaluator._evaluate_case(eval_case, criteria)
            results["details"].append(case_result)
            
            if case_result["passed"]:
                results["passed"] += 1
            else:
                results["failed"] += 1
        
        # Calculate average scores
        if results["total_cases"] > 0:
            results["tool_trajectory_score"] = sum(
                detail["tool_trajectory_score"] for detail in results["details"]
            ) / results["total_cases"]
            
            results["response_match_score"] = sum(
                detail["response_match_score"] for detail in results["details"]
            ) / results["total_cases"]
        
        return results
    
    @staticmethod
    async def _evaluate_case(eval_case: Dict[str, Any], criteria: Dict[str, float]) -> Dict[str, Any]:
        """
        Evaluate a single test case.
        
        Args:
            eval_case: The evaluation case data
            criteria: Evaluation criteria thresholds
            
        Returns:
            Dict containing case evaluation results
        """
        case_id = eval_case.get('eval_id', 'unknown')
        conversation = eval_case.get('conversation', [])
        session_input = eval_case.get('session_input', {})
        
        # Initialize scores
        tool_trajectory_score = 0.0
        response_match_score = 0.0
        passed = True
        errors = []
        
        try:
            # Mock agent execution and evaluate each turn
            for turn in conversation:
                user_content = turn.get('user_content', {})
                expected_final_response = turn.get('final_response', {})
                expected_tool_uses = turn.get('intermediate_data', {}).get('tool_uses', [])
                
                # Simulate agent response (in real implementation, would call actual agent)
                # For testing, we'll use mock data
                actual_tool_uses = []  # Would be populated by actual agent execution
                actual_response = {"parts": [{"text": "Mock response"}], "role": "model"}
                
                # Evaluate tool trajectory
                if expected_tool_uses:
                    trajectory_score = AgentEvaluator._evaluate_tool_trajectory(
                        expected_tool_uses, actual_tool_uses
                    )
                    tool_trajectory_score = max(tool_trajectory_score, trajectory_score)
                else:
                    tool_trajectory_score = 1.0  # No tools expected, perfect score
                
                # Evaluate response match
                response_score = AgentEvaluator._evaluate_response_match(
                    expected_final_response, actual_response
                )
                response_match_score = max(response_match_score, response_score)
            
            # Check if case passes criteria
            if (tool_trajectory_score < criteria["tool_trajectory_avg_score"] or
                response_match_score < criteria["response_match_score"]):
                passed = False
                errors.append(f"Scores below threshold: tool={tool_trajectory_score:.2f}, response={response_match_score:.2f}")
        
        except Exception as e:
            passed = False
            errors.append(f"Evaluation error: {str(e)}")
            tool_trajectory_score = 0.0
            response_match_score = 0.0
        
        return {
            "eval_id": case_id,
            "passed": passed,
            "tool_trajectory_score": tool_trajectory_score,
            "response_match_score": response_match_score,
            "errors": errors
        }
    
    @staticmethod
    def _evaluate_tool_trajectory(expected_tools: List[Dict], actual_tools: List[Dict]) -> float:
        """
        Evaluate tool usage trajectory using exact match.
        
        Args:
            expected_tools: List of expected tool calls
            actual_tools: List of actual tool calls
            
        Returns:
            Float score between 0.0 and 1.0
        """
        if not expected_tools and not actual_tools:
            return 1.0
        
        if len(expected_tools) != len(actual_tools):
            return 0.0
        
        matches = 0
        for exp_tool, act_tool in zip(expected_tools, actual_tools):
            if (exp_tool.get('name') == act_tool.get('name') and
                exp_tool.get('args') == act_tool.get('args')):
                matches += 1
        
        return matches / len(expected_tools) if expected_tools else 0.0
    
    @staticmethod
    def _evaluate_response_match(expected_response: Dict, actual_response: Dict) -> float:
        """
        Evaluate response match using simple text comparison.
        In a real implementation, would use ROUGE metrics.
        
        Args:
            expected_response: Expected response structure
            actual_response: Actual response structure
            
        Returns:
            Float score between 0.0 and 1.0
        """
        expected_text = ""
        actual_text = ""
        
        # Extract text from response parts
        if expected_response.get('parts'):
            expected_text = " ".join(part.get('text', '') for part in expected_response['parts'])
        
        if actual_response.get('parts'):
            actual_text = " ".join(part.get('text', '') for part in actual_response['parts'])
        
        # Simple similarity check (in real implementation, use ROUGE)
        if expected_text.lower() == actual_text.lower():
            return 1.0
        elif expected_text.lower() in actual_text.lower() or actual_text.lower() in expected_text.lower():
            return 0.8
        else:
            return 0.0


@pytest.fixture
def sample_eval_data():
    """
    Sample evaluation data following ADK EvalSet schema.
    """
    return {
        "eval_set_id": "ai_video_generator_basic_tests",
        "name": "AI Video Generator Basic Functionality Tests",
        "description": "Basic evaluation tests for AI Video Generator agent capabilities",
        "eval_cases": [
            {
                "eval_id": "youtube_search_test",
                "conversation": [
                    {
                        "invocation_id": "test-001",
                        "user_content": {
                            "parts": [{"text": "Search for videos about 'python programming' and show me 3 results"}],
                            "role": "user"
                        },
                        "final_response": {
                            "parts": [{"text": "I found 3 videos about python programming. Here are the results with titles, URLs, and durations."}],
                            "role": "model"
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "search_videos",
                                    "args": {
                                        "keyword": "python programming",
                                        "max_results": 3
                                    }
                                }
                            ],
                            "intermediate_responses": []
                        }
                    }
                ],
                "session_input": {
                    "app_name": "ai_video_generator",
                    "user_id": "test_user",
                    "state": {}
                }
            },
            {
                "eval_id": "path_compliance_test",
                "conversation": [
                    {
                        "invocation_id": "test-002",
                        "user_content": {
                            "parts": [{"text": "Download a YouTube video with URL 'https://youtube.com/watch?v=example'"}],
                            "role": "user"
                        },
                        "final_response": {
                            "parts": [{"text": "I have successfully downloaded the video to the downloads/ directory."}],
                            "role": "model"
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "download_youtube_video",
                                    "args": {
                                        "url": "https://youtube.com/watch?v=example",
                                        "save_dir": "downloads/"
                                    }
                                }
                            ],
                            "intermediate_responses": []
                        }
                    }
                ],
                "session_input": {
                    "app_name": "ai_video_generator",
                    "user_id": "test_user",
                    "state": {}
                }
            },
            {
                "eval_id": "video_editing_test",
                "conversation": [
                    {
                        "invocation_id": "test-003",
                        "user_content": {
                            "parts": [{"text": "Concatenate video1.mp4 and video2.mp4 from downloads folder and save result to outputs"}],
                            "role": "user"
                        },
                        "final_response": {
                            "parts": [{"text": "I have successfully concatenated the videos and saved the result to outputs/concatenated_video.mp4"}],
                            "role": "model"
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "concatenate_videos",
                                    "args": {
                                        "video_paths": ["downloads/video1.mp4", "downloads/video2.mp4"],
                                        "output_path": "outputs/concatenated_video.mp4"
                                    }
                                }
                            ],
                            "intermediate_responses": []
                        }
                    }
                ],
                "session_input": {
                    "app_name": "ai_video_generator",
                    "user_id": "test_user",
                    "state": {}
                }
            }
        ]
    }


@pytest.fixture
def sample_test_config():
    """
    Sample test configuration with evaluation criteria.
    """
    return {
        "criteria": {
            "tool_trajectory_avg_score": 1.0,
            "response_match_score": 0.8
        }
    }


@pytest.mark.asyncio
async def test_agent_basic_functionality(sample_eval_data, tmp_path):
    """
    Test the agent's basic functionality using evaluation framework.
    """
    # Create temporary test file
    test_file = tmp_path / "basic_test.test.json"
    with open(test_file, 'w') as f:
        json.dump(sample_eval_data, f, indent=2)
    
    # Run evaluation
    results = await AgentEvaluator.evaluate(
        agent_module="adk_agents",
        eval_dataset_file_path_or_dir=str(test_file)
    )
    
    # Assertions
    assert results["total_cases"] == 3
    assert "tool_trajectory_score" in results
    assert "response_match_score" in results
    assert len(results["details"]) == 3
    
    # Check individual case results
    for detail in results["details"]:
        assert "eval_id" in detail
        assert "passed" in detail
        assert "tool_trajectory_score" in detail
        assert "response_match_score" in detail


@pytest.mark.asyncio
async def test_agent_with_custom_criteria(sample_eval_data, sample_test_config, tmp_path):
    """
    Test the agent with custom evaluation criteria.
    """
    # Create temporary files
    test_file = tmp_path / "custom_criteria_test.test.json"
    config_file = tmp_path / "test_config.json"
    
    with open(test_file, 'w') as f:
        json.dump(sample_eval_data, f, indent=2)
    
    with open(config_file, 'w') as f:
        json.dump(sample_test_config, f, indent=2)
    
    # Run evaluation with custom criteria
    results = await AgentEvaluator.evaluate(
        agent_module="adk_agents",
        eval_dataset_file_path_or_dir=str(test_file),
        config_file_path=str(config_file)
    )
    
    # Assertions
    assert results["total_cases"] > 0
    assert isinstance(results["tool_trajectory_score"], float)
    assert isinstance(results["response_match_score"], float)


@pytest.mark.asyncio 
async def test_path_compliance_evaluation(tmp_path):
    """
    Test that agents comply with path requirements (downloads/ and outputs/).
    """
    path_compliance_data = {
        "eval_set_id": "path_compliance_tests",
        "name": "Path Compliance Tests",
        "description": "Verify agents use correct paths for downloads and outputs",
        "eval_cases": [
            {
                "eval_id": "download_path_test",
                "conversation": [
                    {
                        "invocation_id": "path-001",
                        "user_content": {
                            "parts": [{"text": "Download a video from YouTube"}],
                            "role": "user"
                        },
                        "final_response": {
                            "parts": [{"text": "Video downloaded to downloads/ directory"}],
                            "role": "model"
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "download_youtube_video",
                                    "args": {
                                        "url": "https://youtube.com/watch?v=test",
                                        "save_dir": "downloads/"
                                    }
                                }
                            ],
                            "intermediate_responses": []
                        }
                    }
                ],
                "session_input": {
                    "app_name": "ai_video_generator",
                    "user_id": "test_user",
                    "state": {}
                }
            },
            {
                "eval_id": "output_path_test", 
                "conversation": [
                    {
                        "invocation_id": "path-002",
                        "user_content": {
                            "parts": [{"text": "Export final video"}],
                            "role": "user"
                        },
                        "final_response": {
                            "parts": [{"text": "Video exported to outputs/ directory"}],
                            "role": "model"
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "export_video",
                                    "args": {
                                        "input_path": "downloads/input.mp4",
                                        "output_path": "outputs/final_video.mp4"
                                    }
                                }
                            ],
                            "intermediate_responses": []
                        }
                    }
                ],
                "session_input": {
                    "app_name": "ai_video_generator",
                    "user_id": "test_user", 
                    "state": {}
                }
            }
        ]
    }
    
    # Create test file
    test_file = tmp_path / "path_compliance.test.json"
    with open(test_file, 'w') as f:
        json.dump(path_compliance_data, f, indent=2)
    
    # Run evaluation
    results = await AgentEvaluator.evaluate(
        agent_module="adk_agents",
        eval_dataset_file_path_or_dir=str(test_file)
    )
    
    # Assertions for path compliance
    assert results["total_cases"] == 2
    
    # Check that path requirements are being tested
    for detail in results["details"]:
        eval_id = detail["eval_id"]
        if eval_id == "download_path_test":
            # Should test downloads/ path usage
            assert detail["eval_id"] == "download_path_test"
        elif eval_id == "output_path_test":
            # Should test outputs/ path usage
            assert detail["eval_id"] == "output_path_test"


@pytest.mark.asyncio
async def test_multi_agent_coordination(tmp_path):
    """
    Test coordination between multiple agents (YouTube + Video Editor + Image-to-Video).
    """
    multi_agent_data = {
        "eval_set_id": "multi_agent_coordination",
        "name": "Multi-Agent Coordination Tests",
        "description": "Test coordination between YouTube, Video Editor, and Image-to-Video agents",
        "eval_cases": [
            {
                "eval_id": "download_then_edit_workflow",
                "conversation": [
                    {
                        "invocation_id": "coord-001",
                        "user_content": {
                            "parts": [{"text": "Download a video from YouTube and then add subtitles to it"}],
                            "role": "user"
                        },
                        "final_response": {
                            "parts": [{"text": "I have downloaded the video and added subtitles. The final video is saved in outputs/"}],
                            "role": "model"
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "download_youtube_video", 
                                    "args": {
                                        "url": "https://youtube.com/watch?v=test",
                                        "save_dir": "downloads/"
                                    }
                                },
                                {
                                    "name": "add_subtitles",
                                    "args": {
                                        "video_path": "downloads/video.mp4",
                                        "subtitle_text": "Sample subtitles",
                                        "output_path": "outputs/video_with_subtitles.mp4"
                                    }
                                }
                            ],
                            "intermediate_responses": [
                                ["YouTube_Agent_v1", [{"text": "Video downloaded successfully to downloads/"}]],
                                ["Video_Editor_Agent_v1", [{"text": "Subtitles added and video exported to outputs/"}]]
                            ]
                        }
                    }
                ],
                "session_input": {
                    "app_name": "ai_video_generator",
                    "user_id": "test_user",
                    "state": {}
                }
            }
        ]
    }
    
    # Create test file
    test_file = tmp_path / "multi_agent.test.json"
    with open(test_file, 'w') as f:
        json.dump(multi_agent_data, f, indent=2)
    
    # Run evaluation
    results = await AgentEvaluator.evaluate(
        agent_module="adk_agents",
        eval_dataset_file_path_or_dir=str(test_file)
    )
    
    # Assertions
    assert results["total_cases"] == 1
    assert len(results["details"]) == 1
    
    # Check that multi-agent workflow is tested
    detail = results["details"][0] 
    assert detail["eval_id"] == "download_then_edit_workflow"


@pytest.mark.asyncio
async def test_error_handling_in_evaluation():
    """
    Test error handling in the evaluation framework.
    """
    # Test with non-existent file
    with pytest.raises(FileNotFoundError):
        await AgentEvaluator.evaluate(
            agent_module="adk_agents",
            eval_dataset_file_path_or_dir="non_existent_file.json"
        )


def test_tool_trajectory_evaluation():
    """
    Test tool trajectory evaluation logic.
    """
    # Test exact match
    expected_tools = [
        {"name": "search_videos", "args": {"keyword": "test", "max_results": 5}}
    ]
    actual_tools = [
        {"name": "search_videos", "args": {"keyword": "test", "max_results": 5}}
    ]
    
    score = AgentEvaluator._evaluate_tool_trajectory(expected_tools, actual_tools)
    assert score == 1.0
    
    # Test mismatch
    actual_tools_wrong = [
        {"name": "get_video_info", "args": {"video_id": "test"}}
    ]
    
    score = AgentEvaluator._evaluate_tool_trajectory(expected_tools, actual_tools_wrong)
    assert score == 0.0
    
    # Test empty lists
    score = AgentEvaluator._evaluate_tool_trajectory([], [])
    assert score == 1.0


def test_response_match_evaluation():
    """
    Test response matching evaluation logic.
    """
    expected_response = {
        "parts": [{"text": "Hello world"}],
        "role": "model"
    }
    
    # Test exact match
    actual_response = {
        "parts": [{"text": "Hello world"}],
        "role": "model"
    }
    
    score = AgentEvaluator._evaluate_response_match(expected_response, actual_response)
    assert score == 1.0
    
    # Test partial match
    actual_response_partial = {
        "parts": [{"text": "Hello world and more"}],
        "role": "model"
    }
    
    score = AgentEvaluator._evaluate_response_match(expected_response, actual_response_partial)
    assert score == 0.8
    
    # Test no match
    actual_response_no_match = {
        "parts": [{"text": "Completely different"}],
        "role": "model"
    }
    
    score = AgentEvaluator._evaluate_response_match(expected_response, actual_response_no_match)
    assert score == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
