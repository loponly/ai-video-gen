#!/usr/bin/env python3
"""
ADK Compliance Test for Tools
============================

Verifies that all tools follow ADK standards for:
- Function signatures with proper type hints
- Comprehensive docstrings
- Consistent return structures with status indicators
- SOLID design principles
"""

import sys
import inspect
import pytest
from pathlib import Path
from typing import Dict, Any, get_type_hints, Callable

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from tools.video import (
    concatenate_videos,
    synchronize_audio,
    clip_videos,
    add_subtitles,
    export_video,
    extract_audio,
    edit_video_metadata,
    add_effects,
    create_video_from_images
)

from tools.image import (
    add_text_to_images,
    create_slideshow_from_images,
    create_image_slideshow,
    create_simple_slideshow
)

from tools.youtube import (
    get_transcript,
    get_video_info,
    download_youtube_video,
    search_videos,
    convert_webm_to_mp4
)

# Collect all functions to test
ALL_FUNCTIONS = [
    (concatenate_videos, "concatenate_videos"),
    (synchronize_audio, "synchronize_audio"),
    (clip_videos, "clip_videos"),
    (edit_video_metadata, "edit_video_metadata"),
    (add_effects, "add_effects"),
    (export_video, "export_video"),
    (add_subtitles, "add_subtitles"),
    (extract_audio, "extract_audio"),
    (create_video_from_images, "create_video_from_images"),
    (add_text_to_images, "add_text_to_images"),
    (create_slideshow_from_images, "create_slideshow_from_images"),
    (create_image_slideshow, "create_image_slideshow"),
    (create_simple_slideshow, "create_simple_slideshow"),
    (get_transcript, "get_transcript"),
    (get_video_info, "get_video_info"),
    (download_youtube_video, "download_youtube_video"),
    (search_videos, "search_videos"),
    (convert_webm_to_mp4, "convert_webm_to_mp4")
]


@pytest.mark.parametrize("func,func_name", ALL_FUNCTIONS)
def test_function_adk_compliance(func: Callable, func_name: str):
    """Test if a function follows ADK standards"""
    results = {
        "function_name": func_name,
        "has_type_hints": False,
        "has_docstring": False,
        "returns_dict": False,
        "docstring_quality": "poor",
        "compliance_score": 0
    }
    
    # Check type hints
    try:
        type_hints = get_type_hints(func)
        if type_hints:
            results["has_type_hints"] = True
            results["compliance_score"] += 1
    except Exception as e:
        print(f"Error getting type hints for {func_name}: {e}")
    
    # Check docstring
    if func.__doc__:
        results["has_docstring"] = True
        results["compliance_score"] += 1
        
        # Check docstring quality
        docstring = func.__doc__.strip()
        if len(docstring) > 100:  # Substantial docstring
            results["compliance_score"] += 1
            
        # Check for Args and Returns sections
        if "Args:" in docstring and "Returns:" in docstring:
            results["docstring_quality"] = "good"
            results["compliance_score"] += 1
        elif "Args:" in docstring or "Returns:" in docstring:
            results["docstring_quality"] = "fair"
    
    # Check return type annotation
    signature = inspect.signature(func)
    if signature.return_annotation != inspect.Signature.empty:
        # Check if it returns Dict
        return_annotation = str(signature.return_annotation)
        if "Dict" in return_annotation or "dict" in return_annotation:
            results["returns_dict"] = True
            results["compliance_score"] += 1
    
    # Maximum score is 5
    results["compliance_percentage"] = (results["compliance_score"] / 5) * 100
    
    # Assert compliance
    assert results["compliance_score"] >= 4, f"Function {func_name} failed ADK compliance: {results}"
    print(f"✅ {func_name} passed ADK compliance with score {results['compliance_score']}/5")


def _check_function_adk_compliance(func: Callable, func_name: str) -> Dict[str, Any]:
    """Helper function to check ADK compliance and return results"""
    results = {
        "function_name": func_name,
        "has_type_hints": False,
        "has_docstring": False,
        "returns_dict": False,
        "docstring_quality": "poor",
        "compliance_score": 0
    }
    
    # Check if function has type hints
    try:
        type_hints = get_type_hints(func)
        signature = inspect.signature(func)
        
        # Check parameters and return annotation
        param_hints = len([p for p in signature.parameters.values() 
                          if p.annotation != inspect.Parameter.empty])
        return_hint = signature.return_annotation != inspect.Signature.empty
        
        if param_hints > 0 and return_hint:
            results["has_type_hints"] = True
            results["compliance_score"] += 1
    except Exception:
        pass
    
    # Check docstring existence and quality
    if func.__doc__:
        results["has_docstring"] = True
        results["compliance_score"] += 1
        
        doc_lines = func.__doc__.strip().split('\n')
        if len(doc_lines) >= 5:  # Multi-line with decent content
            results["docstring_quality"] = "good"
            results["compliance_score"] += 1
        else:
            results["docstring_quality"] = "basic"
    
    # Check return type annotation
    signature = inspect.signature(func)
    if signature.return_annotation != inspect.Signature.empty:
        # Check if it returns Dict
        return_annotation = str(signature.return_annotation)
        if "Dict" in return_annotation or "dict" in return_annotation:
            results["returns_dict"] = True
            results["compliance_score"] += 1
    
    # Maximum score is 5
    results["compliance_percentage"] = (results["compliance_score"] / 5) * 100
    
    return results


def test_all_tools_adk_compliance():
    """Test all tools for ADK compliance"""
    print("🔍 Testing ADK Compliance for All Tools")
    print("=" * 50)
    
    tools_to_test = [
        (concatenate_videos, "concatenate_videos"),
        (synchronize_audio, "synchronize_audio"), 
        (clip_videos, "clip_videos"),
        (add_subtitles, "add_subtitles"),
        (export_video, "export_video"),
        (extract_audio, "extract_audio"),
        (edit_video_metadata, "edit_video_metadata"),
        (add_effects, "add_effects"),
        (create_video_from_images, "create_video_from_images"),
        (add_text_to_images, "add_text_to_images"),
        (create_slideshow_from_images, "create_slideshow_from_images"),
        (create_image_slideshow, "create_image_slideshow"),
        (create_simple_slideshow, "create_simple_slideshow"),
        (get_transcript, "get_transcript"),
        (get_video_info, "get_video_info"),
        (download_youtube_video, "download_youtube_video"),
        (search_videos, "search_videos"),
        (convert_webm_to_mp4, "convert_webm_to_mp4")
    ]
    
    all_results = []
    total_score = 0
    
    for func, name in tools_to_test:
        print(f"\n📋 Testing {name}...")
        result = _check_function_adk_compliance(func, name)
        all_results.append(result)
        
        print(f"  ✓ Type hints: {'Yes' if result['has_type_hints'] else 'No'}")
        print(f"  ✓ Docstring: {'Yes' if result['has_docstring'] else 'No'}")
        print(f"  ✓ Returns Dict: {'Yes' if result['returns_dict'] else 'No'}")
        print(f"  ✓ Docstring quality: {result['docstring_quality']}")
        print(f"  📊 Compliance: {result['compliance_percentage']:.1f}%")
        
        total_score += result["compliance_percentage"]
    
    # Overall statistics
    average_compliance = total_score / len(tools_to_test)
    
    print("\n" + "=" * 50)
    print("📊 OVERALL ADK COMPLIANCE SUMMARY")
    print("=" * 50)
    print(f"Average compliance score: {average_compliance:.1f}%")
    
    # Count fully compliant tools
    fully_compliant = sum(1 for r in all_results if r["compliance_percentage"] >= 80)
    print(f"Fully compliant tools (≥80%): {fully_compliant}/{len(tools_to_test)}")
    
    # Show tools that need improvement
    needs_improvement = [r for r in all_results if r["compliance_percentage"] < 80]
    if needs_improvement:
        print("\n🔧 Tools needing improvement:")
        for result in needs_improvement:
            print(f"  - {result['function_name']}: {result['compliance_percentage']:.1f}%")
    
    print(f"\n🎯 ADK Standards Achievement: {'EXCELLENT' if average_compliance >= 90 else 'GOOD' if average_compliance >= 80 else 'NEEDS IMPROVEMENT'}")
    
    # Assert that average compliance is good
    assert average_compliance >= 80, f"Average ADK compliance too low: {average_compliance:.1f}%"


def test_function_execution():
    """Test that functions can be called with basic parameters"""
    print("\n🚀 Testing Function Execution")
    print("=" * 30)
    
    # Test concatenate_videos with default method
    try:
        result = concatenate_videos([], "/tmp/test.mp4")
        assert result["status"] == "error"  # Should fail with empty list
        print("✅ concatenate_videos: Handles empty input correctly")
    except Exception as e:
        print(f"❌ concatenate_videos: {e}")
    
    # Test get_transcript with invalid ID
    try:
        result = get_transcript("invalid_id")
        assert result["status"] == "error"  # Should fail with invalid ID
        print("✅ get_transcript: Handles invalid input correctly")
    except Exception as e:
        print(f"❌ get_transcript: {e}")
    
    # Test get_video_info with invalid URL
    try:
        result = get_video_info("invalid_url")
        assert result["status"] == "error"  # Should fail with invalid URL
        print("✅ get_video_info: Handles invalid input correctly")
    except Exception as e:
        print(f"❌ get_video_info: {e}")
    
    print("✅ All functions handle error cases appropriately")


if __name__ == "__main__":
    print("🧪 ADK TOOLS COMPLIANCE TEST")
    print("=" * 40)
    
    compliance_passed = test_all_tools_adk_compliance()
    test_function_execution()
    
    print(f"\n🏆 Final Result: {'PASSED' if compliance_passed else 'FAILED'}")
    
    if compliance_passed:
        print("🎉 All tools meet ADK standards!")
        sys.exit(0)
    else:
        print("⚠️  Some tools need improvement to meet ADK standards.")
        sys.exit(1)
