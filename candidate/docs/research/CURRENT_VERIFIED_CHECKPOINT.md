

## Verified checkpoint 2026-10-12 08:37 UTC

Installed temporal candidate: 99 selected tests PASS on each SQLAlchemy version (2.1.3, 2.0.51), Python 3.12.14/PostgreSQL 16.15. Same-host wheel rebuilds identical; wheel SHA256 e7ab45df042db200b76337f1acb30bd3f84e7aaa2dc7d19b6979527b31ae4980. Tests: 34 ordinary/versioned/cascade deletion, 6 public temporal metadata, 20 adapter, 15 lifecycle, 24 search cases. Full suite and independent review not done. Initial combined run had a fixture module-path collision at collection; a shared fixture now imports the selected candidate test module. Record that as harness failure, not product failure. Corrected installed runs are GREEN.

Temporal RED: six native-valid cases failed old whitelist. Cache omission: six repeated ordinary deletion cases fail when scoped compiled_cache=None is removed. The guard's original 12 positive cases also pass recovered parent; no historical guard-fix RED claim.

Actual FastAPI (upstream SHA7257e606cb94eada1dca40173e2b7f99dd549bc6; Python3.14.8, SQLAlchemy2.0.51, SQLModel0.0.47, FastAPI0.141.1): native58 PASS. Temporal+explicit-schema private prototype58 call bodies PASS and1 teardown ERROR. Remaining teardown is delete(User), the protected-table bulk operation; it remains refused. No upstream application edits. Nine prototype integration lines plus four fixture lines, correcting old static six-line counter. Independent oracle agrees with36 stored rows,5 non-null CF1 frames. This is storage-only full_name, not encrypted email or a complete application lifecycle.

Real-app reverse planner now tested: refuses unsupported_reverse_suffix_metadata before staging. full_name precedes primary-key ID, hashed_password and created_at. Existing ordered reverse strategy copies/drops suffix columns, whose primary-key/FK/type metadata is outside its bounded contract. Do not weaken the refusal. This is a confirmed removal blocker.

Competing DDL mechanism study: in-place forward and reverse type conversion preserved SELECT * column order, values, table OID, an unrelated FK/view and public comment in a three-row fixture; dropping/renaming the forward column followed by in-place reverse preserved named values but lost positional order. Two mechanism tests PASS. Payloads in this study are explicitly synthetic NON-CRYPTO bytes; this is not encryption/lifecycle evidence. PostgreSQL ALTER TABLE documentation confirms rewrite/lock/disk costs and old-snapshot hazards: https://www.postgresql.org/docs/16/sql-altertable.html . A prospective in-place strategy is a research alternative, not an integrated fix or a repair of legacy already-reordered tables. Retain snapshot fencing. No novelty claim.

Next: fully specified reversible layout alternative with authenticated staging and exact schema checks, legacy-layout repair, protected bulk-DML design, installed real-app verification, second independent app. No release claim; seven gates UNKNOWN.


## S6 integrated diagnostic correction, 2026-10-13

Malformed protection artifacts previously escaped the MigrationPlan constructor as parser, UUID, missing-field or wrong-type exceptions. Ten public malformed-artifact cases establish8RED failures/2controls before correction. The bounded correction translates existing rejection paths to TransitionFailure(code=invalid_plan), suppresses underlying exception display and keeps format/canonical-byte/nonzero UUID/parser bounds unchanged. It does not authenticate an artifact, validate every semantic plan field, admit legacy formats or perform database work during construction.

Source GREEN13PASS includes3 real PostgreSQL plan/protect/reverse controls. Installed complete suites: SQLAlchemy2.1.3 1710PASS/7FAIL/0SKIP287.14s;2.0.51 1692PASS/7FAIL/18SKIP286.75s. All seven failures exactly match prior legacy-profile assertions; no new skip or expectation change. Original legacy test file independently passes10/10 on its original layout implementation. Full-suite acceptance and legacy-layout upgrades remain OPEN. Wheel aa186579a457c1d6b749312071b1786871ee70b652cd3788f1db7cfd9f6da3f1 reproduced twice offline; all34 installed runtime modules byte-match and38 RECORD entries verify. All seven production gates remain UNKNOWN.

Next: reproduce the separate fractional measured-rate planning concern without loosening manifest/lock numeric validation; preserve current correction and all historical failed evidence.


## S7 installed measured-rate correction, 2026-10-13

Both public protection and reversal planners previously rejected valid fractional measured rates after accepting their inputs (RED 2FAIL). A separate transition-artifact decoder now permits positive finite floats only in the two explicit estimate-rate fields and the corresponding reverse source-plan fields. Manifest, lock and descriptor numeric grammar remains unchanged. This is not artifact authentication or comprehensive semantic validation. Existing integer artifacts roundtrip unchanged; older readers refuse new fractional artifacts.

Source validation:61PASS; removal of only the field-scope guard produces3FAIL/12PASS, followed by exact restoration15PASS. Installed full PostgreSQL suites through unchanged dual-role preflights: SQLAlchemy2.1.3 1725PASS/7FAIL/0SKIP286.63s;2.0.51 1707PASS/7FAIL/18SKIP289.55s. Both have2 fork warnings. Exact seven legacy-profile failures remain unchanged; full-suite acceptance stays OPEN. Source stability verified; each server stopped cleanly. Reproducible wheel SHA25619efd5eafede07616c45c21be491fe85206f52cd0c1ada53fa76dee8ab2ea6e8. All seven production qualification gates remain UNKNOWN.

Next: independently reproduce the unqualified public-child table integration gap; protected-table physical binding already exists and must not be reimplemented or weakened. New-cluster/credential approval remains pending; existing authorized lab remains usable.
