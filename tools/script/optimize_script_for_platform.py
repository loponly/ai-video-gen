"""
Platform Script Optimizer Tool

Optimizes scripts for specific social media platforms with platform-specific
formatting, language, and engagement strategies.
"""

from typing import Dict, Any, List


def optimize_script_for_platform(
    script: str,
    source_platform: str = "general",
    target_platform: str = "youtube_shorts",
    optimization_level: str = "high",
    maintain_core_message: bool = True,
    add_platform_elements: bool = True
) -> Dict[str, Any]:
    """
    Optimize a script for a specific social media platform.
    
    Adapts script language, format, and engagement strategies to match
    platform-specific best practices and audience expectations.
    
    Args:
        script (str): The original script to optimize
        source_platform (str): Original platform or "general" if not platform-specific
        target_platform (str): Target platform (youtube_shorts, tiktok, instagram_reels, twitter, linkedin)
        optimization_level (str): Level of optimization (low, medium, high, maximum)
        maintain_core_message (bool): Whether to preserve the core message
        add_platform_elements (bool): Whether to add platform-specific elements
        
    Returns:
        Dict containing:
        - optimized_script: The platform-optimized script
        - platform_analysis: Analysis of target platform requirements
        - optimization_changes: List of changes made
        - engagement_predictions: Predicted engagement improvements
        - platform_specific_tips: Additional optimization tips
        - character_count: Character count for platform limits
        - hashtag_suggestions: Relevant hashtags (if applicable)
        - message: Success/error message
    """
    try:
        # Get platform specifications
        platform_specs = _get_platform_specifications(target_platform)
        
        # Analyze current script
        script_analysis = _analyze_script_structure(script)
        
        # Apply platform-specific optimizations
        optimized_script = _apply_platform_optimizations(
            script, target_platform, optimization_level, platform_specs
        )
        
        # Add platform-specific elements if requested
        if add_platform_elements:
            optimized_script = _add_platform_elements(optimized_script, target_platform, platform_specs)
        
        # Generate hashtag suggestions
        hashtags = _generate_hashtag_suggestions(script, target_platform)
        
        # Calculate optimization changes
        changes = _calculate_optimization_changes(script, optimized_script, target_platform)
        
        # Predict engagement improvements
        engagement_predictions = _predict_engagement_improvements(changes, target_platform)
        
        # Generate platform-specific tips
        platform_tips = _get_platform_specific_tips(target_platform, script_analysis)
        
        # Check character limits
        character_analysis = _analyze_character_limits(optimized_script, platform_specs)
        
        return {
            "optimized_script": optimized_script,
            "platform_analysis": platform_specs,
            "optimization_changes": changes,
            "engagement_predictions": engagement_predictions,
            "platform_specific_tips": platform_tips,
            "character_analysis": character_analysis,
            "hashtag_suggestions": hashtags,
            "original_length": len(script),
            "optimized_length": len(optimized_script),
            "optimization_ratio": f"{(len(optimized_script) / len(script)) * 100:.1f}%",
            "message": f"Successfully optimized script for {target_platform} with {optimization_level} optimization level"
        }
        
    except Exception as e:
        return {
            "optimized_script": script,
            "platform_analysis": {},
            "optimization_changes": [],
            "engagement_predictions": {},
            "platform_specific_tips": [],
            "character_analysis": {},
            "hashtag_suggestions": [],
            "message": f"Error optimizing script for platform: {str(e)}"
        }


def _get_platform_specifications(platform: str) -> Dict[str, Any]:
    """Get detailed specifications for each platform."""
    
    specs = {
        "youtube_shorts": {
            "max_duration": 60,
            "optimal_duration": "45-60 seconds",
            "character_limit": None,
            "hook_time": 3,
            "audience": "broad, all ages",
            "content_style": "educational, entertaining, trending",
            "key_features": ["strong thumbnails", "trending sounds", "quick pacing", "visual elements"],
            "engagement_tactics": ["questions", "cliffhangers", "clear CTAs", "subscribe reminders"],
            "language_style": "conversational but clear",
            "hashtag_limit": None,
            "optimal_posting": "afternoon/evening"
        },
        "tiktok": {
            "max_duration": 60,
            "optimal_duration": "15-30 seconds",
            "character_limit": 2200,
            "hook_time": 2,
            "audience": "younger, trend-focused",
            "content_style": "trendy, authentic, entertaining",
            "key_features": ["trending sounds", "effects", "challenges", "duets"],
            "engagement_tactics": ["trends", "memes", "relatable content", "call to action"],
            "language_style": "casual, trendy, authentic",
            "hashtag_limit": 100,
            "optimal_posting": "evening"
        },
        "instagram_reels": {
            "max_duration": 90,
            "optimal_duration": "30-60 seconds",
            "character_limit": 2200,
            "hook_time": 3,
            "audience": "lifestyle-focused, visual",
            "content_style": "aesthetic, inspirational, lifestyle",
            "key_features": ["visual appeal", "trending audio", "story arcs", "aesthetics"],
            "engagement_tactics": ["save-worthy content", "share prompts", "story questions"],
            "language_style": "inspiring, aesthetic, personal",
            "hashtag_limit": 30,
            "optimal_posting": "morning/afternoon"
        },
        "twitter": {
            "max_duration": 140,
            "optimal_duration": "60-120 seconds",
            "character_limit": 280,
            "hook_time": 5,
            "audience": "news-focused, professional",
            "content_style": "conversational, news, opinions",
            "key_features": ["threads", "conversations", "retweets", "replies"],
            "engagement_tactics": ["questions", "polls", "controversial takes", "thread hooks"],
            "language_style": "conversational, witty, concise",
            "hashtag_limit": 2,
            "optimal_posting": "morning/lunch"
        },
        "linkedin": {
            "max_duration": 600,
            "optimal_duration": "90-180 seconds",
            "character_limit": 3000,
            "hook_time": 10,
            "audience": "professional, business-focused",
            "content_style": "professional, educational, industry insights",
            "key_features": ["professional insights", "industry trends", "career advice"],
            "engagement_tactics": ["professional questions", "industry insights", "career tips"],
            "language_style": "professional, informative, authoritative",
            "hashtag_limit": 5,
            "optimal_posting": "business hours"
        }
    }
    
    return specs.get(platform, specs["youtube_shorts"])


def _analyze_script_structure(script: str) -> Dict[str, Any]:
    """Analyze the current script structure and characteristics."""
    
    sentences = script.split('.')
    words = script.split()
    paragraphs = script.split('\n\n')
    
    # Detect current style elements
    has_question = '?' in script
    has_exclamation = '!' in script
    has_personal_pronouns = any(word.lower() in ['you', 'your', 'yours'] for word in words)
    has_urgency_words = any(word.lower() in ['now', 'today', 'immediately', 'urgent'] for word in words)
    has_emotional_words = any(word.lower() in ['amazing', 'incredible', 'shocking', 'unbelievable'] for word in words)
    
    return {
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "paragraph_count": len([p for p in paragraphs if p.strip()]),
        "has_question": has_question,
        "has_exclamation": has_exclamation,
        "has_personal_pronouns": has_personal_pronouns,
        "has_urgency_words": has_urgency_words,
        "has_emotional_words": has_emotional_words,
        "avg_sentence_length": len(words) / max(len(sentences), 1),
        "readability": "high" if len(words) / max(len(sentences), 1) < 15 else "medium"
    }


def _apply_platform_optimizations(script: str, platform: str, level: str, specs: Dict[str, Any]) -> str:
    """Apply platform-specific optimizations to the script."""
    
    optimized = script
    
    # Platform-specific language adjustments
    if platform == "tiktok":
        # Make more casual and trendy
        optimized = _make_trendy_language(optimized, level)
        optimized = _add_tiktok_elements(optimized, level)
    
    elif platform == "instagram_reels":
        # Make more aesthetic and inspirational
        optimized = _make_aesthetic_language(optimized, level)
        optimized = _add_instagram_elements(optimized, level)
    
    elif platform == "youtube_shorts":
        # Make more educational and engaging
        optimized = _make_educational_language(optimized, level)
        optimized = _add_youtube_elements(optimized, level)
    
    elif platform == "twitter":
        # Make more conversational and debate-worthy
        optimized = _make_conversational_language(optimized, level)
        optimized = _add_twitter_elements(optimized, level)
    
    elif platform == "linkedin":
        # Make more professional and insightful
        optimized = _make_professional_language(optimized, level)
        optimized = _add_linkedin_elements(optimized, level)
    
    # Apply optimization level adjustments
    if level in ["high", "maximum"]:
        optimized = _apply_high_level_optimizations(optimized, platform, specs)
    
    return optimized


def _make_trendy_language(script: str, level: str) -> str:
    """Make language more trendy and TikTok-appropriate."""
    
    replacements = {
        "very": "literally",
        "really": "actually",
        "amazing": "iconic",
        "great": "chef's kiss",
        "good": "slaps",
        "bad": "not it",
        "interesting": "lowkey fascinating"
    }
    
    optimized = script
    if level in ["medium", "high", "maximum"]:
        for old, new in replacements.items():
            optimized = optimized.replace(old, new)
    
    return optimized


def _make_aesthetic_language(script: str, level: str) -> str:
    """Make language more aesthetic and Instagram-appropriate."""
    
    aesthetic_words = {
        "beautiful": "absolutely stunning",
        "nice": "gorgeous",
        "good": "dreamy",
        "great": "divine",
        "amazing": "ethereal"
    }
    
    optimized = script
    if level in ["medium", "high", "maximum"]:
        for old, new in aesthetic_words.items():
            optimized = optimized.replace(old, new)
    
    return optimized


def _make_educational_language(script: str, level: str) -> str:
    """Make language more educational and YouTube-appropriate."""
    
    educational_phrases = {
        "Here's": "Let me explain",
        "This is": "What you need to know is",
        "So": "Now here's the important part:",
        "But": "However, here's what's interesting:"
    }
    
    optimized = script
    if level in ["medium", "high", "maximum"]:
        for old, new in educational_phrases.items():
            optimized = optimized.replace(old, new)
    
    return optimized


def _make_conversational_language(script: str, level: str) -> str:
    """Make language more conversational and Twitter-appropriate."""
    
    conversational = {
        "I think": "Hot take:",
        "In my opinion": "Unpopular opinion:",
        "It's important": "We need to talk about",
        "You should": "You absolutely must"
    }
    
    optimized = script
    if level in ["medium", "high", "maximum"]:
        for old, new in conversational.items():
            optimized = optimized.replace(old, new)
    
    return optimized


def _make_professional_language(script: str, level: str) -> str:
    """Make language more professional and LinkedIn-appropriate."""
    
    professional = {
        "awesome": "exceptional",
        "cool": "innovative",
        "great": "outstanding",
        "good": "effective",
        "bad": "suboptimal"
    }
    
    optimized = script
    if level in ["medium", "high", "maximum"]:
        for old, new in professional.items():
            optimized = optimized.replace(old, new)
    
    return optimized


def _add_tiktok_elements(script: str, level: str) -> str:
    """Add TikTok-specific elements."""
    if level in ["high", "maximum"]:
        # Add TikTok-style hooks
        if not script.startswith(("POV:", "Tell me", "When")):
            script = "POV: " + script
    return script


def _add_instagram_elements(script: str, level: str) -> str:
    """Add Instagram-specific elements."""
    if level in ["high", "maximum"]:
        # Add Instagram-style ending
        if not script.endswith(("✨", "💫", "🌟")):
            script += " ✨"
    return script


def _add_youtube_elements(script: str, level: str) -> str:
    """Add YouTube-specific elements."""
    if level in ["high", "maximum"]:
        # Add YouTube-style CTA
        if "subscribe" not in script.lower():
            script += "\n\nDon't forget to subscribe for more content like this!"
    return script


def _add_twitter_elements(script: str, level: str) -> str:
    """Add Twitter-specific elements."""
    if level in ["high", "maximum"]:
        # Add Twitter-style conversation starter
        if not script.endswith(("?", "thoughts?", "agree?")):
            script += "\n\nWhat are your thoughts on this?"
    return script


def _add_linkedin_elements(script: str, level: str) -> str:
    """Add LinkedIn-specific elements."""
    if level in ["high", "maximum"]:
        # Add LinkedIn-style professional question
        if not "career" in script.lower() and not "business" in script.lower():
            script += "\n\nHow has this impacted your professional experience?"
    return script


def _apply_high_level_optimizations(script: str, platform: str, specs: Dict[str, Any]) -> str:
    """Apply high-level optimizations based on platform specs."""
    
    # Adjust for optimal duration
    target_words = specs.get("optimal_duration", "60 seconds")
    # Extract seconds from duration string
    if "15-30" in target_words:
        target_word_count = 40  # ~15-30 seconds
    elif "30-60" in target_words:
        target_word_count = 80  # ~30-60 seconds
    elif "45-60" in target_words:
        target_word_count = 100  # ~45-60 seconds
    else:
        target_word_count = 80  # default
    
    current_words = len(script.split())
    
    if current_words > target_word_count * 1.2:  # If significantly over
        # Condense the script
        sentences = script.split('.')
        important_sentences = sentences[:int(len(sentences) * 0.7)]  # Keep 70%
        script = '. '.join(important_sentences) + '.'
    
    return script


def _add_platform_elements(script: str, platform: str, specs: Dict[str, Any]) -> str:
    """Add platform-specific elements like CTAs, engagement prompts."""
    
    platform_ctas = {
        "youtube_shorts": "\n\nLike this video if it helped you! Subscribe for more tips like this.",
        "tiktok": "\n\nFollow for more content like this! What should I cover next?",
        "instagram_reels": "\n\nSave this post and share it with someone who needs to see this! ✨",
        "twitter": "\n\nRetweet if you found this helpful! What's your experience with this?",
        "linkedin": "\n\nWhat are your thoughts on this? Share your professional insights in the comments."
    }
    
    cta = platform_ctas.get(platform, "")
    if cta and cta.strip() not in script:
        script += cta
    
    return script


def _generate_hashtag_suggestions(script: str, platform: str) -> List[str]:
    """Generate relevant hashtags for the platform."""
    
    # Extract key words from script
    words = script.lower().split()
    key_words = [word.strip('.,!?;:"()[]') for word in words if len(word) > 4]
    
    # Platform-specific hashtag strategies
    if platform == "tiktok":
        base_tags = ["#fyp", "#viral", "#trending", "#foryou"]
    elif platform == "instagram_reels":
        base_tags = ["#reels", "#instagram", "#viral", "#trending"]
    elif platform == "youtube_shorts":
        base_tags = ["#shorts", "#viral", "#trending"]
    elif platform == "twitter":
        base_tags = ["#thread", "#twitter"]
    else:
        base_tags = ["#viral", "#content"]
    
    # Add content-specific tags
    content_tags = [f"#{word}" for word in key_words[:5] if word.isalpha()]
    
    return base_tags + content_tags[:3]  # Limit total hashtags


def _calculate_optimization_changes(original: str, optimized: str, platform: str) -> List[str]:
    """Calculate what changes were made during optimization."""
    
    changes = []
    
    # Length changes
    orig_words = len(original.split())
    opt_words = len(optimized.split())
    
    if opt_words != orig_words:
        change_percent = ((opt_words - orig_words) / orig_words) * 100
        if change_percent > 0:
            changes.append(f"Expanded content by {change_percent:.1f}% ({opt_words - orig_words} words)")
        else:
            changes.append(f"Condensed content by {abs(change_percent):.1f}% ({abs(opt_words - orig_words)} words)")
    
    # Language style changes
    if platform == "tiktok" and "literally" in optimized and "literally" not in original:
        changes.append("Applied trendy TikTok language")
    
    if platform == "instagram_reels" and "✨" in optimized:
        changes.append("Added aesthetic Instagram elements")
    
    if platform == "youtube_shorts" and "subscribe" in optimized.lower():
        changes.append("Added YouTube-specific call-to-action")
    
    # Structure changes
    if optimized.count('\n\n') != original.count('\n\n'):
        changes.append("Restructured content for better readability")
    
    return changes


def _predict_engagement_improvements(changes: List[str], platform: str) -> Dict[str, str]:
    """Predict engagement improvements based on optimization changes."""
    
    predictions = {
        "retention": "Medium improvement expected",
        "engagement_rate": "Low-medium improvement expected",
        "shareability": "Medium improvement expected",
        "platform_algorithm": "Improved compatibility"
    }
    
    # Adjust predictions based on changes
    if len(changes) >= 3:
        predictions["retention"] = "High improvement expected"
        predictions["engagement_rate"] = "Medium-high improvement expected"
    
    if any("call-to-action" in change.lower() for change in changes):
        predictions["engagement_rate"] = "High improvement expected"
    
    return predictions


def _get_platform_specific_tips(platform: str, analysis: Dict[str, Any]) -> List[str]:
    """Get additional optimization tips specific to the platform."""
    
    tips = {
        "youtube_shorts": [
            "Use strong visual hooks in first 3 seconds",
            "Include text overlays for key points",
            "Use trending sounds or music",
            "Optimize thumbnail for click-through"
        ],
        "tiktok": [
            "Jump on trending sounds quickly",
            "Use trending hashtags strategically",
            "Keep text minimal and punchy",
            "Post during peak hours (6-10pm)"
        ],
        "instagram_reels": [
            "Focus on aesthetic visual appeal",
            "Use Instagram's native editing tools",
            "Create save-worthy content",
            "Include behind-the-scenes content"
        ],
        "twitter": [
            "Create thread-worthy content",
            "Use polls and questions for engagement",
            "Time tweets for maximum visibility",
            "Engage with replies quickly"
        ],
        "linkedin": [
            "Include industry insights and data",
            "Use professional hashtags sparingly",
            "Encourage professional discussion",
            "Share actionable business advice"
        ]
    }
    
    return tips.get(platform, tips["youtube_shorts"])


def _analyze_character_limits(script: str, specs: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze script against platform character limits."""
    
    char_count = len(script)
    char_limit = specs.get("character_limit")
    
    analysis = {
        "character_count": char_count,
        "character_limit": char_limit,
        "within_limits": char_limit is None or char_count <= char_limit,
        "usage_percentage": (char_count / char_limit * 100) if char_limit else None
    }
    
    if char_limit and char_count > char_limit:
        analysis["excess_characters"] = char_count - char_limit
        analysis["recommendation"] = f"Remove {char_count - char_limit} characters to meet platform limit"
    else:
        analysis["recommendation"] = "Character count is optimal for platform"
    
    return analysis


# Function is ready to be imported and used directly
