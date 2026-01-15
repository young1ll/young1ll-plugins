"""Feature engineering for task estimation prediction."""

from typing import Dict, List, Any
import re


def extract_features(task: Dict[str, Any], historical_tasks: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Extract features from a task for ML estimation.

    Args:
        task: Task to estimate
        historical_tasks: Historical tasks for context

    Returns:
        Feature dictionary for ML model
    """
    features = {}

    # Task type encoding (one-hot)
    task_types = ["epic", "story", "task", "bug", "subtask"]
    task_type = task.get("type", "task")
    for t in task_types:
        features[f"type_{t}"] = 1.0 if task_type == t else 0.0

    # Priority encoding
    priority_map = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    features["priority"] = priority_map.get(task.get("priority", "medium"), 2)

    # Title complexity
    title = task.get("title", "")
    features["title_length"] = len(title)
    features["title_words"] = len(title.split())

    # Description complexity
    description = task.get("description", "")
    features["has_description"] = 1.0 if description else 0.0
    features["description_length"] = len(description) if description else 0
    features["description_words"] = len(description.split()) if description else 0

    # Technical keywords (indicating complexity)
    tech_keywords = [
        "api", "database", "integration", "refactor", "migration",
        "security", "performance", "optimization", "algorithm"
    ]
    combined_text = (title + " " + description).lower()
    features["tech_keywords_count"] = sum(
        1 for keyword in tech_keywords if keyword in combined_text
    )

    # Historical context - average points by type
    if historical_tasks:
        same_type_tasks = [t for t in historical_tasks if t.get("type") == task_type]
        if same_type_tasks:
            avg_points = sum(
                t.get("estimate_points", 0) or 0 for t in same_type_tasks
            ) / len(same_type_tasks)
            features["historical_avg_points"] = avg_points
        else:
            features["historical_avg_points"] = 3.0  # Default
    else:
        features["historical_avg_points"] = 3.0

    # Parent task context
    features["is_subtask"] = 1.0 if task.get("parent_id") else 0.0

    return features


def calculate_complexity_score(task: Dict[str, Any]) -> float:
    """
    Calculate a simple complexity score for a task (0-10).

    Args:
        task: Task to analyze

    Returns:
        Complexity score (0-10)
    """
    score = 0.0

    # Base score from task type
    type_scores = {
        "epic": 8.0,
        "story": 5.0,
        "task": 3.0,
        "bug": 2.0,
        "subtask": 1.0,
    }
    score += type_scores.get(task.get("type", "task"), 3.0)

    # Priority multiplier
    priority_multipliers = {
        "critical": 1.3,
        "high": 1.2,
        "medium": 1.0,
        "low": 0.9,
    }
    score *= priority_multipliers.get(task.get("priority", "medium"), 1.0)

    # Description complexity
    description = task.get("description", "")
    if description:
        # Long description adds complexity
        if len(description) > 500:
            score += 1.5
        elif len(description) > 200:
            score += 1.0

    # Technical keywords
    combined_text = (task.get("title", "") + " " + description).lower()
    tech_patterns = [
        r"\bapi\b", r"\bdatabase\b", r"\bintegration\b",
        r"\brefactor\b", r"\bmigration\b", r"\bsecurity\b",
    ]
    tech_count = sum(1 for pattern in tech_patterns if re.search(pattern, combined_text))
    score += tech_count * 0.5

    # Cap at 10
    return min(score, 10.0)
