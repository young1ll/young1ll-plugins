"""Pattern analysis for retrospectives and learnings."""

from typing import Dict, List, Any
from collections import Counter
import re


def analyze_retrospective_text(text: str) -> Dict[str, Any]:
    """
    Analyze retrospective text for patterns and insights.

    Args:
        text: Retrospective text to analyze

    Returns:
        Analysis result with extracted patterns
    """
    # Sentiment keywords
    positive_keywords = [
        "good", "great", "excellent", "well", "success", "improved",
        "better", "effective", "productive", "smooth"
    ]
    negative_keywords = [
        "issue", "problem", "difficult", "slow", "blocked", "unclear",
        "confusing", "missing", "failed", "late"
    ]

    text_lower = text.lower()

    # Count sentiment
    positive_count = sum(1 for word in positive_keywords if word in text_lower)
    negative_count = sum(1 for word in negative_keywords if word in text_lower)

    # Determine overall sentiment
    if positive_count > negative_count:
        sentiment = "positive"
    elif negative_count > positive_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Extract action items (lines starting with TODO, [ ], - [ ], etc.)
    action_pattern = r'(?:^|\n)[\s-]*(?:\[[ x]\]|TODO:|Action:)\s*(.+?)(?:\n|$)'
    actions = re.findall(action_pattern, text, re.IGNORECASE | re.MULTILINE)

    # Extract mentions of tools, processes, practices
    tool_keywords = ["git", "github", "jira", "slack", "tests", "ci", "cd", "review"]
    mentioned_tools = [tool for tool in tool_keywords if tool in text_lower]

    return {
        "sentiment": sentiment,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "action_items": actions,
        "mentioned_tools": mentioned_tools,
        "word_count": len(text.split()),
        "has_structure": "##" in text or "###" in text,
    }


def extract_learning_insights(
    retrospectives: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Extract learning insights from multiple retrospectives.

    Args:
        retrospectives: List of retrospective records

    Returns:
        Aggregated insights
    """
    if not retrospectives:
        return {
            "error": "No retrospectives to analyze",
            "count": 0,
        }

    all_text = " ".join(
        retro.get("notes", "") for retro in retrospectives if retro.get("notes")
    )

    analysis = analyze_retrospective_text(all_text)

    # Find common themes by extracting frequent words
    words = re.findall(r'\b\w{4,}\b', all_text.lower())
    word_freq = Counter(words)

    # Filter out common words
    stop_words = {
        "that", "this", "with", "have", "from", "they", "been",
        "were", "what", "which", "their", "there", "would", "could"
    }
    themes = [
        word for word, count in word_freq.most_common(20)
        if word not in stop_words
    ]

    return {
        "retrospective_count": len(retrospectives),
        "overall_sentiment": analysis["sentiment"],
        "total_action_items": len(analysis["action_items"]),
        "common_themes": themes[:10],
        "frequently_mentioned_tools": analysis["mentioned_tools"],
        "structured_notes_percentage": round(
            sum(1 for r in retrospectives if "##" in r.get("notes", ""))
            / len(retrospectives) * 100, 1
        ),
    }
