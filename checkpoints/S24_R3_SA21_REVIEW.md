# S24 r3 restarted SA21 aggregate: independent terminal audit

## Verdict

The terminal r3 aggregate restores the frozen S23 outcome for every original test. It is **baseline-equivalent, not all green**. The seven pre-existing failures remain open. No production gate is qualified.

- **2,639 ordinary cases:** 2,632 passed, 7 failed, 0 errors, 0 skipped.
- **56 passing subtests**, counted separately; 50 warnings.
- Pytest summary duration: 421.66 seconds. Runner exit: 1, as expected for the seven failures. The stop log confirms `server stopped`.
- The runner receipt's 2,688 passes include the 56 subtests. The JUnit suite total is 2,695, while there are exactly 2,639 distinct JUnit testcase identities. These are different counting levels, not extra ordinary tests.

## Exact comparisons

- Frozen S23 SA21 had 2,638 ordinary cases: 2,631 passed and the same seven failed. Every original identity remains, and every original outcome is unchanged.
- Failed combined r2 had the identical 2,638 identities, with 33 failures. All 26 additional r2 failures now pass.
- The only new identity is `tests.test_doctor_active::test_new_format_malformed_inner_plan_is_rejected_at_constructor_without_raw_error`; it passes.
- The progress log has exactly 2,639 unique starts. Compared with frozen S23, the entire multiset of call reports differs only by one passing report for the new constructor control. There are no nonpassing setup/teardown reports.
- Each historical failure has the same JUnit failure message as frozen S23. The full per-case comparison is in `SA21_EXACT_OUTCOMES_v1.tsv`.

## The seven retained failures

All are in `tests.test_deprotection_ordinals`:

1. `test_reverse_refuses_unhandled_public_suffix_comment_before_staging`
2. `test_changed_public_staging_refuses_switch`
3. `test_public_copy_participates_in_chunk_byte_bound`
4. `test_reverse_refuses_unhandled_suffix_attributes[column_grant]`
5. `test_reverse_refuses_unhandled_suffix_attributes[statistics]`
6. `test_reverse_refuses_unhandled_suffix_attributes[storage]`
7. `test_reverse_refuses_unhandled_suffix_attributes[compression]`

The staging case retains `NoResultFound`; the other six retain `DID NOT RAISE TransitionFailure`. Their test source file is unchanged from frozen S23. This review establishes identity and outcome continuity, not resolution of those obligations.

## Source and masking review

- The final r3 receipt is `worktree-8faa43b3aa46dd11`, on base `2ff72ea4fe7871f31a9fabbbf63f19a5cc714e43`.
- All 153 source/config snapshot entries have identical before/after hashes. The archived source snapshot and live candidate both match. All receipt-pinned source/test files also match the candidate.
- The receipt additionally pins `scripts/test_postgres.py`; the broader snapshot additionally pins `pyproject.toml` and `uv.lock`. Every common hash agrees.
- Against r2, only five test files changed. Runtime source, runner wrapper, pytest configuration and lockfile are unchanged. The edits admit the explicit new retained-native comments format in existing fixture oracles, preserve the synthetic legacy malformed-doctor boundary, and add the separate current-format constructor rejection control.
- No test function was removed: 647 definitions became 648. Skip/xfail decorators are unchanged. The full-suite command targets the candidate's complete tests directory, with no test selector or deselection argument. No runtime skip or xfail masks a regression.
- The synthetic legacy-doctor test is not an old-producer recovery proof. The new constructor test explicitly covers the current-format rejection boundary.

## Evidence closure and corpus isolation

- Terminal JUnit, runner receipt, source-stability, external-source-stability, corpus-isolation and stop-log evidence are all present.
- External-source tracking remained empty and unchanged.
- All 26 prior corpus archives match their pinned hashes. The generated candidate corpus matches its isolation receipt. The receipt reports no deleted corpus, no isolation errors, and restored primary receipts.
- The primary corpus files were independently checked against all 26 prior hashes after terminal cleanup and matched. Later authorized runs may temporarily write their own corpus.
- All seven gates remain `UNKNOWN` in the runner receipt.

## Scope and artifacts

Read-only filesystem analysis of the safe evidence and authorized candidate source; no database or test execution. No raw `tests.json`, `readiness.json`, or `package-origin.json` was opened. No source or evidence was edited. Outputs are confined to this reviewer directory.

- `SA21_AUDIT_v1.json`: machine-readable checks and evidence SHA-256 pins.
- `SA21_EXACT_OUTCOMES_v1.tsv`: all exact ordinary testcase IDs and outcomes.
- `audit_terminal.py`: reproducible evidence-only comparison used for this audit.
