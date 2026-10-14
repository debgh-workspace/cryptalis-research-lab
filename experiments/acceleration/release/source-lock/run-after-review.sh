#!/bin/bash
# SOURCE ONLY: do not run before independent review and execution authorization.
set -euo pipefail
D=$(cd -- "$(dirname -- "$0")" && pwd)
UV=/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/uv
PY=/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3
(cd "$D" && sha256sum --check frozen-inputs.sha256)
(cd "$D/source" && sha256sum --check ../derivative-source.sha256)
(cd "$D/../candidate-accel-payload-integrated-20261014" && sha256sum --check "$D/original-source.sha256")
# No existing output may be reused or overwritten.
mkdir "$D/run"
mkdir "$D/run/home" "$D/run/cache" "$D/run/tmp"
mkdir "$D/run/source-1" "$D/run/source-2"
cp -a "$D/source/." "$D/run/source-1/"
cp -a "$D/source/." "$D/run/source-2/"
mkdir "$D/run/sdist-1" "$D/run/sdist-2" "$D/run/direct-wheel" "$D/run/roundtrip-wheel" "$D/run/extracted"
CLEAN=(env -i PATH=/usr/bin:/bin HOME="$D/run/home" TMPDIR="$D/run/tmp" LC_ALL=C.UTF-8 LANG=C.UTF-8 TZ=UTC SOURCE_DATE_EPOCH=0 UV_OFFLINE=1 UV_CACHE_DIR="$D/run/cache" PYTHONDONTWRITEBYTECODE=1)
"${CLEAN[@]}" "$UV" --version > "$D/run/uv-version.log" 2> "$D/run/uv-version.stderr"
grep -Eq '^uv 0\.12\.23([ (]|$)' "$D/run/uv-version.log"
"${CLEAN[@]}" "$PY" -I -B --version > "$D/run/python-version.log" 2> "$D/run/python-version.stderr"
(cd "$D/run/source-1" && "${CLEAN[@]}" "$UV" build-backend build-sdist "$D/run/sdist-1") > "$D/run/sdist-1.log" 2> "$D/run/sdist-1.stderr"
(cd "$D/run/source-2" && "${CLEAN[@]}" "$UV" build-backend build-sdist "$D/run/sdist-2") > "$D/run/sdist-2.log" 2> "$D/run/sdist-2.stderr"
(cd "$D/run/source-1" && "${CLEAN[@]}" "$UV" build-backend build-wheel "$D/run/direct-wheel") > "$D/run/direct-wheel.log" 2> "$D/run/direct-wheel.stderr"
"${CLEAN[@]}" "$PY" -I -B "$D/extract-sdist.py" > "$D/run/extract.log" 2> "$D/run/extract.stderr"
(cd "$D/run/extracted/cryptalis-0.1.0" && "${CLEAN[@]}" "$UV" build-backend build-wheel "$D/run/roundtrip-wheel") > "$D/run/roundtrip-wheel.log" 2> "$D/run/roundtrip-wheel.stderr"
"${CLEAN[@]}" "$PY" -I -B "$D/verify.py" > "$D/run/verification.json" 2> "$D/run/verification.stderr"
(cd "$D" && sha256sum --check frozen-inputs.sha256) > "$D/run/after-frozen-inputs.log"
(cd "$D/source" && sha256sum --check ../derivative-source.sha256) > "$D/run/after-derivative.log"
(cd "$D/../candidate-accel-payload-integrated-20261014" && sha256sum --check "$D/original-source.sha256") > "$D/run/after-original.log"
