# B9B55 negative-control receipt audit

## Result

The bounded evidence audit passes. Original R1 remains available with 53 passed and 2 failures; both failures are storage search-generation cases. R2 SA21 and SA20 receipts each contain 55 unique passing cases, zero failures/errors/skips, and identical case IDs.

R1 to R2 retains 51 exact IDs and replaces the four header cells with two native search-header constraint controls and two experiment payload-header refusal controls. The only changed path among the 150 recorded source-stability entries is `tests/test_payload_rotation_profile_negatives.py`.

## Exact correction

The native CHECK remains enabled. Search-header controls expect `IntegrityError`, then assert the underlying `psycopg.errors.CheckViolation`, SQLSTATE `23514`, the expected `<payload_column>_frame` constraint, fixture schema and customer table. The error is caught outside the transaction so rollback completes first. The controls assert zero seals, unchanged native/source snapshots, source equal to baseline, ACTIVE pin and empty staging.

Payload-header controls still alter payload generation to 2, explicitly verify the altered bytes reached storage, and assert the experiment refuses with `source_generation_changed`, unchanged persistent state, zero seals and empty staging. The correction does not weaken these into generic exception assertions.

No skip/xfail masking appears in the reviewed negative-test module. R2 JUnit has no skipped, error or failure elements. The original R1 failures remain in its receipt.

## Hash verification

All 150 recorded entries match before/after and their current corresponding candidate. Complete calculated hashes, IDs, nonpassing entries and summary counts are in `verification.json`.

- R1 negative test SHA-256: `154d340b02ac97b001f01c141d308bc9cf21410fc838d6b23d81c3f6efbd4432`
- R2 negative test SHA-256: `ae698ce63da0d786d63bdf52a22a6e7407fa471127f50a28e55038b0defe76f9`
- Current experiment module SHA-256 in both candidates: `ac09b3c0f70c3089aada5bf584d64487072d7b8ea7083292e543773e03a4a8df`

## Limits and remaining scope

The experiment module is absent from the source-stability manifests. Its current equality across candidates does not prove its stability during prior runs.

The safe run receipts do not independently prove interpreter or package versions/provenance. Root reports separate current-interpreter inspection confirming SQLAlchemy 2.1.3/2.0.51, Python 3.12.14, cryptography 50.0.2 and psycopg 3.3.6. This is current-environment evidence, not retrospective proof of the receipt environments.

These are synthetic inactive-only preparation controls. This audit does not establish activation/publication, production readiness, broader compatibility or release approval. Native search-header refusal specifically establishes the database boundary, not execution of an experiment-layer rejection for that input.

## Method and access

Used standard-library JSON/XML parsing, SHA-256 hashing, text reading and diff review. Evidence reads were restricted to tests.log, junit.xml and source-stability.json. No tests.json, package-origin.json or ENV was read. No pytest, PostgreSQL command, candidate import or Git command was run. The only writes are these audit deliverables in the authorized audit directory. No test rerun was performed.
