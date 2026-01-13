---
description: Create report
argument-hint: <topic> [type]
allowed-tools: [Read, Write]
---

# /pm:new-report

Create a report.

## Usage

```bash
/pm:new-report sprint-1
/pm:new-report "model training results" experiment
/pm:new-report api-refactoring implementation
```

## Arguments

- `<topic>`: Report topic (required)
- `[type]`: Report type (optional, default: implementation)

## Report Types

| Type | Description | Use case |
|------|-------------|----------|
| `implementation` | Implementation report (default) | After feature completion |
| `experiment` | Experiment report | ML experiment results |
| `decision` | Decision record (ADR) | Technical decisions |
| `retrospective` | Retrospective report | Sprint/milestone retrospective |

## Generated File

**Location**: `{reports_dir}/REPORT_{date}_{topic}.md`

- reports_dir is `reports_dir` value from PROJECT.yaml (default: `docs/reports`)
- date format: YYYYMMDD
