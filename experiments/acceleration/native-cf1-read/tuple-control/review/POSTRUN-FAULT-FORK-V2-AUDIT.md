# Fault/fork V2 independent postrun data audit

2026-10-14. Reviewed `fault-fork-v2/evidence-01` as saved JSON/source/hash data only. No candidate/harness import, rebuild or rerun by this reviewer.

## Exact finite observations

Both ordinary and -O positives contain the exact ordered88 unique manifest IDs. Every actual record matches its full frozen literal expectation with recursive type-aware comparison. All44 P:T pairs match exactly per mode. Total176 positive observations and88 parity comparisons.

Per mode:60 successes,12 raw MemoryError refusals,6 CryptoBackendUnavailable refusals,10 KeyUnavailable refusals. Checked exact value/type/publication flags, empty MemoryError args and cause flag, typed error metadata/safe args/operation presence, ordered resolution traces, entered/completed tuple counts and fault/expiry-hook counts. Raw info/salt failures remain raw; AAD/equality-message failures remain backend-normalized. Failure records publish no value. Separate fresh recoveries return exact `abcdefg` with complete expected resolution traces.

After-last-tuple expiry rejects at the correct final payload/search resolution in both P and T. Inherited-child material rejects on first payload resolution with zero tuple entries; fresh-child preparation succeeds and parent-after reuse succeeds, as separately retained records.

## Negative and fork evidence

Eight intended negative runs, four per mode, have exact exit1/FAIL/RuntimeError `Supplement mismatch`, expected traceback suffix, no accepted observations and original_verified=true. The raw-boundary/count/trace originals match their selected literals and mutations change exactly the declared field. Fork-PID originals satisfy valid PID relationships; mutations change child_pid to parent_pid and nothing else.

Ten actual-fork receipts are retained: eight in the two positives and two underlying fork-PID negatives. Each has integer child_pid == fork_return_pid, child_pid != parent_pid, observed_parent_pid == parent_pid, exit0 and reaped=true. Each reports source/cache and binding checks PASS before and after child work. Every corresponding fork_attempt record has the correct group/PIDs, PASS/reaped,10-second operation deadline and2-second cleanup budget. IPC sizes range1126–1318bytes, within65536bytes. These are source-supported relational receipts, not independent process-memory attestation.

## Launch, integrity and preservation

Exactly21 evidence files:10 child receipts,10 launch records and aggregate launches.json. Individual and aggregate launch records match in frozen mode order; all result hashes match. All10 top-level records show launcher_reaped=true, terminal_state=reaped and cleanup_errors=[], with180-second deadline/10-second reap budget/65536-byte per-stream cap. Positive output streams are empty; negative stderr is the intended bounded traceback. Mode/-O flags agree. Every child has matching precheck/postcheck PASS and freeze SHA256 `769a44018f19be155d50924017f1208a5fe3467b10df579c7159b2a3404668c9`.

All4473 frozen pins match current bytes and all scoped bytecode inventories match. The frozen diagnostic binary, source manifests and preceding source/artifact pins remain intact. No inconsistent outcome or unexpected failure is present in this bounded evidence directory.

## Limits

This supplies finite diagnostic preallocation-fault, after-last-tuple expiry and actual-fork consumption-boundary evidence with exact P:T parity on public synthetic fixtures. It does not prove true allocator exhaustion behavior, every possible allocation fault, secure erasure, production key-provider custody, cross-platform fork safety or cancellation semantics.

Overflow/timeout/interruption/kill-failure/unconfirmed-reap branches were not deliberately exercised. Successful normal reaping does not qualify those failure-containment paths. Child guard flags and process receipts are not signed execution attestation.

Equality payload expiry immediately after tuple3 remains outside these after-last-tuple cases. Genuine skipped-term/final source mutants, supported sanitizer/leak evidence, full DESIGN mapping/closure and any five-arm timing/product decision remain separate gates. No normalization policy was changed. No timing result or admission is implied.
