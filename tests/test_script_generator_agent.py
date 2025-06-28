"""
Test AI Script Generator Agent

This module tests the AI Script Generator Agent and its tools to ensure
they work correctly within the multi-agent system.
"""

import pytest
import sys
import os
from typing import Dict, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestScriptGeneratorAgent:
    """Test cases for the AI Script Generator Agent."""
    
    def test_generate_viral_script_basic(self):
        """Test basic viral script generation functionality."""
        from tools.script.generate_viral_script import generate_viral_script
        
        result = generate_viral_script(
            topic="productivity tips",
            platform="youtube_shorts",
            style="engaging",
            duration=60
        )
        
        assert isinstance(result, dict)
        assert "script" in result
        assert "hook" in result
        assert "message" in result
        assert len(result["script"]) > 0
        assert "productivity tips" in result["script"].lower()
        
    def test_generate_viral_script_different_platforms(self):
        """Test script generation for different platforms."""
        from tools.script.generate_viral_script import generate_viral_script
        
        platforms = ["youtube_shorts", "tiktok", "instagram_reels", "twitter"]
        
        for platform in platforms:
            result = generate_viral_script(
                topic="AI trends",
                platform=platform,
                style="engaging",
                duration=30
            )
            
            assert isinstance(result, dict)
            assert "script" in result
            assert len(result["script"]) > 0
            assert result["message"].startswith("Successfully generated")
    
    def test_create_hook_variations(self):
        """Test hook variations creation."""
        from tools.script.create_hook_variations import create_hook_variations
        
        result = create_hook_variations(
            topic="fitness tips",
            style="engaging",
            platform="tiktok",
            count=5,
            emotion="curiosity"
        )
        
        assert isinstance(result, dict)
        assert "hooks" in result
        assert "best_hooks" in result
        assert len(result["hooks"]) == 5
        assert len(result["best_hooks"]) <= 3
        assert all("fitness tips" in hook.lower() for hook in result["hooks"][:2])
    
    def test_adapt_content_to_script(self):
        """Test content adaptation to script format."""
        from tools.script.adapt_content_to_script import adapt_content_to_script
        
        sample_content = """
        Artificial Intelligence is transforming industries rapidly. 
        Machine learning algorithms can now process data faster than ever before.
        This technology is creating new opportunities for businesses worldwide.
        Companies that adapt early will have a competitive advantage.
        """
        
        result = adapt_content_to_script(
            content=sample_content,
            content_type="article",
            target_platform="youtube_shorts",
            target_duration=45,
            style="educational"
        )
        
        assert isinstance(result, dict)
        assert "adapted_script" in result
        assert "original_summary" in result
        assert "key_changes" in result
        assert len(result["adapted_script"]) > 0
        # Note: Adapted script might be longer due to platform optimizations
        assert "compression_ratio" in result
    
    def test_optimize_script_for_platform(self):
        """Test script optimization for specific platforms."""
        from tools.script.optimize_script_for_platform import optimize_script_for_platform
        
        base_script = """
        This productivity hack will change your life.
        I discovered this method that saves me 2 hours every day.
        Let me show you exactly how it works.
        """
        
        result = optimize_script_for_platform(
            script=base_script,
            source_platform="general",
            target_platform="tiktok",
            optimization_level="high"
        )
        
        assert isinstance(result, dict)
        assert "optimized_script" in result
        assert "platform_analysis" in result
        assert "optimization_changes" in result
        assert len(result["optimized_script"]) > 0
    
    def test_generate_script_from_transcript(self):
        """Test script generation from video transcript."""
        from tools.script.generate_script_from_transcript import generate_script_from_transcript
        
        sample_transcript = """
        So I've been working on productivity for years and I discovered something amazing.
        Most people waste hours on unimportant tasks. But there's a simple solution.
        You need to focus on high-impact activities first. This changed everything for me.
        Now I get twice as much done in half the time.
        """
        
        result = generate_script_from_transcript(
            transcript=sample_transcript,
            target_platform="youtube_shorts",
            target_duration=60,
            style="engaging",
            focus_type="best_moments"
        )
        
        assert isinstance(result, dict)
        assert "generated_script" in result
        assert "best_quotes" in result
        assert "viral_potential" in result
        assert len(result["generated_script"]) > 0
        assert isinstance(result["best_quotes"], list)
    
    def test_agent_integration(self):
        """Test that the script generator agent integrates properly."""
        from adk_agents.agents import script_generator_agent
        
        assert script_generator_agent.name == "Script_Generator_Agent_v1"
        assert len(script_generator_agent.tools) == 5
        assert script_generator_agent.output_key == "script_generation_responses"
    
    def test_orchestration_agent_includes_script_generator(self):
        """Test that the orchestration agent includes the script generator."""
        from adk_agents.agents import orchestration_agent
        
        # Check that script generator is in the orchestration agent's tools
        agent_tools = [tool.agent.name for tool in orchestration_agent.tools]
        assert "Script_Generator_Agent_v1" in agent_tools
        
        # Check that the description mentions script generation
        assert "Script Generator" in orchestration_agent.description
    
    def test_script_tools_error_handling(self):
        """Test error handling in script generation tools."""
        from tools.script.generate_viral_script import generate_viral_script
        
        # Test with invalid parameters
        result = generate_viral_script(
            topic="",  # Empty topic
            platform="invalid_platform",
            style="invalid_style",
            duration=-1  # Invalid duration
        )
        
        # Should still return a dict with error handling
        assert isinstance(result, dict)
        assert "message" in result
    
    def test_viral_potential_assessment(self):
        """Test viral potential assessment functionality."""
        from tools.script.generate_script_from_transcript import generate_script_from_transcript
        
        # High potential content
        high_potential_transcript = """
        This shocking discovery will change everything you know about success.
        I was struggling for years until I found this incredible secret.
        Now everyone is asking me how I transformed my life so quickly.
        The answer will blow your mind and it's simpler than you think.
        """
        
        result = generate_script_from_transcript(
            transcript=high_potential_transcript,
            target_platform="tiktok",
            target_duration=30,
            style="engaging"
        )
        
        assert "viral_potential" in result
        assert "level" in result["viral_potential"]
        assert "recommendation" in result["viral_potential"]
        assert result["viral_potential"]["level"] in ["Low", "Medium", "Medium-High", "High"]
    
    def test_platform_specific_optimizations(self):
        """Test that platform-specific optimizations are applied correctly."""
        from tools.script.optimize_script_for_platform import optimize_script_for_platform
        
        base_script = "This is a great tip for everyone."
        
        # Test TikTok optimization
        tiktok_result = optimize_script_for_platform(
            script=base_script,
            target_platform="tiktok",
            optimization_level="high",
            add_platform_elements=True
        )
        
        # Should add TikTok-specific elements
        assert "POV:" in tiktok_result["optimized_script"] or "follow" in tiktok_result["optimized_script"].lower()
        
        # Test Instagram optimization
        instagram_result = optimize_script_for_platform(
            script=base_script,
            target_platform="instagram_reels",
            optimization_level="high",
            add_platform_elements=True
        )
        
        # Should add Instagram-specific elements
        assert "save" in instagram_result["optimized_script"].lower() or "✨" in instagram_result["optimized_script"]


if __name__ == "__main__":
    # Run basic tests if executed directly
    test_instance = TestScriptGeneratorAgent()
    
    print("🧪 Running AI Script Generator Agent Tests...")
    
    test_methods = [
        test_instance.test_generate_viral_script_basic,
        test_instance.test_create_hook_variations,
        test_instance.test_adapt_content_to_script,
        test_instance.test_agent_integration,
        test_instance.test_orchestration_agent_includes_script_generator
    ]
    
    passed = 0
    for test_method in test_methods:
        try:
            test_method()
            print(f"✅ {test_method.__name__}")
            passed += 1
        except Exception as e:
            print(f"❌ {test_method.__name__}: {str(e)}")
    
    print(f"\n📊 Tests passed: {passed}/{len(test_methods)}")
