# Independent full SA21 source terminal review

Audit date: 2026-10-15 UTC. The directory suffix identifies the 2026-10-14 experiment packet.

Verdict: **ACCEPT_BOUNDED_FULL_SA21_SOURCE** for this exact completed source-integration cell. The complete original S25 main inventory retains its outcomes, failure messages and phase reports; all 22 added cleanup cases pass. The seven historical failures remain unresolved. This is not an all-green suite, installed-correction qualification, optional SQLModel coverage, release approval or production readiness. No subsequent cell was run by this reviewer.

## Exact execution and identity

Command: /bin/bash /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/async-cleanup-full-integration-plan-20261014/run-sa21.sh

- Packet SHA256: 7135f4958e404469a335ffdc5a364154b67284fdfa01380b0873d81e53fb469d.
- Entry SHA256: 7a544d86f0f96d6ce22f08845eba43894b115a31b6e7ce91c00e7eede899a845.
- Clearance SHA256: 302db3179b1cee7db69115dd54d0dd28c3cb95034c92d51c6e57541b23c8bccf.
- Input manifest SHA256: 55f3ca6716677dd145c63f67a47ba745cd0241f4d41f82f07e447118cb942e1d.
- Accepted source/command review SHA256: 3db0ed2548632ecc11452863578514b6a45f04887eb4692c124363686d6cd8d8.
- This audit-summary.json SHA256: 09491ae3e4d95a881ab889a555debdba0ab903ef6c18980cc5417f9e0b1c155b.
- Final data-only audit_terminal.py SHA256: fe413afb55399f4c17b7bd47dfdd5b56ca13560d630ea42036e7557b2c2ba9e3.

The coordinator reported launch at 2026-10-15T00:27:55Z and observed the terminal outer exit at 00:35:03Z. The exact retained observation identifies session 48363, terminal tool chunk6037c4, the two-element argv and actual outer exit 1. Its bytes and digest are retained in root-outer-status.json and terminal-confirmation.json. No run logs were hashed before terminal confirmation.

Actual outer, wrapper and runner exits are all 1. Both independent pin phases exit 0. The safe wrapper log records exactly one postgres-start exit 0, readiness exit 0, package-origin exit 0, tests exit 1 and postgres-stop exit 0. postgres-stop.log explicitly ends with server stopped. These are separate checks; neither outer exit 1 nor test completion was used as proof of pin success or shutdown.

## Exact outcomes and diagnostics

There are exactly 2661 unique ordinary testcase identities: 2654 passed, seven failed, zero skipped and zero errors. Every one of the original 2639 identities and outcomes equals both accepted S25 source and installed SA21 references. The 22 disjoint additions match literal AST expansion of the new test source and the frozen new-node list, and all pass. No original ID is missing, duplicated, deselected or replaced.

The seven retained failing tests are in tests/test_deprotection_ordinals.py:

- test_reverse_refuses_unhandled_public_suffix_comment_before_staging
- test_changed_public_staging_refuses_switch
- test_public_copy_participates_in_chunk_byte_bound
- test_reverse_refuses_unhandled_suffix_attributes[column_grant]
- test_reverse_refuses_unhandled_suffix_attributes[statistics]
- test_reverse_refuses_unhandled_suffix_attributes[storage]
- test_reverse_refuses_unhandled_suffix_attributes[compression]

Every failure message is exact against both references. Current diagnostic bodies are byte-identical to the S25 installed reference. Relative to the S25 source reference, only one native result.py traceback path changes from release-lab/wheel-venv to release-lab/s25-installed-20261014/sa21. The test, exception, message, code and line numbers are unchanged. No general path or diagnostic normalization was applied. diagnostics.json retains all three safe diagnostic bodies and the exact diff.

The 2661 start events form a bijection with ordinary JUnit IDs, including class-method identity. The complete old setup/call/teardown report multisets equal both S25 references. The 22 additions contribute exactly 66 passing ordinary phase reports. There are 8039 phase reports: 2661 passing setups, 2710 passing calls, seven failed calls and 2661 passing teardowns. The 56 passing subtest events remain separate from ordinary IDs. The JUnit suite header reports 2717 because it includes those subtests; it was not used as the ordinary-case count.

Terminal pytest result: 7 failed, 2654 passed, 50 warnings, 56 subtests passed in 411.03s (0:06:51). Runner elapsed time is 412.1256114229909 seconds. All per-module runner call counts reconcile with progress evidence.

The 50 warnings equal both historical full SA21 runs: two fork-related DeprecationWarnings and 48 DISTINCT ON SADeprecationWarnings. Comparison allows only exact candidate-root substitution and decimal process-ID substitution. Original warning bodies are retained. No selected timeout, bounded-cleanup failure, pending-task, unawaited-coroutine, unraisable-exception, thread-exception or RuntimeWarning indicator is present in the safe logs and JUnit.

## Source, selection, pins and archives

All 566 input target names and resolved interpreter destinations were independently validated against bounded path classes before hashing listed payloads. All 566 hashes match. All 29 packet-member hashes and three actual accepted clearance-review hashes match. Both complete pre/post pin logs contain exactly the expected ordered paths, counts and success messages. The clearance is byte-identical before, archived and after; its documents have the actual accepted verdicts.

The 216-file S25 baseline is unchanged. The complete 217-file candidate matches the accepted focused GREEN manifest. Its only changed original file is src/cryptalis/sqlalchemy.py, and its sole addition is tests/test_sqlalchemy_async_exit_double_failure.py. Every original test, fixture, preflight, lock and dependency declaration remains unchanged. Candidate and baseline extra filenames are cache-only (146 and 170); cache bytes were not read or hashed.

All 31 archived packet/anchor/clearance files equal their originals. All 217 complete candidate-source archive files match the candidate manifest. The wrapper's 156 before/after source/config hashes and every corresponding source-repository copy match. All 155 runner source/test hashes match. These inventories share 154 paths: the wrapper alone includes pyproject.toml and uv.lock; the runner alone includes scripts/test_postgres.py. This is the exact unchanged source-capture design, not missing source. Main external before/after snapshots are empty and stable.

The selected interpreter is the existing s25-installed-20261014/sa21 environment, with the pinned Python 3.12 binary, SQLAlchemy 2.1.3 native files and existing distribution metadata. All 14 current METADATA filenames per main dependency environment equal their pinned sets. This is bounded file identity, not a full dependency-file or every-import attestation.

The command and runner receipt select the entire corrected candidate/tests directory, with the sole original optional ignore test_async_sqlmodel_public_hook.py. There is no new selection narrowing, retry, installed-candidate flag or optional coverage claim. Fresh readiness and test preflights both record the two expected role fingerprints. source-root.json and safe package-origin.log identify candidate-next-unblocked-correctness-20261014/src. That separate origin subprocess is not continuous attestation of every pytest subprocess import.

## Corpus restoration and generated evidence

All 26 original corpus primary filenames equal the frozen baseline. Every original primary byte string and durable prior-corpus archive matches its frozen digest. The primary filename set is unchanged. Isolation records errors=[], deleted_during_run=[] and primary_receipts_restored=true. The archive directory contains exactly the one recorded generated file; no unexpected corpus archive is present.

The generated master-s4-compatibility-flush-corpus-v1-sa2.1.3.json has SHA256 7ab87b55707e2ec8e05b6fd6a0f3fde3561b3cd8dd7fdb5839ef9469530f1bf5. It contains 16 complete unique id/mode records: 12 REJECTED-LOUD and four IDENTICAL. Its complete content agrees with both accepted S25 full-suite archives after replacing only the 12 terminal decimal-hex-hex operation-ID tokens in reason strings. All IDs, modes, classifications, recovery arrays, alternative text, protected SQL counts and scope are otherwise exact. This is retained run evidence; no generated corpus was promoted to a primary.

## Reviewer method corrections and limits

Two reviewer assumptions stopped earlier data-only checker attempts. The first incorrectly treated the 156/155 captures as one set plus uv.lock. The second incorrectly required the full-run generated corpus to have the focused-run empty-results shape. Each failed checker and log is preserved. The coordinator authorized only the specific evidence-supported assertion correction before each data-only rerun. METHOD_CORRECTION.md records the exact causes, source scope and comparison. No packet, candidate, source/test expectation, runtime evidence or corpus file was modified. The final complete audit exits 0.

Only standard-library parsing, AST expansion, path validation, SHA256 hashing and reviewer-file writes were performed. No product, native dependency, wrapper or test import/execution, database/server action, network access, Git operation, installation, environment read or credential read was performed by the reviewer. No raw tests.json, readiness.json, package-origin.json, postgres-start.json or postgres-stop.json was read, hashed or copied.

This evidence establishes one bounded main source SA21 integration result and its recorded cleanup/restoration. It does not establish every pool or OS descendant is stopped, hostile-driver cancellation completeness, installed-correction compatibility, optional SQLModel coverage, packaging/provenance, independent-host/provider evidence or any production gate. All seven production gates remain UNKNOWN. The seven historical failures stay open. S25 remains the highest accepted working candidate unless the coordinator explicitly accepts a stronger bounded candidate. SA20 can only be considered through its separately gated frozen command after coordinator acceptance of this review; this reviewer executes or authorizes no next cell.

Artifacts: audit-summary.json; exact-outcomes.tsv; node-audit.json; diagnostics.json; warnings-comparison.txt; corpus-diagnostic.json; audit-checks.txt; pin-name-validation.txt; safe-read-paths.txt; terminal-confirmation.json; root-outer-status.json; final and retained earlier audit source/logs; METHOD_CORRECTION.md; REVIEW_FILES.sha256.
