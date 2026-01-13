---
description: Initialize new project documentation structure
argument-hint: [project-name]
allowed-tools: [Read, Write, Bash, Glob, AskUserQuestion]
---

# /pm:init

Initialize document structure for a new project.

## Workflow

1. **Confirm project type**
   - Ask project type using AskUserQuestion
   - Options: ML/AI, Backend, Frontend, Library

2. **Suggest core_docs by type**
   | Type | Recommended core_docs |
   |------|----------------------|
   | ML/AI | experiments, metrics, data_schema |
   | Backend | domain_model, api_spec, decisions |
   | Frontend | components, architecture |
   | Library | api_spec, decisions |

3. **Create files**
   - `PROJECT.yaml` - Project settings
   - `MANIFESTO.md` - Vision/direction
   - `MILESTONES.md` - Milestones/tasks
   - `docs/plans/` - Plan documents directory
   - `docs/reports/` - Reports directory

## Templates

Reference templates from `${CLAUDE_PLUGIN_ROOT}/skills/pm/references/templates/`

## Usage

```bash
/pm:init
/pm:init my-project
```
