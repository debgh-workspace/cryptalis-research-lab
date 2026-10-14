# S23 current-source composite review

2026-10-14. Saved-data composition only; no tests, database, Git or reconciler execution by Agent 2.

The current 554-key baseline and separately verified 46 async keys are disjoint and form exactly 600 current keys across the same 159 operation IDs: 444 IDENTICAL and 156 REJECTED-LOUD. COMPOSITE_CURRENT_600_v1.json has SHA-256 84cc859b2bb4cf742f85f68cebb9ce23bb3975a74da86450a2484508d7dfc7e6. It is an additive derived receipt; both input aggregates and all original evidence remain unchanged.

All 275 baseline-consumed hashes and all 1487 additive-consumed hashes freshly match. The two source manifests have exactly the same 213-entry S23 map, current bytes match, and each async run's 152-entry source/config inventory exactly matches its corresponding baseline dependency cell. Safe origins identify the same candidate. The run-local async rows report SQLAlchemy.__version__ 2.1.3 or 2.0.51, matching the baseline identities. There is no separate safe dependency-identity file for the async runs, so this establishes SQLAlchemy-version correspondence and source equality, not byte-identical whole dependency environments or interpreter provenance. Baseline identity observations remain pre-run-only.

Independent raw extension checks confirm all 30 UUID native/protected results, completed arms and original bind preservation, plus all sixteen warm-mapper native/protected complete expected row states. UUID standard-profile fields match baseline; warm-mapper uses the source-bound common application/plan/lock and default attachment without a profile override. Its receipt has no profile field, so that correspondence is source-derived. The separate Agent 5 audit accepts the exact additive receipt and its strict synthetic controls.

The exact 46 added keys are a subset of the historical 82 missing combinations. The original 82-gap rows are copied unchanged into the composite; separate remaining-gap rows preserve all 36 original reasons. These are A6/SQLModel combinations: 24 on SQLAlchemy 2.1.3, plus eleven async and one sync combination on 2.0.51. This does not admit unsupported SQLModel 2.1 or general async SQLModel.

The original S22 aggregate remains INCOMPLETE_OR_FAILED at its original hash with 398/155/one TEST_FAILURE; its one-cell additive retest history remains intact. This composite combines seven separately executed finite source-overlay campaigns, not one 600-test invocation. Existing full-suite failures and all seven UNKNOWN qualification gates remain outside this bounded result.
