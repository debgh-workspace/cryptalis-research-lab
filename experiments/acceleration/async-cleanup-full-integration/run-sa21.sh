#!/bin/bash
# PROPOSED ONLY. No execution authority. Coordinator runs this cell alone after
# both focused GREEN audits and the applicable independent source/terminal reviews.
# Never call another cell from this file. Stop for terminal audit after return.
set -u
cd /workspace/scratch/cb28ee9f5f4a || exit $?
PACKET=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/async-cleanup-full-integration-plan-20261014
AUDIT="$PACKET/run/sa21"
EVIDENCE=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/evidence/async-cleanup-full-integration-sa21-20261014
CLEARANCE=CLEARANCE_MAIN_SA21.sha256
# Additive reviewer clearance is deliberately absent in the preparation packet.
# Only safe reviewer documents/data may be listed. Its digest must be recorded
# by the coordinator before this entry. It is evidence, not user approval.
test -s "$PACKET/$CLEARANCE" || exit 4
test ! -e "$EVIDENCE" || exit 2
test ! -e "$AUDIT" || exit 2
mkdir -p "$PACKET/run" || exit $?
mkdir "$AUDIT" || exit $?
/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python -I -B "$PACKET/verify_frozen.py" --packet "$PACKET" --clearance "$CLEARANCE" --archive "$AUDIT/frozen-inputs" > "$AUDIT/pins-before.log" 2>&1
before_status=$?
printf '%s\n' "$before_status" > "$AUDIT/pins-before-exit.txt" || exit $?
if [ "$before_status" -ne 0 ]; then exit "$before_status"; fi
/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py --python /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/release-lab/s25-installed-20261014/sa21/bin/python --candidate-root /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-next-unblocked-correctness-20261014 --evidence "$EVIDENCE" -- -q -c /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-next-unblocked-correctness-20261014/pyproject.toml /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-next-unblocked-correctness-20261014/tests --ignore=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-next-unblocked-correctness-20261014/tests/test_async_sqlmodel_public_hook.py --tb=short -ra > "$AUDIT/wrapper.log" 2>&1
status=$?
printf '%s\n' "$status" > "$AUDIT/wrapper-exit.txt" || exit $?
/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python -I -B "$PACKET/verify_frozen.py" --packet "$PACKET" --clearance "$CLEARANCE" > "$AUDIT/pins-after.log" 2>&1
after_status=$?
printf '%s\n' "$after_status" > "$AUDIT/pins-after-exit.txt" || exit $?
# A retained historical exit1 remains exit1. No all-green normalization.
# The independent audit must reject ANY pin failure even when wrapper exit1.
if [ "$status" -ne 0 ]; then exit "$status"; fi
if [ "$after_status" -ne 0 ]; then exit 3; fi
exit 0
