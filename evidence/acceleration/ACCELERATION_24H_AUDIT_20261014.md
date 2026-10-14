# Cryptalis 24-hour acceleration audit

Audit time: 2026-10-14 12:46 UTC. Sprint began 2026-10-13 12:36 UTC; deadline 2026-10-16 12:36 UTC. This is the scheduled 24-hour audit, delivered about ten minutes after the boundary; approximately 47h50m remain. No database rerun was used for this audit.

## Integrated comparison

Frozen S14: 2065cb78f3c7126f207fc62c35887ddd204925af, 183 files. S20: 208 files, source checkpoint45ea95be055a9092a90bd04b339d7649819e26b7, qualificationd1e85244b207e0c45bfe46b9b9886b9a477c1037. Main remains S14. S20 is the highest bounded integrated research candidate.

| Installed cell | S14 pass/fail/skip | S20 pass/fail/skip | Change |
|---|---|---|---|
| SQLAlchemy2.1.3 |1831/7/0|2337/7/0|+506 passes|
| SQLAlchemy2.0.51 |1813/7/18|2291/7/46|+478 passes,+28 unavailable-native-API skips|

S20 additionally reports56passing subtests in each cell; S14 reports no subtest count. Six later S14 tests are excluded from baseline full totals. S14 elapsed315.40/315.98s; S20 384.67/374.40s. Different suite sizes prohibit treating those durations as product performance deltas. Same seven legacy failure IDs remain; no full-suite green claim.

## Integrated additions and limits

- S15: complete-package legacy→plaintext→retained-native maintenance bridge, Text/VARCHAR,2PASS per cell; no runtime promotion.
- S17 (correcting held S16): off-by-default public-table UPDATE; reverse operation/digest/predecessor validation; protected textual-reference refusal coverage; native DBAPI transaction-state correction and post-result quarantine; unsafe engine-logging preflight rejection. These refusals do not implement protected ordering, ranges or aggregates.
- S18: offline mapped-selector/setup diagnostics and logging checks without connection/key access; added versioning/public-metadata oracles.
- S19: typed malformed-removal-plan guard; versioned SAVEPOINT and maintenance-fence tests. Unchanged pinned FastAPI app:58cases×4modes=232PASS,0fail/error/skip. Historical S19 evidence, not a new S20 replay.
- S20: private inactive payload batch preparation plus final-return lease/PID, reverse-policy-drift and native-default-boundary tests. All204S19files preserved. Active rotation and implicit-default support remain unimplemented/unqualified.

## Experimental evidence outside S20

B9 durable inactive preparation/profile research passes22cases per dependency cell; negative tests55per cell. Remote-source overlay6PASS18.19s onSA2.0. Source-handoff limitations remain explicit.

Native tuple, staged-primitive and fused/context alternatives remain isolated. Exact1098-record corpus comparisons passed ordinary and optimized Python in selected controls. Paired normal-F data audit verified9836checks,1657pins,23supervisors and16intended negatives; positive records equal normal-D. Staged actual-fork audit verified2347checks,1791pins,24recorded child-PID relations and10intended negatives. Internal independent-data checks are not external security qualification. Six sanitizer builds/24launches are source-reviewed only at audit time; runtime results absent. Leak freedom remains UNKNOWN after the standalone clean LSan control failed.

## Performance

No accepted product speed improvement integrated. C1 failed cross-version consistency (SA2.0 equality13.736% median gain but4/7 favorable versus6/7 required); C5 also failed consistency. C7 full-scan112semantic groups passed but all four overall cost gates failed; median ratios12.432–93.564×native. C9 and C10 both failed relative/absolute performance gates on both cells, each with10500retained observations. C10 gains:SA2.1 IN2/equality2.055%/2.231%,SA2.0 2.541%/1.565%; addedp95 14.035/8.824ms and14.006/9.201ms versus8/3ms limits. Isolated native-component ratios0.553/0.554/0.635 are promising selection evidence only; backend/build differences confound attribution. No five-arm full-reader benchmark completed.

## Remaining defects and gates

Seven legacy failures: public staging tamper, public-copy chunk-byte bound, suffix comment, and suffix column grant/compression/statistics/storage expectations. Retained-profile companion passes explain layout differences but do not resolve these failures. Native/protected default and compiled-bind/cache ordering differences remain; context-aware default list identity differs. Active rotations/current-data reverse/handoff, online writer closure, advanced SQL/types, independent clean recovery and real provider custody remain open.

All seven gates UNKNOWN: G-ADAPTER,G-CRYPTO,G-QUERY,G-LIFECYCLE,G-PROVIDER,G-POLICY,G-RELEASE. No automated count replaces external qualification.

## Recovery and publication

S20 archive1132692bytes,SHA25602f6a9133f4bec6ae024a6b9a8e5e135d91af93a1e604ae445948893fc289d68:24remote parts atddc5c8776176cff93e280c6cfd44248fb42e0d74 reconstructed exactly;216payload hashes verified. Fresh remote-source smoke55PASS4.94s uses existing identical installed wheel, not fresh dependencies/cluster. Separate fresh installed restore55PASS4.58s. Prior checkpoints retained.

Latest search branch head freshly checked5019a1ef65d84a43940dd596704c69bf6b48cf5e; its eight files have exact remote-byte receipts. Ledger read remotely at8c75d0358c18b6eec7b4f0af08539530b0e943b7; local append-only updates extend through12:28UTC. Native controls local capsule3172431bytes/SHA25607f353a569a6b6650b4f6259331e310aa41d6ddc1e53153a74b070a1e9189636:393files verified; two restored native calls independently checked. Local-only, not full platform recovery. Original15-commit mailbox freshly rehashed unchanged9b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd.

## Workstreams and decisions

ORM: finite version/default evidence completed, implicit-default mechanism unresolved. Lifecycle: inactive preparation/recovery completed, activation/handoff decision pending. Search: native alternatives and admission controls active; no timing promotion. Online: finite convergence complete, capture-backed prototype permission pending. Defensive review: paired normal-F and staged-fork data audits completed; source review of sanitizer/removal controls cleared bounded scope. Developer experience: integrated diagnostics/plan guard completed; clean second-app proof blocked. Workers are reassigned to the critical path, not six uninterrupted running processes.

Needed for dependent steps: fresh PostgreSQL cluster/test credentials/extensions and second-app dependency approval; capture/history/WAL plan; real provider access and independent reviewers; active rotation/handoff decision; main-branch promotion approval; specifically denied archive uploads. None are inferred approved. Continue unblocked controls/recovery; freeze speculative work at2026-10-16 00:36UTC, final deadline12:36UTC.

## Evidence sources

CRYPTALIS_BUILD_CHECKLIST.md; persistence-recovery-20261013/{ACCELERATION_BASELINE_20261013.md,s14-qualification-summary.json,s20-full-qualification.json,s20-seven-legacy-failure-classification.json,s20-remote-reconstruction-receipt.json,c7-result.md,c9-timing-final-receipt.json,c10-timing-final-receipt.json,native-composition-results-verification.json,native-controls-restored-smoke-audit.json}; native context review POSTRUN-AUDIT-v7; staged composition review FORK-V3-POSTRUN-AUDIT. No tests rerun for this report.
