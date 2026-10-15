#!/bin/bash
# Final source-only materialization. No stage is authorized by file existence.
# Missing, unaccepted or changed stage bindings fail closed before any runtime.
set -u
set -o noclobber
[ "$#" -eq 1 ] || exit 4
BINDING_SHA256=$1
[[ "$BINDING_SHA256" =~ ^[0-9a-f]{64}$ ]] || exit 4
cd /workspace/scratch/cb28ee9f5f4a || exit $?
PACKET=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/async-cleanup-installed-full-controls-20261015
AUDIT="$PACKET/run/sa21"
EVIDENCE=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/evidence/async-cleanup-installed-full-sa21-20261015
# Literal source digest of the proposed final helper. Rebind only after final
# helper review; no environment or payload acceptance is implied by this pin.
EXPECTED_GUARD_SHA256=3eee13ea4a94277350908217c3a235579a0b68868354c0ee90fcbcb65586b430
admit_guard() {
  /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12 -I -B -c '
from pathlib import Path
import hashlib, re, stat, sys
p=Path(sys.argv[1]); expected=sys.argv[2]
allowed={Path("/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/async-cleanup-installed-full-controls-20261015/verify_runtime_binding.py"),Path("/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/async-cleanup-installed-sqlmodel-controls-20261015/verify_runtime_binding.py")}
assert p in allowed and re.fullmatch("[0-9a-f]{64}",expected)
current=Path("/")
for part in p.parts[1:]:
    current/=part
    mode=current.lstat().st_mode
    assert not stat.S_ISLNK(mode), str(current)
    assert stat.S_ISREG(mode) if current==p else stat.S_ISDIR(mode), str(current)
assert hashlib.sha256(p.read_bytes()).hexdigest()==expected, "HELPER_DIGEST_MISMATCH"
print("VERIFIED_HELPER",expected,str(p))
' "$PACKET/verify_runtime_binding.py" "$EXPECTED_GUARD_SHA256"
}

# Refuse existing paths, including dangling links. Retain every failed attempt.
[ ! -e "$EVIDENCE" ] && [ ! -L "$EVIDENCE" ] || exit 2
[ ! -e "$AUDIT" ] && [ ! -L "$AUDIT" ] || exit 2
[ ! -L "$PACKET" ] && [ ! -L "$PACKET/run" ] || exit 2
# Validate before creating even an audit directory; caller retains this outer
# output if validation refuses. No runtime entry is reached on a failed gate.
admit_guard || exit $?
/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python -I -B "$PACKET/verify_runtime_binding.py" --stage sa21 --binding-sha256 "$BINDING_SHA256" --mode before || exit $?
mkdir -p "$PACKET/run" || exit $?
mkdir "$AUDIT" || exit $?
printf '%s\n' "$BINDING_SHA256" > "$AUDIT/stage-binding-sha256.txt" || exit $?
# The reviewed helper first admits complete exact target/type/link sets, then
# hashes them; generic unchecked sha256sum --check expansion is forbidden.
admit_guard > "$AUDIT/helper-before-admission.log" 2>&1
before_admission_status=$?
printf '%s\n' "$before_admission_status" > "$AUDIT/helper-before-admission-exit.txt" || exit $?
[ "$before_admission_status" -eq 0 ] || exit "$before_admission_status"
/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python -I -B "$PACKET/verify_runtime_binding.py" --stage sa21 --binding-sha256 "$BINDING_SHA256" --mode before --archive "$AUDIT/frozen-inputs" > "$AUDIT/pins-before.log" 2>&1
before_status=$?
printf '%s\n' "$before_status" > "$AUDIT/pins-before-exit.txt" || exit $?
[ "$before_status" -eq 0 ] || exit "$before_status"
# Exactly one unchanged guarded wrapper invocation. Never invoke pytest directly.
/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py --candidate-root /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-next-unblocked-correctness-20261014 --installed-candidate --python /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/release-lab/async-cleanup-installed-20261015/sa21/bin/python --evidence /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/evidence/async-cleanup-installed-full-sa21-20261015 -- -q -c /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-next-unblocked-correctness-20261014/pyproject.toml /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-next-unblocked-correctness-20261014/tests --ignore=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-next-unblocked-correctness-20261014/tests/test_async_sqlmodel_public_hook.py --tb=short -ra > "$AUDIT/wrapper.log" 2>&1
wrapper_status=$?
printf '%s\n' "$wrapper_status" > "$AUDIT/wrapper-exit.txt" || exit $?
# Independently re-admit helper bytes after the wrapper. Do not interpret a
# missing, changed, linked or wrong-type helper, even when wrapper exit is1.
admit_guard > "$AUDIT/helper-after-admission.log" 2>&1
after_admission_status=$?
printf '%s\n' "$after_admission_status" > "$AUDIT/helper-after-admission-exit.txt" || exit $?
if [ "$after_admission_status" -eq 0 ]; then
  /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python -I -B "$PACKET/verify_runtime_binding.py" --stage sa21 --binding-sha256 "$BINDING_SHA256" --mode after > "$AUDIT/pins-after.log" 2>&1
  pins_after_status=$?
else
  pins_after_status=$after_admission_status
  printf '%s\n' 'HOLD: post-wrapper helper admission failed; helper not interpreted.' > "$AUDIT/pins-after.log" || exit $?
fi
printf '%s\n' "$pins_after_status" > "$AUDIT/pins-after-exit.txt" || exit $?
# A nonzero wrapper exit is preserved even if post-pins also fail. Both must be
# audited independently. Exit1 is expected for historical main failures only.
[ "$wrapper_status" -eq 0 ] || exit "$wrapper_status"
[ "$pins_after_status" -eq 0 ] || exit 3
# STOP for independent terminal audit; this entry never starts another stage.
exit 0
