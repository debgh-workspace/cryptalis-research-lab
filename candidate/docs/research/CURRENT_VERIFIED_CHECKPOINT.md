

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


## S8 integrated public-table binding correction, 2026-10-13

Unqualified public-child mappings reproduced a native/protected discrepancy for direct DELETE and parent cascade (2FAIL2PASS). Attachment now resolves ordinary direct public tables on the original runtime search path before lifecycle inspection, then freezes eligible mappings only inside already compiled schemas after validation. Protected models use their existing lock binding. Missing resolutions are not guessed. Schema/name drift rejects. This grants no public DELETE capability: existing private allowlists, grammar, OID checks and locked effect inventories remain required.

Installed SQLAlchemy2.1.3:1760PASS7FAIL0SKIP314.69s;2.0.51:1742PASS7FAIL18SKIP302.26s. Both retain2 known fork warnings and exactly the prior seven legacy-layout failure IDs. All35 new cases pass in both; installed35 modules and before/after source bytes match. Pin-guard removal fails2 tests, and exact restoration is covered by both full suites. Wheel504224d80ff095071039f691e5a742da8f46536bf73947e8a9e67cefc7677cba reproduced twice offline.

Pinned FastAPI7257e606cb94eada1dca40173e2b7f99dd549bc6 with original unqualified mappings:58 native,58 protected,58 package-free before removal and58 after removal PASS, each0 failures/errors/skips. Upstream source edits0; manual table-schema assignments0. Independent decoded7-user/7-item corpus, decrypt-back and real pg_dump/psql restoration match exactly; old encrypted restore fails REMOVED publication check. This is same-host synthetic evidence. Private one-hop cascade, explicit C collation,13 bootstrap/4 fixture lines and operator grants remain. The plaintext role was reused, not newly created. New cluster/credentials approval remains pending.

Full-suite acceptance, legacy-layout upgrade coverage and all seven production gates remain OPEN/UNKNOWN. No production deployment, generic cascade capability, online migration or external-key-custody qualification follows. Next: reconcile remaining integration friction and lifecycle qualification, preserving the seven unmodified legacy assertions and exact frozen compatibility corpus.


## S9 integrated planner numeric-rejection correction, 2026-10-13

Both public planners leaked OverflowError when converting oversized integer rates or forming duration estimates from positive subnormal rates (4FAIL before correction). Rate integer bounds now precede floating conversion. Duration-only arithmetic translates overflow or out-of-artifact-range counters into TransitionFailure(unrepresentable_cost_estimates), suppressing raw numeric exceptions. Representable max integer/float inputs and zero-row subnormal rates remain accepted. Host rate estimates, formulas, confidentiality and artifact parser grammar are unchanged; these estimates are not performance guarantees. Provider calls are not inside the numeric exception handler.

Source29PASS then36PASS; final dedicated14 cases PASS1.96s. Installed2.1.3:1774PASS7FAIL0SKIP301.57s;2.0.51:1756PASS7FAIL18SKIP312.37s, each2 known fork warnings. Same seven legacy-layout failure IDs; full-suite acceptance stays OPEN. All35 installed modules byte-match and source hashes remain fixed. Repeated offline wheel SHA25627d62803d9c6f692d7fa91499983e9e7fcd9fb0c410065fb1223489ffb1da165;39 RECORD entries. All seven production gates remain UNKNOWN.

Next: run the separately prepared retained-layout native/driver/attached benchmark, with exact results and bounded warm same-host measurements. It does not reuse obsolete cache-profile benchmark assumptions. No production latency or throughput claim follows from the result.
