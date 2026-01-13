---
description: Adopt PM document structure for existing project (code analysis)
allowed-tools: [Read, Write, Glob, Grep, Bash, AskUserQuestion]
---

# /pm:adopt

Adopt PM document structure for an existing project. Analyzes codebase to suggest appropriate document structure.

## Usage

```bash
/pm:adopt
```

## Workflow

### 1. Codebase Scan

Analyze dependency files:
- `package.json` (Node.js)
- `pyproject.toml`, `requirements.txt` (Python)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- `pom.xml`, `build.gradle` (Java)

Analyze directory structure:
- `src/`, `lib/` - Source code
- `models/`, `data/` - ML project signals
- `api/`, `routes/` - API server signals
- `components/`, `pages/` - Frontend signals
- `tests/`, `__tests__/` - Tests exist

### 2. Infer Characteristics

| Discovery | Inference | Recommended core_docs |
|-----------|-----------|----------------------|
| pytorch, tensorflow, wandb | ML project | experiments, metrics, data_schema |
| fastapi, express, nestjs | API server | api_spec, domain_model |
| react, vue, next | Frontend | architecture, components |
| migrations/, prisma | Database | domain_model, data_schema |
| openapi.yaml, swagger | API spec exists | api_spec (link existing) |

### 3. Discover Existing Docs

Scan targets:
- `README.md` → Use as MANIFESTO.md draft
- `docs/*.md` → Link to appropriate core_doc role
- `CHANGELOG.md` → Reference
- `ARCHITECTURE.md`, `DESIGN.md` → Link as architecture

### 4. GitHub Issues Migration (Optional)

```bash
# If gh CLI is installed
gh issue list --state open --json number,title,labels
```

Convert open issues to MILESTONES.md Tasks:
```markdown
### Tasks (from GitHub Issues)
- [ ] #123 Fix user authentication bug
- [ ] #124 Improve API response time
```

### 5. User Confirmation and Creation

Show analysis results and suggestions, create files after confirmation.
