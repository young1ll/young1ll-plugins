#!/bin/bash
# common.sh - 공통 유틸리티 함수
# POSIX 호환, macOS/Linux 크로스 플랫폼

set -e

# ============================================================
# 색상 정의 (터미널 지원 시)
# ============================================================

if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  BLUE='\033[0;34m'
  CYAN='\033[0;36m'
  BOLD='\033[1m'
  NC='\033[0m' # No Color
else
  RED=''
  GREEN=''
  YELLOW=''
  BLUE=''
  CYAN=''
  BOLD=''
  NC=''
fi

# ============================================================
# 출력 함수
# ============================================================

pm_info() {
  echo -e "${BLUE}[INFO]${NC} $*"
}

pm_success() {
  echo -e "${GREEN}[OK]${NC} $*"
}

pm_warn() {
  echo -e "${YELLOW}[WARN]${NC} $*"
}

pm_error() {
  echo -e "${RED}[ERROR]${NC} $*" >&2
}

pm_header() {
  echo ""
  echo -e "${BOLD}=== $* ===${NC}"
  echo ""
}

# ============================================================
# OS 감지
# ============================================================

detect_os() {
  case "$OSTYPE" in
    darwin*)  echo "macos" ;;
    linux*)   echo "linux" ;;
    msys*)    echo "windows" ;;
    cygwin*)  echo "windows" ;;
    *)        echo "unknown" ;;
  esac
}

OS_TYPE=$(detect_os)

# ============================================================
# 크로스 플랫폼 sed -i
# ============================================================

sed_inplace() {
  local pattern="$1"
  local file="$2"

  if [ "$OS_TYPE" = "macos" ]; then
    sed -i '' "$pattern" "$file"
  else
    sed -i "$pattern" "$file"
  fi
}

# ============================================================
# 날짜 함수
# ============================================================

get_date() {
  date +%Y-%m-%d
}

get_datetime() {
  date "+%Y-%m-%d %H:%M:%S"
}

# ============================================================
# 파일/디렉토리 유틸리티
# ============================================================

ensure_dir() {
  local dir="$1"
  if [ ! -d "$dir" ]; then
    mkdir -p "$dir"
    pm_info "디렉토리 생성: $dir"
  fi
}

file_exists() {
  [ -f "$1" ]
}

dir_exists() {
  [ -d "$1" ]
}

# ============================================================
# 문자열 유틸리티
# ============================================================

# 문자열을 안전한 파일명으로 변환
slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-_'
}

# 첫 글자 대문자
capitalize() {
  echo "$1" | sed 's/\b\(.\)/\u\1/'
}

# ============================================================
# 프로젝트 루트 탐색
# ============================================================

find_project_root() {
  local current="$PWD"
  while [ "$current" != "/" ]; do
    if [ -f "$current/PROJECT.yaml" ]; then
      echo "$current"
      return 0
    fi
    current=$(dirname "$current")
  done
  return 1
}

# ============================================================
# PROJECT.yaml 검증
# ============================================================

require_project_yaml() {
  if [ ! -f "PROJECT.yaml" ]; then
    pm_error "PROJECT.yaml을 찾을 수 없습니다"
    pm_info "'/pm init'으로 프로젝트를 초기화하세요"
    exit 1
  fi
}

# ============================================================
# 진행률 바
# ============================================================

progress_bar() {
  local current="$1"
  local total="$2"
  local width="${3:-30}"

  if [ "$total" -eq 0 ]; then
    local percent=0
  else
    local percent=$((current * 100 / total))
  fi

  local filled=$((percent * width / 100))
  local empty=$((width - filled))

  printf "["
  printf "%${filled}s" | tr ' ' '#'
  printf "%${empty}s" | tr ' ' '-'
  printf "] %d%%\n" "$percent"
}

# ============================================================
# 확인 프롬프트
# ============================================================

confirm() {
  local message="${1:-계속하시겠습니까?}"
  local default="${2:-n}"

  if [ "$default" = "y" ]; then
    local prompt="$message [Y/n]: "
  else
    local prompt="$message [y/N]: "
  fi

  read -r -p "$prompt" response
  response=${response:-$default}

  case "$response" in
    [yY][eE][sS]|[yY]) return 0 ;;
    *) return 1 ;;
  esac
}

# ============================================================
# 스크립트 디렉토리 경로
# ============================================================

get_script_dir() {
  local source="${BASH_SOURCE[0]}"
  while [ -h "$source" ]; do
    local dir="$(cd -P "$(dirname "$source")" && pwd)"
    source="$(readlink "$source")"
    [[ $source != /* ]] && source="$dir/$source"
  done
  cd -P "$(dirname "$source")" && pwd
}

# lib 디렉토리 경로
LIB_DIR="$(get_script_dir)"

# scripts 디렉토리 경로
SCRIPTS_DIR="$(dirname "$LIB_DIR")"

# skill 루트 디렉토리 경로
SKILL_ROOT="$(dirname "$SCRIPTS_DIR")"

# templates 디렉토리 경로
TEMPLATES_DIR="$SKILL_ROOT/references/templates"
