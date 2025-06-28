"""
Viral Script Generator Tool

Generates engaging viral scripts for short-form content creation.
Uses AI to create scripts optimized for audience retention and engagement.
"""

from typing import Dict, Any
import os


def generate_viral_script(
    topic: str,
    platform: str = "youtube_shorts",
    style: str = "engaging",
    duration: int = 60,
    target_audience: str = "general",
    include_hook: bool = True,
    include_cta: bool = True
) -> Dict[str, Any]:
    """
    Generate a viral script for short-form content creation.
    
    Creates engaging scripts optimized for specific platforms with hooks,
    retention elements, and call-to-actions for maximum viral potential.
    
    Args:
        topic (str): The main topic or theme for the script
        platform (str): Target platform (youtube_shorts, tiktok, instagram_reels, twitter)
        style (str): Script style (engaging, educational, entertaining, inspirational, controversial)
        duration (int): Target duration in seconds (15, 30, 60, 90)
        target_audience (str): Target audience (general, teens, adults, professionals, creators)
        include_hook (bool): Whether to include attention-grabbing hook
        include_cta (bool): Whether to include call-to-action
        
    Returns:
        Dict containing:
        - script: The generated viral script
        - hook: Attention-grabbing opening line
        - key_points: Main talking points
        - cta: Call-to-action text
        - timing_notes: Suggested timing for each section
        - engagement_tips: Tips for maximum engagement
        - message: Success/error message
    """
    try:
        # Platform-specific optimizations
        platform_configs = {
            "youtube_shorts": {
                "max_duration": 60,
                "hook_duration": 3,
                "optimal_length": "45-60 seconds",
                "key_elements": ["strong hook", "quick pacing", "visual cues", "trending sounds"]
            },
            "tiktok": {
                "max_duration": 60,
                "hook_duration": 2,
                "optimal_length": "15-30 seconds", 
                "key_elements": ["immediate hook", "trending hashtags", "visual storytelling", "music sync"]
            },
            "instagram_reels": {
                "max_duration": 90,
                "hook_duration": 3,
                "optimal_length": "30-60 seconds",
                "key_elements": ["aesthetic visuals", "trending audio", "story arc", "shareability"]
            },
            "twitter": {
                "max_duration": 140,
                "hook_duration": 5,
                "optimal_length": "60-120 seconds",
                "key_elements": ["conversation starter", "thread potential", "retweet hooks", "replies bait"]
            }
        }
        
        config = platform_configs.get(platform, platform_configs["youtube_shorts"])
        
        # Style-specific script templates
        style_templates = {
            "engaging": {
                "structure": ["hook", "problem", "solution", "proof", "cta"],
                "tone": "conversational and exciting",
                "elements": ["questions", "relatable scenarios", "emotional triggers"]
            },
            "educational": {
                "structure": ["hook", "context", "main_points", "summary", "cta"],
                "tone": "authoritative but approachable",
                "elements": ["facts", "examples", "actionable tips"]
            },
            "entertaining": {
                "structure": ["hook", "setup", "punchline", "escalation", "payoff"],
                "tone": "fun and energetic",
                "elements": ["humor", "surprises", "relatability"]
            },
            "inspirational": {
                "structure": ["hook", "struggle", "journey", "transformation", "message"],
                "tone": "uplifting and motivational",
                "elements": ["personal stories", "overcoming obstacles", "empowerment"]
            },
            "controversial": {
                "structure": ["bold_claim", "reasoning", "evidence", "counterargument", "conclusion"],
                "tone": "confident and thought-provoking",
                "elements": ["strong opinions", "debate starters", "polarizing takes"]
            }
        }
        
        template = style_templates.get(style, style_templates["engaging"])
        
        # Generate hook variations
        hook_options = []
        if include_hook:
            hook_options = [
                f"Did you know that {topic}...?",
                f"This will change how you think about {topic}",
                f"I wish someone told me this about {topic} earlier",
                f"The truth about {topic} that nobody talks about",
                f"Stop doing this when it comes to {topic}",
                f"This {topic} hack went viral for a reason",
                f"Everyone is wrong about {topic}, here's why"
            ]
        
        # Generate script content based on style and platform
        script_sections = {
            "hook": hook_options[0] if hook_options else f"Let's talk about {topic}",
            "main_content": f"""
Here's what you need to know about {topic}:

{_generate_main_content(topic, style, duration, template)}
""".strip(),
            "cta": _generate_cta(platform, include_cta) if include_cta else ""
        }
        
        # Combine sections into full script
        full_script = f"{script_sections['hook']}\n\n{script_sections['main_content']}"
        if script_sections['cta']:
            full_script += f"\n\n{script_sections['cta']}"
        
        # Generate timing notes
        timing_notes = _generate_timing_notes(duration, template['structure'])
        
        # Generate engagement tips
        engagement_tips = [
            f"Optimize for {platform} with {config['optimal_length']} content",
            f"Use {template['tone']} tone throughout",
            f"Include {', '.join(template['elements'])} for {style} style",
            f"Hook should grab attention within {config['hook_duration']} seconds",
            "Use visual cues and text overlays to support narration",
            "End with a strong call-to-action to drive engagement"
        ]
        
        return {
            "script": full_script,
            "hook": script_sections['hook'],
            "key_points": template['structure'],
            "cta": script_sections['cta'],
            "timing_notes": timing_notes,
            "engagement_tips": engagement_tips,
            "platform_config": config,
            "style_template": template,
            "message": f"Successfully generated {style} viral script for {platform} about '{topic}'"
        }
        
    except Exception as e:
        return {
            "script": "",
            "hook": "",
            "key_points": [],
            "cta": "",
            "timing_notes": {},
            "engagement_tips": [],
            "message": f"Error generating viral script: {str(e)}"
        }


def _generate_main_content(topic: str, style: str, duration: int, template: Dict) -> str:
    """Generate main content based on style and duration."""
    
    if style == "educational":
        return f"""
Key point 1: Understanding {topic} fundamentals
Key point 2: Common mistakes people make
Key point 3: Proven strategies that work
Key point 4: Action steps you can take today
"""
    elif style == "entertaining":
        return f"""
So here's the funny thing about {topic}...
*insert relatable scenario*
But wait, it gets better...
*escalate the situation*
And that's how you master {topic}!
"""
    elif style == "inspirational":
        return f"""
I used to struggle with {topic} just like you.
But then I discovered this simple truth...
It changed everything for me.
And now I want to share it with you.
"""
    elif style == "controversial":
        return f"""
Everyone thinks {topic} works one way.
But they're completely wrong.
Here's the real truth based on evidence...
And this is why it matters to you.
"""
    else:  # engaging (default)
        return f"""
Here's why {topic} is more important than you think.
Most people don't realize this simple fact...
But once you understand it, everything changes.
Let me show you exactly what I mean.
"""


def _generate_cta(platform: str, include_cta: bool) -> str:
    """Generate platform-specific call-to-action."""
    
    if not include_cta:
        return ""
    
    ctas = {
        "youtube_shorts": "Like if this helped you and subscribe for more viral content tips!",
        "tiktok": "Follow for more content like this! What should I cover next?",
        "instagram_reels": "Save this post and share it with someone who needs to see this!",
        "twitter": "Retweet if you agree! What's your take on this? Reply below."
    }
    
    return ctas.get(platform, "Engage with this content if it was helpful!")


def _generate_timing_notes(duration: int, structure: list) -> Dict[str, str]:
    """Generate timing notes for script sections."""
    
    section_count = len(structure)
    base_time = duration // section_count
    
    timing_notes = {}
    current_time = 0
    
    for i, section in enumerate(structure):
        if i == 0:  # Hook gets less time
            section_time = min(5, base_time)
        elif i == len(structure) - 1:  # CTA gets remaining time
            section_time = duration - current_time
        else:
            section_time = base_time
        
        timing_notes[section] = f"{current_time}-{current_time + section_time}s"
        current_time += section_time
    
    return timing_notes


# Function is ready to be imported and used directly
