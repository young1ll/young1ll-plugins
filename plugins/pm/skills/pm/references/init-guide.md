# Project Init Guide

Claude가 프로젝트 문서 체계를 초기화하는 상세 프로세스.

## 코드베이스 분석 Flow

### Step 1: 프로젝트 스캔

```bash
# 확인할 파일들
package.json          # Node.js 의존성, 스크립트
pyproject.toml        # Python 의존성, 도구 설정
Cargo.toml            # Rust 프로젝트
go.mod                # Go 모듈
pom.xml / build.gradle # Java 프로젝트

# 디렉토리 구조
src/, lib/, app/      # 소스 코드
models/, ml/          # ML 모델 관련
data/, datasets/      # 데이터 관련
experiments/          # 실험 관련
tests/, __tests__/    # 테스트
docs/                 # 기존 문서
migrations/           # DB 마이그레이션
```

### Step 2: 특성 추론 매트릭스

| 발견 항목 | 추론 | 제안 문서 |
|----------|------|----------|
| pytorch, tensorflow, wandb | ML 프로젝트 | experiments, metrics |
| experiments/ 디렉토리 | 실험 관리 필요 | experiments |
| models/ 디렉토리 | 모델 아키텍처 관리 | architecture |
| data/, datasets/ | 데이터 파이프라인 | data_schema |
| entities/, models/ (ORM) | 도메인 모델링 | domain_model |
| migrations/ | 스키마 변경 추적 | domain_model, decisions |
| api/, routes/ | API 서버 | api_spec |
| openapi.yaml, swagger | API 문서화 | api_spec |
| fastapi, nestjs, express | 백엔드 서비스 | api_spec, architecture |
| react, vue, next | 프론트엔드 | architecture, components |
| docker, k8s | 인프라 | architecture, deployment |
| .github/workflows | CI/CD | architecture |

### Step 3: 문서 구조 제안

```
[분석 요약]
- 스택: Python, FastAPI, PyTorch
- 주요 관심사: ML 실험, API 서빙
- 기존 구조: experiments/, models/, data/

[제안하는 core_docs]
vision: MANIFESTO.md           # 프로젝트 비전
progress: MILESTONES.md        # 진행 추적
architecture: docs/ARCH.md     # 모델 + 서빙 구조
experiments: docs/EXP.md       # 실험 로그
data_schema: docs/DATA.md      # 데이터 명세
metrics: docs/METRICS.md       # 평가 지표
api_spec: docs/API.md          # 서빙 API

이 구조로 진행할까요? 추가/제거할 문서가 있나요?
```

### Step 4: 확인 및 생성

사용자 확인 후:
1. PROJECT.yaml 생성
2. 핵심 문서 템플릿 생성
3. plans/, reports/ 디렉토리 생성

## 대화형 정의 Flow

### 질문 템플릿

```
1. 프로젝트 개요
   "이 프로젝트의 주요 목표와 산출물은 무엇인가요?"

2. 추적 대상
   "어떤 종류의 결정/변경사항을 기록해야 하나요?"
   예시: 실험 결과, 아키텍처 변경, API 변경, 데이터 스키마

3. 특수 요구사항
   "특별히 관리가 필요한 영역이 있나요?"
   예시: 자주 변경되는 스키마, 복잡한 알고리즘, 외부 연동

4. 기존 패턴
   "현재 사용 중인 문서화 방식이 있나요?"
   예시: README에 모두 기록, 별도 문서 없음, wiki 사용
```

### 답변 → 문서 매핑

| 답변 키워드 | 제안 문서 |
|------------|----------|
| 실험, 하이퍼파라미터, 모델 버전 | experiments |
| 성능, 정확도, 벤치마크 | metrics |
| 데이터, 스키마, 전처리 | data_schema |
| API, 엔드포인트, REST | api_spec |
| 엔티티, 관계, 도메인 | domain_model |
| 구조, 아키텍처, 파이프라인 | architecture |
| 결정, 선택, 이유 | decisions |
| 알고리즘, 이론, 수학 | theory |

## 문서 역할 선택 가이드

### 필수 (모든 프로젝트)

```yaml
core_docs:
  vision: MANIFESTO.md      # WHY: 존재 이유
  progress: MILESTONES.md   # WHAT: 목표와 진행
```

### ML/AI 프로젝트 추가 고려

```yaml
  experiments: docs/EXPERIMENTS.md  # 실험 관리
  metrics: docs/METRICS.md          # 평가 체계
  architecture: docs/ARCHITECTURE.md # 모델 구조
  data_schema: docs/DATA.md         # 데이터 명세
  theory: docs/THEORY.md            # 이론적 배경 (필요시)
```

### 백엔드 서비스 추가 고려

```yaml
  domain_model: docs/MODEL.md       # 엔티티/관계
  api_spec: docs/API.md             # API 명세
  architecture: docs/ARCHITECTURE.md # 시스템 구조
  decisions: docs/DECISIONS.md      # ADR
```

### 라이브러리 추가 고려

```yaml
  api_spec: docs/API.md             # 공개 API
  decisions: docs/DECISIONS.md      # 설계 결정
  architecture: docs/ARCHITECTURE.md # 내부 구조
```

## Init 후 검증

```bash
# 생성된 파일 확인
./scripts/validate-docs.sh

# 출력 예시
✓ PROJECT.yaml
✓ MANIFESTO.md
✓ MILESTONES.md
✓ docs/ARCHITECTURE.md
✗ docs/EXPERIMENTS.md (missing)
```

## 점진적 추가

프로젝트 진행 중 새 문서가 필요하면:

```yaml
# PROJECT.yaml에 추가
core_docs:
  ...existing...
  new_concern: docs/NEW_DOC.md  # 새로 추가
```

Claude는 다음 작업부터 이 문서를 참조/관리한다.
