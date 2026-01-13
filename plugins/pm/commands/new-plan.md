---
description: Create new plan document
argument-hint: <plan-name>
allowed-tools: [Read, Write]
---

# /pm:new-plan

Create a new plan document.

## Usage

```bash
/pm:new-plan user-authentication
/pm:new-plan "API refactoring"
```

## Arguments

- `<plan-name>`: Plan name (required)

## Generated File

**Location**: `{plans_dir}/PLAN_{name}.md`

- plans_dir is `plans_dir` value from PROJECT.yaml (default: `docs/plans`)

## Template

```markdown
# PLAN: {{ plan-name }}

**Status**: DRAFT
**Created**: {{ date }}
**Milestone**: {{ current-milestone }}

---

## Summary

[Write plan summary here]

## Goals

- [ ] Goal 1
- [ ] Goal 2

## Non-Goals

- Things not covered in this plan

## Approach

### Phase 1: Preparation

1. Step 1
2. Step 2

### Phase 2: Implementation

1. Step 1
2. Step 2

## Tasks

- [ ] Task 1
- [ ] Task 2

## Open Questions

- [ ] Question 1
- [ ] Question 2
```
