# Independent full SA20 source terminal review

Audit date: 2026-10-15 UTC. The directory suffix identifies the 2026-10-14 experiment packet.

Verdict: **ACCEPT_BOUNDED_FULL_SA20_SOURCE** for this exact completed source-integration cell. The complete original S25 main inventory retains its outcomes, failure messages, skip reasons and phase reports; all 22 added cleanup cases pass. The seven historical failures remain unresolved. This is not an all-green suite, installed-correction qualification, optional SQLModel coverage, release approval or production readiness. No subsequent cell was run by this reviewer.

## Exact execution and identity

Command: /bin/bash /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/async-cleanup-full-integration-plan-20261014/run-sa20.sh

- Packet SHA256: 7135f4958e404469a335ffdc5a364154b67284fdfa01380b0873d81e53fb469d.
- Entry SHA256: c0a18d997e27e162c1db1781fd678679cc6012d54a0ac304beb2588359971fc3.
- Clearance SHA256: e06580217479f893051006715cd9a08713c1887b4c69f126ca96010c1ff7e7a6.
- Input manifest SHA256: 55f3ca6716677dd145c63f67a47ba745cd0241f4d41f82f07e447118cb942e1d.
- Accepted source/command review SHA256: 3db0ed2548632ecc11452863578514b6a45f04887eb4692c124363686d6cd8d8.
- Accepted preceding full SA21 review SHA256: 1f7f9acbbc2677d9537dfa5bba83bf2ec4defb34e2e828b5629d9b384c913b38.
- This audit-summary.json SHA256: 8e85f14861c73cad18b052342acbe5e8a2153a038e95db68da20d8d50d188998.
- Final data-only audit_terminal.py SHA256: 3e632059c35213f17b600dfc0c65f77b49adeddcb1664afd965123995bc02c53.

The coordinator reported launch at 2026-10-15T00:40:21Z and observed the terminal outer exit at 00:47:52Z. The retained observation identifies session 63837, terminal tool chunk7653e7, the two-element argv and actual outer exit 1. Its exact bytes are retained in root-outer-status.json, SHA256 909d1b80e0762d71a36c7b89b00c8f0769674e62c4c67a69ba46e335fad68e8e; terminal-confirmation.json records the coordinator authorization. No current mutable SA20 logs, evidence payloads or primary corpus bytes were read or hashed before terminal confirmation. The data-only checker gates all such work on that receipt.

Actual outer, wrapper and runner exits are all 1. Both independent pin phases exit 0. The safe wrapper log records exactly one postgres-start exit 0, readiness exit 0, package-origin exit 0, tests exit 1 and postgres-stop exit 0. postgres-stop.log explicitly ends with server stopped. These are separate checks; neither outer exit 1 nor test completion was used as proof of pin success or shutdown.

## Exact outcomes and diagnostics

There are exactly 2661 unique ordinary testcase identities: 2608 passed, seven failed, 46 skipped and zero errors. Every one of the original 2639 identities and outcomes equals both accepted S25 source and installed SA20 references. The 22 disjoint additions match literal AST expansion of the new test source and the frozen new-node list, and all pass. No original ID is missing, duplicated, deselected or replaced. Expected counts were used only as assertions against parsed terminal evidence, never as a substitute for results.

The seven retained failing tests are in tests/test_deprotection_ordinals.py:

- test_reverse_refuses_unhandled_public_suffix_comment_before_staging
- test_changed_public_staging_refuses_switch
- test_public_copy_participates_in_chunk_byte_bound
- test_reverse_refuses_unhandled_suffix_attributes[column_grant]
- test_reverse_refuses_unhandled_suffix_attributes[statistics]
- test_reverse_refuses_unhandled_suffix_attributes[storage]
- test_reverse_refuses_unhandled_suffix_attributes[compression]

Every failure message is exact against both references. Current failure diagnostic bodies are byte-identical to the S25 installed reference. Relative to the S25 source reference, only two occurrences of one native result.py traceback path change from release-lab/s20-payload-preparation-sa20-20261014 to release-lab/s25-installed-20261014/sa20, within test_changed_public_staging_refuses_switch. The exception, message, code and line numbers are unchanged.

All 46 skipped identities and messages remain exact: 10 native collection API skips, eight session-wide execution-options skips, 12 generic aggregate_order_by skips and 16 distinct_on syntax-extension skips. Each skip diagnostic body differs from both S25 references only by its single leading absolute test-source root: candidate-s25-async-sqlmodel-integration-20261014 becomes candidate-next-unblocked-correctness-20261014. Every line number, reason and remaining byte is exact. These 46 explicit source-root diffs are retained separately from failure diffs in diagnostics.json. No general path or diagnostic normalization was applied.

The 2661 start events form a bijection with ordinary JUnit IDs, including class-method identity. The complete old setup/call/teardown report multisets equal both S25 references. The 22 additions contribute exactly 66 passing ordinary phase reports. There are 8021 phase reports: 2643 passing setups, 18 skipped setups, 2664 passing calls, seven failed calls, 28 skipped calls and 2661 passing teardowns. The 56 passing subtest events remain separate from ordinary IDs. The JUnit suite header reports 2717 because it includes those subtests; it was not used as the ordinary-case count. All per-module runner call counts reconcile with progress evidence; its 28 call skips do not include the 18 setup skips.

Terminal pytest result: 7 failed, 2608 passed, 46 skipped, 2 warnings, 56 subtests passed in 397.02s (0:06:37). Runner elapsed time is 398.2730334420048 seconds.

The two fork-related DeprecationWarnings equal both historical full SA20 runs. Comparison allows only exact candidate-root substitution and decimal process-ID substitution. Original warning bodies are retained. No selected timeout, bounded-cleanup failure, pending-task, unawaited-coroutine, unraisable-exception, thread-exception or RuntimeWarning indicator is present in the safe logs and JUnit.

## Source, selection, pins and archives

All 566 input target names and resolved interpreter destinations were independently validated against bounded path classes before hashing listed payloads. All 566 hashes match. All 29 packet-member hashes and four actual accepted clearance-review hashes match. Both complete pre/post pin logs contain exactly the expected ordered paths, counts and success messages. The clearance is byte-identical before, archived and after; its documents contain the actual accepted verdicts, including the prior full SA21 acceptance.

The 216-file S25 baseline is unchanged. The complete 217-file candidate matches the accepted focused GREEN manifest. Its only changed original file is src/cryptalis/sqlalchemy.py, and its sole addition is tests/test_sqlalchemy_async_exit_double_failure.py. Every original test, fixture, preflight, lock and dependency declaration remains unchanged. Candidate and baseline extra filenames are cache-only (146 and 170); cache bytes were not read or hashed.

All 31 archived packet/anchor/clearance files equal their originals. All 217 complete candidate-source archive files match the candidate manifest. The wrapper's 156 before/after source/config hashes and every corresponding source-repository copy match. All 155 runner source/test hashes match. These inventories share 154 paths: the wrapper alone includes pyproject.toml and uv.lock; the runner alone includes scripts/test_postgres.py. This is the exact unchanged source-capture design, not missing source. Main external before/after snapshots are empty and stable.

The selected interpreter is the existing s25-installed-20261014/sa20 environment, with the pinned Python 3.12 binary, SQLAlchemy 2.0.51 native files and existing distribution metadata. All 14 current METADATA filenames per main dependency environment equal their pinned sets. This is bounded file identity, not a full dependency-file or every-import attestation.

The command and runner receipt select the entire corrected candidate/tests directory, with the sole original optional ignore test_async_sqlmodel_public_hook.py. There is no new selection narrowing, retry, installed-candidate flag or optional coverage claim. Fresh readiness and test preflights both record the two expected role fingerprints. source-root.json and safe package-origin.log identify candidate-next-unblocked-correctness-20261014/src. That separate origin subprocess is not continuous attestation of every pytest subprocess import.

## Corpus restoration and generated evidence

All 26 original corpus primary filenames equal the frozen baseline. Every original primary byte string and durable prior-corpus archive matches its frozen digest. The primary filename set is unchanged. Isolation records errors=[], deleted_during_run=[] and primary_receipts_restored=true. The archive directory contains exactly the one recorded generated file; no unexpected corpus archive is present.

The generated master-s4-compatibility-flush-corpus-v1-sa2.0.51.json has SHA256 a6b05364d9d6d47f088d77dd9cba49d29c1e37ac23948c31c29ec06383554d30. It contains 16 complete unique id/mode records: 12 REJECTED-LOUD and four IDENTICAL. Its complete content agrees with both accepted S25 full-suite archives after replacing only the 12 terminal decimal-hex-hex operation-ID tokens in reason strings. All IDs, modes, classifications, recovery arrays, alternative text, protected SQL counts and scope are otherwise exact. corpus-diagnostic.json retains all three payloads and exact archive hashes. This is retained run evidence; no generated corpus was promoted to a primary.

## Reviewer preparation, execution and limits

The checker was independently adapted from the final corrected SA21 data-only design before this cell terminated. Exact SA20 old maps, skip reasons and phases, warning bodies, native traceback paths and historical full-corpus structure were checked against immutable prior evidence. PREPARATION.md and sa20-adaptation.patch record these differences. The initially prepared but unexecuted source is preserved as audit_terminal.prepared-v1.py; a subsequent pre-execution refinement added the exact leading source-root substitution needed for absolute skip diagnostic paths, with coordinator agreement. No broader failure, warning or operation-ID normalization was introduced.

The accepted SA21 review's earlier failed checker attempts and documented inventory/corpus corrections remain preserved in its original reviewer directory. This SA20 terminal checker ran once, after explicit coordinator terminal confirmation, and exited 0. No failed SA20 audit attempt or runtime retry was discarded. No packet, candidate, source/test expectation, runtime evidence or corpus file was modified.

Only standard-library parsing, AST expansion, path validation, SHA256 hashing and reviewer-file writes were performed. No product, native dependency, wrapper or test import/execution, database/server action, network access, Git operation, installation, environment read or credential read was performed by this reviewer. No raw tests.json, readiness.json, package-origin.json, postgres-start.json or postgres-stop.json was read, hashed or copied.

This evidence establishes one bounded main source SA20 integration result and its recorded cleanup/restoration. Together with the separately accepted full SA21 source cell, it completes the observed corrected-source main-cell pair; coordinator acceptance and any candidate designation remain separate. It does not establish every pool or OS descendant is stopped, hostile-driver cancellation completeness, installed-correction compatibility, optional SQLModel coverage, packaging/provenance, independent-host/provider evidence or any production gate. All seven production gates remain UNKNOWN. The seven historical failures stay open. This reviewer executes or authorizes no next cell.

Artifacts: audit-summary.json; exact-outcomes.tsv; node-audit.json; diagnostics.json; warnings-comparison.txt; corpus-diagnostic.json; audit-checks.txt; pin-name-validation.txt; safe-read-paths.txt; terminal-confirmation.json; root-outer-status.json; audit_terminal.py; audit_terminal.prepared-v1.py; audit-run.log; audit-exit.txt; PREPARATION.md; sa20-adaptation.patch; REVIEW_FILES.sha256.
