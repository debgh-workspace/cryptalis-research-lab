# Independent full installed SA20 terminal review

Date: 2026-10-15 UTC.

## Verdict

**ACCEPT_BOUNDED_FULL_SA20_INSTALLED** for the exact completed cleanup217 installed SA20 cell. All 2661 ordinary identities and outcomes equal the accepted cleanup217 source result: 2608 PASS, seven historical FAIL, 46 exact SKIP and zero ERROR. All 22 cleanup additions pass. The 56 passing subtests remain separate from ordinary counts. The seven historical failures remain unresolved. This is bounded installed regression acceptance, not an all-green suite, optional result, release approval or production-readiness claim.

No runtime cell was launched by this reviewer. Together with the separately accepted installed SA21 review, this supplies the bounded main installed-cell pair; coordinator acceptance and any candidate designation remain separate. It does not authorize or select optional runtime or another cell.

## Exact execution and anchors

Base: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable.

- Packet: experiments/async-cleanup-installed-full-controls-20261015.
- Evidence: evidence/async-cleanup-installed-full-sa20-20261015.
- Audit run: experiments/async-cleanup-installed-full-controls-20261015/run/sa20.
- Exact actual argv: /bin/bash; the packet's run-full-sa20.sh; sole binding argument 1e747bd9c00c6301994af20d7f2275819e8f6e68eda10a7cfa4bf8b4d52d90a5.
- Root session: 34596; coordinator selection time 2026-10-15T03:09:45.499284+00:00; actual terminal outer exit 1.
- Binding SHA256: 1e747bd9c00c6301994af20d7f2275819e8f6e68eda10a7cfa4bf8b4d52d90a5.
- Entry SHA256: 6fd61b3c4ed84279b47403f77e7f6b2ee428adbf78e2725b13bf6192769f72d4.
- Helper SHA256: 3eee13ea4a94277350908217c3a235579a0b68868354c0ee90fcbcb65586b430.
- ENTRY.sha256: 2b2c32091528e11d666399d1260d0c21231418da7c3c07608790a409000b4140; exactly 278 targets.
- INPUTS.sha256: 05e353bb8344ed9b93a4cadc6949b5d70e69aa00e57deb5bac74b120012ef2fe; exactly 882 targets.
- POSTINSTALL_CLEARANCE.sha256: 73857c19170f1e7c1bd5500448afdc067778b0eb4ecc72454cefca99ec7ab679; exactly 93 targets.
- CLEARANCE_SA20.sha256: 1248b82b85ca786b33425779bbd6028128505501bf3f24c23d8cef28ffbf6a3d; exactly nine targets.
- Accepted SOURCE_COMMAND_REVIEW.md: 4bca9708ae3990a8a1e50a177343f8b467a56d55136f64997b0d9d3c7258ff99.
- Accepted SA20_GATE_ACCEPTANCE.md: 246f251bdabd6103faaaf94ae8acb25b2347d2ea76536e4dc2cd4675a1c02346.
- Accepted SA20_FINAL_ACCEPTANCE.md: d2c0b80429efdfa9b1c9a92784440b395cd0761fca28bee0d795d5c349a8e23b.
- Genuine preceding installed SA21 review: fe5427ac4fb49231e17a9ac862d931e25c4680d505bf217259d633e1a7f69e60.
- Successful audit-attempt-2.py: 40cc99e9f9c07ae97ab336b4393922e12e455d16405ac7b3d01258b9c07a7865.
- attempt-2.audit-summary.json: 8c1990b838228925d980948443b04e52a95d8bff7527c57a6d7c63ac84a417e1.

The root's terminal notification preceded every current run/evidence payload read and live corpus read. The retained terminal-confirmation.json has SHA256 2b289d78cc740508e086e88da7e6738cbb49173a4cfa7e0d606c7e46111a6ecb. It pins coordinator selection.json, entry.log and exit.txt and preserves the root's explicit terminal observation. Actual argv, binding, the initial helper-admission line, the complete initial pre-directory validation map and outer exit were independently checked. Prospective COMMAND_ARGV.json is not used as evidence that execution occurred.

## Outcomes, phases and safe diagnostics

All 2661 ordinary JUnit IDs are unique and bijective with progress start events, including class-method identity. They equal the accepted cleanup217 source run and the original 2639 S25 outcome map plus exactly 22 disjoint new passes. Literal AST expansion of the unchanged new test source matches the 22 frozen node IDs exactly. There are no missing, extra, duplicate, deselected, xfailed or error outcomes. Exact start identity and order match the source217 reference.

Every one of the 8021 setup/call/teardown reports matches the complete accepted source217 multiset, not just its totals:

- Setup: 2643 PASS and 18 SKIP.
- Call: 2664 PASS, seven FAIL and 28 SKIP.
- Teardown: 2661 PASS.

The 56 additional passing calls are retained as separate subtest evidence. Each setup-skipped case has no call report; all new cleanup nodes have exactly three passing ordinary phases, for 66 added phases. Runner per-module counts reconcile with the complete progress map. Its 28 call skips do not include the 18 setup skips. The JUnit header's 2717 count includes 56 subtests and is not the ordinary ID count.

The seven historical failing identities remain in tests/test_deprotection_ordinals.py:

- test_reverse_refuses_unhandled_public_suffix_comment_before_staging
- test_changed_public_staging_refuses_switch
- test_public_copy_participates_in_chunk_byte_bound
- test_reverse_refuses_unhandled_suffix_attributes[column_grant]
- test_reverse_refuses_unhandled_suffix_attributes[statistics]
- test_reverse_refuses_unhandled_suffix_attributes[storage]
- test_reverse_refuses_unhandled_suffix_attributes[compression]

All failure messages and diagnostic bodies equal the accepted source217 map except two occurrences of one literal native result.py traceback path in test_changed_public_staging_refuses_switch. The prefix changes from ../release-lab/s25-installed-20261014/sa20 to ../release-lab/async-cleanup-installed-20261015/sa20. Native result.py line numbers 1518 and 799, code, exception, message and every other character remain unchanged. No general path or traceback normalization was applied.

All 46 skipped identities, messages and full diagnostic bodies equal source217 exactly: 10 native collection API skips, eight session-wide execution-options skips, 12 generic aggregate_order_by skips and 16 distinct_on syntax-extension skips. No skip-body path substitution is needed because both runs use the same candidate test root.

Terminal pytest summary: 7 failed, 2608 passed, 46 skipped, 2 warnings, 56 subtests passed in 392.36s (0:06:32). Runner elapsed time is 393.57443906599656 seconds. Both fork-related DeprecationWarning bodies equal accepted source217 after replacing only decimal fork-process IDs. There are no DISTINCT ON SADeprecationWarnings in this cell. No selected timeout, bounded-cleanup failure, pending-task, unawaited-coroutine, unraisable-exception, thread-exception, RuntimeWarning or new SAWarning marker appears in the safe tests/wrapper/JUnit evidence. Complete diagnostics and warning comparisons are retained.

## Installed origin, selection and gates

The sole literal wrapper argv equals the accepted full-main command. It uses --installed-candidate, the fresh release-lab/async-cleanup-installed-20261015/sa20/bin/python interpreter, the original candidate cwd/config, the whole candidate tests directory and only the original test_async_sqlmodel_public_hook.py ignore. The actual runner receipt preserves that complete selection. There is no narrowed retry, direct pytest substitution, source overlay or copied console script.

Safe package-origin.log and the wrapper's origin line agree on release-lab/async-cleanup-installed-20261015/sa20/lib/python3.12/site-packages/cryptalis/__init__.py. Both report installed=true, verified=true and 41 byte-matched modules. All 41 installed module bytes were independently compared with the accepted source manifest and accepted wheel. The same 41 pins in the SA21 installation remain identical; its runtime acceptance is supplied by its separate genuine terminal review. The wrapper's expected_source field identifies comparison source, not import origin.

Readiness and tests independently record fresh dual-role preflights with fingerprints 76053d5b and a38ab71b; the runner receipt records select_1_each=passed. Unchanged full source and outcome maps preserve the original source-free -I -S absence/removal controls in test_deprotection.py and the native worker, with sys.executable subprocess routing.

The exact nine clearance targets and all six accepted review roles are retained, including source SA21, source SA20, packaging, closed installed payload, final command review and genuine completed installed SA21 terminal review. The final SA20 gate's actual accepted verdict and exact hash are checked independently; draft wording in the binding's inherited notes is not used as authority. Both prior SA21 gate hashes remain exact current controls.

Origin is a separate subprocess check combined with byte equality. It does not establish continuous current-pytest, every-subprocess, every-import or historical-bytecode provenance. No stronger imported-code guarantee is inferred from hashes.

## Binding, source and archive identity

The exact finite union has 887 targets with complete input-role coverage, no conflicting digests and all four current-stage manifest maps equal to the accepted binding. All 861 non-corpus target hashes pass after complete bounded metadata/path/link admission. The 26 live corpus targets were independently hash-verified in the earlier shared-state boundary; this audit did not resample mutable primaries after closing those reads.

Both current source trees retain their exact 217-name non-cache sets and accepted bytes. The fresh installed cells retain 82 source-equal module pins, both actual installed RECORD pins, 42 selected dependency-source/METADATA pins and exactly 14 current METADATA names per cell. Three interpreter routes retain four exact approved literal symlinks to the approved Python 3.12 endpoint. No secret, environment or cache payload was traversed or read.

The accepted wheel SHA256 is 77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b. Its exact six directory records and 46 regular payload names were metadata/type-admitted before reading the 41 runtime Python module payloads. Those module hashes equal installed and source bytes. Current installed RECORD identity, 51-row scope and accepted hash/size/coverage flags agree with the separate accepted installed-payload audit. This terminal audit relies on that complete payload audit for all owned-file RECORD coverage and broader dependency verification; it does not claim to repeat every owned-file digest/size check. Inherited pycparser/iniconfig metadata-versus-lock discrepancies remain unresolved.

Initial pre-directory validation, pre-wrapper helper admission/pins and post-wrapper helper admission/pins all independently succeed. Each helper admission matches the exact reviewed regular-path bytes. Both pin phases exit 0 and retain the full 887-target, 278-member packet and 26-corpus maps. Actual outer, wrapper and runner exits are separately 1. Expected historical-failure exit 1 is not converted into success.

There are exactly 285 active control/source files. The pinned archiver intentionally captures the current stage's 283 files: 278 immutable packet members, four current-stage manifests and BINDING_SA20.json. Every one of those archived bytes equals its active accepted identity. BINDING_SA21.json and CLEARANCE_SA21.sha256 are the two active-only prior-stage controls; their current exact hashes are independently checked, but they are not falsely claimed as members of this archive. The archive also contains all 217 complete source files. SOURCE_ARCHIVE217.json retains the prepared source map and does not substitute for the fresh runtime archive.

Main external-source declarations and before/after snapshots are exactly empty and stable. Every wrapper source-repository copy matches its 156-file source/config snapshot. All 155 runner source/test hashes match. The capture sets share 154 paths: the wrapper alone has pyproject.toml and uv.lock; the runner alone has scripts/test_postgres.py. These separate capture sets are not silently equated.

## Corpus restoration and explicit shutdown

The independent shared-state-boundary.json has SHA256 5b0360701f9b38027f69aaef35ff5d417fdb232533769cfe7cdc31183d80f644. Before any subsequent shared-lab reuse, it established all 26 exact original primary names and hashes, all 26 durable prior copies and restored live bytes, the complete generated-archive inventory, errors=[], deleted_during_run=[] and primary_receipts_restored=true. The acceptance and live-read closure were reported immediately to the coordinator. This is a recorded boundary, not continuous live-state attestation.

The only generated archive is master-s4-compatibility-flush-corpus-v1-sa2.0.51.json, SHA256 7b26dfcb79ff8f4758aba67af9b12f7b2ba24893b1e58025a88677399d98e6d1. It has exactly 16 unique id/mode records: 12 REJECTED-LOUD and four IDENTICAL. Its complete parsed content equals the accepted source217 corpus, SHA256 a6b05364d9d6d47f088d77dd9cba49d29c1e37ac23948c31c29ec06383554d30, after replacing only the exact 12 terminal operation-token substrings in reason fields. All three components are hexadecimal; the first is a PID formatted with :x, not decimal. Every other reason character, identity, mode, classification, recovery array, alternative, protected SQL count and scope is identical. Exact tokens and complete normalized structures are retained. The archive remains run evidence and was not promoted to a primary.

The safe wrapper phase ledger separately records postgres-start 0, readiness 0, package-origin 0, tests 1 and postgres-stop 0. postgres-stop.log explicitly ends with server stopped. Explicit stop checks are required because the wrapper's main exit does not propagate stop failures. Completion or process disappearance was not used as substitute evidence.

## Attempts, read ledger and limits

The accepted installed SA21 audit's failed attempts 1 and 2, final attempt 3 and both narrow correction notes are retained unchanged in their original directory and copied here with predecessor-sa21 prefixes. The inherited exact ZIP directory/type rule and explicit ancillary-read ledger fix were incorporated before this SA20 run's evidence was read.

The shared-state boundary passed its first attempt. Full SA20 attempt 1 passed the input, installed-payload and guard checks, then stopped because the reviewer had incorrectly equated active285 with the pinned archiver's current-stage283 capture. Its source, log, exit and diagnostic inventory are preserved. After explicit coordinator authorization, attempt 2 changed only that archive set/count and accurate reporting, retained active285 and both prior-stage gate checks, used separate output names and exited 0. METHOD_CORRECTION_ARCHIVE_SCOPE.md and the exact patch document this change. No runtime diagnostic normalization or substantive evidence expectation was loosened; no evidence, archive or source was edited. The initial unexecuted preparation version is also retained.

The successful full audit ledger contains 1592 safe payload identities. postgres-start.log and native-deparser-proof.json were explicitly metadata-admitted and hashed before their identities entered the summary. The separate boundary ledger includes the exact live primary reads. Only standard-library data parsing, AST inspection, metadata admission, hashing and writes inside this reviewer directory occurred. No product/helper/dependency/test execution or import, test collection, database/server action, installation, network or Git operation occurred. Raw tests.json, readiness.json, package-origin.json, postgres-start.json and postgres-stop.json were not read, hashed or copied; neither were credentials, raw environment dumps or cache payloads.

Single-writer validation, recorded quiescence and terminal restoration do not establish hostile-race resistance, every-pool/OS-descendant shutdown, hostile-driver cancellation completeness, independent-host/provider evidence or production readiness. Seven historical failures remain open. G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE all remain UNKNOWN.

Final artifacts include attempt-2.audit-summary.json, attempt-2.exact-outcomes.tsv, attempt-2.node-audit.json, attempt-2.diagnostics.json, attempt-2.warnings-comparison.txt, attempt-2.corpus-audit.json, attempt-2.path-admission.json, attempt-2.read-hashes.sha256, attempt-2.audit-checks.txt, shared-state-boundary.json, terminal-confirmation.json, both retained full attempts, the archive correction note and inherited predecessor materials. REVIEW_FILES.sha256 records final reviewer-file identities.
