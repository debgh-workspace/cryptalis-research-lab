# Decision: retain the baseline for this slice

Do not promote either canonical-tenant cache candidate. Both timing screens are HOLD. Preserve every sample, the prospective thresholds and both source packets. No additional optimization or rerun is proposed.

## Source explanation

The original baseline calls UUID(tenant), then performs the tenant/point checks and real-CF1 processing. It has no cache construction or shortcut predicate.

The first candidate adds an exact-UUID cache at processor construction. Each non-NULL row loads that cache, checks presence and exact str type, checks current tenant identity, and compares the input with cached canonical text. A canonical hit avoids UUID parsing/allocation. An uppercase input cannot hit: it pays those checks and then the same UUID constructor as the baseline. Tenant/point and cryptographic work still follow.

The successor moves text equality ahead of identity, after the unchanged presence/type guards. An uppercase mismatch skips the current-tenant attribute lookup and cached UUID identity expression. It still loads the cache, checks presence/type, indexes cached text, compares strings and branches before calling UUID. It removes part of the added work; it does not give fallback a corresponding saved parse. Exact-str must precede equality to avoid changing subtype/object dispatch, and identity must still gate reuse after sequential rebinding.

This structural asymmetry is a plausible reason for fallback cost, not proof of the cause or magnitude of either observed regression. Interpreter specialization, allocation, scheduling and the surrounding CF1/loop costs also affect measurements. No per-expression timing or CPU profile was collected. Separate runs against the same baseline do not causally isolate the reorder from host/time variation.

## Evidence and limits

Original benchmark V2 is bound by SOURCE402f4c7aec63b1aec00840eea25255ec21ca56fdc95a153d814f50ff3e8289c8. Its independent BENCHMARK_TERMINAL_REVIEW.md under recovery-work/search-proposal-review-20261017 accepts experiment integrity and retains screen HOLD:24 flags, including16 samples with more than2 involuntary switches. No major faults occurred. Some fallback medians were near or below1; it is inaccurate to say every uppercase cell was slower. Storage16 uppercase CPU median ratio1.035918 and failed fallback consistency checks prevent acceptance. Favorable canonical medians do not override the gates.

Successor benchmark is bound by SOURCEd176ed1773d01d731dca7c8406a04ed552e692ba6ae159ae36c962a57a7daeec. Root reported its screen HOLD as well. Its independent terminal audit is in progress separately; this memo does not duplicate or pre-approve that audit or invent second-run numerical results. Later acceptance of capture integrity would not turn its failed performance screen into PASS.

Each fixed experiment declares16 processes,128 samples and524288 timed calls, with identical workload/gates and no trimming. All original samples and noise flags remain evidence. Correctness acceptance of the first candidate and successor is separate from performance acceptance. The timing excludes processor construction and cached-string initialization, which add cost and remain unmeasured. Neither warmed results nor correctness support tiny-resultset, end-to-end, provider, DB or production claims.

## Recommendation and unresolved question

Retain the original baseline as the source choice for this bounded slice; this is not a new production qualification. Keep both candidates as unpromoted evidence. Correctness-preserving fast paths can still have an unfavorable fallback trade-off, and this finite evidence has not met the preset acceptance screen.

No materially distinct experiment is justified now by the available workload evidence. A useful prerequisite for a future decision would be an independently established application contract/distribution for canonical versus alternate tenant representations and result-set sizes. Without that evidence, estimating a weighted benefit would require guessing the hit rate and ignoring unmeasured construction costs. This is an unresolved product-workload question, not authorization to collect production data, relax fallback behavior or run another benchmark.

Preparation used source/diff and saved-review inspection only. No product execution, DB, Git action, new optimization, sample removal or threshold change occurred.
