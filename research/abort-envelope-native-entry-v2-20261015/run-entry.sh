#!/bin/bash
# HELD: root selects only after both source reviews and latest terminal acceptance.
set -eu
[ "$#" -eq 2 ] || exit 4
[[ "$1" =~ ^[0-9a-f]{64}$ ]] || exit 4
[[ "$2" =~ ^[0-9a-f]{64}$ ]] || exit 4
B=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable
P="$B/experiments/abort-envelope-native-entry-v2-20261015"
HOST=/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12
ENTRY_SHA=6aface4a47fc5d33f7592675481aea70a2f586134777acd4c6d39945ad50bfda
FIXED=(/usr/bin/env -i "HOME=$B/runtime/home" "PATH=$B/toolchain/pg16/bin:/usr/bin:/bin" "LANG=C.UTF-8" "TZ=UTC")
cd "$B"
umask 077
ulimit -c 0
# Authenticate source before executing it. Root independently anchors this shell.
"${FIXED[@]}" "$HOST" -I -B -c '
from pathlib import Path
import hashlib, stat, sys
p=Path(sys.argv[1]); expected=sys.argv[2]
assert p==Path("/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/abort-envelope-native-entry-v2-20261015/entry.py")
current=Path("/")
for part in p.parts[1:]:
    current/=part
    mode=current.lstat().st_mode
    assert stat.S_ISREG(mode) if current==p else stat.S_ISDIR(mode)
assert p.stat().st_size<=65536
assert hashlib.sha256(p.read_bytes()).hexdigest()==expected, "ENTRY_DIGEST_MISMATCH"
' "$P/entry.py" "$ENTRY_SHA"
exec "${FIXED[@]}" "$HOST" -I -B "$P/entry.py" --selection-sha256 "$1" --entry-seal-sha256 "$2"
