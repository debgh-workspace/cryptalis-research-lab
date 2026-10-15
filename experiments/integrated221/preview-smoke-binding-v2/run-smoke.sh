#!/bin/bash
# HELD source. Root selection requires actual source acceptance and ACL approval.
# This file does not bind or invent approval and never retries a selected run.
set -u
set -o noclobber
[ "$#" -eq 2 ] || exit 4
SELECTION_SHA=$1
PACKET_SHA=$2
[[ "$SELECTION_SHA" =~ ^[0-9a-f]{64}$ ]] || exit 4
[[ "$PACKET_SHA" =~ ^[0-9a-f]{64}$ ]] || exit 4
W=/workspace/scratch/cb28ee9f5f4a
B="$W/cryptalis-executable"
P="$B/experiments/preview-smoke-installed221-binding-v2-20261015"
M="$B/experiments/integrated221-installed-full-controls-v3-20261015"
V5="$B/experiments/preview-smoke-adapter-v5-installed221-20261015"
SOURCE="$B/candidate-cluster-retained-integrated-v2-20261015"
AUDIT="$P/run"
EVIDENCE="$B/evidence/preview-smoke-installed221-v2-sa21-20261015"
PRIVATE=/tmp/cryptalis-preview-smoke-installed221-v2-sa21-20261015
COORD="$B/repo/.venv/bin/python"
HOST=/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12
INSTALLED="$B/release-lab/integrated221-installed-20261015/sa21/bin/python"
RUNTIME_BINDING=669cb3c408144f597cc70de5d8c23295e26ba47f9c68888b1d986e431171cf54
GUARD_SHA=c135fb94da3d011a1a7fb2a97c2d6abe0f3fcde6d8909d0c7eb17dfb8c7ed8ba
ARCHIVE_SHA=87f34db5691695b71a75c203f5ddf9f3b0ae8eff3b1a0420595ad175522a7ff0
RUNTIME_GUARD_SHA=c84e168fd2f9dc5a5e8af943ea52d868f495b542ae00c2e9da47c470d391c861
FIXED=(/usr/bin/env -i "HOME=$B/runtime/home" "PATH=$B/toolchain/pg16/bin:/usr/bin:/bin" "LANG=C.UTF-8" "TZ=UTC")
cd "$W" || exit $?
umask 077
ulimit -c 0 || exit $?

admit_helper() {
  "${FIXED[@]}" "$HOST" -I -B -c '
from pathlib import Path
import hashlib, stat, sys
p=Path(sys.argv[1]); expected=sys.argv[2]
allowed={Path("/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/preview-smoke-installed221-binding-v2-20261015/admit_smoke.py"),Path("/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/preview-smoke-installed221-binding-v2-20261015/archive_smoke.py"),Path("/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/integrated221-installed-full-controls-v3-20261015/verify_runtime_binding.py")}
assert p in allowed
current=Path("/")
for part in p.parts[1:]:
    current/=part
    mode=current.lstat().st_mode
    assert stat.S_ISREG(mode) if current==p else stat.S_ISDIR(mode), str(current)
assert hashlib.sha256(p.read_bytes()).hexdigest()==expected, "HELPER_DIGEST_MISMATCH"
print("VERIFIED_HELPER",expected,str(p))
' "$1" "$2"
}

# No live cell/corpus read, DB/status, or audit creation before selection admission.
admit_helper "$P/admit_smoke.py" "$GUARD_SHA" || exit $?
"${FIXED[@]}" "$HOST" -I -B "$P/admit_smoke.py" --selection-sha256 "$SELECTION_SHA" --packet-seal-sha256 "$PACKET_SHA" --mode before || exit $?
for path in "$AUDIT" "$EVIDENCE" "$PRIVATE"; do
  [ ! -e "$path" ] && [ ! -L "$path" ] || exit 2
done
/bin/mkdir "$AUDIT" || exit $?
printf '%s\n' "$SELECTION_SHA" > "$AUDIT/selection-sha256.txt" || exit $?
printf '%s\n' "$PACKET_SHA" > "$AUDIT/packet-seal-sha256.txt" || exit $?
# A single pinned data-only producer owns metadata admission, checked copies,
# exact directory/file inventories and archived-byte verification. Its nonzero
# exit is retained and blocks all live runtime validation and database/status work.
admit_helper "$P/archive_smoke.py" "$ARCHIVE_SHA" > "$AUDIT/archive-helper.log" 2>&1 || exit $?
"${FIXED[@]}" "$HOST" -I -B "$P/archive_smoke.py" --selection-sha256 "$SELECTION_SHA" --packet-seal-sha256 "$PACKET_SHA" > "$AUDIT/archive.log" 2>&1
archive_status=$?
printf '%s\n' "$archive_status" > "$AUDIT/archive-exit.txt" || exit $?
[ "$archive_status" -eq 0 ] || exit "$archive_status"
admit_helper "$M/verify_runtime_binding.py" "$RUNTIME_GUARD_SHA" > "$AUDIT/runtime-helper-before.log" 2>&1 || exit $?
"${FIXED[@]}" "$COORD" -I -B "$M/verify_runtime_binding.py" --stage sa21 --binding-sha256 "$RUNTIME_BINDING" --mode before > "$AUDIT/runtime-before.log" 2>&1
runtime_before=$?
printf '%s\n' "$runtime_before" > "$AUDIT/runtime-before-exit.txt" || exit $?
[ "$runtime_before" -eq 0 ] || exit "$runtime_before"
# The root must already own exclusive selection after the preceding accepted task.
# This independent exact-target status proof is additional to the wrapper's lock.
"${FIXED[@]}" "$B/toolchain/pg16/bin/pg_ctl" -D "$B/runtime/data" status > "$AUDIT/pre-status.log" 2> "$AUDIT/pre-status.stderr"
pre_status=$?
printf '%s\n' "$pre_status" > "$AUDIT/pre-status-exit.txt" || exit $?
[ "$pre_status" -eq 3 ] || exit 3
# Recheck immediately before pytest's destructive --basetemp semantics become reachable.
for path in "$EVIDENCE" "$PRIVATE"; do
  [ ! -e "$path" ] && [ ! -L "$path" ] || exit 2
done
"${FIXED[@]}" "CRYPTALIS_PREVIEW_IDENTITY_FILE=$B/evidence/preview-identity-capture-v3-sa21-20261015/safe-identity.json" "CRYPTALIS_PREVIEW_IDENTITY_SHA256=089bac088003d7921f755409509afed5544741ebfee8af66faea0776fbfbb92c" "$COORD" -B "$P/launch_cold_smoke.py" --candidate-root "$SOURCE" --installed-candidate --python "$INSTALLED" --evidence "$EVIDENCE" -- -q -c "$SOURCE/pyproject.toml" "$V5" --tb=short -x "--basetemp=$PRIVATE" > "$AUDIT/wrapper.log" 2>&1
wrapper_status=$?
printf '%s\n' "$wrapper_status" > "$AUDIT/wrapper-exit.txt" || exit $?
# Always retain post-status and source/runtime post-checks after a returned wrapper.
"${FIXED[@]}" "$B/toolchain/pg16/bin/pg_ctl" -D "$B/runtime/data" status > "$AUDIT/post-status.log" 2> "$AUDIT/post-status.stderr"
post_status=$?
printf '%s\n' "$post_status" > "$AUDIT/post-status-exit.txt" || exit $?
admit_helper "$P/admit_smoke.py" "$GUARD_SHA" > "$AUDIT/source-helper-after.log" 2>&1
source_after=$?
if [ "$source_after" -eq 0 ]; then
  "${FIXED[@]}" "$HOST" -I -B "$P/admit_smoke.py" --selection-sha256 "$SELECTION_SHA" --packet-seal-sha256 "$PACKET_SHA" --mode after > "$AUDIT/source-after.log" 2>&1
  source_after=$?
fi
printf '%s\n' "$source_after" > "$AUDIT/source-after-exit.txt" || exit $?
runtime_after=4
if [ "$source_after" -eq 0 ]; then
  admit_helper "$M/verify_runtime_binding.py" "$RUNTIME_GUARD_SHA" > "$AUDIT/runtime-helper-after.log" 2>&1
  runtime_after=$?
  if [ "$runtime_after" -eq 0 ]; then
    "${FIXED[@]}" "$COORD" -I -B "$M/verify_runtime_binding.py" --stage sa21 --binding-sha256 "$RUNTIME_BINDING" --mode after > "$AUDIT/runtime-after.log" 2>&1
    runtime_after=$?
  fi
fi
printf '%s\n' "$runtime_after" > "$AUDIT/runtime-after-exit.txt" || exit $?
[ "$wrapper_status" -eq 0 ] || exit "$wrapper_status"
[ "$post_status" -eq 3 ] && [ "$source_after" -eq 0 ] && [ "$runtime_after" -eq 0 ] || exit 3
# Independent terminal audit and stopped-boundary acceptance still required.
exit 0
