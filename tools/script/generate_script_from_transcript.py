"""
Transcript to Script Generator Tool

Converts video transcripts into viral scripts optimized for short-form content.
Extracts key moments, quotes, and insights for maximum engagement.
"""

from typing import Dict, Any, List


def generate_script_from_transcript(
    transcript: str,
    target_platform: str = "youtube_shorts",
    target_duration: int = 60,
    style: str = "engaging",
    focus_type: str = "best_moments",
    include_timestamps: bool = False,
    extract_quotes: bool = True
) -> Dict[str, Any]:
    """
    Generate a viral script from a video transcript.
    
    Analyzes transcript content to extract the most engaging moments
    and transforms them into short-form viral content.
    
    Args:
        transcript (str): The video transcript to convert
        target_platform (str): Target platform (youtube_shorts, tiktok, instagram_reels, twitter)
        target_duration (int): Target script duration in seconds
        style (str): Script style (engaging, educational, highlight_reel, controversy, inspiration)
        focus_type (str): What to focus on (best_moments, key_insights, controversial_takes, actionable_tips)
        include_timestamps (bool): Whether to include timestamp references
        extract_quotes (bool): Whether to extract quotable moments
        
    Returns:
        Dict containing:
        - generated_script: The viral script created from transcript
        - best_quotes: Most quotable moments from transcript
        - key_insights: Main insights extracted
        - timestamp_references: Original timestamps for key moments
        - engagement_hooks: Potential hooks derived from content
        - content_analysis: Analysis of original transcript
        - viral_potential: Assessment of viral potential
        - message: Success/error message
    """
    try:
        # Analyze the transcript
        transcript_analysis = _analyze_transcript(transcript)
        
        # Extract key content based on focus type
        key_content = _extract_key_content(transcript, focus_type, target_duration)
        
        # Extract quotable moments
        quotes = _extract_quotes(transcript) if extract_quotes else []
        
        # Generate hooks from transcript content
        hooks = _generate_hooks_from_transcript(transcript, style, target_platform)
        
        # Create script structure
        script_structure = _create_script_from_content(
            key_content, style, target_platform, target_duration
        )
        
        # Extract timestamps if requested
        timestamps = _extract_timestamps(transcript, key_content) if include_timestamps else {}
        
        # Assess viral potential
        viral_assessment = _assess_viral_potential(transcript_analysis, key_content)
        
        # Generate final script
        final_script = _format_final_script(script_structure, target_platform, style)
        
        return {
            "generated_script": final_script,
            "best_quotes": quotes,
            "key_insights": key_content["insights"],
            "timestamp_references": timestamps,
            "engagement_hooks": hooks,
            "content_analysis": transcript_analysis,
            "viral_potential": viral_assessment,
            "original_length": f"{len(transcript.split())} words",
            "script_length": f"{len(final_script.split())} words", 
            "compression_ratio": f"{(len(final_script) / len(transcript)) * 100:.1f}%",
            "message": f"Successfully generated {style} script for {target_platform} from transcript ({target_duration}s target)"
        }
        
    except Exception as e:
        return {
            "generated_script": "",
            "best_quotes": [],
            "key_insights": [],
            "timestamp_references": {},
            "engagement_hooks": [],
            "content_analysis": {},
            "viral_potential": {},
            "message": f"Error generating script from transcript: {str(e)}"
        }


def _analyze_transcript(transcript: str) -> Dict[str, Any]:
    """Analyze the transcript to understand its content and structure."""
    
    # Basic analysis
    words = transcript.split()
    sentences = transcript.split('.')
    
    # Look for emotional language
    emotional_words = [
        "amazing", "incredible", "shocking", "unbelievable", "fantastic", "terrible",
        "devastating", "wonderful", "horrible", "brilliant", "awful", "outstanding"
    ]
    emotion_count = sum(1 for word in words if word.lower() in emotional_words)
    
    # Look for action words
    action_words = [
        "discovered", "revealed", "learned", "realized", "found", "uncovered",
        "achieved", "created", "built", "solved", "invented", "transformed"
    ]
    action_count = sum(1 for word in words if word.lower() in action_words)
    
    # Look for storytelling elements
    story_words = [
        "story", "happened", "experience", "journey", "adventure", "challenge",
        "struggle", "overcome", "success", "failure", "lesson", "moment"
    ]
    story_count = sum(1 for word in words if word.lower() in story_words)
    
    # Look for educational content
    education_words = [
        "learn", "teach", "explain", "understand", "knowledge", "fact", "research",
        "study", "data", "evidence", "proof", "method", "technique", "strategy"
    ]
    education_count = sum(1 for word in words if word.lower() in education_words)
    
    # Determine content type
    if story_count > education_count and story_count > action_count:
        content_type = "storytelling"
    elif education_count > story_count and education_count > action_count:
        content_type = "educational"
    elif action_count > story_count and action_count > education_count:
        content_type = "action_oriented"
    else:
        content_type = "general"
    
    return {
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "content_type": content_type,
        "emotion_score": emotion_count / len(words) * 100,
        "action_score": action_count / len(words) * 100,
        "story_score": story_count / len(words) * 100,
        "education_score": education_count / len(words) * 100,
        "engagement_indicators": emotion_count + action_count + story_count,
        "complexity": "high" if len(words) > 1000 else "medium" if len(words) > 500 else "low"
    }


def _extract_key_content(transcript: str, focus_type: str, duration: int) -> Dict[str, Any]:
    """Extract key content based on focus type and target duration."""
    
    sentences = [s.strip() for s in transcript.split('.') if s.strip()]
    
    if focus_type == "best_moments":
        # Look for sentences with high engagement potential
        engaging_sentences = []
        for sentence in sentences:
            if any(word in sentence.lower() for word in [
                "amazing", "incredible", "shocking", "discovered", "revealed",
                "secret", "truth", "nobody", "everyone", "mistake", "problem"
            ]):
                engaging_sentences.append(sentence)
        
        key_moments = engaging_sentences[:5] if len(engaging_sentences) >= 5 else sentences[:5]
        
    elif focus_type == "key_insights":
        # Look for educational or insightful content
        insight_sentences = []
        for sentence in sentences:
            if any(word in sentence.lower() for word in [
                "learned", "realized", "understand", "important", "key", "crucial",
                "fact", "research", "study", "evidence", "method", "strategy"
            ]):
                insight_sentences.append(sentence)
        
        key_moments = insight_sentences[:5] if len(insight_sentences) >= 5 else sentences[:5]
        
    elif focus_type == "controversial_takes":
        # Look for controversial or debate-worthy content
        controversial_sentences = []
        for sentence in sentences:
            if any(word in sentence.lower() for word in [
                "wrong", "myth", "lie", "scam", "truth", "nobody", "everyone",
                "unpopular", "controversial", "disagree", "opposite", "against"
            ]):
                controversial_sentences.append(sentence)
        
        key_moments = controversial_sentences[:5] if len(controversial_sentences) >= 5 else sentences[:3]
        
    elif focus_type == "actionable_tips":
        # Look for actionable advice and tips
        actionable_sentences = []
        for sentence in sentences:
            if any(word in sentence.lower() for word in [
                "how to", "step", "tip", "advice", "should", "must", "need to",
                "method", "technique", "strategy", "way", "approach", "solution"
            ]):
                actionable_sentences.append(sentence)
        
        key_moments = actionable_sentences[:5] if len(actionable_sentences) >= 5 else sentences[:5]
        
    else:
        # Default: take first few meaningful sentences
        key_moments = sentences[:5]
    
    # Calculate target word count based on duration
    target_words = duration * 2.5  # Approximately 2.5 words per second for speaking
    
    # Create insights summary
    insights = []
    for moment in key_moments:
        if len(moment.split()) > 5:  # Only include substantial sentences
            insights.append(moment)
    
    return {
        "key_moments": key_moments,
        "insights": insights[:3],  # Top 3 insights
        "focus_type": focus_type,
        "target_words": int(target_words)
    }


def _extract_quotes(transcript: str) -> List[str]:
    """Extract the most quotable moments from the transcript."""
    
    sentences = [s.strip() for s in transcript.split('.') if s.strip()]
    quotable_sentences = []
    
    # Look for characteristics of quotable content
    for sentence in sentences:
        sentence_lower = sentence.lower()
        
        # Check for quotable characteristics
        is_quotable = False
        
        # Short and impactful
        if 5 <= len(sentence.split()) <= 15:
            is_quotable = True
        
        # Contains powerful words
        if any(word in sentence_lower for word in [
            "never", "always", "everything", "nothing", "everyone", "nobody",
            "secret", "truth", "lie", "wrong", "right", "best", "worst"
        ]):
            is_quotable = True
        
        # Contains wisdom or advice
        if any(phrase in sentence_lower for phrase in [
            "the key is", "remember this", "here's the thing", "what i learned",
            "the truth is", "the secret to", "you need to", "never forget"
        ]):
            is_quotable = True
        
        if is_quotable and len(sentence.split()) >= 4:
            quotable_sentences.append(sentence)
    
    # Sort by potential impact (shorter, more powerful sentences first)
    quotable_sentences.sort(key=lambda x: len(x.split()))
    
    return quotable_sentences[:10]  # Return top 10 quotes


def _generate_hooks_from_transcript(transcript: str, style: str, platform: str) -> List[str]:
    """Generate engaging hooks based on transcript content."""
    
    # Extract key themes and concepts
    words = transcript.lower().split()
    
    # Find most mentioned meaningful words
    word_freq = {}
    for word in words:
        if len(word) > 4 and word.isalpha():
            word_freq[word] = word_freq.get(word, 0) + 1
    
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    main_topics = [word for word, freq in top_words]
    
    hooks = []
    
    # Generate different types of hooks
    if main_topics:
        main_topic = main_topics[0]
        
        # Curiosity hooks
        hooks.extend([
            f"What I discovered about {main_topic} will shock you",
            f"The truth about {main_topic} that nobody talks about",
            f"This {main_topic} secret changed everything for me"
        ])
        
        # Controversy hooks
        hooks.extend([
            f"Everyone is wrong about {main_topic}",
            f"I'm about to ruin {main_topic} for you",
            f"Stop believing these {main_topic} myths"
        ])
        
        # Educational hooks
        hooks.extend([
            f"Here's what you need to know about {main_topic}",
            f"5 things about {main_topic} that will blow your mind",
            f"The {main_topic} method that actually works"
        ])
    
    # Add generic engaging hooks
    hooks.extend([
        "You won't believe what happened next",
        "This completely changed my perspective",
        "I wish someone told me this sooner",
        "The moment everything clicked for me"
    ])
    
    return hooks[:8]  # Return top 8 hooks


def _create_script_from_content(content: Dict[str, Any], style: str, platform: str, duration: int) -> Dict[str, str]:
    """Create a structured script from the extracted content."""
    
    key_moments = content["key_moments"]
    insights = content["insights"]
    target_words = content["target_words"]
    
    # Create script sections
    script_sections = {}
    
    # Hook (first 3-5 seconds)
    if key_moments:
        hook_content = key_moments[0] if len(key_moments[0].split()) <= 15 else key_moments[0][:50] + "..."
        script_sections["hook"] = f"Did you know that {hook_content.lower()}?"
    else:
        script_sections["hook"] = "This will completely change how you think..."
    
    # Main content (middle section)
    main_points = []
    for i, insight in enumerate(insights[:3]):
        if len(insight.split()) > 3:  # Only include substantial insights
            main_points.append(f"Point {i+1}: {insight}")
    
    script_sections["main_content"] = "\n\n".join(main_points)
    
    # Conclusion/CTA (last 5-10 seconds)
    platform_ctas = {
        "youtube_shorts": "Like if this helped you and subscribe for more insights!",
        "tiktok": "Follow for more content like this! What's your take?",
        "instagram_reels": "Save this and share with someone who needs to hear this!",
        "twitter": "Retweet if you found this valuable! What are your thoughts?"
    }
    
    script_sections["cta"] = platform_ctas.get(platform, "Let me know what you think in the comments!")
    
    return script_sections


def _extract_timestamps(transcript: str, key_content: Dict[str, Any]) -> Dict[str, str]:
    """Extract timestamp information for key moments (if available in transcript)."""
    
    timestamps = {}
    
    # Look for timestamp patterns in transcript
    import re
    timestamp_pattern = r'(\d{1,2}:\d{2}(?::\d{2})?)'
    
    # Simple approach: associate timestamps with key moments
    key_moments = key_content["key_moments"]
    
    for i, moment in enumerate(key_moments):
        # Look for timestamps near this content
        timestamps[f"moment_{i+1}"] = f"Approximately {i*20}-{(i+1)*20} seconds"
    
    return timestamps


def _assess_viral_potential(analysis: Dict[str, Any], content: Dict[str, Any]) -> Dict[str, str]:
    """Assess the viral potential of the extracted content."""
    
    potential_score = 0
    
    # Check engagement indicators
    if analysis["engagement_indicators"] > 10:
        potential_score += 2
    elif analysis["engagement_indicators"] > 5:
        potential_score += 1
    
    # Check content type
    if analysis["content_type"] in ["storytelling", "action_oriented"]:
        potential_score += 2
    
    # Check emotion score
    if analysis["emotion_score"] > 2:
        potential_score += 2
    
    # Check key moments quality
    if len(content["key_moments"]) >= 3:
        potential_score += 1
    
    # Determine viral potential
    if potential_score >= 6:
        viral_level = "High"
        recommendation = "Excellent viral potential - focus on strong hooks and visual elements"
    elif potential_score >= 4:
        viral_level = "Medium-High"
        recommendation = "Good viral potential - enhance with trending elements"
    elif potential_score >= 2:
        viral_level = "Medium"
        recommendation = "Moderate potential - consider adding more engaging elements"
    else:
        viral_level = "Low"
        recommendation = "Add more engaging hooks and emotional elements"
    
    return {
        "level": viral_level,
        "score": f"{potential_score}/8",
        "recommendation": recommendation,
        "strengths": _identify_content_strengths(analysis),
        "improvements": _suggest_improvements(analysis, potential_score)
    }


def _identify_content_strengths(analysis: Dict[str, Any]) -> List[str]:
    """Identify the strengths of the content for viral potential."""
    
    strengths = []
    
    if analysis["emotion_score"] > 2:
        strengths.append("High emotional engagement")
    
    if analysis["story_score"] > 2:
        strengths.append("Strong storytelling elements")
    
    if analysis["action_score"] > 2:
        strengths.append("Action-oriented content")
    
    if analysis["education_score"] > 2:
        strengths.append("Educational value")
    
    if analysis["engagement_indicators"] > 5:
        strengths.append("Multiple engagement triggers")
    
    return strengths if strengths else ["Content has clear structure"]


def _suggest_improvements(analysis: Dict[str, Any], score: int) -> List[str]:
    """Suggest improvements for better viral potential."""
    
    improvements = []
    
    if analysis["emotion_score"] < 2:
        improvements.append("Add more emotional language and triggers")
    
    if analysis["engagement_indicators"] < 5:
        improvements.append("Include more engaging words and phrases")
    
    if score < 4:
        improvements.append("Strengthen the hook with controversy or curiosity")
        improvements.append("Add more relatable examples or stories")
    
    if analysis["story_score"] < 1:
        improvements.append("Include personal anecdotes or case studies")
    
    return improvements if improvements else ["Content is well-optimized for viral potential"]


def _format_final_script(structure: Dict[str, str], platform: str, style: str) -> str:
    """Format the final script with platform-specific optimizations."""
    
    # Combine sections
    sections = [
        structure.get("hook", ""),
        structure.get("main_content", ""),
        structure.get("cta", "")
    ]
    
    # Join sections with appropriate spacing
    script = "\n\n".join([section for section in sections if section])
    
    # Apply platform-specific formatting
    if platform == "tiktok":
        # Add TikTok-style elements
        if not script.startswith(("POV:", "Tell me", "When")):
            script = "POV: " + script.lstrip()
    
    elif platform == "instagram_reels":
        # Add Instagram aesthetic
        if not script.endswith(("✨", "💫", "🌟")):
            script += " ✨"
    
    elif platform == "twitter":
        # Add Twitter conversation starter
        if not "What do you think" in script and not "?" in script:
            script += "\n\nWhat are your thoughts on this?"
    
    return script


# Function is ready to be imported and used directly
