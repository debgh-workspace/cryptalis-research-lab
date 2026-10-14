# S22 full SA21 independent evidence review

2026-10-14 UTC. No blocking discrepancy found in the completed source-overlay full-suite evidence. This does not establish a green full suite, installed qualification, comprehensive Python analysis, or production readiness. All seven release gates remain UNKNOWN.

## Counts and delta

Terminal summary: 2623 passed, 7 failed, zero skipped, 56 passed subtests, 50 warnings, 407.51 seconds. Actual JUnit testcase elements independently give 2623 passes and 7 failures, with no errors/skips. Progress has 2630 starts, 2630 passing setups and teardowns, 2679 passing calls and 7 failed calls. The 56 excess passing calls are the separately reported subtests. JUnit suite tests=2686 includes those subtests; there are 2630 top-level testcase elements.

Every S21 SA21 testcase retains exactly its previous outcome. There are no removed prior IDs or outcome changes. Exactly 98 cases are added and pass: 78 statement-binding cases and 20 NamedExpr cases. The seven unchanged failures remain in tests/test_deprotection_ordinals.py:

- test_reverse_refuses_unhandled_public_suffix_comment_before_staging
- test_changed_public_staging_refuses_switch
- test_public_copy_participates_in_chunk_byte_bound
- test_reverse_refuses_unhandled_suffix_attributes[column_grant]
- test_reverse_refuses_unhandled_suffix_attributes[statistics]
- test_reverse_refuses_unhandled_suffix_attributes[storage]
- test_reverse_refuses_unhandled_suffix_attributes[compression]

## Provenance and stability

The safe package-origin log identifies candidate-s22-scanner-20261014/src/cryptalis/__init__.py and reports verified true. The source-root receipt identifies the same candidate and records preflight_unchanged true. This is source-overlay execution, not an installed package test.

All 151 executable/test/build entries in the run's before/after inventory are unchanged; they also independently match the current source. All 212 preparation-manifest hashes independently match the current source after completion. scripts/test_postgres.py and tests/conftest.py remain byte-identical to frozen S21. The prior composition review established that all S21 files are retained and only the scanner and two added test files differ. No test weakening is present in that composition.

The shutdown log reports that the server stopped. Root reports postgres-stop exit zero; this reviewer corroborated the shutdown text, not an independently extracted numeric exit code. Historical dependency provenance is not established by the SA21 label alone.

## Artifacts and limits

SA21_AUDIT.json contains exact counts, failure IDs, unchanged prior-outcome comparison, added-case breakdown, origin, preparation/source checks, and hashes of safe evidence files. No tests, database operations, Git operations, or candidate edits were performed by this reviewer. No tests.json, package-origin.json, environment, or credential files were read. Only separate reviewer artifacts were written. Other dependency-cell results, installed tests, and remote restoration require separate evidence and are not inferred here.
