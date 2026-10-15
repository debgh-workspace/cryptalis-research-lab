#!/bin/bash
# HELD. Root must independently accept source, select read-only SA21 scope,
# verify current closed predecessor and provide both externally anchored digests.
set -u
set -o noclobber
[ "$#" -eq 3 ] || exit 4
CELL=$1
SELECTION_SHA=$2
PACKET_SHA=$3
[ "$CELL" = sa21 ] || exit 4
[[ "$SELECTION_SHA" =~ ^[0-9a-f]{64}$ ]] || exit 4
[[ "$PACKET_SHA" =~ ^[0-9a-f]{64}$ ]] || exit 4
B=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable
P="$B/experiments/json-transport-native-probe-v2-20261015"
M="$B/experiments/integrated221-installed-full-controls-v3-20261015"
SOURCE="$B/candidate-cluster-retained-integrated-v2-20261015"
AUDIT="$P/run/sa21"
EVIDENCE="$B/evidence/json-transport-native-probe-v2-sa21-20261015"
COORD="$B/repo/.venv/bin/python"
HOST=/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12
INSTALLED="$B/release-lab/integrated221-installed-20261015/sa21/bin/python"
GUARD_SHA=096f201196f4a6a5ce17e2be31b5b29db0c1c6876cdad72729408dae2886b47e
RUNTIME_GUARD_SHA=c84e168fd2f9dc5a5e8af943ea52d868f495b542ae00c2e9da47c470d391c861
RUNTIME_BINDING=669cb3c408144f597cc70de5d8c23295e26ba47f9c68888b1d986e431171cf54
FIXED=(/usr/bin/env -i "HOME=$B/runtime/home" "PATH=$B/toolchain/pg16/bin:/usr/bin:/bin" "LANG=C.UTF-8" "TZ=UTC")
cd "$B" || exit $?
umask 077
ulimit -c 0 || exit $?

admit_helper() {
  "${FIXED[@]}" "$HOST" -I -B -c '
from pathlib import Path
import hashlib, stat, sys
p=Path(sys.argv[1]); expected=sys.argv[2]
allowed={Path("/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/json-transport-native-probe-v2-20261015/admit_packet.py"),Path("/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/integrated221-installed-full-controls-v3-20261015/verify_runtime_binding.py")}
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

# No output, installed/corpus, DB/status action before actual source/selection gate.
admit_helper "$P/admit_packet.py" "$GUARD_SHA" || exit $?
"${FIXED[@]}" "$HOST" -I -B "$P/admit_packet.py" --cell sa21 --selection-sha256 "$SELECTION_SHA" --packet-seal-sha256 "$PACKET_SHA" --mode before || exit $?
for path in "$AUDIT" "$EVIDENCE"; do
  [ ! -e "$path" ] && [ ! -L "$path" ] || exit 2
done
[ ! -L "$P/run" ] || exit 2
/bin/mkdir -p "$P/run" || exit $?
/bin/mkdir "$AUDIT" || exit $?
printf '%s\n' "$SELECTION_SHA" > "$AUDIT/selection-sha256.txt" || exit $?
printf '%s\n' "$PACKET_SHA" > "$AUDIT/packet-seal-sha256.txt" || exit $?
admit_helper "$P/admit_packet.py" "$GUARD_SHA" > "$AUDIT/archive-helper.log" 2>&1 || exit $?
"${FIXED[@]}" "$HOST" -I -B "$P/admit_packet.py" --cell sa21 --selection-sha256 "$SELECTION_SHA" --packet-seal-sha256 "$PACKET_SHA" --mode archive > "$AUDIT/archive.log" 2>&1
archive_status=$?
printf '%s\n' "$archive_status" > "$AUDIT/archive-exit.txt" || exit $?
[ "$archive_status" -eq 0 ] || exit "$archive_status"
# The unchanged accepted main guard supplies identity only, not new authority.
admit_helper "$M/verify_runtime_binding.py" "$RUNTIME_GUARD_SHA" > "$AUDIT/runtime-helper-before.log" 2>&1 || exit $?
"${FIXED[@]}" "$COORD" -I -B "$M/verify_runtime_binding.py" --stage sa21 --binding-sha256 "$RUNTIME_BINDING" --mode before > "$AUDIT/runtime-before.log" 2>&1
runtime_before=$?
printf '%s\n' "$runtime_before" > "$AUDIT/runtime-before-exit.txt" || exit $?
[ "$runtime_before" -eq 0 ] || exit "$runtime_before"
"${FIXED[@]}" "$B/toolchain/pg16/bin/pg_ctl" -D "$B/runtime/data" status > "$AUDIT/pre-status.log" 2> "$AUDIT/pre-status.stderr"
pre_status=$?
printf '%s\n' "$pre_status" > "$AUDIT/pre-status-exit.txt" || exit $?
[ "$pre_status" -eq 3 ] || exit 3
[ ! -e "$EVIDENCE" ] && [ ! -L "$EVIDENCE" ] || exit 2
# Exactly one unchanged cold launcher/guarded wrapper invocation. No direct pytest.
"${FIXED[@]}" "$COORD" -B "$M/launch_cold_wrapper.py" --candidate-root "$SOURCE" --installed-candidate --python "$INSTALLED" --evidence "$EVIDENCE" -- -q -c "$SOURCE/pyproject.toml" "$P/test_native_transport.py" "--confcutdir=$P" -p no:cacheprovider --tb=short -x > "$AUDIT/wrapper.log" 2>&1
wrapper_status=$?
printf '%s\n' "$wrapper_status" > "$AUDIT/wrapper-exit.txt" || exit $?
# Always attempt independent stopped proof and separately admitted post gates.
"${FIXED[@]}" "$B/toolchain/pg16/bin/pg_ctl" -D "$B/runtime/data" status > "$AUDIT/post-status.log" 2> "$AUDIT/post-status.stderr"
post_status=$?
printf '%s\n' "$post_status" > "$AUDIT/post-status-exit.txt" || exit $?
admit_helper "$P/admit_packet.py" "$GUARD_SHA" > "$AUDIT/source-helper-after.log" 2>&1
source_after=$?
if [ "$source_after" -eq 0 ]; then
  "${FIXED[@]}" "$HOST" -I -B "$P/admit_packet.py" --cell sa21 --selection-sha256 "$SELECTION_SHA" --packet-seal-sha256 "$PACKET_SHA" --mode after > "$AUDIT/source-after.log" 2>&1
  source_after=$?
fi
printf '%s\n' "$source_after" > "$AUDIT/source-after-exit.txt" || exit $?
admit_helper "$M/verify_runtime_binding.py" "$RUNTIME_GUARD_SHA" > "$AUDIT/runtime-helper-after.log" 2>&1
runtime_after=$?
if [ "$runtime_after" -eq 0 ]; then
  "${FIXED[@]}" "$COORD" -I -B "$M/verify_runtime_binding.py" --stage sa21 --binding-sha256 "$RUNTIME_BINDING" --mode after > "$AUDIT/runtime-after.log" 2>&1
  runtime_after=$?
fi
printf '%s\n' "$runtime_after" > "$AUDIT/runtime-after-exit.txt" || exit $?
[ "$wrapper_status" -eq 0 ] || exit "$wrapper_status"
[ "$post_status" -eq 3 ] && [ "$source_after" -eq 0 ] && [ "$runtime_after" -eq 0 ] || exit 3
# A zero entry exit is not terminal acceptance. Root must obtain independent audit.
exit 0
