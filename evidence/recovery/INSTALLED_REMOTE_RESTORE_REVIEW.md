# Independent actual installed remote restoration result review

## Decision

ACCEPT the completed authenticated-readback inert evidence restoration at `persistence-recovery-20261013/async-cleanup-installed-remote-fresh-restore-v1`.

This acceptance concerns inert restored evidence only. It does not restore or qualify an installed environment, runtime, database, production deployment, or release. Seven historical failures and UNKNOWN production gates remain. Prior failed remote V2 remains failed; the accepted prior V3 receipt remains pinned.

## Exact authority and observed result

The reviewed restore source has SHA256 `5eac994e22ff7404c483b493c55a9136c451449a58dd3a8dbc63787919cce902`; its prior independent source acceptance report has SHA256 `4452a82b6367e0c42b91c3ae54682c9a3f89028e4d5bf16c3244367a636dff35`. Both exact files were checked. Source constants were decoded with AST literal parsing, without importing or executing the restore source.

Coordinator selection names that exact source, eight external pins and shell=false. Coordinator exit is 0, stderr is empty, and stdout is byte-identical to the restored verification receipt. The installed immutable commit is `a36b75e60903288c71b185cc4909ae16083e0043`; installed provenance SHA256 is `1b4d571709690d9d7be2bf81d9280b8686afd1e0d03d7179e06a61a629136af3`.

All 43 installed readback files, plus the provenance, were checked against exact directory closure, bounded single-link regular-file metadata, SHA256 and Git blob identities. The 12 focused/base and 24 additive readback rows were independently checked against their accepted dependency pins. All per-file provenance rows identify the same respective immutable commits, repository, prefix, paths and authenticated readbacks. The two accepted dependency restoration receipts match their pinned hashes. Local staging was not substituted.

This was an offline audit against coordinator-supplied actual authenticated observations and immutable pins. No new network authentication was performed; local provenance assertions alone would not establish remote authentication.

## Admission and reconstruction

Every actual output path was metadata-admitted before output content reads. All external readback and dependency receipt paths were metadata-admitted before reading their bodies. Reads were bounded, no-follow, single-link regular-file reads with metadata continuity checks.

All three reconstructed archives match their accepted compressed identities. Before accessing any member body, the independent audit validated all 1,421 physical canonical USTAR headers: exact names, order, mode, size, type, attributes, padding, bounds and stream closure. Each stream is one bounded CRC64 XZ stream. Stream hashes and every admitted member body identity then matched the accepted literal inventories. Nested payloads remained opaque.

The installed manifest dependencies, 3,818 logical paths, 79 controls, input pins, original-plus-supplement inventory union, aliases, lineage and empty-directory contract were checked. Content locators were resolved only within the admitted archive inventories, never followed as arbitrary live paths. All 217 GREEN source files match their accepted focused/base archive members.

## Exact actual output

- 5,538 data files and 322,809,407 data bytes
- Three verification/admission receipts, for 5,541 total files
- 522 subdirectories, or 523 directories including the output root
- Exact file and directory closure, including accepted empty directories
- Single-link regular files with mode 0600; directories with mode 0700
- Every data file compared byte-for-byte against the independently reconstructed accepted content
- All restore receipt fields, header receipt fields, input metadata receipt paths and metadata values, and all selected CLI pins verified
- Input bytes and metadata, and output file metadata, remained unchanged during verification

Restore receipt SHA256: `410269c788695376274bcadf99006390caf302b48d275828cf732177161cd0a8`.

Header receipt SHA256: `9c30b45a547fb91f494fafe0abd45c9e618eee2eef8e4ea22b7ae99a7b59fa7d`.

Input metadata receipt SHA256: `182b6e4c554e0e1cff9dc3a5854ac33126886519892597c5f9cecba9a3216899`.

## Preserved audit history and limits

The first independent audit stopped after the complete header barrier and member verification because its toolchain namespace check incorrectly applied full-output exceptions to an unprefixed logical manifest path. This was an audit-only error, not a restore failure. `audit.py`, `HEADER_BARRIER.json`, `exit.txt`, `stdout.log`, and `stderr.log` preserve that failed attempt.

The coordinator authorized the narrow correction: remove only the incorrectly unprefixed path check, retaining the unchanged safety check on the full group-prefixed output path. `audit-v2.py` also adds authorized read-only receipt metadata, exact CLI/receipt and manifest lineage checks. Its fresh captures are `exit-v2.txt` (0), `stderr-v2.log` (empty), `stdout-v2.log`, `HEADER_BARRIER-v2.json` and `RESULT.json`.

No restored or source artifact was modified. No product tests, archived code execution, product import, installation, database, network or Git operation occurred. No forbidden raw phase JSON, environment, credentials, cache or secrets were read, hashed or copied. The restored accepted source and nested archives/wheels were treated strictly as inert data.
