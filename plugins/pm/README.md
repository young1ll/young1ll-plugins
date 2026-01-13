# PM Plugin for Claude Code

프로젝트 문서 관리 및 작업 흐름 조율 플러그인.

PROJECT.yaml 기반 체계적 문서 관리, 마일스톤 추적, 자동 검증을 제공합니다.

## 설치

```bash
# Claude Code에서
/plugins add pm@claude-plugins-young1ll
```

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/pm:help` | PM 플러그인 도움말 표시 |
| `/pm:init [project-name]` | 새 프로젝트 문서 체계 초기화 |
| `/pm:status` | 현재 마일스톤 진행률 및 문서 상태 확인 |
| `/pm:validate` | 프로젝트 전체 검증 (6가지 항목) |
| `/pm:new-plan <name>` | 새 계획 문서 생성 |
| `/pm:new-report <topic> [type]` | 보고서 생성 |
| `/pm:sync` | MILESTONES.md 진행률 자동 동기화 |
| `/pm:adopt` | 기존 프로젝트에 PM 문서 체계 도입 |

## 문서 체계

### PROJECT.yaml

프로젝트 루트에 생성되는 설정 파일:

```yaml
name: my-project
version: 0.1.0

core_docs:
  vision: docs/MANIFESTO.md
  progress: docs/MILESTONES.md

plans_dir: docs/plans
reports_dir: docs/reports
```

### 핵심 문서

- **MANIFESTO.md**: 프로젝트 비전, 목표, 핵심 가치
- **MILESTONES.md**: 마일스톤 및 태스크 진행 추적

### 보고서 유형

| 유형 | 설명 | 용도 |
|------|------|------|
| `implementation` | 구현 보고서 (기본) | 기능 완료 후 |
| `experiment` | 실험 보고서 | ML 실험 결과 |
| `decision` | 결정 기록 (ADR) | 기술 결정 |
| `retrospective` | 회고 보고서 | 스프린트/마일스톤 회고 |

## 검증 항목 (/pm:validate)

1. **구조 검증**: PROJECT.yaml 필수 필드
2. **문서 존재**: core_docs 파일 존재 확인
3. **문서 품질**: 빈 파일, 템플릿 플레이스홀더, 오래된 문서
4. **일관성**: 미등록 문서, 진행률 동기화 상태
5. **정리 필요**: 오래된 DRAFT, 임시 파일
6. **진행 상황**: 마일스톤 정보, 블로커 존재

## ignore 설정

PROJECT.yaml에서 검증 제외 항목 설정:

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

## 라이선스

MIT
