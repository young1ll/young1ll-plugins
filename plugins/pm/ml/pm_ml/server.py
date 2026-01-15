"""PM ML MCP Server - Machine learning features for PM plugin."""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .db.sqlite import DatabaseManager
from .estimation.model import EstimationModel
from .analysis.hotspots import analyze_file_hotspot, analyze_hotspots, get_recommendations
from .analysis.patterns import extract_learning_insights, analyze_retrospective_text


# Initialize database
DB_PATH = os.environ.get("PM_DB_PATH", str(Path.home() / ".claude" / "pm.db"))
db = DatabaseManager(DB_PATH)

# Initialize ML model
MODEL_PATH = Path.home() / ".claude" / "pm_ml_model.pkl"
model = EstimationModel(MODEL_PATH if MODEL_PATH.exists() else None)

# Create MCP server
server = Server("pm-ml-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available ML tools"""
    return [
        Tool(
            name="pm_ml_predict_estimation",
            description="Predict story points for a task using ML",
            inputSchema={
                "type": "object",
                "properties": {
                    "taskId": {
                        "type": "string",
                        "description": "Task UUID to estimate",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["epic", "story", "task", "bug", "subtask"],
                        "description": "Task type (optional, overrides DB value)",
                    },
                },
                "required": ["taskId"],
            },
        ),
        Tool(
            name="pm_ml_analyze_risk",
            description="Analyze code hotspots and risk factors",
            inputSchema={
                "type": "object",
                "properties": {
                    "filePath": {
                        "type": "string",
                        "description": "File path to analyze",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "File pattern (e.g., '*.ts') for bulk analysis",
                    },
                },
            },
        ),
        Tool(
            name="pm_ml_suggest_buffer",
            description="Suggest buffer time based on risk and confidence",
            inputSchema={
                "type": "object",
                "properties": {
                    "taskId": {
                        "type": "string",
                        "description": "Task UUID",
                    },
                },
                "required": ["taskId"],
            },
        ),
        Tool(
            name="pm_ml_analyze_retrospective",
            description="Analyze retrospective text for patterns and insights",
            inputSchema={
                "type": "object",
                "properties": {
                    "sprintId": {
                        "type": "string",
                        "description": "Sprint UUID to analyze retrospectives",
                    },
                    "text": {
                        "type": "string",
                        "description": "Retrospective text to analyze",
                    },
                },
            },
        ),
        Tool(
            name="pm_ml_learning_insights",
            description="Extract learning insights from historical data",
            inputSchema={
                "type": "object",
                "properties": {
                    "projectId": {
                        "type": "string",
                        "description": "Project UUID to analyze",
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    if name == "pm_ml_predict_estimation":
        task_id = arguments["taskId"]

        # Get task from database
        task = db.query_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
        if not task:
            return [TextContent(type="text", text=f"Task not found: {task_id}")]

        # Override type if provided
        if "type" in arguments:
            task["type"] = arguments["type"]

        # Get historical tasks for context
        historical = db.query(
            "SELECT * FROM tasks WHERE project_id = ? AND estimate_points > 0 LIMIT 100",
            (task["project_id"],)
        )

        # Predict
        result = model.predict(task, historical)

        output = f"""ML Estimation Prediction:
- Predicted Points: {result['predicted_points']}
- Confidence: {result['confidence']:.2%}
- Method: {result['method']}
- Complexity Score: {result['complexity_score']:.1f}/10
"""

        if result["method"] == "ml":
            output += f"- Raw Prediction: {result['raw_prediction']:.2f}\n"
        else:
            output += "\nNote: Using rule-based estimation (not enough training data)\n"

        return [TextContent(type="text", text=output)]

    elif name == "pm_ml_analyze_risk":
        if "filePath" in arguments:
            # Single file analysis
            file_path = arguments["filePath"]
            repo_root = os.getcwd()

            result = analyze_file_hotspot(file_path, repo_root)

            if "error" in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]

            recommendations = get_recommendations(result)

            output = f"""Hotspot Analysis: {result['file']}
- Risk Score: {result['risk_score']}/10
- Risk Level: {result['risk_level']}
- Commit Count: {result['commit_count']}
- Total Churn: {result['churn']} lines

Recommendations:
"""
            for rec in recommendations:
                output += f"- {rec}\n"

            return [TextContent(type="text", text=output)]

        elif "pattern" in arguments:
            # Bulk analysis
            pattern = arguments["pattern"]
            repo_root = os.getcwd()

            results = analyze_hotspots(repo_root, [pattern], limit=10)

            if not results:
                return [TextContent(type="text", text="No files found matching pattern")]

            output = f"Top 10 Hotspots (pattern: {pattern}):\n\n"
            for i, result in enumerate(results, 1):
                output += f"{i}. {result['file']}\n"
                output += f"   Risk: {result['risk_score']}/10 ({result['risk_level']})\n"
                output += f"   Commits: {result['commit_count']}, Churn: {result['churn']}\n\n"

            return [TextContent(type="text", text=output)]

        else:
            return [TextContent(type="text", text="Either filePath or pattern is required")]

    elif name == "pm_ml_suggest_buffer":
        task_id = arguments["taskId"]

        # Get task
        task = db.query_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
        if not task:
            return [TextContent(type="text", text=f"Task not found: {task_id}")]

        # Get historical tasks
        historical = db.query(
            "SELECT * FROM tasks WHERE project_id = ? AND estimate_points > 0 LIMIT 100",
            (task["project_id"],)
        )

        # Get buffer suggestion
        result = model.suggest_buffer(task, historical)

        output = f"""Buffer Time Suggestion:
- Base Estimate: {result['base_estimate']} points
- Buffer: {result['buffer_points']} points ({result['buffer_percentage']}%)
- Total Estimate: {result['total_estimate']} points

Reasoning:
- Confidence: {result['confidence']:.2%}
- Complexity: {result['complexity']:.1f}/10

Recommendation: Plan for {result['total_estimate']} points to account for uncertainty.
"""

        return [TextContent(type="text", text=output)]

    elif name == "pm_ml_analyze_retrospective":
        if "text" in arguments:
            # Analyze provided text
            text = arguments["text"]
            result = analyze_retrospective_text(text)

            output = f"""Retrospective Analysis:
- Sentiment: {result['sentiment']}
- Positive mentions: {result['positive_count']}
- Negative mentions: {result['negative_count']}
- Action items found: {len(result['action_items'])}
- Mentioned tools: {', '.join(result['mentioned_tools']) or 'none'}
- Structured format: {'Yes' if result['has_structure'] else 'No'}
"""

            if result['action_items']:
                output += "\nAction Items:\n"
                for action in result['action_items'][:5]:
                    output += f"- {action}\n"

            return [TextContent(type="text", text=output)]

        elif "sprintId" in arguments:
            # Analyze sprint retrospectives
            sprint_id = arguments["sprintId"]

            # Get retrospectives (assuming they're stored in sprint notes or events)
            # For now, return a placeholder
            return [TextContent(
                type="text",
                text="Sprint retrospective analysis not yet implemented"
            )]

        else:
            return [TextContent(type="text", text="Either text or sprintId is required")]

    elif name == "pm_ml_learning_insights":
        project_id = arguments.get("projectId")

        # Get historical data
        if project_id:
            query = "SELECT * FROM tasks WHERE project_id = ? AND status = 'done'"
            params = (project_id,)
        else:
            query = "SELECT * FROM tasks WHERE status = 'done' LIMIT 200"
            params = ()

        completed_tasks = db.query(query, params)

        if not completed_tasks:
            return [TextContent(type="text", text="No completed tasks found")]

        # Calculate insights
        total_tasks = len(completed_tasks)
        avg_points = sum(
            t.get("estimate_points", 0) or 0 for t in completed_tasks
        ) / total_tasks if total_tasks > 0 else 0

        # Task type distribution
        type_counts = {}
        for task in completed_tasks:
            t = task.get("type", "task")
            type_counts[t] = type_counts.get(t, 0) + 1

        output = f"""Learning Insights:
- Completed Tasks: {total_tasks}
- Average Story Points: {avg_points:.1f}

Task Type Distribution:
"""
        for task_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            percentage = count / total_tasks * 100
            output += f"- {task_type}: {count} ({percentage:.1f}%)\n"

        # Train model if enough data
        if total_tasks >= 10:
            train_result = model.train(completed_tasks)
            if "error" not in train_result:
                output += f"\nML Model Training:
- Trained on {train_result['samples']} tasks
- R² Score: {train_result['r2_score']:.3f}
- MAE: {train_result['mae']:.2f} points
- Features: {train_result['feature_count']}

Model saved and ready for predictions.
"""
                # Save model
                model.save(MODEL_PATH)
            else:
                output += f"\nML Model Training: {train_result['error']}\n"

        return [TextContent(type="text", text=output)]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
