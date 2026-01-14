# PM Plugin 로드맵 (LEVEL_3)

프로덕션 안정화 및 기능 확장 계획.

**작성일**: 2025-01-14
**기반 버전**: v1.0.0 (LEVEL_2 완료)

---

## 1. LEVEL_2 달성 현황

### ✅ 완료된 작업
- Critical: Shell injection 취약점 수정
- High: 하이브리드 ID 시스템 (UUID + seq)
- High: GitHub 양방향 동기화
- Medium: Git 유틸 통합
- Medium: 문서화 완성
- 526개 테스트 전체 통과

### 현재 상태
```
✅ 보안: 0 취약점
✅ 타입: 0 에러
✅ 테스트: 526/526 passed
✅ 빌드: 73KB
✅ 문서: 892 lines
```

---

## 2. LEVEL_3 목표

### 2.1 비전
> "완전한 Git-First 프로젝트 관리 플랫폼"

### 2.2 핵심 목표
1. **Git 워크플로우 완성** - commits, PR 완전 추적
2. **오프라인 우선** - sync_queue 구현
3. **성능 최적화** - 쿼리 최적화, 캐싱
4. **Reflexion 강화** - 학습 기반 추정 개선
5. **플러그인 에코시스템** - 확장 가능한 아키텍처

---

## 3. 기능 로드맵

### Phase 4: Git 추적 강화 (High Priority)

**목표**: 완전한 Git 히스토리 관리

#### 4.1 Commits 테이블 활성화
```typescript
// Repository
class CommitRepository {
  create(sha, taskId, message, author, branch)
  getByTask(taskId)
  getByBranch(branch)
  search(query)
}

// MCP Tools
pm_commit_list(taskId?, branch?, limit?)
pm_commit_get(sha)
pm_commit_stats(from?, to?)
```

**작업 항목**:
- [x] 테이블 스키마 정의됨 (schema.sql)
- [ ] CommitRepository 구현
- [ ] MCP 도구 3개 추가
- [ ] 자동 커밋 기록 (PostToolUse hook)
- [ ] 테스트 추가 (~30개)

**예상 시간**: 2-3시간
**우선순위**: High

---

#### 4.2 Pull Requests 테이블 활성화
```typescript
// Repository
class PullRequestRepository {
  create(taskId, number, title, repo, url)
  getByTask(taskId)
  updateStatus(id, status, mergedAt?)
}

// MCP Tools
pm_pr_create(taskId, title?, body?)     // GitHub PR 생성
pm_pr_link(taskId, prNumber)            // 기존 PR 연결
pm_pr_list(taskId?, status?)
pm_pr_status(prNumber)                  // 상태 동기화
```

**작업 항목**:
- [x] 테이블 스키마 정의됨
- [ ] PullRequestRepository 구현
- [ ] MCP 도구 4개 추가
- [ ] GitHub PR 자동 추적
- [ ] 상태 자동 동기화 (webhook or polling)
- [ ] 테스트 추가 (~40개)

**예상 시간**: 3-4시간
**우선순위**: High

**총 예상 시간**: 5-7시간

---

### Phase 5: 오프라인 우선 (Medium Priority)

**목표**: 네트워크 불안정 환경 지원

#### 5.1 Sync Queue 구현
```typescript
// MCP Tools
pm_sync_queue_list(status?, limit?)
pm_sync_queue_process(queueId?)        // 수동 재시도
pm_sync_queue_stats()                  // 큐 통계
pm_sync_queue_clear(daysOld?)          // 완료 항목 정리

// Auto-retry Logic
- sync 실패 시 자동으로 큐에 추가
- exponential backoff (1s, 2s, 4s, 8s, 16s)
- 최대 재시도 5회
- 실패 시 에러 메시지 저장
```

**작업 항목**:
- [x] 테이블 스키마 정의됨
- [x] SyncQueueRepository 구현됨
- [ ] server.ts에서 활성화
- [ ] MCP 도구 4개 추가
- [ ] 자동 재시도 로직
- [ ] 백그라운드 워커 (optional)
- [ ] 테스트 추가 (~35개)

**예상 시간**: 3-4시간
**우선순위**: Medium

---

### Phase 6: 의존성 관리 (Medium Priority)

**목표**: 태스크 간 의존 관계 시각화

#### 6.1 Task Dependencies
```typescript
// Repository
class TaskDependencyRepository {
  addDependency(taskId, dependsOnTaskId, type?)
  removeDependency(taskId, dependsOnTaskId)
  getDependencies(taskId)               // 이 태스크가 의존하는 것들
  getDependents(taskId)                 // 이 태스크에 의존하는 것들
  detectCycles()                        // 순환 의존성 감지
}

// MCP Tools
pm_task_dependency_add(taskId, dependsOn)
pm_task_dependency_remove(taskId, dependsOn)
pm_task_dependency_graph(taskId)       // 의존성 그래프 (ASCII art)
pm_task_blockers(projectId?)           // 블로커 감지
```

**작업 항목**:
- [ ] 테이블 스키마 추가
- [ ] TaskDependencyRepository 구현
- [ ] MCP 도구 4개 추가
- [ ] 의존성 그래프 시각화 (ASCII)
- [ ] 블로커 자동 감지
- [ ] 순환 의존성 방지
- [ ] 테스트 추가 (~30개)

**예상 시간**: 4-5시간
**우선순위**: Medium

---

### Phase 7: Git 이벤트 추적 (Low Priority)

**목표**: 완전한 Git 히스토리 감사

#### 7.1 Git Events
```typescript
// Repository
class GitEventRepository {
  record(eventType, metadata)
  getEvents(from?, to?, type?)
  getByBranch(branch)
  getByAuthor(author)
}

// Event Types
- branch_created
- branch_deleted
- commit_created
- push
- pull
- merge
- rebase

// MCP Tools
pm_git_events(from?, to?, type?)
pm_git_timeline(taskId)                // 태스크 Git 타임라인
```

**작업 항목**:
- [ ] 테이블 스키마 추가
- [ ] GitEventRepository 구현
- [ ] PostToolUse 훅에서 자동 기록
- [ ] MCP 도구 2개 추가
- [ ] 테스트 추가 (~25개)

**예상 시간**: 2-3시간
**우선순위**: Low

---

### Phase 8: Reflexion 강화 (Low Priority)

**목표**: AI 기반 추정 정확도 개선

#### 8.1 Estimation Accuracy
```typescript
// Repository
class EstimationAccuracyRepository {
  record(taskId, estimated, actual)
  getAccuracy(projectId, sprintId?)
  getHistory(taskId)
  analyze()                             // 추정 오류 패턴 분석
}

// MCP Tools
pm_estimation_accuracy(projectId)
pm_estimation_suggest(taskType, complexity) // AI 추정 제안
```

#### 8.2 Episodic Memory
```typescript
// Repository
class EpisodicMemoryRepository {
  store(episode, context, outcome, reflection)
  retrieve(context)                     // 유사 컨텍스트 검색
  learn(feedback)                       // 피드백 학습
}
```

**작업 항목**:
- [ ] 테이블 스키마 추가 (2개)
- [ ] Repository 구현 (2개)
- [ ] MCP 도구 추가
- [ ] pm-reflector 에이전트와 통합
- [ ] 테스트 추가 (~20개)

**예상 시간**: 5-6시간
**우선순위**: Low

---

### Phase 9: 성능 최적화 (Ongoing)

**목표**: 대규모 프로젝트 지원

#### 9.1 쿼리 최적화
- [ ] 복합 인덱스 추가
- [ ] EXPLAIN QUERY PLAN 분석
- [ ] N+1 쿼리 제거
- [ ] 페이지네이션 개선

#### 9.2 캐싱 전략
- [ ] 자주 조회되는 데이터 캐싱
- [ ] 프로젝트 설정 캐싱
- [ ] 속도 계산 캐싱

#### 9.3 벤치마크
- [ ] 태스크 1000개 시나리오
- [ ] 스프린트 100개 시나리오
- [ ] 동시 요청 처리

**예상 시간**: 3-4시간
**우선순위**: Medium

---

### Phase 10: UX 개선 (Ongoing)

**목표**: 사용자 경험 향상

#### 10.1 에러 메시지
- [ ] 명확한 에러 메시지
- [ ] 해결 방법 제안
- [ ] 에러 코드 체계

#### 10.2 프로그레스
- [ ] 긴 작업에 프로그레스 바
- [ ] 백그라운드 작업 상태
- [ ] 알림 시스템

#### 10.3 대시보드
- [ ] ASCII 대시보드 개선
- [ ] 컬러 출력 (ANSI colors)
- [ ] 인터랙티브 요소

**예상 시간**: 2-3시간
**우선순위**: Low

---

## 4. 우선순위 매트릭스

### Critical Path (Phase 4 → Phase 5)
```
Phase 4: Git 추적 강화 (5-7h)
    ↓
Phase 5: 오프라인 우선 (3-4h)
    ↓
Phase 9: 성능 최적화 (3-4h)
```

**총 예상 시간**: 11-15시간

### Parallel Track (독립적)
```
Phase 6: 의존성 관리 (4-5h)
Phase 7: Git 이벤트 (2-3h)
Phase 8: Reflexion (5-6h)
Phase 10: UX 개선 (2-3h)
```

---

## 5. Reserved 테이블 활성화 순서

### Tier 1: Git 워크플로우 (Phase 4)
- [x] project_config (활성화됨)
- [ ] commits
- [ ] pull_requests

### Tier 2: 오프라인 지원 (Phase 5)
- [ ] sync_queue

### Tier 3: 의존성 & 이벤트 (Phase 6-7)
- [ ] task_dependencies
- [ ] git_events

### Tier 4: AI & 학습 (Phase 8)
- [ ] estimation_accuracy
- [ ] episodic_memory

### Tier 5: 캐싱 & 기타 (Phase 9-10)
- [ ] code_analysis_cache
- [ ] session_summaries
- [ ] releases

---

## 6. 테스트 전략

### 목표 커버리지: 85%+

**현재**: 81%
**추가 예상 테스트**: ~180개

| Phase | 테스트 수 | 누적 |
|-------|----------|------|
| 현재 | 526 | 526 |
| Phase 4 | +70 | 596 |
| Phase 5 | +35 | 631 |
| Phase 6 | +30 | 661 |
| Phase 7 | +25 | 686 |
| Phase 8 | +20 | 706 |

**목표**: 700+ 테스트

---

## 7. 릴리스 계획

### v1.1.0 (Phase 4 완료)
- Git 추적 강화
- commits, pull_requests 테이블
- 7개 MCP 도구 추가

**예상 일정**: 2-3일

### v1.2.0 (Phase 5 완료)
- 오프라인 우선
- sync_queue 구현
- 자동 재시도

**예상 일정**: 1-2일

### v1.3.0 (Phase 6-7 완료)
- 의존성 관리
- Git 이벤트 추적

**예상 일정**: 3-4일

### v2.0.0 (Phase 8-10 완료)
- Reflexion 강화
- 성능 최적화
- UX 개선

**예상 일정**: 4-5일

---

## 8. 성공 지표

### 기술 지표
- [ ] 700+ 테스트 통과
- [ ] 85%+ 커버리지
- [ ] 0 TypeScript 에러
- [ ] 0 보안 취약점
- [ ] < 100ms 평균 응답 시간

### 기능 지표
- [ ] 10개 Reserved 테이블 중 7개 활성화
- [ ] 35+ MCP 도구 (현재 29개)
- [ ] 완전한 Git 워크플로우 지원
- [ ] 오프라인 우선 아키텍처

### 품질 지표
- [ ] 포괄적인 문서화
- [ ] E2E 테스트 자동화
- [ ] CI/CD 파이프라인
- [ ] 성능 벤치마크

---

## 9. 리스크 & 완화 전략

### 리스크 1: 복잡도 증가
**완화**:
- 단계적 구현
- 충분한 테스트
- 리팩토링 우선

### 리스크 2: 성능 저하
**완화**:
- 벤치마크 선행
- 쿼리 최적화
- 캐싱 전략

### 리스크 3: 하위 호환성
**완화**:
- 마이그레이션 스크립트
- 버전 관리
- Deprecation 경고

---

## 10. 다음 작업

### 즉시 시작 가능 (Phase 4)
1. CommitRepository 구현
2. pm_commit_* 도구 3개 추가
3. 자동 커밋 기록 훅
4. 테스트 추가

### 준비 작업
- [ ] LEVEL_3 계획 검토 및 승인
- [ ] Phase 4 브랜치 생성
- [ ] 마일스톤 설정

---

**문서 버전**: 1.0.0
**마지막 업데이트**: 2025-01-14
**다음 검토**: Phase 4 완료 시
