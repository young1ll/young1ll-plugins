#!/bin/bash
# yaml-parser.sh - 순수 bash YAML 파서
# PROJECT.yaml 파싱용 간단한 구현

# ============================================================
# YAML 값 읽기
# ============================================================

# 단일 값 읽기
# Usage: yaml_get "key" "file.yaml"
yaml_get() {
  local key="$1"
  local file="${2:-PROJECT.yaml}"

  if [ ! -f "$file" ]; then
    return 1
  fi

  grep "^${key}:" "$file" | sed "s/${key}:[[:space:]]*//" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//'
}

# 중첩 값 읽기 (한 단계)
# Usage: yaml_get_nested "parent" "child" "file.yaml"
yaml_get_nested() {
  local parent="$1"
  local child="$2"
  local file="${3:-PROJECT.yaml}"

  if [ ! -f "$file" ]; then
    return 1
  fi

  # parent 섹션 내에서 child 찾기
  awk -v parent="$parent" -v child="$child" '
    BEGIN { in_section = 0 }
    /^[a-zA-Z_]+:/ {
      if ($0 ~ "^" parent ":") {
        in_section = 1
        next
      } else if (in_section) {
        in_section = 0
      }
    }
    in_section && /^[[:space:]]+/ {
      gsub(/^[[:space:]]+/, "")
      if ($0 ~ "^" child ":") {
        sub(child ":[[:space:]]*", "")
        print
        exit
      }
    }
  ' "$file"
}

# ============================================================
# core_docs 파싱
# ============================================================

# core_docs의 모든 키-값 쌍 출력
# Usage: yaml_get_core_docs "file.yaml"
# Output: key:path (한 줄씩)
yaml_get_core_docs() {
  local file="${1:-PROJECT.yaml}"

  if [ ! -f "$file" ]; then
    return 1
  fi

  awk '
    BEGIN { in_core_docs = 0 }
    /^core_docs:/ { in_core_docs = 1; next }
    /^[a-zA-Z_]+:/ && !/^[[:space:]]/ { in_core_docs = 0 }
    in_core_docs && /^[[:space:]]+[a-zA-Z_]+:/ {
      gsub(/^[[:space:]]+/, "")
      gsub(/:[[:space:]]+/, ":")
      gsub(/#.*$/, "")  # 주석 제거
      gsub(/[[:space:]]*$/, "")
      if (length > 0) print
    }
  ' "$file"
}

# core_docs에서 특정 역할의 경로 가져오기
# Usage: yaml_get_core_doc "vision" "file.yaml"
yaml_get_core_doc() {
  local role="$1"
  local file="${2:-PROJECT.yaml}"

  yaml_get_core_docs "$file" | grep "^${role}:" | cut -d':' -f2
}

# ============================================================
# 리스트 파싱
# ============================================================

# 리스트 형태의 값 읽기 (인라인: [a, b, c])
# Usage: yaml_get_list "key" "file.yaml"
yaml_get_list() {
  local key="$1"
  local file="${2:-PROJECT.yaml}"

  local value
  value=$(yaml_get "$key" "$file")

  # [a, b, c] 형태 파싱
  if [[ "$value" =~ ^\[.*\]$ ]]; then
    echo "$value" | sed 's/^\[//' | sed 's/\]$//' | tr ',' '\n' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//'
  fi
}

# ============================================================
# meta 섹션 파싱
# ============================================================

# meta 섹션의 값 읽기
# Usage: yaml_get_meta "stack" "file.yaml"
yaml_get_meta() {
  local key="$1"
  local file="${2:-PROJECT.yaml}"

  yaml_get_nested "meta" "$key" "$file"
}

# ============================================================
# 프로젝트 정보
# ============================================================

# 프로젝트 이름
yaml_project_name() {
  yaml_get "name" "${1:-PROJECT.yaml}"
}

# 프로젝트 설명
yaml_project_description() {
  yaml_get "description" "${1:-PROJECT.yaml}"
}

# plans 디렉토리
yaml_plans_dir() {
  local dir
  dir=$(yaml_get "plans_dir" "${1:-PROJECT.yaml}")
  echo "${dir:-docs/plans}"
}

# reports 디렉토리
yaml_reports_dir() {
  local dir
  dir=$(yaml_get "reports_dir" "${1:-PROJECT.yaml}")
  echo "${dir:-docs/reports}"
}

# ============================================================
# ignore 섹션 파싱
# ============================================================

# ignore.files 리스트 가져오기
# Usage: yaml_get_ignore_files "file.yaml"
# Output: 패턴 (한 줄씩)
yaml_get_ignore_files() {
  local file="${1:-PROJECT.yaml}"

  if [ ! -f "$file" ]; then
    return 1
  fi

  awk '
    BEGIN { in_ignore = 0; in_files = 0 }
    /^ignore:/ { in_ignore = 1; next }
    /^[a-z_]+:/ && !/^[[:space:]]/ { in_ignore = 0; in_files = 0 }
    in_ignore && /^[[:space:]]+files:/ { in_files = 1; next }
    in_ignore && /^[[:space:]]+[a-z_]+:/ && !/^[[:space:]]+files:/ { in_files = 0 }
    in_files && /^[[:space:]]+-[[:space:]]/ {
      gsub(/^[[:space:]]+-[[:space:]]*/, "")
      gsub(/^"/, "")
      gsub(/"$/, "")
      gsub(/[[:space:]]*#.*$/, "")
      gsub(/[[:space:]]*$/, "")
      if (length > 0) print
    }
  ' "$file"
}

# ignore.rules 리스트 가져오기
# Usage: yaml_get_ignore_rules "file.yaml"
# Output: 규칙 이름 (한 줄씩)
yaml_get_ignore_rules() {
  local file="${1:-PROJECT.yaml}"

  if [ ! -f "$file" ]; then
    return 1
  fi

  awk '
    BEGIN { in_ignore = 0; in_rules = 0 }
    /^ignore:/ { in_ignore = 1; next }
    /^[a-z_]+:/ && !/^[[:space:]]/ { in_ignore = 0; in_rules = 0 }
    in_ignore && /^[[:space:]]+rules:/ { in_rules = 1; next }
    in_ignore && /^[[:space:]]+[a-z_]+:/ && !/^[[:space:]]+rules:/ { in_rules = 0 }
    in_rules && /^[[:space:]]+-[[:space:]]/ {
      gsub(/^[[:space:]]+-[[:space:]]*/, "")
      gsub(/^"/, "")
      gsub(/"$/, "")
      gsub(/[[:space:]]*#.*$/, "")
      gsub(/[[:space:]]*$/, "")
      if (length > 0) print
    }
  ' "$file"
}

# 파일이 ignore 패턴에 매칭되는지 확인
# Usage: is_ignored_file "path/to/file"
# Returns: 0 if ignored, 1 if not
is_ignored_file() {
  local file="$1"
  local yaml_file="${2:-PROJECT.yaml}"
  local patterns

  patterns=$(yaml_get_ignore_files "$yaml_file")

  # 패턴이 없으면 무시하지 않음
  [ -z "$patterns" ] && return 1

  while IFS= read -r pattern; do
    [ -z "$pattern" ] && continue
    # glob 패턴 매칭 (bash extended globbing)
    # shellcheck disable=SC2053
    if [[ "$file" == $pattern ]]; then
      return 0
    fi
    # basename으로도 매칭 시도
    if [[ "$(basename "$file")" == $pattern ]]; then
      return 0
    fi
  done <<< "$patterns"

  return 1
}

# 규칙이 ignore 목록에 있는지 확인
# Usage: is_ignored_rule "rule_name"
# Returns: 0 if ignored, 1 if not
is_ignored_rule() {
  local rule="$1"
  local yaml_file="${2:-PROJECT.yaml}"

  yaml_get_ignore_rules "$yaml_file" | grep -qx "$rule"
}

# ============================================================
# 검증
# ============================================================

# 필수 필드 존재 확인
yaml_validate_required() {
  local file="${1:-PROJECT.yaml}"
  local errors=0

  if [ ! -f "$file" ]; then
    echo "파일을 찾을 수 없음: $file"
    return 1
  fi

  # name 필수
  if [ -z "$(yaml_get 'name' "$file")" ]; then
    echo "필수 필드 누락: name"
    errors=$((errors + 1))
  fi

  # core_docs 필수
  local core_docs
  core_docs=$(yaml_get_core_docs "$file")
  if [ -z "$core_docs" ]; then
    echo "필수 필드 누락: core_docs"
    errors=$((errors + 1))
  fi

  # vision, progress 필수
  if [ -z "$(yaml_get_core_doc 'vision' "$file")" ]; then
    echo "필수 core_doc 누락: vision"
    errors=$((errors + 1))
  fi

  if [ -z "$(yaml_get_core_doc 'progress' "$file")" ]; then
    echo "필수 core_doc 누락: progress"
    errors=$((errors + 1))
  fi

  return $errors
}
