# PM ML Service

Machine learning features for the PM plugin, providing:
- Task estimation prediction using Random Forest
- Code hotspot analysis
- Retrospective pattern analysis
- Learning insights from historical data

## Architecture

```
pm_ml/
├── server.py          # FastMCP server with 5 MCP tools
├── estimation/        # ML estimation models
│   ├── model.py       # Random Forest regressor
│   └── features.py    # Feature engineering
├── analysis/          # Code & text analysis
│   ├── hotspots.py    # Git-based hotspot detection
│   └── patterns.py    # NLP pattern extraction
└── db/
    └── sqlite.py      # Shared SQLite access
```

## MCP Tools

### 1. `pm_ml_predict_estimation`
Predict story points for a task using ML or rule-based estimation.

**Input:**
- `taskId` (required): Task UUID
- `type` (optional): Task type override

**Output:** Predicted points, confidence, complexity score

### 2. `pm_ml_analyze_risk`
Analyze code files for risk factors based on git history.

**Input:**
- `filePath`: Single file to analyze
- `pattern`: File pattern for bulk analysis (e.g., "*.ts")

**Output:** Risk score (0-10), commit count, churn, recommendations

### 3. `pm_ml_suggest_buffer`
Suggest buffer time based on confidence and complexity.

**Input:**
- `taskId` (required): Task UUID

**Output:** Base estimate, buffer points, total estimate

### 4. `pm_ml_analyze_retrospective`
Analyze retrospective text for sentiment and action items.

**Input:**
- `text`: Retrospective text to analyze
- `sprintId`: Sprint UUID (alternative)

**Output:** Sentiment, action items, mentioned tools

### 5. `pm_ml_learning_insights`
Extract learning insights from historical data.

**Input:**
- `projectId` (optional): Filter by project

**Output:** Task statistics, type distribution, ML model training status

## Installation

```bash
cd plugins/pm/ml
pip install -e .
```

## Usage

### As MCP Server

```bash
python -m pm_ml.server
```

### Configuration

Add to `.claude-plugin/mcp.json`:

```json
{
  "mcpServers": {
    "pm": {
      "command": "node",
      "args": ["dist/mcp/main.js"]
    },
    "pm-ml": {
      "command": "python",
      "args": ["-m", "pm_ml.server"],
      "env": {
        "PM_DB_PATH": "/path/to/.claude/pm.db"
      }
    }
  }
}
```

## Model Training

The ML model automatically trains when you run `pm_ml_learning_insights` with at least 10 completed tasks with estimates. The trained model is saved to `~/.claude/pm_ml_model.pkl`.

## Features

### Estimation Model
- Random Forest with 100 trees
- Features: task type, priority, title/description complexity, technical keywords
- Confidence scoring based on tree variance
- Fallback to rule-based estimation

### Hotspot Analysis
- Commit frequency
- Code churn (additions + deletions)
- File size
- Risk scoring (0-10)

### Pattern Analysis
- Sentiment analysis
- Action item extraction
- Tool mention detection
- Theme extraction

## Dependencies

- `mcp>=1.0.0` - Model Context Protocol
- `scikit-learn>=1.4.0` - Machine learning
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.26.0` - Numerical computing

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```
