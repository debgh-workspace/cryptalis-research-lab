# Bounded T fault/fork V2 result

2026-10-14. Independent source review and separate root authorization preceded
execution of the exact frozen ten-process schedule. All evidence is preserved in
evidence-01; V1 remains unexecuted and unchanged.

- 88 literal observations PASS in ordinary mode; 88 PASS in -O.
- 44 exact P:T parity pairs PASS per mode.
- Eight declared record/receipt negatives fail with the exact expected signature.
- Ten top-level processes report reaped, with no cleanup errors, timeout, retry or
  unexpected failure. Actual fork children total ten: four positive groups plus
  one fork-PID negative in each mode. Every observed child is reaped.
- All source/cache checks and child-reported pre/post binding checks PASS.

Each positive mode contains 60 successful returned values and 28 refusals: 12 raw
MemoryError boundaries, six CryptoBackendUnavailable boundaries, six after-last-
tuple expiry refusals, and four inherited-key PID refusals. No normalization was
changed. Preallocation injection validates selected T arguments before returning
MemoryError; it does not exercise real allocation exhaustion or prove all-
allocation equivalence. P uses corresponding local tuple-path injection in a
byte-identical isolated S20 module, leaving the canonical P module untouched.

Valid/fault/recovery and valid/expiry/recovery sequences use freshly prepared
public material per invocation. Success always returns exact `abcdefg`, while
failed calls publish no value. Tuple entry/completion and exact hook counts match
the frozen literals. Helpers return exact immutable bytes, without subclasses.

Actual fork groups reject inherited PreparedKeys at the child's first payload
resolution with zero tuple calls, then succeed using fresh public material in the
child. Parent-before and parent-after both succeed. Parent records real fork
return/child/parent PID relations, exit status, IPC length and reaping. Source,
cache and binding guards are child-reported checks before/after observations,
not independent attestation of child memory.

The stream-cap, forced-kill, secondary-cleanup-error and terminal-UNKNOWN failure
branches remain source-reviewed, not fault-injected or newly proven by clean
runs. Equality payload expiry immediately after tuple 3 is not in this slice;
selected equality expiry is after tuple 6. Sanitizers/leaks, code-removal mutants,
real allocator exhaustion, full original DESIGN, distribution and timing remain
separate. No rebuild, product/PG change, network, install, credentials or Git work.

Freeze SHA256: 769a44018f19be155d50924017f1208a5fe3467b10df579c7159b2a3404668c9.
Independent data-only postrun audit was requested; this report does not preempt it.
