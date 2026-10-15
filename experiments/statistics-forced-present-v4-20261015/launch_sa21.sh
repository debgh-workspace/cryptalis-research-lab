#!/bin/bash
# REVIEW SOURCE ONLY. This file was prepared, not launched.
# Coordinator must verify this file, scope_guard.sh, and ANCHORS.sha256 against
# independent external digests before invoking this exact one-operation vector.
set -uo pipefail
BASE=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable
P=$BASE/experiments/statistics-forced-present-v4-20261015
O=$BASE/experiments/s24-statistics-diagnostic-v4-20261014
S=$BASE/candidate-s24-statistics-diagnostic-v4-20261014
C=$BASE/candidate-statistics-forced-present-v4-20261015
E=$BASE/evidence/statistics-forced-present-v4-sa21-20261015
CAP=$BASE/evidence/statistics-forced-present-v4-sa21-packet-20261015
GUARD=$P/scope_guard.sh
GUARD_SHA256=a82f663c2bb90d1ac799f8f83105d6d8a74009c33758d8764015668ff41d5620
if [[ $# != 3 || "$1" != --coordinator-selected-sa21 || "$2" != --anchors-sha256 || ! "$3" =~ ^[0-9a-f]{64}$ ]]; then
  printf 'HOLD: explicit coordinator selection and independent anchor digest required.\n' >&2; exit 64
fi
ANCHOR_DIGEST=$3
# These fixed parents are admitted before the first capture write. Later actions
# repeat full parent admission locally and do not depend on this initial check.
for parent in /workspace /workspace/scratch /workspace/scratch/cb28ee9f5f4a "$BASE" "$BASE/evidence"; do
  [[ -d "$parent" && ! -L "$parent" ]] || { printf 'HOLD: invalid capture parent.\n' >&2; exit 73; }
done
cd "$BASE" || exit 70
# Metadata-only freshness check precedes any write. Failure leaves both targets absent/untouched.
if [[ -e "$E" || -L "$E" || -e "$CAP" || -L "$CAP" || ! -d "$BASE/evidence" || -L "$BASE/evidence" ]]; then
  printf 'HOLD: destination collision or invalid evidence parent; no launch.\n' >&2; exit 73
fi
if ! mkdir -- "$CAP"; then printf 'HOLD: exclusive capture creation failed; no launch.\n' >&2; exit 73; fi
mkdir -- "$CAP/actions" || exit 73
printf 'Both fixed evidence destinations were absent immediately before exclusive capture creation.\n' > "$CAP/actions/before.freshness.stdout" || { capture_rc=$?; printf 'HOLD: initial status capture failed (exit=%s).\n' "$capture_rc" >&2; exit "$capture_rc"; }
: > "$CAP/actions/before.freshness.stderr" || { capture_rc=$?; printf 'HOLD: initial status capture failed (exit=%s).\n' "$capture_rc" >&2; exit "$capture_rc"; }
printf '{"phase":"before","action":"freshness","exit_code":0,"stdout":"actions/before.freshness.stdout","stderr":"actions/before.freshness.stderr"}\n' > "$CAP/action-status.jsonl" || { capture_rc=$?; printf 'HOLD: initial status capture failed (exit=%s).\n' "$capture_rc" >&2; exit "$capture_rc"; }
runner_rc=null
interrupted=false
post_started=false
post_failures=0
before_failures=0
run_action() {
  local phase=$1 label=$2 rc log_rc
  shift 2
  admit_output "$CAP" "actions/$phase.$label.stdout" || return 2
  admit_output "$CAP" "actions/$phase.$label.stderr" || return 2
  admit_regular "$CAP" action-status.jsonl || return 2
  "$@" > "$CAP/actions/$phase.$label.stdout" 2> "$CAP/actions/$phase.$label.stderr"
  rc=$?
  jq -cn --arg phase "$phase" --arg action "$label" --argjson code "$rc" --arg out "actions/$phase.$label.stdout" --arg err "actions/$phase.$label.stderr" \
    '{phase:$phase,action:$action,exit_code:$code,stdout:$out,stderr:$err}' >> "$CAP/action-status.jsonl"
  log_rc=$?
  if [[ "$log_rc" -ne 0 ]]; then
    printf 'HOLD: action-status capture failed for %s/%s (action_exit=%s status_exit=%s).\n' "$phase" "$label" "$rc" "$log_rc" >&2
    # Preserve a primary action failure; a logging-only failure also stops the caller.
    [[ "$rc" -eq 0 ]] || return "$rc"
    return "$log_rc"
  fi
  return "$rc"
}
safe_name() {
  local rel=$1
  [[ "$rel" =~ ^[A-Za-z0-9_./-]+$ && "$rel" != /* && "$rel" != */ ]] || return 2
  case "/$rel/" in *'/../'*|*'/./'*|*'//'*|*'/__pycache__/'*|*'/.pytest_cache/'*|*'/.git/'*|*'/.env/'*|*'.pyc/'*|*'.pyo/'*|*'/package-origin.json/'*|*'/postgres-start.json/'*|*'/postgres-stop.json/'*|*'/readiness.json/'*|*'/tests.json/'*|*'/credentials/'*) return 2;; esac
}
admit_directory() {
  local absolute=$1 cur= part
  local -a components
  [[ "$absolute" == /* && "$absolute" != *//* ]] || return 2
  IFS=/ read -r -a components <<< "${absolute#/}"
  for part in "${components[@]}"; do
    [[ -n "$part" && "$part" != . && "$part" != .. ]] || return 2
    cur="$cur/$part"
    [[ -d "$cur" && ! -L "$cur" ]] || return 2
  done
}
admit_regular() {
  local root=$1 rel=$2 target
  safe_name "$rel" || return 2
  admit_directory "$root" || return 2
  target="$root/$rel"
  admit_directory "${target%/*}" || return 2
  [[ -f "$target" && ! -L "$target" && $(stat -c %h -- "$target") == 1 ]] || return 2
}
admit_output() {
  local root=$1 rel=$2 target
  safe_name "$rel" || return 2
  admit_directory "$root" || return 2
  target="$root/$rel"
  admit_directory "${target%/*}" || return 2
  if [[ -e "$target" || -L "$target" ]]; then admit_regular "$root" "$rel" || return 2; fi
}
guard_action() {
  local actual
  admit_regular "$P" scope_guard.sh || return 2
  actual=$(sha256sum -- "$GUARD"); actual=${actual%% *}
  [[ "$actual" == "$GUARD_SHA256" ]] || { printf "HOLD: validator source drift.\n" >&2; return 2; }
  bash "$GUARD" "$@"
}
queue_idle() {
  local fd
  admit_regular "$BASE/runtime" lab-session.lock || return 2
  exec {fd}<"$BASE/runtime/lab-session.lock" || return 2
  flock -n "$fd" || { exec {fd}<&-; return 75; }
  flock -u "$fd" || { exec {fd}<&-; return 2; }
  exec {fd}<&-
  printf 'Nonblocking existing queue lock was idle. Wrapper must reacquire it; a race still fails closed.\n'
}
admit_named_source() {
  local source=$1 list=$2 destination=$3 scope count rel
  # Each capture action selects its own exact source/list/destination tuple.
  case "$source|$list|$destination" in
    "$S|$P/CANDIDATE_PATHS.txt|$CAP/original-source") scope=original-source; count=215;;
    "$C|$P/CANDIDATE_PATHS.txt|$CAP/derivative-source") scope=derivative-source; count=215;;
    "$O|$P/ORIGINAL_AUTHORED_PATHS.txt|$CAP/original-packet") scope=original-packet; count=38;;
    "$P|$P/PACKET_PATHS.txt|$CAP/mutation-packet") scope=overlay; count=69;;
    *) return 2;;
  esac
  # This independent action does not rely on an earlier inventory result.
  guard_action "$scope" "$ANCHOR_DIGEST" || return 2
  admit_regular "$P" "${list#"$P/"}" || return 2
  mapfile -t NAMED_PATHS < "$list"
  [[ ${#NAMED_PATHS[@]} -eq "$count" && $(printf '%s\n' "${NAMED_PATHS[@]}" | LC_ALL=C sort -u | wc -l) -eq "$count" ]] || return 2
  for rel in "${NAMED_PATHS[@]}"; do admit_regular "$source" "$rel" || return 2; done
  admit_directory "$CAP" || return 2
}
admit_named_capture() {
  local destination=$1 rel parent record type
  local -A expected=() found=() dirs=()
  admit_directory "$destination" || return 2
  for rel in "${NAMED_PATHS[@]}"; do
    admit_regular "$destination" "$rel" || return 2
    expected[$rel]=1; parent=${rel%/*}
    if [[ "$parent" != "$rel" ]]; then
      while :; do dirs[$parent]=1; [[ "$parent" == */* ]] || break; parent=${parent%/*}; done
    fi
  done
  # Complete filename/type inventory before the first comparison; no cache exceptions.
  while IFS= read -r -d '' record; do
    rel=${record%$'\t'*}; type=${record##*$'\t'}
    safe_name "$rel" || return 2
    case "$type" in
      f) [[ ${expected[$rel]+present} ]] || return 2; found[$rel]=1;;
      d) [[ ${dirs[$rel]+present} ]] || return 2;;
      *) return 2;;
    esac
  done < <(find "$destination" -mindepth 1 -printf '%P\t%y\0' || printf 'FIND_FAILED\t!\0')
  [[ ${#found[@]} -eq ${#NAMED_PATHS[@]} ]] || return 2
}
copy_named() {
  local source=$1 list=$2 destination=$3 rel target
  admit_named_source "$source" "$list" "$destination" || return 2
  [[ ! -e "$destination" && ! -L "$destination" ]] || return 2
  mkdir -- "$destination" || return 2
  for rel in "${NAMED_PATHS[@]}"; do
    target=$destination/$rel
    mkdir -p -- "${target%/*}" || return 2
    admit_regular "$source" "$rel" || return 2
    admit_output "$destination" "$rel" || return 2
    cp -- "$source/$rel" "$target" || return 2
  done
  admit_named_capture "$destination" || return 2
  for rel in "${NAMED_PATHS[@]}"; do
    admit_regular "$source" "$rel" || return 2
    admit_regular "$destination" "$rel" || return 2
    cmp -- "$source/$rel" "$destination/$rel" || return 2
    printf 'CAPTURED_AND_EQUAL %s\n' "$rel"
  done
}
compare_named() {
  local source=$1 list=$2 destination=$3 rel
  admit_named_source "$source" "$list" "$destination" || return 2
  admit_named_capture "$destination" || return 2
  for rel in "${NAMED_PATHS[@]}"; do
    admit_regular "$source" "$rel" || return 2
    admit_regular "$destination" "$rel" || return 2
    cmp -- "$source/$rel" "$destination/$rel" || return 2
    printf 'CAPTURE_EQUAL %s\n' "$rel"
  done
}
capture_wrapper_argv() {
  # Admit this output locally; preserve every array element as data after --.
  admit_output "$CAP" outer-wrapper-argv.json || return 2
  jq -n --args '$ARGS.positional' -- "${ARGV[@]}" > "$CAP/outer-wrapper-argv.json"
}
capture_terminal() {
  admit_regular "$CAP" wrapper.stdout || return 2
  admit_regular "$CAP" wrapper.stderr || return 2
  admit_output "$CAP" terminal.log || return 2
  cat -- "$CAP/wrapper.stdout" "$CAP/wrapper.stderr" > "$CAP/terminal.log"
}
check_safe_stop() {
  admit_regular "$CAP" wrapper.stdout || return 2
  admit_regular "$E" postgres-stop.log || return 2
  [[ $(grep -c '^postgres-stop exit 0$' "$CAP/wrapper.stdout") -eq 1 ]] || return 2
  [[ $(grep -c '^postgres-stop exit ' "$CAP/wrapper.stdout") -eq 1 ]] || return 2
  grep -F 'server stopped' "$E/postgres-stop.log"
}
check_safe_corpus() {
  admit_regular "$E" candidate-corpus-isolation.json || return 2
  jq -e '.primary_receipts_restored == true and .errors == []' "$E/candidate-corpus-isolation.json"
}
after_all() {
  [[ "$post_started" == false ]] || return
  post_started=true
  # No short-circuit chain: each final check keeps its own output and exit.
  run_action after terminal-capture capture_terminal || post_failures=$((post_failures+1))
  run_action after direct-anchors guard_action anchors "$ANCHOR_DIGEST" || post_failures=$((post_failures+1))
  for scope in original-source derivative-source original-packet frozen-packet overlay; do
    run_action after "inventory-$scope" guard_action "$scope" "$ANCHOR_DIGEST" || post_failures=$((post_failures+1))
  done
  run_action after all-pins guard_action pins "$ANCHOR_DIGEST" || post_failures=$((post_failures+1))
  run_action after original-safe-pins guard_action original-safe-pins "$ANCHOR_DIGEST" || post_failures=$((post_failures+1))
  run_action after original-source-capture compare_named "$S" "$P/CANDIDATE_PATHS.txt" "$CAP/original-source" || post_failures=$((post_failures+1))
  run_action after derivative-source-capture compare_named "$C" "$P/CANDIDATE_PATHS.txt" "$CAP/derivative-source" || post_failures=$((post_failures+1))
  run_action after original-packet-capture compare_named "$O" "$P/ORIGINAL_AUTHORED_PATHS.txt" "$CAP/original-packet" || post_failures=$((post_failures+1))
  run_action after overlay-capture compare_named "$P" "$P/PACKET_PATHS.txt" "$CAP/mutation-packet" || post_failures=$((post_failures+1))
  run_action after explicit-safe-stop check_safe_stop || post_failures=$((post_failures+1))
  run_action after safe-corpus-status check_safe_corpus || post_failures=$((post_failures+1))
  admit_output "$CAP" filesystem-status.json || {
    post_failures=$((post_failures+1))
    printf 'HOLD: filesystem-status output admission failed (exit=2).\n' >&2
    return 2
  }
  jq -n --argjson runner "$runner_rc" --argjson interrupted "$interrupted" --argjson before "$before_failures" --argjson after "$post_failures" \
    '{status:"STOP_FOR_INDEPENDENT_ACTUAL_RESULT_REVIEW",runner_exit:$runner,interrupted:$interrupted,before_failures:$before,after_failures:$after,mutation_accepted:false,raw_phase_payloads_inspected:false}' > "$CAP/filesystem-status.json"
  local status_rc=$?
  if [[ "$status_rc" -ne 0 ]]; then
    post_failures=$((post_failures+1))
    printf 'HOLD: filesystem-status capture failed (exit=%s).\n' "$status_rc" >&2
    return "$status_rc"
  fi
}
finish() {
  local rc=$?
  trap - EXIT
  after_all
  # A post-run capture failure cannot normalize or replace a real runner failure.
  if [[ "$runner_rc" != null && "$runner_rc" -ne 0 ]]; then exit "$runner_rc"; fi
  if [[ "$rc" -eq 0 && "$post_failures" -ne 0 ]]; then exit 2; fi
  exit "$rc"
}
interrupt() { interrupted=true; exit 130; }
trap finish EXIT
trap interrupt INT TERM HUP
run_action before direct-anchors guard_action anchors "$ANCHOR_DIGEST" || { before_failures=$((before_failures+1)); exit 2; }
for scope in original-source derivative-source original-packet frozen-packet overlay; do
  run_action before "inventory-$scope" guard_action "$scope" "$ANCHOR_DIGEST" || before_failures=$((before_failures+1))
done
run_action before all-pins guard_action pins "$ANCHOR_DIGEST" || before_failures=$((before_failures+1))
run_action before original-safe-pins guard_action original-safe-pins "$ANCHOR_DIGEST" || before_failures=$((before_failures+1))
[[ "$before_failures" -eq 0 ]] || exit 2
run_action before original-source-capture copy_named "$S" "$P/CANDIDATE_PATHS.txt" "$CAP/original-source" || { before_failures=$((before_failures+1)); exit 2; }
run_action before derivative-source-capture copy_named "$C" "$P/CANDIDATE_PATHS.txt" "$CAP/derivative-source" || { before_failures=$((before_failures+1)); exit 2; }
run_action before original-packet-capture copy_named "$O" "$P/ORIGINAL_AUTHORED_PATHS.txt" "$CAP/original-packet" || { before_failures=$((before_failures+1)); exit 2; }
run_action before overlay-capture copy_named "$P" "$P/PACKET_PATHS.txt" "$CAP/mutation-packet" || { before_failures=$((before_failures+1)); exit 2; }
# Recheck exact inventories and pins after capture and immediately before collection.
for scope in original-source derivative-source original-packet frozen-packet overlay; do
  run_action before "final-inventory-$scope" guard_action "$scope" "$ANCHOR_DIGEST" || before_failures=$((before_failures+1))
done
run_action before final-all-pins guard_action pins "$ANCHOR_DIGEST" || before_failures=$((before_failures+1))
[[ "$before_failures" -eq 0 ]] || exit 2
run_action before idle-queue queue_idle || { before_failures=$((before_failures+1)); exit 75; }
[[ ! -e "$E" && ! -L "$E" ]] || { before_failures=$((before_failures+1)); exit 73; }
# Exact unchanged wrapper route; no eval, substitutions, retry or added pytest flags.
ARGV=(
  "$BASE/release-lab/s23-installed-20261014/sa21/bin/python"
  "$BASE/candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py"
  --candidate-root "$C"
  --python "$BASE/release-lab/s23-installed-20261014/sa21/bin/python"
  --evidence "$E"
  -- -q -o "pythonpath=$C/tests" "$O"
  -k test_exact_aggregate_and_remedy_contract --tb=short
)
for rel in outer-wrapper-argv.json wrapper.stdout wrapper.stderr wrapper-exit.txt; do
  admit_output "$CAP" "$rel" || { before_failures=$((before_failures+1)); exit 2; }
done
admit_regular "$CAP" action-status.jsonl || { before_failures=$((before_failures+1)); exit 2; }
if run_action before wrapper-argv capture_wrapper_argv; then
  :
else
  argv_capture_rc=$?
  before_failures=$((before_failures+1))
  exit "$argv_capture_rc"
fi
"${ARGV[@]}" > "$CAP/wrapper.stdout" 2> "$CAP/wrapper.stderr"
runner_rc=$?
admit_output "$CAP" wrapper-exit.txt || exit 2
printf '%s\n' "$runner_rc" > "$CAP/wrapper-exit.txt" || { post_failures=$((post_failures+1)); exit 2; }
# Keep both streams separately; the independent terminal-capture action below
# admits both complete paths before concatenating stdout then stderr.
admit_regular "$CAP" action-status.jsonl || exit 2
jq -cn --argjson code "$runner_rc" '{phase:"runner",action:"exact-wrapper",exit_code:$code,stdout:"wrapper.stdout",stderr:"wrapper.stderr",terminal:"terminal.log"}' >> "$CAP/action-status.jsonl"
runner_log_rc=$?
if [[ "$runner_log_rc" -ne 0 ]]; then
  post_failures=$((post_failures+1))
  printf 'HOLD: runner-status capture failed (runner_exit=%s status_exit=%s).\n' "$runner_rc" "$runner_log_rc" >&2
fi
after_all
# Preserve the actual nonzero runner result; expected exit 1 is never normalized.
if [[ "$runner_rc" -ne 0 ]]; then exit "$runner_rc"; fi
[[ "$post_failures" -eq 0 ]] || exit 2
exit 0
