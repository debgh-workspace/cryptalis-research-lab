

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


## S10 allocation correction verified, 2026-10-13

The tuple encoder now joins count/length prefixes and original part references in one pass. Wire bytes and strict bytes-only checks are unchanged. No key cache, compiled cache, nonce, AEAD, HKDF, authentication, key lifetime or validation change. Independent writer oracle includes132 cases and7 invalid-type controls. Focused source151PASS.

Installed full PostgreSQL suites: SQLAlchemy2.1.3 1776PASS/7FAIL/0SKIP301.99s;2.0.51 1758PASS/7FAIL/18SKIP303.38s. Both retain exactly the seven known legacy-profile failures and two fork warnings. Source hashes match; both servers stopped. Full-suite acceptance remains OPEN. Wheel SHA256 f773483c07aa97d588585acb69c55d988263ed56713b214d62393d161458a9b6; repeated offline build identical.

For an8MiB input, incremental Python-traced peak allocation fell from16,777,664 to8,388,864 bytes. This is not request RSS. Same-session seven-block paired IN2 medians:13.360 to12.653ms on2.1.3,12.359 to11.818ms on2.0.51;7/7 and6/7 favorable blocks. Point/equality results vary; no blanket speedup or production performance claim. All seven production gates remain UNKNOWN.

Next: implement the missing read-only pre-adoption scanner/doctor under explicit checked/unknown boundaries. Existing database only; second cluster and credential approval remains pending. Original online-migration workstream S6 remains OPEN; corrective slice numbering does not imply its completion.


## S11 advisory diagnostic currency, 2026-10-13

Reconciliation found an existing bounded source scanner, so it is retained instead of rebuilt. Its UUID literal finding still asserted that UUID-01 was unapproved and all strings refused, although the runtime had already admitted PostgreSQL16 UUID text. Its Core DML warning omitted the private bounded DELETE profile. Five new source-report regressions failed against S10.

The separate S11 candidate reuses the runtime UUID grammar for literal classification, retains a refusal for malformed text, and reports admitted text as requiring staging rather than granting admission. Default Core DML refusal remains; its remedy now explains that private DELETE needs exact target/effect-inventory/staging verification. No runtime query admission, crypto, source execution, SQL execution or privilege change is added by this correction.

Eight real native/protected point-read controls independently verify canonical, compact, braced and four-digit-group spellings recover the same UUID and protected values. Existing invalid-literal and source-sanitization controls remain unchanged. Focused41PASS2.23s. PostgreSQL16 primary source corroborates the alternative spellings: https://www.postgresql.org/docs/16/datatype-uuid.html . No novel grammar claim.

Repeated offline wheel SHA256 cbc0ba6a34bf4d8d9c617da881005f94625555868886dce7d1aef82cbc63d99a;39RECORD entries,35installed runtime modules byte-match. Installed full suites:1789PASS/7FAIL/0SKIP310.59s on2.1.3;1771PASS/7FAIL/18SKIP297.10s on2.0.51. Both retain exactly the seven known legacy-profile failures and two fork warnings. Source hashes unchanged and servers stopped. No full-suite acceptance claim. Complete unified doctor remains unimplemented; all seven production gates UNKNOWN.


## S12 bounded doctor verified, 2026-10-13

Partial OBJ-DX-02 implementation: cryptalis doctor declaration.json --json checks only product declaration grammar and returns exit3 for valid-but-incomplete inspection. Explicit-host cryptalis.doctor.doctor(...) adds native pre-adoption compiler admission and supplied-source compatibility inspection. It never imports application source by name, calls attach, migrates, repairs permissions, reads application values or accesses keys. Roles/provider/ciphertext checks are NOT_INSPECTED; complete/ready are always false. Active diagnostic mode rejects explicitly. Full doctor objective remains OPEN. See docs/doctor.md.

Source169PASS6.24s; removing existing read-only enforcement/assertion makes2 new controls fail; exact restoration14PASS0.43s. Installed console entry point returns expected incomplete report without modifying input. Installed full suites: SQLAlchemy2.1.3 1803PASS/7FAIL/0SKIP305.74s;2.0.51 1785PASS/7FAIL/18SKIP309.25s. Exact same seven legacy-profile failures, two fork warnings, unchanged source hashes; both servers stopped. Repeated wheel db6e83817fd4bad3e9be8f98b9aebbbc5641ac38f09e64e94ab11be84b77e332;40RECORD entries and36installed modules verified. All seven production gates remain UNKNOWN.

Read-only is a bounded database safeguard, not a sandbox for trusted host callbacks or a guarantee of zero disk writes. No production/fresh-cluster/provider qualification follows. Next: extend diagnostic coverage only with exact lifecycle/role/provider contracts and preserve the open independent-review and fresh-cluster requirements.


## S13 active deployment doctor, 2026-10-13

The explicit-host doctor API adds phase="active" with deployment=(plan,pin) and the planned runtime engine. It reuses existing check_attachment policy, requires an ACTIVE matching pin and matching declaration, and owns a PostgreSQL-enforced REPEATABLE READ/READ ONLY transaction. It checks active catalog/journal/pin consistency and the existing planned-runtime effective-permission/routine policy. It does not call attach, change mappings, grant privileges, inspect provider custody or authenticate row ciphertext. The host remains responsible for authenticating the external pin; later schema/permission changes are outside the snapshot. Full doctor and all seven production gates remain OPEN/UNKNOWN.

Three new controls failed before the API extension. Source17PASS then expanded62PASS. Omitting only the deployment inspector produces2FAIL (wrong owner and schema drift), followed by exact source restoration. Installed affected-path suites:157PASS10.89s onSQLAlchemy2.1.3;157PASS10.52s on2.0.51, zero failures/errors/skips. These cover both doctor modes, CLI, advisory source scanner, migration audit and9 new active controls. Both preserve exact source bytes; PostgreSQL stopped. The full suite was NOT rerun for this isolated diagnostic extension; last full baseline is S12 (1803/1785PASS and7 unresolved legacy-profile failures). Do not label S13 full-suite-qualified.

Wheel1600f108e2d6a44fecc5ecd7b2f38421492f58add9c9ddc764c9a498ad575cf9 reproduced twice;40RECORD entries and36installed modules match. No new cluster, credentials, crypto primitive, key cache or maintenance-approval exemption. Row integrity verification still follows the existing approved verification contract.


## S14 bounded ciphertext observation verified, 2026-10-13

The active doctor now accepts explicit ciphertext-audit opt-in, an existing trusted key resolver and strict global row/estimated-byte bounds. Active metadata and planned-role checks precede payload-only observation in one PostgreSQL REPEATABLE READ/READ ONLY transaction. Existing CF1 authentication and exact plan-bound key-policy/lease rules remain unchanged. No new credentials, key cache, provider, journal write or lifecycle certificate. Static CLI and default doctor calls do not access keys or row values.

CHECKED covers visible non-NULL cells only. NULL substitution, missing rows, same-context replay/freshness, external membership and provider custody are not proven. Any generation admitted by the policy can authenticate; active-write-generation readiness is not established. The estimated projection budget excludes metadata/lookahead and does not bound total network bytes, RSS, server work or elapsed time. Reports suppress data and arbitrary provider error text; comprehensive host logging hygiene was not tested. Full doctor and all seven independent gates remain OPEN/UNKNOWN.

Source controls: missing API3FAIL, then90PASS after one test-setup SQL correction (failed setup retained). Authentication removal1FAIL; byte-bound removal1FAIL; exact restoration19PASS. Full installed runtime suites: SQLAlchemy2.1.3 1831PASS/7FAIL/0SKIP315.40s;2.0.51 1813PASS/7FAIL/18SKIP315.98s. Both preserve exactly the seven legacy-layout failure IDs, two fork warnings and stable source hashes; both servers stopped. Full-suite acceptance remains OPEN.

Six additional tests were added after those full runs, with runtime bytes unchanged. All6PASS on each installed dependency cell (1.99s/1.81s): committed interleaved writer retains one snapshot, old-source SELECT independently denied with42501 while payload audit succeeds, audit-stage writes refused with25006 in normal/AUTOCOMMIT modes, global cross-table row bound and empty data. Replacing only REPEATABLE READ with READ COMMITTED makes the snapshot test fail (1 authenticated cell rather than6); exact runtime restoration and installed recheck PASS. Do not describe these six later tests as part of the earlier full-run counts.

Repeated wheel SHA25643c98cb0128c0a8cfda090febc8f485bd9b4883f3c9c047aefd155fe263ac080; sdist535e554d1df9e3fe59e59b4653e24d3c5ec6bbc1c86cf56ca598d8ae78209109.41RECORD entries and37installed modules verified. No audit latency benchmark, bigint/single-tenant audit-specific campaign or production-provider qualification yet. Native/CF1 independent fixture oracles are software checks, not external security review.
