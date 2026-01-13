---
description: Full project validation (6 checks)
allowed-tools: [Read, Glob, Grep, Bash]
---

# /pm:validate

Validate project status from 6 perspectives.

## Validation Items

### 1. Structure Validation
- PROJECT.yaml required fields (name, core_docs)
- core_docs.vision defined
- core_docs.progress defined
- plans_dir, reports_dir directories exist

### 2. Document Existence
- All files defined in core_docs exist
- Verify file path for each document role

### 3. Document Quality
- Detect empty files
- Template placeholders remaining ({{ }}, [TODO], [TBD])
- Stale documents (30+ days without modification) — ignorable with `stale_documents` rule

### 4. Consistency Validation
- Unregistered docs/*.md not in core_docs — ignorable with `unregistered_docs` rule
- MILESTONES.md progress sync status

### 5. Cleanup Check
- Old DRAFT documents (14+ days) — ignorable with `old_drafts` rule
- Temp/backup files (.bak, ~, .tmp) — ignorable with `temp_files` rule

### 6. Progress Validation
- Current milestone info
- Overall task progress
- Blocker existence

## ignore Configuration

In PROJECT.yaml:

```yaml
ignore:
  files:
    - "docs/archived/*"
    - "*.bak"
  rules:
    - unregistered_docs
    - stale_documents
    - old_drafts
    - temp_files
```

## CLI Script

```bash
${CLAUDE_PLUGIN_ROOT}/skills/pm/scripts/pm validate
```
