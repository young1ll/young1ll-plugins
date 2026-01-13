---
description: PM plugin usage guide
---

# /pm:help

Display PM plugin usage information.

## Output

Print the following **exactly as shown**:

```
PM — Project Management v1.0.0

Project documentation management and workflow orchestration.

Getting Started
   /pm:init           Initialize new project
   /pm:adopt          Adopt existing project (code analysis)

View
   /pm:status         Milestone progress + document status
   /pm:validate       Full project validation (6 checks)

Create
   /pm:new-plan <name>       Create plan document
   /pm:new-report <topic>    Create report

Sync
   /pm:sync           Auto-calculate MILESTONES progress

Core Files
   PROJECT.yaml       Project settings (required)
   MANIFESTO.md       Vision/direction
   MILESTONES.md      Milestones/tasks

Agents
   project-analyzer   Project structure analysis
   milestone-tracker  Milestone progress tracking

Quick Start
   New project    -> /pm:init
   Existing       -> /pm:adopt
   Check progress -> /pm:status
```
