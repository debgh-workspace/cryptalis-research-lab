# Sealed doctor-remedy unit proof: proposed root execution

Status: prepared, NOT EXECUTED. Independent review and explicit coordinator
selection are required before any project import, test or proof execution.

## Scope

This proof executes exact copied CLI, doctor, parser, declaration, header,
canonicalization and package-initializer sources. Each baseline source copy must
match the selected Integrated221 manifest. It calls the real CLI `main` and
records its actual captured stdout, stderr and returned exit value. Expected
messages and report fields are independently written in the proof.

Compiler/compatibility import collaborators are explicit unit stubs. Unentered
compiler, active, setup and ciphertext paths use fail-fast sentinels. Their
positive controls must demonstrate that all four raise and record entry. No
SQLAlchemy, psycopg, installed package or application is imported. These stubs
deliberately bypass installed dependency/import integration. This proof cannot
qualify that boundary, native read-only behavior, providers or the complete
doctor objective.

No product source body is rewritten. The baseline CLI copy is exact. The
derivative contains only the already reviewed proposed remedy-rendering line.
The omission-mutant is a separate copy with that exact line absent. The
exact-restored variant is a separate byte-identical copy of the derivative.
Preflight checks all of these relations and the retained original patch hash.

## Fixed execution inputs

- Interpreter: `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12`
- Interpreter SHA-256: `fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7`
- Working directory: this `proof-v1` directory, never a live installed cell.
- Interpreter flags: `-I -B -S` and
  `-X pycache_prefix=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/preview-doctor-dx-slice-20261015/proof-v1/no-bytecode-use`
- The bytecode-prefix path must be absent before and after each run. `-B` prevents
  creation; the fresh prefix prevents consumption of retained bytecode caches.
- Environment: root must pass an empty environment mapping. The proof verifies
  it is empty without printing or consuming environment values.
- Script: the absolute path to `prove_doctor_remedy.py` in this directory.
- Arguments: exactly one variant below and the independently handed-off final
  SHA-256 of `INPUTS.sha256`. Supply the literal external hash, not a runtime
  substitution that trusts an unanchored local inventory.
- Source manifest anchor:
  `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`.
- Original one-line patch anchor:
  `31e117393dd77d40a8d10733434defe55c6b590958ec25d73afaaa5821592e10`.

`INPUTS.sha256` pins the complete 21-file input set, including the proof source,
plan, case inventory, three fixtures, eight original product sources, three CLI
variant copies, original patch, original source manifest and stdlib inventories.
The coordinator must independently verify the proof source and inventory anchor
before launch; self-checking a program is not an independent trust root.

`STDLIB_SHA256.txt` pins exactly 472 regular `.py` and extension `.so` files at
depth at most two under the approved runtime's `lib/python3.12`. The corresponding
path list excludes caches, site-packages, tests and unrelated GUI/tool packages.
The proof verifies every pinned stdlib file and all preloaded module origins.
It rejects an unexpected stdlib ZIP or search path. Native interpreter/system
dynamic-library dependencies are outside this unit's separate pin inventory;
this is not clean-host interpreter provenance or a supply-chain qualification.

The Python audit guard refuses runtime file writes, unadmitted file reads,
directory discovery, subprocess/network/ctypes calls and environment changes.
Product sources are compiled and executed unchanged from verified in-memory
bytes. Fixtures are existing bounded local regular files, rechecked before and
after each call. The proof writes no result file; root captures process streams
to new evidence files outside the immutable input inventory. The guard is a
unit assertion boundary, not an OS sandbox for arbitrary hostile native code.

## Four separate, serial processes

1. `baseline-red`: exact original CLI; expected exit 1 and exactly D01/D02 FAIL.
2. `derivative-green`: proposed one-line delta; expected exit 0 and all 11 PASS.
3. `omission-mutant`: separate exact omission; expected exit 1 and exactly D01/D02 FAIL.
4. `exact-restored`: separate exact derivative bytes; expected exit 0 and all 11 PASS.

For each expected RED, only `expected_text_exact` may be false in D01/D02.
Exit, empty stderr and redaction checks must still pass. Every other case must
pass. Expected RED remains process exit 1 and is recorded as real failures.
No `expectedFailure`, skip, alternate assertion or waiver is used.

Do not launch the next variant until the preceding actual receipt is reviewed.
Any other failure, ERROR, missing/duplicate case, missing terminal marker,
postrun mismatch, signal, timeout or wrong process exit is a HOLD. Retain that
evidence and report; no automatic retries or source changes are selected here.

## Cases and independent acceptance

The exact ordered 11-case list is in `EXPECTED_CASE_IDS.json` and independently
fixed in the proof. D01/D02 establish malformed and semantic declaration
rejections and safe remedy delivery. D03 requires exact valid plain output and
exit 3. D04/D05 require exact complete rejected/valid JSON bytes and values,
unchanged exits and no private marker. D06/D07/D08 force write, short-write and
flush failures and require the existing operational exit and safe diagnostic.
D09 fails both output channels and requires exit 4. D10 checks every dynamic
sentinel. D11 injects all four synthetic private markers into the collector and
requires detection before accepting absence on ordinary calls.

Root should additionally compare D03/D04/D05 captured stdout and exit across
all four independent process receipts. The expected JSON values do not use
product report helpers. Runtime source and fixture bytes are rechecked after
the cases; no mutation touches selected product sources.

## Resource and termination bounds

Each process sets CPU <=15 seconds, address space <=384 MiB, file-size <=2 MiB
and open descriptors <=64; existing stricter hard limits are retained. An
internal 20-second wall alarm supplements root supervision. Root must enforce
an external 30-second wall deadline with a short termination grace, retain the
actual exit/signal and terminal resource accounting, and cap captured output
at 2 MiB. There are no child processes, database connections or network calls.

Normal case records retain wall time, actual output or failed-delivery attempts,
every boolean assertion and PASS/FAIL/ERROR. Failed-writer buffers are explicitly
labeled delivery attempts, not successful stream delivery. Terminal records
retain actual counts, IDs, expected RED IDs separately, CPU/RSS and postrun
integrity. Root must account for a killed process even if no terminal JSON exists.

Stop after all four finite processes and independent result audit, or on HOLD.
No package build, installed integration, selected-candidate change, release,
provider/cluster test or doctor-completion claim follows from this unit proof.
