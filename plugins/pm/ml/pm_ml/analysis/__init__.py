"""Code analysis module."""

from .hotspots import analyze_file_hotspot, analyze_hotspots, get_recommendations
from .patterns import analyze_retrospective_text, extract_learning_insights

__all__ = [
    "analyze_file_hotspot",
    "analyze_hotspots",
    "get_recommendations",
    "analyze_retrospective_text",
    "extract_learning_insights",
]
