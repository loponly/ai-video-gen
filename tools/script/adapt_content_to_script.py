"""
Content to Script Adapter Tool

Converts existing content (articles, blog posts, transcripts) into viral scripts.
Optimizes content structure and language for short-form video formats.
"""

from typing import Dict, Any, List, Optional


def adapt_content_to_script(
    content: str,
    content_type: str = "article",
    target_platform: str = "youtube_shorts", 
    target_duration: int = 60,
    style: str = "engaging",
    focus_points: Optional[List[str]] = None,
    maintain_key_messages: bool = True
) -> Dict[str, Any]:
    """
    Adapt existing content into a viral script format.
    
    Transforms long-form content into short-form scripts optimized
    for viral potential and platform-specific requirements.
    
    Args:
        content (str): The original content to adapt
        content_type (str): Type of content (article, blog_post, transcript, essay, news)
        target_platform (str): Target platform (youtube_shorts, tiktok, instagram_reels, twitter)
        target_duration (int): Target script duration in seconds
        style (str): Adaptation style (engaging, educational, entertaining, controversial)
        focus_points (List[str]): Specific points to emphasize (optional)
        maintain_key_messages (bool): Whether to preserve core messages
        
    Returns:
        Dict containing:
        - adapted_script: The converted script
        - original_summary: Summary of original content
        - key_changes: List of major adaptations made
        - hook: Generated hook from content
        - main_points: Extracted key points
        - removed_content: Content that was removed during adaptation
        - adaptation_notes: Notes about the adaptation process
        - message: Success/error message
    """
    try:
        # Content analysis
        word_count = len(content.split())
        original_length = len(content)
        
        # Extract key information from original content
        content_analysis = _analyze_content(content, content_type)
        
        # Determine adaptation strategy based on content type
        adaptation_strategy = _get_adaptation_strategy(content_type, target_platform, target_duration)
        
        # Extract main points and themes
        main_points = _extract_main_points(content, focus_points)
        
        # Generate hook from content
        hook = _generate_hook_from_content(content, style, target_platform)
        
        # Structure content for script format
        script_structure = _structure_for_script(
            content, main_points, target_duration, style, adaptation_strategy
        )
        
        # Apply platform-specific optimizations
        optimized_script = _optimize_for_platform(script_structure, target_platform, style)
        
        # Track what was removed/changed
        removed_content = _track_removed_content(content, optimized_script)
        key_changes = _identify_key_changes(content, optimized_script, adaptation_strategy)
        
        # Generate adaptation notes
        adaptation_notes = _generate_adaptation_notes(
            content_analysis, adaptation_strategy, target_platform, target_duration
        )
        
        return {
            "adapted_script": optimized_script,
            "original_summary": content_analysis["summary"],
            "key_changes": key_changes,
            "hook": hook,
            "main_points": main_points,
            "removed_content": removed_content,
            "adaptation_notes": adaptation_notes,
            "original_stats": {
                "word_count": word_count,
                "character_count": original_length,
                "estimated_read_time": f"{word_count // 200} minutes"
            },
            "adapted_stats": {
                "word_count": len(optimized_script.split()),
                "character_count": len(optimized_script),
                "estimated_video_time": f"{target_duration} seconds"
            },
            "compression_ratio": f"{(len(optimized_script) / original_length) * 100:.1f}%",
            "message": f"Successfully adapted {content_type} to {style} {target_platform} script ({target_duration}s)"
        }
        
    except Exception as e:
        return {
            "adapted_script": "",
            "original_summary": "",
            "key_changes": [],
            "hook": "",
            "main_points": [],
            "removed_content": "",
            "adaptation_notes": [],
            "message": f"Error adapting content to script: {str(e)}"
        }


def _analyze_content(content: str, content_type: str) -> Dict[str, Any]:
    """Analyze the original content to understand its structure and themes."""
    
    # Basic content analysis
    sentences = content.split('.')
    paragraphs = content.split('\n\n')
    words = content.split()
    
    # Identify key themes (simplified approach)
    word_freq = {}
    for word in words:
        word_clean = word.lower().strip('.,!?;:"()[]')
        if len(word_clean) > 3:
            word_freq[word_clean] = word_freq.get(word_clean, 0) + 1
    
    # Get most frequent meaningful words
    common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    themes = [word for word, freq in common_words]
    
    # Generate summary (first few sentences or key points)
    summary_sentences = sentences[:3] if len(sentences) >= 3 else sentences
    summary = '. '.join(summary_sentences).strip() + '.'
    
    return {
        "summary": summary,
        "themes": themes,
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "content_type": content_type,
        "complexity": "high" if len(words) > 500 else "medium" if len(words) > 200 else "low"
    }


def _get_adaptation_strategy(content_type: str, platform: str, duration: int) -> Dict[str, Any]:
    """Determine the best adaptation strategy based on content type and target."""
    
    strategies = {
        "article": {
            "approach": "extract_key_points",
            "focus": "main_arguments",
            "structure": ["hook", "key_point_1", "key_point_2", "key_point_3", "conclusion"],
            "tone_shift": "more_conversational"
        },
        "blog_post": {
            "approach": "storytelling",
            "focus": "personal_insights",
            "structure": ["hook", "problem", "solution", "example", "cta"],
            "tone_shift": "maintain_personality"
        },
        "transcript": {
            "approach": "highlight_best_moments",
            "focus": "quotable_content",
            "structure": ["hook", "best_quote", "context", "elaboration", "takeaway"],
            "tone_shift": "written_to_spoken"
        },
        "essay": {
            "approach": "simplify_concepts",
            "focus": "core_thesis",
            "structure": ["hook", "thesis", "evidence", "implications", "cta"],
            "tone_shift": "academic_to_casual"
        },
        "news": {
            "approach": "emphasize_impact",
            "focus": "why_it_matters",
            "structure": ["hook", "what_happened", "why_important", "impact", "action"],
            "tone_shift": "formal_to_engaging"
        }
    }
    
    base_strategy = strategies.get(content_type, strategies["article"])
    
    # Adjust strategy based on platform
    if platform == "tiktok":
        base_strategy["tone_shift"] = "very_casual"
        base_strategy["pace"] = "very_fast"
    elif platform == "youtube_shorts":
        base_strategy["pace"] = "fast"
        base_strategy["visual_cues"] = True
    elif platform == "instagram_reels":
        base_strategy["aesthetic_focus"] = True
        base_strategy["storytelling"] = True
    
    # Adjust for duration
    if duration <= 30:
        base_strategy["compression"] = "maximum"
        base_strategy["structure"] = base_strategy["structure"][:3]  # Shorten structure
    elif duration <= 60:
        base_strategy["compression"] = "high"
    else:
        base_strategy["compression"] = "moderate"
    
    return base_strategy


def _extract_main_points(content: str, focus_points: Optional[List[str]] = None) -> List[str]:
    """Extract the main points from the content."""
    
    # If focus points are provided, use them
    if focus_points:
        return focus_points
    
    # Simple extraction approach - look for key sentences
    sentences = content.split('.')
    main_points = []
    
    # Look for sentences with key indicators
    key_indicators = [
        "important", "key", "main", "crucial", "essential", "significant",
        "remember", "note that", "it's worth", "the fact is", "studies show",
        "research indicates", "evidence suggests", "data shows"
    ]
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20:  # Skip very short sentences
            for indicator in key_indicators:
                if indicator in sentence.lower():
                    main_points.append(sentence)
                    break
    
    # If no key sentences found, take first few meaningful sentences
    if not main_points:
        meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
        main_points = meaningful_sentences[:3]
    
    # Limit to top 5 points
    return main_points[:5]


def _generate_hook_from_content(content: str, style: str, platform: str) -> str:
    """Generate an engaging hook based on the content."""
    
    # Extract key themes from first paragraph
    first_paragraph = content.split('\n\n')[0] if '\n\n' in content else content[:200]
    
    # Simple hook generation based on content themes
    if "study" in content.lower() or "research" in content.lower():
        return f"New research just revealed something shocking..."
    elif "problem" in content.lower() or "issue" in content.lower():
        return f"This problem is affecting millions of people..."
    elif "solution" in content.lower() or "how to" in content.lower():
        return f"I just discovered the solution everyone's been looking for..."
    elif "story" in content.lower() or "happened" in content.lower():
        return f"You won't believe what just happened..."
    else:
        # Extract first meaningful concept
        words = first_paragraph.split()
        important_words = [w for w in words if len(w) > 4 and w.isalpha()]
        if important_words:
            key_concept = important_words[0]
            return f"Everything you know about {key_concept.lower()} is wrong..."
        else:
            return "This will change how you think about everything..."


def _structure_for_script(content: str, main_points: List[str], duration: int, style: str, strategy: Dict[str, Any]) -> str:
    """Structure the content according to script format requirements."""
    
    structure = strategy["structure"]
    script_parts = []
    
    for section in structure:
        if section == "hook":
            script_parts.append(_generate_hook_from_content(content, style, "youtube_shorts"))
        elif section in ["key_point_1", "key_point_2", "key_point_3"]:
            point_index = int(section.split('_')[-1]) - 1
            if point_index < len(main_points):
                script_parts.append(f"Point {point_index + 1}: {main_points[point_index]}")
        elif section == "conclusion" or section == "cta":
            script_parts.append("Here's what this means for you: Take action on this information today!")
        elif section == "problem":
            script_parts.append("Here's the problem everyone's facing...")
        elif section == "solution":
            script_parts.append("And here's the solution that actually works...")
        else:
            # Generic content for other sections
            script_parts.append(f"[{section.replace('_', ' ').title()}]")
    
    return '\n\n'.join(script_parts)


def _optimize_for_platform(script: str, platform: str, style: str) -> str:
    """Apply platform-specific optimizations to the script."""
    
    optimizations = {
        "youtube_shorts": {
            "add_visual_cues": True,
            "pacing": "fast",
            "call_to_action": "Like and subscribe for more!"
        },
        "tiktok": {
            "trendy_language": True,
            "shorter_sentences": True,
            "call_to_action": "Follow for more content like this!"
        },
        "instagram_reels": {
            "aesthetic_language": True,
            "story_focus": True,
            "call_to_action": "Save this post and share with someone who needs to see this!"
        },
        "twitter": {
            "thread_format": True,
            "conversational": True,
            "call_to_action": "Retweet if you found this helpful!"
        }
    }
    
    platform_opts = optimizations.get(platform, optimizations["youtube_shorts"])
    
    # Apply optimizations
    optimized_script = script
    
    if platform_opts.get("shorter_sentences"):
        # Break long sentences
        sentences = optimized_script.split('. ')
        short_sentences = []
        for sentence in sentences:
            if len(sentence) > 80:
                # Simple sentence breaking
                parts = sentence.split(', ')
                short_sentences.extend(parts)
            else:
                short_sentences.append(sentence)
        optimized_script = '. '.join(short_sentences)
    
    # Add call to action
    if platform_opts.get("call_to_action"):
        optimized_script += f"\n\n{platform_opts['call_to_action']}"
    
    return optimized_script


def _track_removed_content(original: str, adapted: str) -> str:
    """Track what content was removed during adaptation."""
    
    # Simple approach - estimate removed content
    original_words = set(original.lower().split())
    adapted_words = set(adapted.lower().split())
    removed_words = original_words - adapted_words
    
    if len(removed_words) > 20:
        return f"Approximately {len(removed_words)} unique words and concepts were condensed or removed to fit the target format."
    else:
        return "Minimal content removal - mostly restructuring and optimization."


def _identify_key_changes(original: str, adapted: str, strategy: Dict[str, Any]) -> List[str]:
    """Identify the key changes made during adaptation."""
    
    changes = [
        f"Applied {strategy['approach']} adaptation strategy",
        f"Restructured content using {len(strategy['structure'])}-part format",
        f"Applied {strategy.get('tone_shift', 'tone optimization')} for better engagement",
        f"Compressed content by approximately {100 - (len(adapted) / len(original) * 100):.0f}%",
        "Added viral hooks and engagement elements",
        "Optimized pacing for short-form video format"
    ]
    
    return changes


def _generate_adaptation_notes(analysis: Dict[str, Any], strategy: Dict[str, Any], platform: str, duration: int) -> List[str]:
    """Generate notes about the adaptation process."""
    
    notes = [
        f"Adapted {analysis['content_type']} with {analysis['complexity']} complexity",
        f"Used {strategy['approach']} strategy for {platform}",
        f"Target duration: {duration} seconds",
        f"Preserved {len(analysis['themes'])} main themes",
        f"Applied {strategy.get('tone_shift', 'standard')} tone adjustment"
    ]
    
    if strategy.get("compression") == "maximum":
        notes.append("Applied maximum compression for short duration")
    
    return notes


# Function is ready to be imported and used directly
