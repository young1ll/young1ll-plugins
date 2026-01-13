---
description: Check current milestone progress and document status
allowed-tools: [Read, Glob, Grep]
---

# /pm:status

Check current project progress.

## Prerequisites

- `PROJECT.yaml` file must exist
- `MILESTONES.md` file must exist

## Output Information

1. **Milestone info**
   - Current milestone name
   - Progress (% and progress bar)
   - Completed/total tasks

2. **Task list**
   - Remaining tasks (unchecked)
   - Completed tasks (checked)

3. **Document status**
   - core_docs list
   - Last modified date for each document
   - File existence status

## Output Format

```
PM Status — {{ project-name }}

Current Milestone: v0.1.0 — Initial Setup
   ████████░░░░░░░░ 50% (4/8)

Remaining Tasks:
   - [ ] Setup basic structure
   - [ ] Write tests
   - [ ] Documentation
   - [ ] Code review

Document Status:
   vision     │ MANIFESTO.md    │ 3 days ago
   progress   │ MILESTONES.md   │ today
   api_spec   │ docs/API.md     │ 7 days ago
```
