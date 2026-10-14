# Independent S source-removal postrun audit

2026-10-14. PASS for the bounded data/receipt-consistency and four-control oracle-sensitivity scope. No discrepancies found in 2,398 explicit checks. This audit performed no candidate/harness imports, builds, cryptographic execution or test reruns.

Reproducible independent data audit: audit_removal_data.py. Result: REMOVAL-DATA-AUDIT.json.

## Exact outcomes

All eight control/optimization combinations contain four complete, ordered records: healthy-before, target-original, target-mutant and healthy-recovery. All thirty-two records exactly match frozen predictions, including full text/type, safe diagnostics, complete domain/tenant/purpose/generation traces, primitive order, exact-byte-return flags and expiry-hook counts.

- Wrong-term control: unchanged S rejects with RepresentationMismatch after initial payload/search resolutions and six primitive entries. The isolated skip_term copy returns exact abcdefg, performs only SHA/HKDF/decrypt and reaches all four resolutions. Healthy unchanged S succeeds before and after.
- Storage final-payload expiry: canonical S rejects at its final payload resolution; skip_final returns abcdefg with only initial payload resolution. Both execute three primitives and exactly one post-native expiry hook.
- Equality final-payload expiry: canonical S rejects after initial payload/search and final payload attempt; skip_final returns abcdefg after only initial payload/search. Both execute all six primitives and exactly one hook.
- Equality final-search expiry: canonical S succeeds at final payload resolution then refuses final search. skip_final returns abcdefg after only initial payload/search. Both retain all six primitives and exactly one hook.

Each behavior appears separately under optimization 0 and 1. The independent audit reconstructs primitive order, expected hook execution and resolution precedence from the reviewed semantics, rather than merely accepting the manifest's arrays.

All eight launches then reject the actual divergent removal result using exactly RuntimeError('Frozen S oracle rejected removal mutant') and nonzero child exit. Their divergence receipts contain the verified actual mutant result and unchanged canonical expectation; both verified-phase flags are true. The four supporting phases must already have matched their separate predictions, so a crash, backend error or incorrect mutant result cannot masquerade as an intended rejection.

## Provenance and cleanup evidence

- All 1,847 pinned input files and existing bytecode cache inventories match; tool/Python resolutions match.
- Both exact source deltas remain only the warning plus declared guard removal, with one unique source anchor each. No outcome-driven change to an oracle or source was found.
- All 41 delivered file hashes match. All 167 completed S package files and all 64 completed fork package files remain unchanged against their pinned delivery inventories.
- Runner and launcher post-pin/cache statuses are PASS. Native binary/hash, mapped library path, exact command/optimization mode, parent acceptance and child/supervisor receipt hashes agree for every launch.
- Supervisors report clean direct-child reap, no reason, no cleanup error, the declared sixty-second/two-MiB limits and empty group signal-attempt lists. They explicitly do not verify all descendants absent.

Governing PINS digest: c1d565a4eb38506bd268317d2d01659323c4c10f70850936728285e9f882af84.

## Bounded conclusion

The evidence establishes finite sensitivity of these frozen S oracles to removing term verification and final material resolutions under the four named controls, in both interpreter modes. The invalid copies remain deliberately test-only. This result complements the earlier receipt-field mutation negatives; it is actual source-removal sensitivity evidence rather than only comparator field sensitivity.

These are internally consistent files/receipts, not externally attested execution. The reviewed router source establishes that expiry occurs after the real primitive returns and that its original immutable byte object is returned; receipts observe hook counts and exact-byte flags, not standalone object-identity proof. No fresh cryptographic recomputation of fixture bytes was performed.

The controls are not exhaustive mutation adequacy, native memory safety, leak/erasure proof, unselected failure/provider/queue qualification, containment-fault stress testing, timing/five-arm attribution, database qualification or product adoption. Those gates remain separate and unchanged.
