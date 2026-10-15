#!/bin/bash
# PROPOSED ONLY. One cell after genuine review/coordinator clearance; no next-cell launch.
set -u
cd /workspace/scratch/cb28ee9f5f4a || exit $?
PACKET=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/cleanup-transport-full-plan-v2-20261015
AUDIT="$PACKET/run/sa20"
EVIDENCE=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/evidence/cleanup-transport-full-v2-sa20-20261015
CLEARANCE=CLEARANCE_MAIN_SA20.sha256
# Bounded single-writer admission only; no hostile concurrent race guarantee.
# Repeat all fixed path/type/digest checks immediately before EVERY interpretation.
admit_verifier() {
  test -d "$PACKET" && test "$(realpath -- "$PACKET")" = "$PACKET" || return 4
  test -f "$PACKET/verify_frozen.py" && test ! -L "$PACKET/verify_frozen.py" || return 4
  test "$(sha256sum -- "$PACKET/verify_frozen.py")" = "2366ef4e31b6ed1a098b9c935fdf4f1ef70f3accccbfd7f159136c96663b825f  $PACKET/verify_frozen.py" || return 4
}
# Validate output parents and clearance metadata without interpreting the helper.
test -d "$PACKET" && test "$(realpath -- "$PACKET")" = "$PACKET" || exit 4
test -f "$PACKET/$CLEARANCE" && test ! -L "$PACKET/$CLEARANCE" && test -s "$PACKET/$CLEARANCE" || exit 4
test ! -e "$EVIDENCE" && test ! -L "$EVIDENCE" || exit 2
test ! -e "$AUDIT" && test ! -L "$AUDIT" || exit 2
if [ -e "$PACKET/run" ] || [ -L "$PACKET/run" ]; then
  test -d "$PACKET/run" && test "$(realpath -- "$PACKET/run")" = "$PACKET/run" || exit 4
else
  mkdir "$PACKET/run" || exit $?
fi
mkdir "$AUDIT" || exit $?
if admit_verifier > "$AUDIT/admission-before.log" 2>&1; then
  /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python -I -B "$PACKET/verify_frozen.py" --cell sa20 --phase before > "$AUDIT/pins-before.log" 2>&1
  before_status=$?
  admission_before_status=0
else
  admission_before_status=$?
  before_status="$admission_before_status"
  printf '%s\n' 'Verifier admission failed; helper NOT INTERPRETED.' > "$AUDIT/pins-before.log" || exit $?
fi
printf '%s\n' "$admission_before_status" > "$AUDIT/admission-before-exit.txt" || exit $?
printf '%s\n' "$before_status" > "$AUDIT/pins-before-exit.txt" || exit $?
if [ "$before_status" -ne 0 ]; then exit "$before_status"; fi
/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py --python /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/release-lab/s25-installed-20261014/sa20/bin/python --candidate-root /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-cleanup-transport-metadata-20261014 --evidence "$EVIDENCE" -- -q -c /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-cleanup-transport-metadata-20261014/pyproject.toml /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-cleanup-transport-metadata-20261014/tests --ignore=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-cleanup-transport-metadata-20261014/tests/test_async_sqlmodel_public_hook.py --tb=short -ra > "$AUDIT/wrapper.log" 2>&1
status=$?
printf '%s\n' "$status" > "$AUDIT/wrapper-exit.txt" || exit $?
if admit_verifier > "$AUDIT/admission-after.log" 2>&1; then
  /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python -I -B "$PACKET/verify_frozen.py" --cell sa20 --phase after > "$AUDIT/pins-after.log" 2>&1
  after_status=$?
  admission_after_status=0
else
  admission_after_status=$?
  after_status="$admission_after_status"
  printf '%s\n' 'Verifier admission failed; helper NOT INTERPRETED.' > "$AUDIT/pins-after.log" || exit $?
fi
printf '%s\n' "$admission_after_status" > "$AUDIT/admission-after-exit.txt" || exit $?
printf '%s\n' "$after_status" > "$AUDIT/pins-after-exit.txt" || exit $?
# Preserve actual nonzero wrapper status, even when after admission/pins fail.
# Independent terminal audit must inspect BOTH separate after-status receipts.
if [ "$status" -ne 0 ]; then exit "$status"; fi
if [ "$after_status" -ne 0 ]; then exit 3; fi
exit 0
