# S24 r3 SA20 aggregate: independent terminal audit

## Verdict

The SA20 terminal run is **baseline-equivalent, not all green**. Every frozen S23 SA20 ordinary testcase remains with the same outcome. The separate new constructor control passes. The same seven historical failures remain open; no production gate is qualified.

- **2,639 ordinary cases:** 2,586 passed, 7 failed, 46 skipped, 0 errors.
- **56 passing subtests**, counted separately; 2 warnings.
- Pytest summary duration: 419.88 seconds. Runner exit: 1. The stop log confirms `server stopped`.
- Frozen S23 SA20 had 2,585 passed, the same 7 failed, and the same 46 skipped across 2,638 ordinary cases.

## Exact-ID findings

- No original testcase was removed, renamed, or changed to a different outcome.
- All 46 skipped IDs and their JUnit skip reasons match the frozen SA20 baseline exactly. No new skip was added.
- The seven failure IDs and all their failure messages match the frozen SA20 baseline. They are the same seven deprotection-ordinal failures listed in `SA21_REVIEW_v1.md`.
- All 26 additional failure IDs from the failed SA21 r2 aggregate pass in SA20 r3 as well. This is a cross-cell corroboration; the exact SA20 baseline comparison uses the original SA20 run.
- The only additional testcase is `tests.test_doctor_active::test_new_format_malformed_inner_plan_is_rejected_at_constructor_without_raw_error`; it passes.
- Across 2,639 unique progress starts, the complete multiset of call reports differs from frozen S23 only by the new constructor test's one passing report.

## Count reconciliation

JUnit and the pytest summary are the authoritative ordinary-case totals here. The runner receipt counts call reports, so it records:

- 2,642 passes = 2,586 ordinary passes + 56 passing subtests.
- 7 failures.
- 28 call-phase skips.

A further **18 tests skip during setup**, giving **46 total skipped ordinary cases**. The progress log proves this split. There are 2,677 call reports across 2,621 distinct call-stage identities, an excess of 56 passing subtest reports. JUnit's suite total of 2,695 includes those 56 subtests; its 2,639 distinct testcase elements give the ordinary total. No result is missing merely because the runner receipt omits setup skips.

## Source and closure

- Final source revision: `worktree-8faa43b3aa46dd11`, identical to the audited SA21 r3 source.
- All 153 source/config snapshot entries are stable and match the archived snapshot and candidate. All 152 runner source/test pins also match.
- The five r3 test-file changes, one added test definition, unchanged runtime/configuration, unchanged skip/xfail decorators, and lack of collection/deselection changes are independently checked in `SA20_AUDIT_v1.json`.
- All terminal evidence is present. External-source tracking is empty and stable.
- All 26 prior corpus archives and primary corpus files match their hashes after cleanup. The one generated SA20 candidate corpus is archived with its matching isolation hash. No isolation error or deletion is recorded.
- The seven production gates remain `UNKNOWN`.

## Artifacts and scope

- `SA20_AUDIT_v1.json`: checks, count reconciliation, and input SHA-256 pins.
- `SA20_EXACT_OUTCOMES_v1.tsv`: exact IDs across frozen S23 SA20, failed r2 SA21, and terminal r3 SA20.
- `audit_terminal.py`: reusable evidence-only audit logic, including setup/call skip accounting.

No database or test execution. No candidate source or evidence edits. Raw `tests.json`, `readiness.json`, and `package-origin.json` were not opened. Outputs are confined to this reviewer directory.
