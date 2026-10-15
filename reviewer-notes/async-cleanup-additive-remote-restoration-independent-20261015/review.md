# Independent actual authenticated paired recovery result review

Date: 2026-10-15 UTC.

Decision: **ACCEPT_ACTUAL_REMOTE_PAIRED_DATA_ONLY_RESTORE_RESULT**.

The independently authored data-only verifier passed on its first attempt: exit0, 17 grouped checks. This accepts the completed V3 execution's exact inert byte-recovery result, not runtime qualification. No checker failure or repair occurred in this review.

## Execution and trust binding

- Executed source SHA256: `60b7666952832ac2e1aba155d70cc1cb38c02968d71a5352c0e3281381640c59`.
- Independently accepted V3 source review SHA256: `5f76a98eba310ad83412d9387072a3bb03319a1cd38ae847ba36628181f363d9`.
- Fresh result root: `persistence-recovery-20261013/async-cleanup-full-source-additive-remote-paired-restore-v2`.
- Actual coordinator `selection.json`, `exit.txt`, `stdout.log` and `stderr.log` were independently read and rechecked. The exact command selects the pinned V3 source with `python -I -S` and all five accepted external arguments. Exit is0, stderr is empty and stdout identifies the exact result and successful receipt.
- Additive immutable commit: `0c74347b6d89cfc82d766973e14d2450fd294032`.
- Additive actual-readback provenance SHA256: `3c822410850b54d23a83e468151bcf4d2af5f951585eba8d862f21436e4378e0`.
- Accepted base commit: `86fb0e26ac4032a405b8c077939eb3e288e69db5`.
- Base provenance SHA256: `93b32a8e71db994724409f506c3040e3aad64c9b03a650cf14df7f970e1d7995`.
- Base receipt SHA256: `c83fbc9e129e6d95f2705d82ff3ff55703e3652d705b5bd5b6750107d89d1d92`.
- Completed output receipt `RESTORE_VERIFICATION.json` SHA256: `e33e0d3f3a9bc7202fd2b49c3cbbf03fee66893f67cc270db5461222de73e3b2`.

All 24 local actual additive readback bodies match exact accepted byte lengths, SHA256 and Git-blob identities; their individual provenance rows match, and the readback directory has exactly these24 files plus its pinned provenance. The accepted base archive, provenance and exact receipt remain unchanged. This review relies on the coordinator's previously pinned authenticated observations; it did not independently contact the service, repeat remote authentication or relabel staging. The offline trust limitation remains explicit.

## Independently reconstructed result contract

The verifier parsed the pinned source as AST data only. It did not import, compile, evaluate or execute reviewed source, restored source or copied reviewed helpers. Expected additive/base identities were obtained from literal dictionaries in that accepted source. Logical destination identities were independently bound to the prior accepted resolution metadata SHA256 `54fa04656d927709c3168dddc5008ce831778e6592581a8c543e00e6b8e6e01d`. Every logical destination resolves to the exact pinned additive/base member identity, without opening any live origin.

GREEN was independently derived from the accepted base source member dictionary; RED substitutes the one accepted baseline SQLAlchemy body; baseline removes the accepted new test file. The full expected namespace was constructed independently from those identities, before inspecting any restored payload. This yields:

- 3,909 data files, exactly129,238,667 bytes.
- One completion receipt, for3,910 total regular files.
- 358 directories below the output root, including the required explicitly empty optional candidate-corpus directory.
- 2,386 logical files, exactly65,285,835 bytes; canonical logical-list SHA256 `d08d157801d02aecee0136ac4e2bbe2136b473e575b00d965b52136a9cc5fd8c`.
- Full GREEN217, RED217 and baseline216 source views.
- Exact additive355 and base516 restored member closures, plus both compressed archives.

The namespace has no exact or casefold collisions or file/directory collisions. All expected names passed independent raw-phase, environment, credential, cache, traversal and forbidden-suffix gates. The only toolchain paths are the one exact required inert directory and the two previously accepted exact leaf files. This is no permission to read a live toolchain.

Before any restored body was opened, the verifier walked and admitted the complete observed output closure using metadata: exact expected names, real directory and regular-file types, directory0700, file0600, single-link files and empty-directory checks. No unexpected path was opened. `OUTPUT_METADATA_ADMISSION-v1.json` records that complete admission. Parent-directory traversal and file reads use descriptor-based no-follow opens and bounded reads with before/after identity checks.

Every restored data body was then read and verified independently against its expected length and SHA256. Every field of the completion receipt was compared with the exact accepted source's report-data expression through a small restricted AST-data interpreter, without general evaluation or function execution. Actual coordinator exit0 and stdout were required in addition to receipt presence. The final complete namespace/metadata inspection was unchanged, and every read input and output was independently re-read with no digest or identity drift.

No archive decompression was necessary in this result review. The restored compressed archives and all admitted member bytes match the accepted identities. Full archive-header admission remains established by the accepted earlier archive/source reviews and the pinned successful restore; this result review does not claim to have repeated that header parser.

## Preserved failure and qualification boundaries

The failed V2 suffix-v1 output was not opened or changed. Its prior failed status remains preserved. No repaired or rerun product execution is claimed.

Writes were confined to this fresh independent-review directory. No restored code, archived program, product import, test, build, install, database/server action, network operation, Git operation or publication occurred. No live logical corpus, raw phase, secret, environment, credential or cache body was read. Nested packaging bodies were hashed only as opaque accepted bytes, without unpacking or executing. Already accepted synthetic fixture dispositions were not reopened as a new scan or printed.

Seven historical failures remain unresolved. All seven production gates remain UNKNOWN. The result establishes exact accepted inert recovery bytes only; it does not establish an installed or runnable dependency/database environment, fresh-host or independent-builder product reproducibility, physical-release guarantee, release approval or production readiness.

## Preserved review evidence

`verify_result_v1.py` is the independent checker; `verification-run-v1.log` and `verification-exit-v1.txt` preserve its first and only run. `VERIFICATION_SUMMARY-v1.json` contains all grouped checks and exact result counts. `CONTINUITY-v1.json` records every read file's identity and hash through the final zero-drift pass. `REVIEW_FILES.sha256` seals this review's seven artifacts, excluding itself.
