"""Code hotspot analysis - identify risky areas of codebase."""

from typing import Dict, List, Any
from pathlib import Path
import subprocess
import json


def analyze_file_hotspot(
    file_path: str,
    repo_root: str,
    max_commits: int = 100
) -> Dict[str, Any]:
    """
    Analyze a file for risk factors based on git history.

    Args:
        file_path: Relative path to file from repo root
        repo_root: Repository root directory
        max_commits: Max commits to analyze

    Returns:
        Hotspot analysis result
    """
    try:
        # Get commit count for file
        result = subprocess.run(
            ["git", "log", "--oneline", f"-n{max_commits}", "--", file_path],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        commit_count = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0

        # Get lines changed
        result = subprocess.run(
            ["git", "log", "--numstat", f"-n{max_commits}", "--", file_path],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )

        total_additions = 0
        total_deletions = 0
        for line in result.stdout.split("\n"):
            parts = line.split("\t")
            if len(parts) >= 2 and parts[0].isdigit():
                total_additions += int(parts[0])
                total_deletions += int(parts[1])

        # Calculate risk score (0-10)
        # More commits = higher risk (frequent changes)
        commit_factor = min(commit_count / 20.0, 5.0)

        # More churn (adds + deletes) = higher risk
        churn = total_additions + total_deletions
        churn_factor = min(churn / 1000.0, 3.0)

        # Lines of code
        try:
            with open(Path(repo_root) / file_path, "r") as f:
                lines = len(f.readlines())
            size_factor = min(lines / 500.0, 2.0)
        except:
            size_factor = 0.0

        risk_score = commit_factor + churn_factor + size_factor

        return {
            "file": file_path,
            "risk_score": round(risk_score, 2),
            "commit_count": commit_count,
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "churn": churn,
            "risk_level": get_risk_level(risk_score),
        }

    except subprocess.CalledProcessError as e:
        return {
            "file": file_path,
            "error": f"Git command failed: {e}",
            "risk_score": 0,
        }


def get_risk_level(score: float) -> str:
    """Convert risk score to level"""
    if score >= 8.0:
        return "critical"
    elif score >= 6.0:
        return "high"
    elif score >= 4.0:
        return "medium"
    else:
        return "low"


def analyze_hotspots(
    repo_root: str,
    file_patterns: List[str],
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Analyze multiple files for hotspots.

    Args:
        repo_root: Repository root directory
        file_patterns: List of file patterns to analyze
        limit: Max files to return

    Returns:
        List of hotspot analysis results, sorted by risk
    """
    # Get all files matching patterns
    all_files = []
    for pattern in file_patterns:
        try:
            result = subprocess.run(
                ["git", "ls-files", pattern],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True,
            )
            files = [f for f in result.stdout.strip().split("\n") if f]
            all_files.extend(files)
        except subprocess.CalledProcessError:
            continue

    # Analyze each file
    results = []
    for file_path in all_files[:50]:  # Limit to 50 files to avoid timeout
        hotspot = analyze_file_hotspot(file_path, repo_root)
        if "error" not in hotspot:
            results.append(hotspot)

    # Sort by risk score descending
    results.sort(key=lambda x: x["risk_score"], reverse=True)

    return results[:limit]


def get_recommendations(hotspot: Dict[str, Any]) -> List[str]:
    """
    Get recommendations for a hotspot file.

    Args:
        hotspot: Hotspot analysis result

    Returns:
        List of recommendations
    """
    recommendations = []
    risk_level = hotspot.get("risk_level", "low")

    if risk_level in ["critical", "high"]:
        recommendations.append("Consider refactoring to reduce complexity")
        recommendations.append("Add comprehensive unit tests")
        recommendations.append("Review recent changes for potential issues")

    if hotspot.get("commit_count", 0) > 30:
        recommendations.append("High change frequency - consider stabilizing the API")

    if hotspot.get("churn", 0) > 1000:
        recommendations.append("High code churn - may indicate design issues")

    return recommendations
