"""
Hook Variations Generator Tool

Creates multiple attention-grabbing hook variations for viral content.
Optimized for different platforms and content styles.
"""

from typing import Dict, Any, List


def create_hook_variations(
    topic: str,
    style: str = "engaging",
    platform: str = "youtube_shorts",
    count: int = 10,
    emotion: str = "curiosity"
) -> Dict[str, Any]:
    """
    Generate multiple hook variations for viral content creation.
    
    Creates diverse attention-grabbing opening lines optimized for 
    maximum engagement and retention.
    
    Args:
        topic (str): The main topic for the hooks
        style (str): Hook style (engaging, educational, controversial, emotional, question-based)
        platform (str): Target platform (youtube_shorts, tiktok, instagram_reels, twitter)
        count (int): Number of hook variations to generate (5-20)
        emotion (str): Target emotion (curiosity, surprise, fear, excitement, anger, empathy)
        
    Returns:
        Dict containing:
        - hooks: List of generated hook variations
        - best_hooks: Top 3 recommended hooks
        - hook_analysis: Analysis of each hook's strengths
        - platform_tips: Platform-specific hook recommendations
        - message: Success/error message
    """
    try:
        # Emotion-based hook templates
        emotion_templates = {
            "curiosity": [
                f"Did you know that {topic}...?",
                f"The secret about {topic} that nobody tells you",
                f"What if I told you {topic} could...",
                f"This {topic} fact will blow your mind",
                f"I bet you didn't know {topic}..."
            ],
            "surprise": [
                f"You'll never believe what happened with {topic}",
                f"This {topic} discovery shocked everyone",
                f"Plot twist: {topic} is actually...",
                f"Breaking: Scientists discover {topic}...",
                f"Nobody expected {topic} to..."
            ],
            "fear": [
                f"Stop doing this with {topic} immediately",
                f"This {topic} mistake could ruin everything",
                f"Warning: {topic} is more dangerous than you think",
                f"Don't let {topic} destroy your...",
                f"The scary truth about {topic}"
            ],
            "excitement": [
                f"This {topic} hack is going viral!",
                f"I can't believe {topic} actually works!",
                f"Game-changer: {topic} just got amazing",
                f"This {topic} trend is taking over",
                f"Finally! Someone cracked the {topic} code"
            ],
            "anger": [
                f"I'm so tired of people lying about {topic}",
                f"Stop falling for these {topic} myths",
                f"This {topic} industry is scamming you",
                f"Why is nobody talking about {topic}?",
                f"I'm calling out the {topic} community"
            ],
            "empathy": [
                f"I wish someone told me about {topic} sooner",
                f"If you struggle with {topic}, this is for you",
                f"I used to think {topic} was impossible",
                f"To everyone who's failed at {topic}...",
                f"I understand your {topic} frustration"
            ]
        }
        
        # Style-specific hook patterns
        style_patterns = {
            "engaging": [
                f"The {topic} secret that changed everything",
                f"How I mastered {topic} in 30 days",
                f"This {topic} trick works every time",
                f"The real reason {topic} matters",
                f"What experts don't want you to know about {topic}"
            ],
            "educational": [
                f"Here's what you need to know about {topic}",
                f"The science behind {topic} explained",
                f"5 facts about {topic} that will surprise you",
                f"Everything you learned about {topic} is wrong",
                f"The complete guide to understanding {topic}"
            ],
            "controversial": [
                f"Unpopular opinion: {topic} is overrated",
                f"I'm about to ruin {topic} for you",
                f"Everyone is wrong about {topic}",
                f"Why {topic} is actually harmful",
                f"The {topic} industry doesn't want you to know this"
            ],
            "emotional": [
                f"This {topic} story made me cry",
                f"How {topic} saved my life",
                f"The {topic} moment that changed everything",
                f"Why {topic} matters more than you think",
                f"This {topic} truth hit me hard"
            ],
            "question-based": [
                f"What would happen if {topic}...?",
                f"Why does {topic} always...?",
                f"How can {topic} possibly...?",
                f"When will {topic} finally...?",
                f"Where does {topic} really come from?"
            ]
        }
        
        # Platform-specific optimizations
        platform_hooks = {
            "youtube_shorts": [
                f"In the next 60 seconds, I'll show you {topic}",
                f"Before you scroll, here's why {topic} matters",
                f"This {topic} hack got 10M views",
                f"POV: You finally understand {topic}",
                f"Watch this before trying {topic}"
            ],
            "tiktok": [
                f"Tell me you don't know {topic} without telling me",
                f"POV: {topic} just made sense",
                f"This {topic} trend is everything",
                f"When someone asks about {topic}:",
                f"That {topic} girl/guy is me"
            ],
            "instagram_reels": [
                f"Things I wish I knew about {topic}",
                f"The {topic} glow up is real",
                f"Get ready with me: {topic} edition",
                f"This {topic} aesthetic hits different",
                f"Soft launch: my {topic} journey"
            ],
            "twitter": [
                f"Hot take: {topic} is...",
                f"Thread: Everything wrong with {topic}",
                f"Normalize talking about {topic}",
                f"Nobody: ... Me: {topic} thoughts",
                f"Daily reminder that {topic}..."
            ]
        }
        
        # Generate hooks from different sources
        all_hooks = []
        
        # Add emotion-based hooks
        emotion_hooks = emotion_templates.get(emotion, emotion_templates["curiosity"])
        all_hooks.extend(emotion_hooks)
        
        # Add style-based hooks
        style_hooks = style_patterns.get(style, style_patterns["engaging"])
        all_hooks.extend(style_hooks)
        
        # Add platform-specific hooks
        platform_specific = platform_hooks.get(platform, platform_hooks["youtube_shorts"])
        all_hooks.extend(platform_specific)
        
        # Add general viral patterns
        viral_patterns = [
            f"This {topic} mistake costs people everything",
            f"I tried {topic} for 30 days, here's what happened",
            f"Rich people know this {topic} secret",
            f"The {topic} method that actually works",
            f"How to {topic} like a pro in 2024",
            f"The {topic} transformation nobody talks about",
            f"Why {topic} is trending right now",
            f"The future of {topic} is here",
            f"This {topic} advice aged like milk",
            f"Plot twist: {topic} isn't what you think"
        ]
        all_hooks.extend(viral_patterns)
        
        # Select and deduplicate hooks
        unique_hooks = list(dict.fromkeys(all_hooks))  # Remove duplicates while preserving order
        selected_hooks = unique_hooks[:count]
        
        # Analyze hooks and select best ones
        hook_analysis = {}
        for i, hook in enumerate(selected_hooks):
            analysis = _analyze_hook(hook, platform, emotion)
            hook_analysis[f"Hook {i+1}"] = {
                "text": hook,
                "analysis": analysis
            }
        
        # Select top 3 best hooks based on analysis
        best_hooks = _select_best_hooks(selected_hooks, platform, emotion)
        
        # Platform-specific tips
        platform_tips = _get_platform_tips(platform)
        
        return {
            "hooks": selected_hooks,
            "best_hooks": best_hooks,
            "hook_analysis": hook_analysis,
            "platform_tips": platform_tips,
            "emotion_used": emotion,
            "style_used": style,
            "message": f"Successfully generated {len(selected_hooks)} {style} hooks for {platform} about '{topic}'"
        }
        
    except Exception as e:
        return {
            "hooks": [],
            "best_hooks": [],
            "hook_analysis": {},
            "platform_tips": [],
            "message": f"Error generating hook variations: {str(e)}"
        }


def _analyze_hook(hook: str, platform: str, emotion: str) -> Dict[str, Any]:
    """Analyze a hook's potential effectiveness."""
    
    analysis = {
        "length": len(hook),
        "word_count": len(hook.split()),
        "emotion_trigger": emotion in hook.lower(),
        "question_format": "?" in hook,
        "urgency_words": any(word in hook.lower() for word in ["now", "today", "immediately", "stop", "urgent"]),
        "curiosity_gap": any(word in hook.lower() for word in ["secret", "truth", "nobody", "hidden", "revealed"]),
        "personal_connection": any(word in hook.lower() for word in ["you", "your", "yourself"]),
        "platform_optimized": True  # Would check platform-specific elements
    }
    
    # Calculate score
    score = 0
    if analysis["length"] <= 100:  # Good length for most platforms
        score += 1
    if analysis["question_format"]:
        score += 1
    if analysis["urgency_words"]:
        score += 1
    if analysis["curiosity_gap"]:
        score += 2
    if analysis["personal_connection"]:
        score += 1
    
    analysis["effectiveness_score"] = score
    analysis["recommendation"] = "High potential" if score >= 4 else "Medium potential" if score >= 2 else "Low potential"
    
    return analysis


def _select_best_hooks(hooks: List[str], platform: str, emotion: str) -> List[str]:
    """Select the top 3 hooks based on effectiveness criteria."""
    
    scored_hooks = []
    for hook in hooks:
        analysis = _analyze_hook(hook, platform, emotion)
        scored_hooks.append((hook, analysis["effectiveness_score"]))
    
    # Sort by score and return top 3
    scored_hooks.sort(key=lambda x: x[1], reverse=True)
    return [hook for hook, score in scored_hooks[:3]]


def _get_platform_tips(platform: str) -> List[str]:
    """Get platform-specific hook optimization tips."""
    
    tips = {
        "youtube_shorts": [
            "Keep hooks under 3 seconds for maximum retention",
            "Use visual text overlays to reinforce your hook",
            "Test multiple hooks with A/B testing",
            "Include trending keywords in your hook"
        ],
        "tiktok": [
            "Use trending sounds and phrases in your hook",
            "Start with movement or visual interest",
            "Keep hooks under 2 seconds",
            "Use popular TikTok formats and memes"
        ],
        "instagram_reels": [
            "Make hooks visually appealing with good lighting",
            "Use Instagram-specific language and trends",
            "Consider your hook as the thumbnail text",
            "Include relatable scenarios in hooks"
        ],
        "twitter": [
            "Make hooks thread-worthy and conversation starters",
            "Use Twitter-specific language and formats",
            "Include controversial or debate-worthy angles",
            "Keep hooks punchy and quotable"
        ]
    }
    
    return tips.get(platform, tips["youtube_shorts"])


# Function is ready to be imported and used directly
