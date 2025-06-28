# AI Video Generator Agent Evaluation Framework

## Overview

This document describes the comprehensive agent evaluation framework implemented for the AI Video Generator project, following ADK (Agent Development Kit) best practices and guidelines.

## Purpose

The evaluation framework provides automated testing and quality assurance for:
- **Trajectory and Tool Use**: Analyzing the steps agents take to reach solutions
- **Final Response Quality**: Assessing the quality and correctness of agent outputs
- **Multi-Agent Coordination**: Testing coordination between YouTube, Video Editor, and Image-to-Video agents
- **Path Compliance**: Ensuring agents use correct file paths (downloads/ and outputs/)

## Framework Components

### 1. Agent Evaluator (`test_agent_evaluation.py`)

The core evaluation engine that implements:
- **Tool Trajectory Evaluation**: Compares expected vs actual tool usage
- **Response Match Evaluation**: Evaluates response quality using text similarity
- **Custom Criteria Support**: Configurable evaluation thresholds
- **Error Handling**: Robust error handling and reporting

```python
from tests.test_agent_evaluation import AgentEvaluator

# Basic usage
results = await AgentEvaluator.evaluate(
    agent_module="adk_agents",
    eval_dataset_file_path_or_dir="tests/youtube_functionality.evalset.json"
)
```

### 2. Evaluation Data Files

#### YouTube Functionality Tests (`youtube_functionality.evalset.json`)
Tests core YouTube agent capabilities:
- Video search with keyword queries
- Video downloading with path compliance
- Transcript extraction
- Video information retrieval

#### Video Editing Tests (`video_editing_functionality.evalset.json`)
Tests video editing agent capabilities:
- Video concatenation with proper output paths
- Subtitle addition
- Audio extraction
- Video export with custom settings
- Video clipping/trimming

#### Multi-Agent Workflow Tests (`multi_agent_workflows.evalset.json`)
Tests coordination between multiple agents:
- Download-then-edit workflows
- Search-download-process pipelines
- Image slideshow with YouTube audio
- Complete video production workflows

### 3. Configuration Files

#### Test Configuration (`test_config.json`)
Defines evaluation criteria:
```json
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,
    "response_match_score": 0.8
  }
}
```

## Evaluation Schema

Our evaluation files follow the ADK EvalSet schema with these key components:

### EvalSet Structure
```json
{
  "eval_set_id": "unique_identifier",
  "name": "Human readable name",
  "description": "Description of what this eval set tests",
  "eval_cases": [...]
}
```

### EvalCase Structure
```json
{
  "eval_id": "unique_case_identifier",
  "conversation": [
    {
      "invocation_id": "unique_invocation_id",
      "user_content": {
        "parts": [{"text": "User query"}],
        "role": "user"
      },
      "final_response": {
        "parts": [{"text": "Expected response"}],
        "role": "model"
      },
      "intermediate_data": {
        "tool_uses": [...],
        "intermediate_responses": [...]
      }
    }
  ],
  "session_input": {
    "app_name": "ai_video_generator",
    "user_id": "test_user",
    "state": {}
  }
}
```

## Running Evaluations

### 1. Using pytest (Recommended)

```bash
# Run all evaluation tests
pytest tests/test_agent_evaluation.py tests/test_adk_compatible_evaluation.py -v

# Run specific test categories
pytest tests/test_agent_evaluation.py::test_path_compliance_evaluation -v
pytest tests/test_adk_compatible_evaluation.py::test_youtube_functionality_with_adk_pattern -v

# Run with detailed output
pytest tests/ -k "evaluation" -v -s
```

### 2. Using Python directly

```python
import asyncio
from tests.test_agent_evaluation import AgentEvaluator

async def run_evaluation():
    results = await AgentEvaluator.evaluate(
        agent_module="adk_agents",
        eval_dataset_file_path_or_dir="tests/youtube_functionality.evalset.json",
        config_file_path="tests/test_config.json"
    )
    print(f"Evaluation completed: {results['passed']}/{results['total_cases']} passed")

asyncio.run(run_evaluation())
```

### 3. Command Line Interface (Future)

Following ADK patterns, you can run evaluations via CLI:
```bash
# This follows the ADK eval command pattern
adk eval adk_agents tests/youtube_functionality.evalset.json --config_file_path=tests/test_config.json
```

## Evaluation Metrics

### Tool Trajectory Average Score
- **Range**: 0.0 to 1.0
- **Purpose**: Measures accuracy of tool usage sequence
- **Default Threshold**: 1.0 (requires perfect match)
- **Evaluation Methods**:
  - Exact match: Perfect tool sequence match
  - In-order match: Correct tools in correct order (allows extras)
  - Any-order match: Correct tools in any order (allows extras)

### Response Match Score
- **Range**: 0.0 to 1.0  
- **Purpose**: Measures quality of final response
- **Default Threshold**: 0.8 (allows slight variations)
- **Evaluation Logic**:
  - 1.0: Exact text match
  - 0.8: Partial match (contains expected text)
  - 0.0: No match

## Path Compliance Testing

The framework specifically tests adherence to project path conventions:

### Downloads Path (`downloads/`)
- All YouTube video downloads must go to `downloads/` directory
- Tested in: YouTube functionality tests
- Tools affected: `download_youtube_video`

### Outputs Path (`outputs/`)
- All final video outputs must go to `outputs/` directory  
- Tested in: Video editing and multi-agent workflow tests
- Tools affected: `export_video`, `concatenate_videos`, `add_subtitles`, etc.

## Multi-Agent Coordination Testing

The framework tests complex workflows involving multiple agents:

1. **Sequential Workflows**: YouTube → Video Editor
2. **Parallel Processing**: Multiple downloads → Concatenation
3. **Cross-Agent Data Flow**: YouTube audio → Image slideshow
4. **Complete Pipelines**: Search → Download → Edit → Export

## Adding New Evaluations

### 1. Create Evaluation Data

Create a new `.evalset.json` file following the schema:

```json
{
  "eval_set_id": "your_test_set",
  "name": "Your Test Description", 
  "description": "What this test validates",
  "eval_cases": [
    {
      "eval_id": "your_test_case",
      "conversation": [...],
      "session_input": {...}
    }
  ]
}
```

### 2. Add Test Function

Add a new test function in `test_adk_compatible_evaluation.py`:

```python
@pytest.mark.asyncio
async def test_your_new_functionality():
    eval_file = Path(__file__).parent / "your_new_test.evalset.json"
    config_file = Path(__file__).parent / "test_config.json"
    
    results = await AgentEvaluator.evaluate(
        agent_module="adk_agents",
        eval_dataset_file_path_or_dir=str(eval_file),
        config_file_path=str(config_file)
    )
    
    # Add your specific assertions
    assert results["total_cases"] > 0
```

### 3. Update Documentation

Update this document to include your new evaluation category.

## Best Practices

### 1. Test Design
- Create focused, single-purpose test cases
- Use realistic user queries and scenarios
- Include both positive and edge cases
- Test error handling scenarios

### 2. Path Management
- Always specify full paths in test data
- Use relative paths starting from project root
- Test both input sources and output destinations
- Verify path compliance in assertions

### 3. Multi-Agent Tests
- Include intermediate response expectations
- Test agent handoff scenarios
- Verify data flow between agents
- Check final output integration

### 4. Maintenance
- Regular review and update of test cases
- Monitor evaluation score trends
- Update thresholds based on performance
- Add tests for new features

## Integration with CI/CD

The evaluation framework can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Agent Evaluations
  run: |
    pytest tests/test_agent_evaluation.py tests/test_adk_compatible_evaluation.py -v
    
- name: Generate Evaluation Report
  run: |
    pytest tests/ -k "evaluation" --junitxml=evaluation_results.xml
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **File Not Found**: Check evaluation file paths are correct
3. **Schema Validation**: Verify JSON structure matches EvalSet schema
4. **Async Issues**: Use `pytest-asyncio` for async test functions

### Debug Mode

Enable detailed logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run evaluation with debug info
results = await AgentEvaluator.evaluate(...)
print(json.dumps(results, indent=2))
```

## Future Enhancements

1. **ROUGE Metrics**: Implement proper ROUGE scoring for response evaluation
2. **Visual Comparison**: Add support for video/image output comparison
3. **Performance Metrics**: Track execution time and resource usage
4. **Interactive Web UI**: Build web interface for evaluation management
5. **Continuous Monitoring**: Real-time evaluation in production

## Conclusion

This evaluation framework provides comprehensive testing capabilities for the AI Video Generator agents, ensuring quality, reliability, and adherence to project standards. Regular use of these evaluations will help maintain and improve agent performance throughout development and deployment.
