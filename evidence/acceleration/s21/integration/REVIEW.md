# S21 independent integration data review

2026-10-14 UTC. No tests, database operations, Git operations, or candidate edits were performed by this reviewer. Prior binding review remains unchanged. Full test JSON, package-origin JSON, environment and credential files were not read.

## Decision and scope

The bounded source composition and full-suite evidence reconcile. No new failure IDs, removed prior cases, or changed prior case outcomes appear relative to the corresponding S20 installed full-suite JUnit evidence. This supports retaining/publishing S21 as a source-overlay correctness derivative with explicit known failures. It is not a green full suite and not installed-candidate qualification. Existing dependency provenance limitations remain. All seven release gates remain UNKNOWN.

## Composition

All 210 entries in `persistence-recovery-20261013/s21-source-preparation.json` hash to the current S21 files. All 208 accepted files in `candidate-s20-source-lock-20261014/source` are retained. Exactly two existing files differ: migration.py and manifest/compatibility.py. Exactly two tests are added: test_maintenance_budget_boundary.py and test_compatibility_string_bindings.py. All four are byte-identical to the respective isolated candidate files.

All 40 original S20 Python modules are present; exactly 38 are byte-identical, with only the stated two fixes different. Existing tests are not weakened. `scripts/test_postgres.py` and `tests/conftest.py` are byte-identical across original S20, accepted source-lock derivative, and S21. The packaging configuration matches the accepted source-lock derivative; uv.lock matches both that derivative and original S20.

An initial comparison used the source-lock container rather than its `source` subdirectory and failed with a missing-path error. The reviewer paused and obtained the corrected root and explicit continuation authorization before proceeding. No permissions were bypassed.

## Reconciled terminal results

- SA21-labeled source overlay: 2525 top-level passed, 7 failed, 0 skipped, 56 passed subtests, 50 warnings, 419.65 seconds.
- SA20-labeled source overlay: 2479 top-level passed, 7 failed, 46 skipped, 56 passed subtests, 2 warnings, 417.97 seconds.

Terminal summaries match actual JUnit testcase outcomes. Each run has 2532 top-level testcase elements and progress start events. JUnit suite tests=2588 includes 56 subtests that are not separate testcase elements. SA21 progress records 2581 passed calls: 2525 top-level plus 56 subtests. SA20 records 2535 passed calls: 2479 top-level plus 56 subtests. SA20 skips comprise 18 setup-stage and 28 call-stage skips, for 46 total. Counting only call-stage skips or treating all passing call events as distinct tests would misstate the results.

Against S20 installed full-suite evidence, every existing testcase ID retains its outcome in both cells. There are exactly 188 added passing cases: 56 scanner-binding cases and 132 maintenance-budget cases. This comparison is historical evidence comparison, not a claim that S21 was installed or that the environments are otherwise proven equivalent.

The seven unchanged failing IDs are all in tests/test_deprotection_ordinals.py:

- test_reverse_refuses_unhandled_public_suffix_comment_before_staging
- test_changed_public_staging_refuses_switch
- test_public_copy_participates_in_chunk_byte_bound
- test_reverse_refuses_unhandled_suffix_attributes[column_grant]
- test_reverse_refuses_unhandled_suffix_attributes[statistics]
- test_reverse_refuses_unhandled_suffix_attributes[storage]
- test_reverse_refuses_unhandled_suffix_attributes[compression]

## Provenance and stability

Both package-origin logs resolve to the S21 candidate source tree and report verified true. Source-root receipts record the intended root, candidate override, and unchanged preflight. Readiness logs record successful dual-role preflight. Each full run inventories 149 executable/test/build files with identical before/after maps; each inventory also independently matches the current candidate. The full 210-file preparation manifest independently matches after both runs. External-source inventories are empty and do not establish external-source coverage.

The separate AUDIT.json records exact reconciled counts, failure IDs, empty prior-outcome-change lists, source mismatches, and safe evidence SHA-256 identities. No claim is made that receipt directory names alone prove historical dependency versions. Root separately observed current interpreter version/module origins; that is not historical execution attestation.

## Key SHA-256 identities

- preparation manifest: e1e3555ec97bea01c3e816cb73143d63d304b24d08e798589335826456b2be46
- migration.py: 0c6df2baa2b3b8c25a9dedb5ee2d6e7a1b47804da3e04ebf4dda5c2a3a465b9a
- compatibility.py: 4d42e25714eed40dfb3c27d10239705855d6ffe963a5ef642de7511f85abe460
- maintenance tests: ea8e48b6304887d65df72d0b0d0ad3ee99a4fd97bfabfa13aedc32693129ab81
- binding tests: fea21ff5374d165112d4370514fbdd430f708db96635e0aea2d4f9aff22f1ed8
- unchanged test_postgres.py: 118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12
- unchanged conftest.py: fa521d4bec6b84320304ad59d22e7551c342d7e60f2c254c8b6495b07bdf06dd
- accepted pyproject.toml: 4653756dfe6a3dd1a185f636efb1ea0135b5235d9cdc138f30667d1f0975487f
- unchanged uv.lock: faae077d223037c4a7d9a54e1aafc4760cf217057eb18fbd93fc021908be343e
