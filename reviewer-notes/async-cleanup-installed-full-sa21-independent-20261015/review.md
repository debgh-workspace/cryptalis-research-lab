# Independent full installed SA21 terminal review

Date: 2026-10-15 UTC.

## Verdict

**ACCEPT_BOUNDED_FULL_SA21_INSTALLED** for the exact completed cleanup217 installed SA21 cell. All 2661 ordinary identities and outcomes equal the accepted cleanup217 source result: 2654 PASS and seven historical FAIL, with no skip or error. All 22 cleanup additions pass; all 56 passing subtests remain separate from ordinary counts. The seven historical failures remain unresolved. This is a bounded installed regression acceptance, not an all-green suite, counterpart/optional result, release approval or production-readiness claim.

No runtime cell was launched by this reviewer. This genuine terminal review is available for the coordinator's separately reviewed SA20 stage gate. It does not itself authorize or select SA20 or optional runtime.

## Exact execution and anchors

Base: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable.

- Packet: experiments/async-cleanup-installed-full-controls-20261015.
- Evidence: evidence/async-cleanup-installed-full-sa21-20261015.
- Audit run: experiments/async-cleanup-installed-full-controls-20261015/run/sa21.
- Exact argv: /bin/bash; the packet's run-full-sa21.sh; sole binding argument 10c8eeb0ab9d632121bd1d0eeffa624639ba7197e219e082ad6c62cc3bdf866e.
- Actual root session: 48756; coordinator selection time 2026-10-15T02:50:27.755561+00:00; actual terminal outer exit 1.
- Binding SHA256: 10c8eeb0ab9d632121bd1d0eeffa624639ba7197e219e082ad6c62cc3bdf866e.
- Entry SHA256: 99d12275f1e18c45797d7035d5f42d75ef3f25637d4850029fcdd92f7bac5ea3.
- Helper SHA256: 3eee13ea4a94277350908217c3a235579a0b68868354c0ee90fcbcb65586b430.
- ENTRY.sha256: 2b2c32091528e11d666399d1260d0c21231418da7c3c07608790a409000b4140; exactly 278 targets.
- INPUTS.sha256: 05e353bb8344ed9b93a4cadc6949b5d70e69aa00e57deb5bac74b120012ef2fe; exactly 882 targets.
- POSTINSTALL_CLEARANCE.sha256: 73857c19170f1e7c1bd5500448afdc067778b0eb4ecc72454cefca99ec7ab679; exactly 93 targets.
- CLEARANCE_SA21.sha256: fe365586a84ac09e64573b0e1c2d78921e3bbbd7793b948bb20190758861ef61; exactly eight targets.
- Accepted SOURCE_COMMAND_REVIEW.md: 4bca9708ae3990a8a1e50a177343f8b467a56d55136f64997b0d9d3c7258ff99.
- Accepted SA21_GATE_ACCEPTANCE.md: 0fb3ba6c655dad856128404f50d548349eba5273074c97fcfaf7fecaf5319edb.
- Accepted SA21_FINAL_ACCEPTANCE.md: 8b0ec6fc8a590697d984ff2617ff481a937f61458414a3f2e4f77d4fe9dfaaab.
- Successful audit-attempt-3.py: c73139a06e1fd87ec8fc08aeb188577062f404f5cdf37c085b35ed45eb3d038c.
- Final attempt-3.audit-summary.json: 25879a1af15daec9f27513870309cbc31f364090f0c227962a8d2743fa839809.

The root's terminal notification preceded all new runtime-payload reads. The retained terminal-confirmation.json pins coordinator selection.json, entry.log and exit.txt. Their exact actual argv, binding, initial helper-admission line, complete initial pre-directory validation map and outer exit were independently checked. The prospective COMMAND_ARGV.json is not used as proof that execution occurred.

## Outcomes, phases and safe diagnostics

All 2661 ordinary JUnit IDs are unique and bijective with progress start events, including class-method identity. They equal the accepted cleanup217 source run in exact order and outcomes, and the original 2639 S25 outcomes plus exactly 22 disjoint new passes. Literal AST expansion of the unchanged new test source matches the 22 frozen node IDs exactly. There are no missing, extra, duplicate, deselected, xfailed, skipped or error outcomes.

All 8039 setup/call/teardown report entries match the complete accepted cleanup217 source multiset, rather than only its totals: 2661 passing setups, 2710 passing calls, seven failing calls and 2661 passing teardowns. The 56 additional passing calls are retained as separate subtest evidence. Every new cleanup node has exactly three passing ordinary phases, for 66 added phases. Runner per-module counts reconcile with the complete progress evidence. The JUnit header's 2717 count includes the 56 subtests and is not the ordinary ID count.

The seven historical failure identities are unchanged in tests/test_deprotection_ordinals.py:

- test_reverse_refuses_unhandled_public_suffix_comment_before_staging
- test_changed_public_staging_refuses_switch
- test_public_copy_participates_in_chunk_byte_bound
- test_reverse_refuses_unhandled_suffix_attributes[column_grant]
- test_reverse_refuses_unhandled_suffix_attributes[statistics]
- test_reverse_refuses_unhandled_suffix_attributes[storage]
- test_reverse_refuses_unhandled_suffix_attributes[compression]

Six retain the exact DID NOT RAISE TransitionFailure diagnostic; one retains the exact NoResultFound diagnostic. Every message and diagnostic body is identical to the accepted source217 map except the one literal native result.py traceback path for test_changed_public_staging_refuses_switch. That path changes from ../release-lab/s25-installed-20261014/sa21/lib/python3.12/site-packages/sqlalchemy/engine/result.py to ../release-lab/async-cleanup-installed-20261015/sa21/lib/python3.12/site-packages/sqlalchemy/engine/result.py. Its line number, code, exception and other text remain unchanged. No general path or traceback normalization was applied.

The terminal pytest summary is 7 failed, 2654 passed, 50 warnings, 56 subtests passed in 398.30s (0:06:38). Runner elapsed time is 399.47916930000065 seconds. All 50 warnings retain the exact accepted source217 bodies: two fork-related DeprecationWarnings and 48 DISTINCT ON SADeprecationWarnings. Only decimal fork-process IDs are normalized. No selected timeout, bounded-cleanup failure, pending-task, unawaited-coroutine, unraisable-exception, thread-exception, RuntimeWarning or new SAWarning marker is present in the safe tests/wrapper/JUnit evidence. Safe full diagnostic and warning bodies are retained in attempt-3.diagnostics.json and attempt-3.warnings-comparison.txt.

## Installed origin, selection and original controls

The sole literal wrapper argv exactly matches the accepted full-main command. It uses --installed-candidate, the fresh release-lab/async-cleanup-installed-20261015/sa21/bin/python interpreter, the original candidate cwd/config, the whole candidate tests directory and only the original test_async_sqlmodel_public_hook.py ignore. The runner receipt preserves that complete selection. There is no narrowed retry, direct pytest call, source overlay or copied console script.

Safe package-origin.log and the wrapper's origin line agree on the actual loaded path:

release-lab/async-cleanup-installed-20261015/sa21/lib/python3.12/site-packages/cryptalis/__init__.py

Both report installed=true, verified=true and 41 byte-matched modules. All 41 installed source-module bytes were independently compared with the accepted source manifest and accepted wheel. The same 41 pins in the SA20 installation remain identical; that is payload identity, not an SA20 runtime result. The wrapper's expected_source field is the comparison source, not its import origin.

Both readiness and tests record fresh dual-role preflights with fingerprints 76053d5b and a38ab71b. The runner receipt independently records select_1_each=passed. The exact source217 identities preserve the original source-free -I -S absence/removal controls in test_deprotection.py and the native worker, together with sys.executable subprocess routing. Their ordinary outcomes are included in the unchanged full map.

Origin is a separate subprocess check combined with byte equality. It does not establish continuous current-pytest, every-subprocess, every-import or historical-bytecode provenance. No stronger imported-code guarantee is inferred from hashes.

## Binding, source, pins and archives

The exact finite union has 886 targets with complete input-role coverage, no conflicting digests and all four manifest target maps matching the accepted binding. The complete non-corpus set was metadata/path/link-admitted before expanded payload hashing. All 860 non-corpus target hashes pass in the full terminal audit. The remaining 26 live corpus targets were independently hash-verified in the frozen shared-state boundary before the coordinator could reuse the lab; the full audit relies on that boundary rather than resampling mutable primaries during subsequent work.

Every packet member, source file, dependency pin, accepted review/receipt and manifest identity matches. Both current source trees retain their exact 217-name non-cache sets. The fresh installed cells retain 82 source-equal module pins, their actual installed RECORD pins, 42 selected dependency-source/METADATA pins, and exactly 14 current METADATA names per cell. Three interpreter routes retain the four exact approved literal symlinks to the approved Python 3.12 endpoint. No secret, environment or cache payload was traversed or read.

The accepted wheel SHA256 is 77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b. Its exact six directory records and 46 regular payload names were metadata-admitted before reading the 41 Python module payloads. Current installed RECORD identity, 51-row scope and accepted hash/size/coverage flags agree with the accepted independent installed-payload audit. This terminal audit relies on that full payload audit for complete installed owned-file RECORD coverage and broader dependency audit; it does not falsely claim to repeat every owned-file digest/size check. The inherited pycparser/iniconfig metadata-versus-lock discrepancies remain unresolved.

Initial pre-directory validation, pre-wrapper helper admission/pins and post-wrapper helper admission/pins all independently succeed. Each helper admission matches the exact reviewed regular-path bytes. Both pin phases exit 0 and retain the exact full 886-target, 278-packet and 26-corpus maps. Actual outer, wrapper and runner exit 1 remain distinct from those successful postchecks. Expected historical-failure exit 1 is not converted to success.

The new frozen-inputs archive contains exactly 283 active packet/manifests/binding files and all 217 complete source files. Every archived byte matches its active accepted identity. The prepared source-archive217 map is preserved and does not substitute for this fresh runtime archive. Main external-source declarations and before/after snapshots are exactly empty and stable. The wrapper's 156 source/config files and every source-repository copy match. The runner's 155 source/test hashes match. They share 154 paths; only the wrapper includes pyproject.toml and uv.lock, and only the runner includes scripts/test_postgres.py. No source-capture set is silently equated with another.

## Corpus restoration and shutdown

The independently completed shared-state-boundary.json has SHA256 83de6ec8f75b9f23776b5ea55dbbd413cab9f2cdd3dff58ca35bfa0d45c0cc3f. It establishes all 26 exact original primary filenames and hashes, all 26 durable prior copies and restored live bytes, the complete generated-archive inventory, errors=[], deleted_during_run=[] and primary_receipts_restored=true. It was sent to the coordinator before any subsequent shared-state reuse. It is a recorded boundary, not continuous live-state attestation.

The only generated archive is master-s4-compatibility-flush-corpus-v1-sa2.1.3.json, SHA256 42755e59b90366c52f4721876484e28bad070bd476540066b65353f40a691e5d. It has exactly 16 unique id/mode records: 12 REJECTED-LOUD and four IDENTICAL. Its complete parsed content equals the accepted source217 full-run corpus, anchored by SHA256 7ab87b55707e2ec8e05b6fd6a0f3fde3561b3cd8dd7fdb5839ef9469530f1bf5, after replacing only the exact 12 terminal operation-token substrings in reason fields. All three token components are hexadecimal; the first is a PID formatted with :x, not decimal. Every other reason character, identity, mode, classification, recovery array, alternative, protected SQL count and scope is identical. The exact compared tokens and full normalized structures are retained. The generated archive remains evidence and was not promoted to a primary.

The safe wrapper phase ledger separately records postgres-start 0, readiness 0, package-origin 0, tests 1 and postgres-stop 0. postgres-stop.log explicitly ends with server stopped. These explicit stop checks are required because the wrapper's main exit does not propagate stop failures. Completion or process disappearance was not used as substitute evidence.

## Reviewer attempts and scope limits

The shared-state boundary passed its first data-only attempt. Full audit attempt 1 stopped on a reviewer ZIP-directory assumption after all input identity checks passed. The coordinator authorized only exact six-directory canonical/type handling, preserving all 46 regular names and the same 41 module checks. Attempt 2 passed all substantive checks but stopped while assembling a summary because two admitted safe ancillary files had not yet been hashed. The coordinator authorized only explicit hashes of postgres-start.log and native-deparser-proof.json. Attempt 3 retains every substantive assertion, writes prefixed new outputs, and exits 0. All previous sources, logs, exit files and generated outputs remain intact; both narrow corrections are documented. No evidence/source/oracle assertion was relaxed, and no runtime evidence was edited.

Only standard-library data parsing, AST inspection, bounded metadata admission, hashing and reviewer-file writes occurred. The reviewer did not execute or import target/helper/product/dependency/test code, collect or run tests, touch DB/server state, install software, use network or Git, or read/hash/copy raw tests.json, readiness.json, package-origin.json, postgres-start.json or postgres-stop.json. No credentials, raw environment dumps or cache payloads were read.

Single-writer validation, recorded quiescence and terminal restoration are not hostile-race, every-pool/OS-descendant, hostile-driver cancellation, independent-host/provider or production guarantees. The seven historical failures remain open. G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE all remain UNKNOWN.

Final artifacts: attempt-3.audit-summary.json, attempt-3.exact-outcomes.tsv, attempt-3.node-audit.json, attempt-3.diagnostics.json, attempt-3.warnings-comparison.txt, attempt-3.corpus-audit.json, attempt-3.path-admission.json, attempt-3.read-hashes.sha256, attempt-3.audit-checks.txt, shared-state-boundary.json, terminal-confirmation.json, all retained attempt files and both method-correction notes. REVIEW_FILES.sha256 records their final review identities.
