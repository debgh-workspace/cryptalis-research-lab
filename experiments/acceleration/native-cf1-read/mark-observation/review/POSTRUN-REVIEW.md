# Independent data-only postrun review

Disposition: PASS within the frozen diagnostic scope. 2026-10-14.

No candidate imports, preparation, builds, native execution, reruns, network, PG or Git were performed. The audit used only jq on JSON receipts and SHA-256 reads. Newly written artifacts are confined to this review directory.

Both mode receipts contain exactly the manifest's 60 unique IDs in order. All setup mark statuses and control mutation statuses are exact. Every public distance/pop/endpoint/final-drain observation equals its applicable frozen oracle. Per mode, four no-helper baselines match preservation; eight active controls differ from preservation and exactly equal their independently prescribed altered traces; 48 helper cases match preservation and exact inherited outcomes (eight byte successes and forty private RuntimeError refusals). The two complete result documents are equal after removing only their optimization-mode field.

All current PINS entries and all build receipt pin entries verify. Every frozen source pin remains represented unchanged in the build receipt. Binary hash 289226d2c3cd4b8ae6316b5457f8dcdd2be04c92bf45bc3934af90e00d0c6528 and manifest hash b70cfd9895309386bc8c5968987a003af893a0d0fd750f83ec0f40c955e6ceac agree with the files, build record and both result records. The runtime version recorded is OpenSSL 3.5.7 9 Jun 2026. The preceding unmarked observation package's 17 ARTIFACTS.json entries also independently rehash correctly, including its source and built/results artifacts.

Build receipt records one C -O2 CF1_DIAGNOSTIC build, exit zero and no compiler output. The build/O0/O1 launch receipts each record exit zero, empty stderr, no timeout, a 60-second deadline, an owned process group and kill/reap timeout handling. Run stdout is exactly PASS 60 0 / PASS 60 1. Command paths agree with the reviewed build and runner; O1 adds -O. These are audited receipt claims, not a new replay or independent live instrumentation.

RESULTS.md numerical claims and finite-scope interpretation agree with the audited data. Its 'independent postrun data audit pending at authoring' wording accurately describes its earlier authoring time; this document supplies the completed review.

Evidence: POSTRUN-AUDIT.json records data checks; postrun-audit.jq preserves the independent comparison; POSTRUN-SHA256.txt records audited input, build, launch and result file hashes. The earlier REVIEW.md contains the independent operation walk and unchanged-helper source review.

Limits remain: destructive observations on owned thread-local test state, endpoint rather than hidden complete-state inspection, four selected mark configurations, at most three test-created queue entries, selected helper branches and one pinned diagnostic backend. No arbitrary nesting/capacity/concurrency, actual allocation failure, failed mark creation, other backend/provider lifecycle or normal-binary conclusion follows. This bounded evidence supports preservation in the selected cases and does not support the earlier categorical mark-loss claim or a universal guarantee. No product adoption, classifier decision, timing or full design admission is granted by this audit.
