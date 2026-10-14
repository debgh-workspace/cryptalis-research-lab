# Async cleanup correction: deferred full source integration

Status: PROPOSED, NOT EXECUTED, NOT INDEPENDENTLY REVIEWED. S25 remains the highest accepted working candidate. This packet does not promote a feature, change a checklist, authorize a new runtime action, or qualify installed/release artifacts.

## Entry conditions and sequence

The coordinator must first accept independent terminal audits of BOTH focused GREEN runs in experiments/next-unblocked-correctness-20261014. Before packet freeze, both focused terminal audits were accepted as ACCEPT_BOUNDED_GREEN: SA21 46 passes in4.43 seconds; SA20 46 passes in4.55 seconds. FOCUSED_ENTRY_EVIDENCE.json identifies the exact safe reviews; their reviews, summaries and node audits are pinned. These are bounded focused results only. An accepted focused result alone does not qualify this full matrix.

After independent source/command review of this packet, the order is:

1. Main source SA21. Stop for independent complete terminal audit.
2. Main source SA20. Stop for independent complete terminal audit.
3. Optional SQLModel38 only after separate overlay source/command review and coordinator clearance. Stop for independent complete terminal audit.

Run one run-*.sh entry at a time. No script starts the next entry. No test/database/runtime/import/installation command was executed by the preparer. No new environment, installation, package version, credentials, database role, cluster, runner, plugin, timeout or network access is proposed.

## Exact source and integration boundary

Candidate: candidate-next-unblocked-correctness-20261014, 217 manifest files. Parent: candidate-s25-async-sqlmodel-integration-20261014, 216 files. The sole changed original file is src/cryptalis/sqlalchemy.py. The sole added file is tests/test_sqlalchemy_async_exit_double_failure.py with 22 statically enumerated cases. Every original test, optional helper, fixture, preflight, dependency declaration/lock and configuration remains unchanged. SOURCE_DELTA.patch and the two complete source manifests bind this boundary. Only this new packet and its separate optional evidence packet are written.

Both main commands select the complete candidate/tests directory and explicitly ignore only tests/test_async_sqlmodel_public_hook.py, exactly the original declared optional applicability boundary. No new filter, xfail, deselection, assertion change or historical-failure waiver is introduced. Optional38 is neither 38 passes nor 38 skips in the unsupported main cells.

The main commands reuse release-lab/s25-installed-20261014/{sa21,sa20}/bin/python without activation or installation. They intentionally OMIT --installed-candidate. The unchanged corpus-v2 wrapper selects the corrected candidate/src; safe package-origin.log must identify the correction source tree. The old installed S25 product remains untouched and is not the product under test. Existing main interpreters use Python3.12, SQLAlchemy2.1.3 or2.0.51, psycopg3.3.6; exact interpreter targets, selected native SQLAlchemy source and all existing distribution metadata are pinned without import. These pins establish their bounded file identity, not a full dependency-file or every-import attestation.

## Expected matrix, not results

Each main cell selects 2661 ordinary IDs: the complete2639 S25 main inventory plus22 added cleanup IDs. Full expected maps are EXPECTED_SA21_OUTCOMES.tsv and EXPECTED_SA20_OUTCOMES.tsv. Original maps are separately retained and checked against accepted S25 source and installed JUnit.

- SA21:2654 ordinary passes,7 historical failures,0 skips/errors;56 passing subtest events separately. Runner passing call count would be2710. Expected actual wrapper/runner exit remains1.
- SA20:2608 ordinary passes,7 historical failures,46 skips,0 errors;56 passing subtest events separately. Preserve18 setup skips and28 call skips, with their exact reasons. Runner passing call count would be2664 and call-phase skip count28. Expected actual wrapper/runner exit remains1.
- Main total:5322 ordinary case instances,5262 passes,14 failure instances,46 skips;2661 distinct ordinary IDs.112 passing subtest events remain separate.
- If separately qualified optional38 passes, the three-cell total would be5360 ordinary instances,5300 passes,14 failure instances,46 skips,2699 distinct semantic IDs. This is not one2699-node run in the optional environment. It is not installed qualification. Targeted3 overlaps core36 and adds no new optional IDs; core36 plus disjoint DML2 is38.

JUnit suite test counters include subtests in these historical runs; count ordinary testcase elements/IDs explicitly. Do not count runner call reports or suite header counters as ordinary cases.

All seven historical failures remain selected, unresolved and visible in both main cells. S25_SA21_DIAGNOSTICS.json and S25_SA20_DIAGNOSTICS.json preserve exact messages and original source diagnostic text. The required comparison is exact failure/skip messages and semantic diagnostics. Absolute source paths in traceback text differ across source/installed/candidate runs; do not hide a semantic failure change by normalizing everything. Retain raw safe diagnostic text and explain any path-only difference. Unexpected additional failures, missing IDs, changed old outcomes/messages, or extra skips require STOP, not an updated expected map.

## Unchanged lab containment

The entry is the existing lab_session_corpus_v2.py, with unchanged corpus_artifacts_v2.py, toolchain/lab_progress.py, toolchain/run_baseline.py, and byte-identical scripts/test_postgres.py. Its exclusive nonblocking lab-session lock, fresh private-URL reload and dual-role preflights, source origin check, test supervision, server shutdown and corpus restoration are unchanged. Do not run pytest directly, bypass preflight, substitute credentials/roles, create another cluster, terminate backends, increase the timeout or retry automatically.

The existing wrapper bounds the test subprocess to600 seconds, other subprocess phases to90 seconds, and supplies180-second faulthandler diagnostics. These are not guarantees about every descendant or hostile driver. If a timeout, missing terminal receipt, failed shutdown, pending cleanup or source drift occurs, stop and inspect the retained evidence through allowed safe files. Never treat disappearance of a process as successful cleanup.

## Fresh destinations and capture

- SA21 evidence: evidence/async-cleanup-full-integration-sa21-20261014; command logs and full source copies: this packet/run/sa21.
- SA20 evidence: evidence/async-cleanup-full-integration-sa20-20261014; command logs and full source copies: this packet/run/sa20.
- Optional evidence and packet are specified in OPTIONAL_SQLMODEL.md.

All were absent at preparation. Existing evidence or run destinations cause refusal; do not delete/overwrite them to retry. A new attempt requires a separately reviewed new destination and reason.

verify_frozen.py is a data-only helper. It validates ALL manifest target names and symlink destinations before hashing any listed payload. It pins the complete216/217 source inventories, native source/metadata/interpreters, unchanged wrapper/preflight, explicitly selected safe S25 reference evidence/reviews and26 original corpus files. It never expands historical evidence inventories. Before a run it archives every sealed packet file, the additive reviewer clearance, and all217 candidate files, including non-Python fixture/example/documentation bytes that the unchanged wrapper does not archive. The wrapper separately archives its156 current source/config entries and emits runner source/test pins. All post-run pins and the exact actual wrapper status are retained separately.

CORPUS_BASELINE.json freezes the26 current original primary corpus artifacts. Require the wrapper to preserve their name set and original bytes, retain pre-run originals, archive each generated/changed artifact and restore the original primaries. A generated archive is run evidence, not promotion of a primary corpus. Every isolation error, deletion or absent restoration is a blocker.

## Additive clearance files

No clearance is fabricated in preparation. Independent reviewers/coordinator add CLEARANCE_MAIN_SA21.sha256 and then CLEARANCE_MAIN_SA20.sha256 only after the corresponding required reviews actually exist. These are evidence bindings under the already required review sequence, not new user authorization or substitute approval. Each line is SHA256, two spaces, then an absolute safe reviewer artifact path. The verifier admits only regular safe .md/.json/.txt/.tsv files in reviewer-notes/async-cleanup-*-20261014 and refuses raw phase JSON or secret/environment names.

SA21 clearance must bind both focused GREEN terminal reviews/audits and the full integration source/command review. SA20 clearance must bind those same accepted reviews plus the completed full SA21 terminal audit. The coordinator records the exact clearance manifest digest before running its entry and retains it with the source review. Rehash and archive the same clearance before/after; a later replacement is not the same reviewed execution. Clearance contents must be checked for the actual verdict and scope, not inferred merely from their presence.

## Security and claims boundary

Never read, hash, parse, copy, archive or publish raw tests.json, readiness.json, package-origin.json, postgres-start.json or postgres-stop.json. Never read credential files, secrets or environment dumps. The unchanged wrapper may generate its pre-existing raw phase files; this packet does not consume or package them. Use tests.log, readiness.log, package-origin.log, postgres-start.log, postgres-stop.log, safe outer wrapper logs, runner-receipt.json, source/corpus manifests, JUnit and progress only after path validation. INPUTS.sha256 and any existing manifest are not general traversal or publication authority.

All seven production gates remain UNKNOWN: G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY, G-RELEASE. All seven historical failures remain open. Focused or full source results do not establish natural DBAPI-fault equivalence, provider/independent-host qualification, full optional cross-module qualification, changed version admission, installed correction qualification, packaging provenance or production readiness.
