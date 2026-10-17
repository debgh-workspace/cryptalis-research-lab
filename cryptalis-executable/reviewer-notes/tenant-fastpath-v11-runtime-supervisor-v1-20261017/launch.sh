#!/bin/bash
# HELD source. Requires fresh external source/tool admission and root selection.
# Reviewed entry is clean env LANG/LC_ALL=C.UTF-8 TZ=UTC and /usr/bin/bash
# --noprofile --norc this absolute source, with one admitted SOURCE seal argument.
set -Eeuo pipefail
umask 077
readonly D=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/reviewer-notes/tenant-fastpath-v11-runtime-supervisor-v1-20261017
readonly P=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/tenant-fastpath-no-db-packet-v11-20261017
readonly T=$D/outer-001
[[ $# == 1 && $1 =~ ^[0-9a-f]{64}$ && ${BASH_SOURCE[0]} == "$D/launch.sh" ]]
[[ ! -e $T && ! -L $T && ! -e $D/attempt-001 && ! -L $D/attempt-001 ]]
p=$D
while [[ $p != / ]]; do [[ -d $p && ! -L $p ]]; p=${p%/*}; [[ -n $p ]] || p=/; done
/usr/bin/mkdir -m 700 -- "$T"
set -C
exec 3> "$T/outer.receipt"
printf '%s\n' 'scope=correctness_only' 'external_admission=REQUIRED_SEPARATE_RECORD' "source_sha256=$1" >&3
set +e
(
  ulimit -c 0 || { printf '%s\n' 'stop_reason=CORE_LIMIT_FAILED' >&3; exit 70; }
  ulimit -t 480 || { printf '%s\n' 'stop_reason=CPU_LIMIT_FAILED' >&3; exit 71; }
  ulimit -v 1048576 || { printf '%s\n' 'stop_reason=ADDRESS_LIMIT_FAILED' >&3; exit 72; }
  ulimit -f 8192 || { printf '%s\n' 'stop_reason=FILE_LIMIT_FAILED' >&3; exit 73; }
  [[ $(ulimit -c) == 0 && $(ulimit -t) == 480 && $(ulimit -v) == 1048576 && $(ulimit -f) == 8192 ]] || { printf '%s\n' 'stop_reason=LIMIT_READBACK_FAILED' >&3; exit 74; }
  cd "$D" || exit 75
  printf '%s\n' 'limits_setup=PASS' 'wall_term_seconds=600' 'kill_grace_seconds=30' 'per_process_cpu_seconds=480' 'per_process_address_bytes=1073741824' 'per_file_write_bytes=8388608' 'combined_outer_diagnostic_ceiling_bytes=16777216' >&3 || exit 76
  printf 'cwd=%q\nsource_seal=%q\n' "$PWD" "$1" >&3 || exit 76
  exec 3>&-
  exec /usr/bin/env -i LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC \
    /usr/bin/timeout --signal=TERM --kill-after=30s 600s \
    /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12 \
    -I -S -B -X "pycache_prefix=$P/bytecode-absent" "$D/supervisor.py" \
    0ee0e251481d6bd01e5eda6dbf67e3e568c25ed643570c565c635ae3fdc2f7a2 "$1"
) < /dev/null > "$T/stdout" 2> "$T/stderr"
status=$?
set -e
printf 'supervisor_exit=%s\n' "$status" >&3
exec 3>&-
[[ $status == 0 && -f $D/attempt-001/TERMINAL.json && ! -L $D/attempt-001/TERMINAL.json ]]
# Zero only enables independent receipt review; no implicit rerun or promotion.
