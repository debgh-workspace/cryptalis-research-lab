# Fixture runner V2 first selection: retained STARTUP HOLD

Actual capture: persistence-recovery-20261013/fixture-hardening-v2-20261017-1805. Child exit1, external after-check exit0. The raw MODULE_DIAGNOSTICS_JSON reports HOLD, AssertionError at STARTUP, zero admitted inputs, zero cases, empty product/dependency origins and empty inner preservation. stderr is empty and cache_absent true. This is a startup rejection, not a failed recording case or accepted nineteen-case run.

Independently reconciled external before.json hashes/metadata and after.json: exactly681 matching unique paths, all after pass=true. The inner runner provides no preservation evidence because admission had not begun; preservation is the separate root aftercheck evidence. CHECKS.json pins all eight ordinary capture files. No runtime was repeated during review.

## Invocation classification

INVOCATION.json supplies exactly four keys to /bin/bash -c, applies resource limits and then execs timeout directly around Python. There is no second environment reset after bash. The unchanged runner requires dict(os.environ) to equal exactly LANG=C.UTF-8, LC_ALL=C.UTF-8, TZ=UTC, PSYCOPG_IMPL=binary before input admission. Bash may introduce exported PWD/SHLVL/_ values; therefore outer clean-env selection does not ensure the required Python environment.

The receipt reports only STARTUP/AssertionError and does not serialize the assertion label or actual environment. Shell-added environment is a source-consistent explanation, not directly captured proof of the exact assertion. No secrets or environment-body inspection is needed or authorized to establish the proposed correction.

## Narrow corrected invocation accepted in source

Keep frozen runner V2 SOURCE07769e9545bb30fa0233ec6b9eebaa7147edd1304d8ec86a1dd9eaeffb7ab0f0, its source acceptance and all input/hash/origin policies unchanged. In the root shell invocation, replace the segment after timeout's 60s operand with:

/usr/bin/env -i LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC PSYCOPG_IMPL=binary "$2" -I -B -S -X "pycache_prefix=$3/bytecode-absent" "$3/run_module_diagnostics.py" combined "$4"

Use freshly admitted /usr/bin/env alongside existing interpreter/bash/timeout/tool controls. The reset sits inside the existing timeout boundary and immediately before Python, preserving argv/cwd/resource bounds and the exact four-key runner assertion. Do not relax the assertion or change the frozen packet. Use a new root-owned capture path, require cold bytecode absence, preserve this HOLD and all inputs, and run unconditional external afterchecks. Root alone may select that correction after fresh admission; no worker execution is authorized by this note.

The scope remains nineteen direct original recording calls with genuine pytest imports and no DB session. No DB, native-fixture mutation, publication, installation, Git, output overwrite or policy expansion is implied. An initial guessed INVOCATION.txt filename was absent; the actual listed INVOCATION.json was used without retrying the absent name.

Root supplementary observation at18:06: a controlled host-only probe on the same four-key environment → bash → pinned Python route returned keys LANG, LC_ALL, PSYCOPG_IMPL, PWD, SHLVL, TZ and _. This independently reported probe confirms shell expansion on that route; it does not recover the original unrecorded assertion label. No target code/imports were used in the reported probe.
