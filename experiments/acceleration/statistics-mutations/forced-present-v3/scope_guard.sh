#!/bin/bash
# Source/data-only scope and pin validator. It never imports or runs Python.
set -euo pipefail
BASE=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable
P=$BASE/experiments/statistics-forced-present-v3-20261015
O=$BASE/experiments/s24-statistics-diagnostic-v4-20261014
S=$BASE/candidate-s24-statistics-diagnostic-v4-20261014
C=$BASE/candidate-statistics-forced-present-v3-20261015
PY=/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12
cd "$BASE"
fail() { printf 'SCOPE_HOLD: %s\n' "$*" >&2; exit 2; }
name_ok() {
  local rel=$1
  [[ "$rel" =~ ^[A-Za-z0-9_./-]+$ && "$rel" != /* && "$rel" != */ ]] || return 1
  case "/$rel/" in *'/../'*|*'/./'*|*'//'*|*'/__pycache__/'*|*'/.pytest_cache/'*|*'/.git/'*|*'/.env/'*|*'.pyc/'*|*'.pyo/'*|*'/package-origin.json/'*|*'/postgres-start.json/'*|*'/postgres-stop.json/'*|*'/readiness.json/'*|*'/tests.json/'*|*'/runtime/'*|*'/credentials/'*) return 1;; esac
}
directory() {
  local absolute=$1 cur= part
  local -a components
  [[ "$absolute" == /* && "$absolute" != *//* ]] || fail 'invalid absolute directory'
  IFS=/ read -r -a components <<< "${absolute#/}"
  for part in "${components[@]}"; do
    [[ -n "$part" && "$part" != . && "$part" != .. ]] || fail 'invalid directory component'
    cur="$cur/$part"
    [[ -d "$cur" && ! -L "$cur" ]] || fail 'non-directory or symlink parent'
  done
}
regular() {
  local root=$1 rel=$2 target
  name_ok "$rel" || fail "forbidden target name"
  directory "$root"
  target="$root/$rel"
  directory "${target%/*}"
  [[ -f "$target" && ! -L "$target" && $(stat -c %h -- "$target") == 1 ]] || fail "non-regular or linked target: $rel"
}
input_target() {
  local rel=$1
  name_ok "$rel" || fail 'forbidden input target name'
  case "$rel" in toolchain/sa20-venv/bin/python|release-lab/s23-installed-20261014/sa21/bin/python)
    directory "$BASE/${rel%/*}"
    directory "${PY%/*}"
    [[ -L "$BASE/$rel" && $(readlink -- "$BASE/$rel") == "$PY" && $(readlink -f -- "$BASE/$rel") == "$PY" && -f "$PY" && ! -L "$PY" ]] || fail "interpreter identity: $rel"
    ;;
    *) regular "$BASE" "$rel";;
  esac
}
load_list() {
  local file=$1 count=$2 rel
  regular "$P" "${file#"$P/"}"
  mapfile -t LIST < "$file"
  [[ ${#LIST[@]} -eq "$count" ]] || fail "wrong list count: $file"
  [[ $(printf '%s\n' "${LIST[@]}" | LC_ALL=C sort -u | wc -l) -eq "$count" ]] || fail 'duplicate list paths'
  for rel in "${LIST[@]}"; do name_ok "$rel" || fail 'forbidden list name'; done
}
inventory() {
  local root=$1 list=$2 count=$3 record rel type ignored=0
  load_list "$list" "$count"
  declare -A expected=() found=() dirs=()
  dirs[.]=1
  for rel in "${LIST[@]}"; do
    expected[$rel]=1; regular "$root" "$rel"
    local parent=${rel%/*}
    if [[ "$parent" != "$rel" ]]; then
      while :; do dirs[$parent]=1; [[ "$parent" == */* ]] || break; parent=${parent%/*}; done
    fi
  done
  # Filename/type enumeration only. No generated-file payload is opened.
  while IFS= read -r -d '' record; do
    rel=${record%$'\t'*}; type=${record##*$'\t'}
    [[ -n "$rel" ]] || continue
    if [[ "$type" == d && ( "$rel" == __pycache__ || "$rel" == */__pycache__ ) ]]; then
      local parent=${rel%/__pycache__}; [[ "$parent" == "$rel" ]] && parent=.
      [[ ${dirs[$parent]+present} ]] || fail 'cache directory outside authored parents'
      continue
    fi
    if [[ "$type" == f && ( "$rel" == __pycache__/*.pyc || "$rel" == */__pycache__/*.pyc ) && "$rel" =~ ^[A-Za-z0-9_./-]+$ ]]; then
      ignored=$((ignored+1)); printf 'CACHE_NAME_EXCLUDED %s\n' "$rel"; continue
    fi
    # pytest's own cache contains no authored Python and is never payload-read.
    if [[ "$rel" == .pytest_cache || "$rel" == .pytest_cache/* ]]; then
      [[ "$type" == f || "$type" == d ]] || fail 'nonordinary pytest cache entry'
      [[ "$rel" != *.py && "$rel" != *.pyc && "$rel" != *.pyo ]] || fail 'executable payload in pytest cache'
      printf 'PYTEST_CACHE_NAME_EXCLUDED %s\n' "$rel"; continue
    fi
    name_ok "$rel" || fail 'invalid observed path'
    case "$type" in
      f) [[ ${expected[$rel]+present} ]] || fail "unlisted authored file: $rel"; found[$rel]=1;;
      d) [[ ${dirs[$rel]+present} ]] || fail "unlisted directory: $rel";;
      *) fail "unexpected path type: $rel";;
    esac
  done < <(find "$root" -mindepth 1 -printf '%P\t%y\0' || printf 'FIND_FAILED\t!\0')
  [[ ${#found[@]} -eq "$count" ]] || fail 'missing authored file'
  printf 'INVENTORY_OK %s files=%s cache_payloads_read=0 cache_filenames_excluded=%s\n' "$root" "$count" "$ignored"
}
validate_inputs() {
  regular "$P" INPUTS.sha256
  regular "$P" INPUTS_MANIFEST.json
  regular "$P" SAFE_INPUT_PATHS.txt
  mapfile -t allowed < "$P/SAFE_INPUT_PATHS.txt"
  [[ ${#allowed[@]} -eq 548 && $(printf '%s\n' "${allowed[@]}"|LC_ALL=C sort -u|wc -l) -eq 548 ]] || fail 'input allowlist count/duplicates'
  declare -A permit=() seen=()
  local rel line digest path
  for rel in "${allowed[@]}"; do input_target "$rel"; permit[$rel]=1; done
  while IFS= read -r line; do
    [[ "$line" =~ ^([0-9a-f]{64})\ \ ([A-Za-z0-9_./-]+)$ ]] || fail 'invalid hash line'
    digest=${BASH_REMATCH[1]}; path=${BASH_REMATCH[2]}
    [[ ${permit[$path]+present} && ! ${seen[$path]+present} ]] || fail 'unlisted/duplicate hash target'
    seen[$path]=1
  done < "$P/INPUTS.sha256"
  [[ ${#seen[@]} -eq ${#permit[@]} ]] || fail 'incomplete input map'
  cmp <(jq -r '.files|to_entries|sort_by(.key)[]|.value+"  "+.key' "$P/INPUTS_MANIFEST.json") <(LC_ALL=C sort -k2 "$P/INPUTS.sha256") || fail 'JSON/hash-list mismatch'
  printf 'ALL_INPUT_NAMES_TYPES_VALIDATED %s before payload hashes\n' "${#seen[@]}"
}
anchors() {
  local expected=$1 actual line rel
  [[ "$expected" =~ ^[0-9a-f]{64}$ ]] || fail 'missing independent digest'
  regular "$P" ANCHORS.sha256
  actual=$(sha256sum -- "$P/ANCHORS.sha256"); actual=${actual%% *}
  [[ "$actual" == "$expected" ]] || fail 'direct anchor drift'
  while IFS= read -r line; do
    [[ "$line" =~ ^([0-9a-f]{64})\ \ (experiments/statistics-forced-present-v3-20261015/[A-Za-z0-9_./-]+)$ ]] || fail 'invalid anchor target'
    rel=${BASH_REMATCH[2]}; regular "$BASE" "$rel"
  done < "$P/ANCHORS.sha256"
  sha256sum -c -- "$P/ANCHORS.sha256"
}
if [[ "${1-}" != anchors ]]; then anchors "${2-}"; fi
case "${1-}" in
  original-source) inventory "$S" "$P/CANDIDATE_PATHS.txt" 215;;
  derivative-source) inventory "$C" "$P/CANDIDATE_PATHS.txt" 215;;
  original-packet) inventory "$O" "$P/ORIGINAL_AUTHORED_PATHS.txt" 38;;
  frozen-packet) inventory "$P/frozen-original-packet" "$P/ORIGINAL_AUTHORED_PATHS.txt" 38;;
  overlay) inventory "$P" "$P/PACKET_PATHS.txt" 69;;
  pins) validate_inputs; sha256sum -c -- "$P/INPUTS.sha256";;
  validate-inputs) validate_inputs;;
  anchors) anchors "${2-}";;
  original-safe-pins)
    # This action is independent: an earlier inventory/pins rejection is not admission.
    # Admit both checksum maps and every original target before awk/cmp/hash reads.
    regular "$P" ORIGINAL_SAFE_INPUTS.sha256
    regular "$O" INPUTS.sha256
    load_list "$P/ORIGINAL_SAFE_INPUT_PATHS.txt" 261
    for rel in "${LIST[@]}"; do input_target "$rel"; done
    cmp <(printf '%s\n' "${LIST[@]}") <(awk '{print $2}' "$P/ORIGINAL_SAFE_INPUTS.sha256") || fail 'original safe-map mismatch'
    cmp "$P/ORIGINAL_SAFE_INPUTS.sha256" "$O/INPUTS.sha256" || fail 'original input map changed'
    sha256sum -c -- "$P/ORIGINAL_SAFE_INPUTS.sha256";;
  *) fail 'unknown scope check';;
esac
