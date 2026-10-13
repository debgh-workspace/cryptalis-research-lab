# Cryptalis 72-hour acceleration baseline

Receipt:2026-10-13 12:36:11UTC. Target:2026-10-16 12:36:11UTC (18:06:11Asia/Kolkata). This is a time budget, not a waiver of objective/security/acceptance requirements.

Integrated baseline is S14 at2065cb78f3c7126f207fc62c35887ddd204925af. The183-file candidate inventory SHA256 is7d0fbca30b4cf09e784ac06fbf2afeeee9a71180316aa6c5465a8087913f8121. All remote batch bytes, candidate restore hashes and restored runtime imports passed. Original15-message mailbox remains9b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd.

Three actual native engineering workers have isolated, verified183-file source copies and separate branches rooted at the baseline:
- ORM: candidate-accel-orm-20261013, accel/orm-20261013. First finite gate: off-by-default exact public-table UPDATE with native semantics and locked conservative effect inventory. Protected bulk UPDATE remains outside this first gate.
- Lifecycle: candidate-accel-lifecycle-20261013, accel/lifecycle-20261013. First gate: inactive, distinct rewrap successor artifact and full root-equivalence inventory; strict active-dispatch refusal remains. Publication/rollback protocol needs integration review.
- Search/performance: candidate-accel-search-20261013, accel/search-20261013. First gate: measured immutable public CF1 metadata reuse only; no secret/derived-key/operation cache and no skipped authentication/HKDF.

Coordinator owns main integration, evidence, checklist and all Git publication. No two workers edit one source copy. One approved PostgreSQL16cluster is shared: coordinator serializes every DB test via unchanged role preflights and exclusive lab lock. New cluster/credentials remain pending. Local subprocess/pure workloads may run independently; source isolation does not mean separate machines or external independent security review.

Observed resources:9online CPU threads,9967MiB RAM total,8641MiB available,25GiB free disk. Effective cgroup quotas not exposed at expected paths. Platform capacity permits7total agent slots, initially3engineering workers plus coordinator. Separate billing/allowances are not exposed and remain UNKNOWN. No external paid service was started.

Hours0–6: reconcile frozen baseline and start finite gates. Hours6–24: correctness and targeted native tests. Hours24–48: qualified lifecycle/compatibility integrations and executable online/privacy alternatives. Hours48–60: focused measurement and failure/recovery qualification. Hours60–72: stop speculative starts, integrate/freeze/regress/build/recover and deliver strongest verified candidate plus complete blocker register. Quantitative audits at24/48/72hours are scheduled. External security review, real provider evidence, fresh-cluster qualification and all seven gates remain open until actual evidence exists.
