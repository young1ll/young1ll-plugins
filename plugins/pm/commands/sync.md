---
description: Auto-sync MILESTONES.md progress
allowed-tools: [Read, Edit, Grep]
---

# /pm:sync

Auto-calculate and update progress in MILESTONES.md based on task checkboxes.

## Usage

```bash
/pm:sync
```

## Operation

1. **Read MILESTONES.md**
   - Check core_docs.progress path in PROJECT.yaml
   - Parse file content

2. **Calculate progress**
   - Completed tasks: Lines starting with `- [x]` or `- [X]`
   - Incomplete tasks: Lines starting with `- [ ]`
   - Progress = (completed / total) * 100

3. **Update file**
   - Update `Progress: N%` line
   - Update `Last updated: YYYY-MM-DD` line

## Example

### Before
```markdown
## Current: v0.1.0

Progress: 25%
Last updated: 2024-01-10

### Tasks
- [x] Setup basic structure
- [x] Initialize project
- [ ] Implement core features
- [ ] Write tests
```

### After
```markdown
## Current: v0.1.0

Progress: 50%
Last updated: 2024-01-13

### Tasks
- [x] Setup basic structure
- [x] Initialize project
- [ ] Implement core features
- [ ] Write tests
```

## CLI Script

```bash
${CLAUDE_PLUGIN_ROOT}/skills/pm/scripts/pm sync
```
