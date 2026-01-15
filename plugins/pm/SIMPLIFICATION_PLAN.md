# PM Plugin 단순화 계획

## 목표

**"Local Task → GitHub Issue → GitHub Project"** 핵심 워크플로우에 집중

## 현재 복잡성

- NestJS 모듈: 6개 (~2,195 lines)
- 레거시 server.ts: 2,029 lines
- Python ML 서비스: 11 files
- 총 레이어: agents, commands, skills, hooks
- 총 테스트: 526개

## 단순화 전략

### Phase 1: 제거 (Immediate)

1. **NestJS 모듈 삭제**
   - `mcp/modules/` 전체 삭제
   - `mcp/core/` 삭제 (database, events, common)
   - `mcp/transport/` 삭제
   - `mcp/main.ts`, `mcp/app.module.ts` 삭제
   - 이유: 과도한 엔지니어링, 실제 사용되지 않음

2. **Python ML 서비스 삭제**
   - `ml/` 전체 삭제
   - `.claude-plugin/mcp.json`에서 pm-ml 제거
   - 이유: 추정 예측/핫스팟은 프리미엄 기능, 핵심 워크플로우 아님

3. **불필요한 에이전트 삭제**
   - `agents/pm-planner/`, `agents/pm-reflector/` 삭제
   - `agents/pm-executor/` 유지 (핵심 실행 로직)
   - 이유: Plan-and-Execute 패턴은 과도, 단순 명령어로 충분

4. **Sprint/Sync 기능 제거**
   - Sprint 관련 MCP 도구 제거
   - Sync 큐 기능 제거
   - 이유: 복잡도 높고 사용 빈도 낮음

### Phase 2: 단순화 (Core Refactoring)

1. **server.ts 단순화**
   - 2,029 lines → ~500 lines
   - 핵심 MCP 도구만 유지:
     - Task: create, list, get, update, status
     - Project: create, list
     - GitHub: create_issue, link_task, sync_to_project
   - 제거: sprint, velocity, burndown, analytics

2. **스키마 단순화**
   - `storage/schema.sql` 단순화
   - 유지: tasks, projects, events
   - 제거: sprints, commits, pull_requests, sync_queue

3. **명령어 단순화**
   - `/pm:init` - 프로젝트 초기화
   - `/pm:task` - 태스크 CRUD
   - `/pm:sync` - GitHub 동기화 (issue → project)
   - 제거: `/pm:sprint`, `/pm:status` (복잡한 대시보드)

### Phase 3: 핵심 워크플로우 구현

**"Local Task → GitHub Issue → GitHub Project"**

```typescript
// 1. Local task 생성
pm_task_create({ title: "User auth" })
  → SQLite에 저장

// 2. GitHub Issue 생성
pm_github_create_issue({ taskId: "uuid" })
  → GitHub API 호출
  → task에 issue_number 링크

// 3. GitHub Project에 추가
pm_github_sync_to_project({ taskId: "uuid", projectId: 123 })
  → GitHub Projects API 호출
  → task 상태 업데이트
```

## 새로운 구조

```
plugins/pm/
├── .claude-plugin/
│   ├── plugin.json
│   └── mcp.json (pm-server만 유지)
├── mcp/
│   ├── server.ts          # 500 lines (단일 MCP 서버)
│   └── lib/
│       ├── db.ts          # DatabaseManager
│       ├── github.ts      # GitHub CLI 래퍼
│       └── git.ts         # Git 명령어 래퍼
├── storage/
│   ├── schema.sql         # tasks, projects, events만
│   └── lib/events.ts      # 이벤트 소싱 (유지)
├── commands/
│   ├── init.md            # /pm:init
│   ├── task.md            # /pm:task
│   └── sync.md            # /pm:sync
├── lib/
│   └── (git, github 유틸리티)
└── tests/
    ├── unit/              # ~100 tests
    └── integration/       # ~50 tests
```

## MCP 도구 (최종)

**총 10개 도구** (기존 40+개에서 대폭 감소)

### Task (5개)
- `pm_task_create`
- `pm_task_list`
- `pm_task_get`
- `pm_task_update`
- `pm_task_status`

### Project (2개)
- `pm_project_create`
- `pm_project_list`

### GitHub (3개)
- `pm_github_create_issue` - Local task → GitHub Issue
- `pm_github_link_task` - 기존 Issue와 Task 연결
- `pm_github_sync_to_project` - Issue → GitHub Project

## 예상 결과

| 메트릭 | 현재 | 목표 |
|--------|------|------|
| 총 코드 라인 | ~6,000+ | ~1,500 |
| MCP 도구 | 40+ | 10 |
| 테스트 | 526 | ~150 |
| 디렉토리 | 12+ | 6 |
| 의존성 | NestJS, Python | TypeScript만 |
| server.ts | 2,029 lines | ~500 lines |

## 구현 순서

1. ✅ 계획 수립 (이 문서)
2. ⏳ NestJS 모듈 삭제
3. ⏳ Python ML 삭제
4. ⏳ server.ts 단순화
5. ⏳ 스키마 단순화
6. ⏳ GitHub 동기화 구현
7. ⏳ 테스트 업데이트
8. ⏳ 문서 업데이트

## 성공 기준

- [ ] server.ts < 600 lines
- [ ] MCP 도구 <= 10개
- [ ] 테스트 < 200개, 모두 통과
- [ ] "Local Task → GitHub Issue → GitHub Project" 워크플로우 동작
- [ ] 빌드 0 에러
