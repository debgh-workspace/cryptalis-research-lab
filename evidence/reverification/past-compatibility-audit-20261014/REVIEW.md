# Independent bounded S20 compatibility evidence audit

Date: 2026-10-14, approximately 14:45 UTC. Source/evidence review only.

## Result

The checklist's S20 headline counts and unchanged seven failures are supported by the saved logs and JUnit. Two receipt-accounting limits need explicit preservation: the runner receipt omits 18 SQLAlchemy 2.0 skips, and its external-source stability comparison has empty inventories. Neither invalidates the observed test outcomes. Neither establishes complete compatibility or release qualification.

No project code, tests, database commands, installs, network or Git operations ran. Only bounded reads, standard-library evidence parsing/hashing, and this additive report were performed. No tests.json, package-origin.json, environment or credential files were opened. No candidate source was edited.

## Exact outcome reconciliation

Sources: evidence/s20-installed-full-sa21-20261014 and evidence/s20-installed-full-sa20-20261014; exact file digests are in SOURCE_PINS.json.

| Cell | tests.log terminal summary | runner-receipt counts | JUnit |
|---|---|---|---|
| SA2.1 | 2337 passed, 7 failed, 50 warnings, 56 subtests passed; 384.67 s | 2393 passed, 7 failed; exit 1 | 7 failures, 0 errors, 0 skips; 2344 testcase elements; tests attribute 2400 |
| SA2.0 | 2291 passed, 7 failed, 46 skipped, 2 warnings, 56 subtests passed; 374.40 s | 2347 passed, 7 failed, 28 skipped; exit 1 | 7 failures, 0 errors, 46 skips; 2344 testcase elements; tests attribute 2400 |

The 56-count pass difference is exactly the separately reported subtests. The JUnit suite tests attribute also includes those 56, although there are only 2344 testcase elements. Do not compare these count conventions without normalization.

The runner's SA2.0 skipped count is 18 below the log and JUnit. JUnit identifies 10 skipped async collection-method cases, 8 session-execution-option cases, and 28 textual-clause cases. The runner module inventory contains only the latter 28 skips. The saved skip reasons explicitly identify native API availability. The same runner discrepancy exists in S19: its SA2.0 receipt records 28 skips while its log records 46. This is a historical aggregate-reporting defect, not evidence that cases were secretly executed, removed or newly skipped.

The checklist correctly uses log-level 2337/2291 passes, 56 subtests and 46 skips. Current S20 entries do not give a warning count. If warning counts are added, use 50 for SA2.1: two fork deprecations plus 48 DISTINCT ON deprecations; SA2.0 has the two fork deprecations. Do not carry an older two-warning-only statement forward to SA2.1 S20.

## Seven failures independently matched

All seven failure summary IDs are byte-identical between S19 and S20 in each dependency cell. JUnit identifies the same seven S20 failures, all in tests/test_deprotection_ordinals.py:

1. test_reverse_refuses_unhandled_public_suffix_comment_before_staging
2. test_changed_public_staging_refuses_switch
3. test_public_copy_participates_in_chunk_byte_bound
4. test_reverse_refuses_unhandled_suffix_attributes[column_grant]
5. test_reverse_refuses_unhandled_suffix_attributes[statistics]
6. test_reverse_refuses_unhandled_suffix_attributes[storage]
7. test_reverse_refuses_unhandled_suffix_attributes[compression]

The failing test module hash is unchanged in the S19/S20 receipts and current S20 source: 4855458d1b0847c353accab010b8521cc7374601f272340df8b2367ea8ea9cd5. This supports unchanged test identity/source. It does not by itself resolve whether an old expectation or implementation must change; no failure is waived.

S19 logs record 2282/2236 passes, seven failures, 56 subtests and 46 SA2.0 skips. Thus the S20 pass increase is exactly 55 in each cell. It is an observed added passing slice, not completion of previously failing removal capabilities.

## Source/provenance reconciliation

- Each S20 source-before inventory contains 147 source/test/config paths. Every current S20 byte hash matches; the saved before and after mappings are exactly equal.
- Runner source_test_sha256 and source-before agree on every shared path. Their scope differs: the runner includes scripts/test_postgres.py and excludes pyproject.toml/uv.lock; source-before includes the latter two and excludes the wrapper. The current S20 wrapper also matches its recorded runner hash. This is an inventory-scope distinction, not source drift.
- Both runner receipts identify worktree-1a0fe83a117f3c96, return exit 1, and retain all seven qualification gates UNKNOWN. The saved preflight states select_1_each passed. This audit does not run or independently repeat a role probe.
- Both external-source-stability.json files contain before={}, after={}, unchanged=true. This is a vacuous comparison. Checklist wording such as 'source/external stable' must not imply nonempty external-application or dependency-source attestation from these receipts.
- These are present source-byte comparisons and recorded execution observations. They do not prove exact historical imported bytecode, clean-machine dependency identity, production custody, or independent security qualification. The checklist's existing installed-lock/provenance gap remains open. This audit did not inspect installed-origin or dependency metadata.

## Actionable disposition

1. Preserve checklist counts; do not relabel S20 a green full suite.
2. Add the runner aggregate skip limitation and empty external-source inventory qualification to evidence summaries where those receipts are used. Do not overwrite historical receipts.
3. A future reporting-only correction can reconcile setup/collection skips and distinguish top-level passes from subtests using preserved receipts; rerunning S20 tests is unnecessary merely to repair summary presentation. Any executable change requires its own bounded question/review.
4. Do not treat the unchanged seven legacy failures as waived or as evidence of complete native/remove compatibility. Source hashes establish continuity, not feature completion.

## Separate source-inferred OPEN defect retained

Assignment-expression rebinding remains OPEN and unexecuted. In candidate-compat-binding-20261014/src/cryptalis/manifest/compatibility.py, Assign/AnnAssign are handled at lines 220–231, but NamedExpr has no visitor. Supplied source that imports sqlalchemy.delete, then executes a syntactic assignment expression `(delete := custom_callable)`, then calls delete can be falsely attributed to SQLAlchemy by lines 288–295. Contract docs/compatibility.md:261 and the existing rebound-import oracle require an UNRESOLVED finding. This is a source inference, not a reproduced runtime result. No fix was made during the in-flight S21 tests. It is separate from the historical S20 evidence recheck above.
