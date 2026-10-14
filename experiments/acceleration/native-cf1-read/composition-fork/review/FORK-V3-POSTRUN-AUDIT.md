# Independent S actual-fork v3 data audit

2026-10-14. PASS for the finite fork receipt/data-consistency scope. No discrepancy found in 2,347 explicit independent checks. This audit used only JSON/file/hash inspection; no candidate or harness import, actual fork, cryptographic execution, build or test rerun.

Reproducible audit: audit_fork_v3_data.py. Detailed results and raw PID pairs: FORK-V3-DATA-AUDIT.json.

## Independently verified evidence

- Both O0/O1 positive launches have the complete ordered storage and equality cases. Their sixteen read attempts comprise twelve exact successes (parent-before, fresh-child, parent-after) and four exact inherited-key refusals. Each inherited attempt stops at the first payload resolution with KeyUnavailable, the complete safe diagnostic contract and zero primitive entries.
- Successful storage reads have the expected two payload resolutions and three primitive entries; equality reads have payload/search/payload/search resolutions and six primitive entries. Exact domain, tenant, generation, text/type and full error metadata match. Expected success/refusal records were independently reconstructed from the unchanged public fixture and reviewed contract, rather than accepting only manifest summary fields.
- All twelve launches, including negative runs, retain two complete original records. For all twenty-four recorded fork children, the audit checks raw PID types and recomputes all seven relationships: parent unchanged, parent-owned inherited material, fork return equals child, distinct child/parent, child's parent equals parent, inherited child's key PID remains parent, and fresh child's key PID equals child. Every relation agrees with the frozen expectations and recorded relation fields.
- All ten observation negatives first contain the exact verified equality record and then precisely the declared mutation: fresh text, inherited diagnostic stage, inherited resolution trace, inherited primitive entry or raw child PID with recomputed relation. Each mutated record differs from its frozen expectation and is rejected by the intended RuntimeError comparator with nonzero exit. Arbitrary infrastructure failure would not satisfy this check.
- Inner receipts show zero wait status, successful reap, pipe EOF and no cleanup errors. Outer supervisors show direct-child reaping, no reason/error, empty cleanup_errors and the exact 60-second/2-MiB limits. All twelve group_signals_attempted lists are empty and group_termination_attempted is false. descendants_verified_absent remains false; the audit does not turn successful reap into a stronger descendant claim.
- Parent and runner anchored post-pin/cache statuses are PASS throughout. Exact child command lines, optimization modes, native binary/hash, mapped libcrypto path, acceptance envelopes and receipt hashes agree. The finite mode/optimization matrix is complete and unique.
- All 1,791 PINS_v3 hashes match actual files; source/cache inventories and tool/Python resolutions match. All v1/v2/v3 artifact entries and all 64 DELIVERY_INDEX files match their hashes. The completed S package's independently pinned delivery index and all 167 files remain unchanged. No prior case/oracle/result was replaced.
- SUMMARY_v3 counts and per-launch receipt hashes agree with the underlying evidence. The result rests on complete record comparison and PID recomputation, not those summaries alone.

Governing PINS_v3 digest: a1dd0e98d92e0d930dabf8ce6c58996102df65602dcbd178bc98c16d1bd3fdd0.

## Bounded conclusion

This evidence closes the specifically named S actual-fork observation gap for these two public storage/equality vectors, the existing normal native binary and both interpreter optimization modes: inherited parent material is refused before primitive entry, freshly constructed child material succeeds, and the parent remains usable afterward.

It is internally consistent receipt evidence, not externally attested execution or independent proof of Python object identity. The reviewed source provides the same-inherited-object/fresh-child construction meaning, and the raw PID observations support that meaning within the harness scope.

No timeout/overflow/descriptor/signal/reap-failure injection occurred. Successful processes and observation-negative comparator exits do not qualify all cleanup-failure paths, multithreaded fork behavior, external competing reapers, deliberate escape or absence of all descendants. No cryptographic fixture recomputation was required for this audit. Leak/erasure, broader queue/provider/causal-failure behavior, full DESIGN, timing/five-arm attribution, database integration and product-adoption gates remain unchanged.
