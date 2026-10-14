# Pre-execution owned-resource accounting review

Outcome: PASS STATIC ONLY. No blocking defect found in frozen source, expected resource ledger, or harness. No compilation, native import, candidate execution, database operation, Git operation, or shared candidate modification was performed. Only this review directory was written.

The author freeze matches the seven reviewed source files recorded in STATIC_AUDIT.json. The stdlib-only audit performed 465 checks, including 152 wrapper observations (149 unchanged inherited fault-oracle cases plus three term-sequence cases), 18 direct ABI observations, all referenced fixture hashes, independent acquisition-stage expectations, requested scratch capacity, Python syntax, and no assertion-dependent checks.

## Source review

Compared the complete diff against candidate-native-cf1-read-20261014/native_cf1.c. Changes are diagnostic counters, wrappers, entry reset of per-call deltas, result release/transfer accounting, and a snapshot method. The diagnostic-only compile guard rejects non-diagnostic builds; original implementation is not edited.

- Eight EVP resource categories increment only for non-null returned owned references. Null-safe cleanup wrappers decrement only non-null owned references and invoke the original matching release function once. The derivation helper frees each set before returning, so payload and search derivation have per-category peak one despite acquisition count two.
- Scratch capacity remains n + EVP_MAX_BLOCK_LENGTH, with the original overflow and input-bound checks intact. The header value is 32. The same capacity is used for allocation and clear-free accounting. Null allocation does not increment counts or bytes; null cleanup does not subtract bytes.
- Reserved PyBytes counts an owned reference, not a unique physical allocator block. Refusal records release immediately before Py_XDECREF; success records ownership transfer immediately before returning the reference. These are distinct operations. PyBytes destruction after return is outside the accounting boundary.
- Existing arity, selector, representation and frame admission returns precede acquisition. balance_begin runs before those checks, resetting per-call deltas and initializing peaks from existing outstanding balances. Live counts and outstanding scratch bytes persist across calls, including refusal/recovery sequences. Thus a prior imbalance is not simply erased at the next call.
- The snapshot allocates reporting Python objects outside the boundary; its list owns inserted rows and its result takes list ownership. No counted operation runs inside the snapshot.
- Data buffers, output-length checks, cleansing calls, authentication checks and error mapping were unchanged. This review does not independently qualify provider write bounds, erasure or partial-provider-failure behavior.

## Oracle and harness

Expected resource counts are predeclared from acquisition cutoffs, not learned from diagnostic output. Independent static enumeration confirms all 152 wrapper expectations, including bad-tag cutoff at authentication finalization, term mismatch after full acquisition, successful result transfer and refusal result release. Scratch expectations are independently checked against frame lengths. The direct admission refusals require zero resources; successful calls compare the representation-specific seven-byte success ledger.

The unchanged Python wrapper and mapper are used, with native routing only. Actual public values/failure fields, trace and native call count must exactly match the inherited oracle before resource accounting passes. The final ordered IDs must cover all 170 observations. Comparator checks do not disappear with Python optimization. Native origin/version, wrapper origins, interpreter and input provenance are checked by the harness.

The captured direct-call arguments are overwritten before each success-designated routed call. Each such call is subsequently validated against its expected success. The last storage and equality captured arguments are successful seven-byte recovery inputs, so direct before/refusal/recovery cases are valid.

Negative controls first accept a real successful observed record, then corrupt one recorded release or transfer field. This demonstrates comparator sensitivity, not a native leak or skipped cleanup experiment. Native counters and release wrappers remain related instrumentation; the independent stage inventory and static diff reduce, but cannot eliminate, common-mode defects.

Build freeze writes source pins before compilation and complete pins before imports. Original source trees are included in preserved provenance. Runtime evidence must still be inspected after execution; this report is not a runtime pass.

## Limits

Evidence can establish matched helper-owned reference cleanup invocations and result transfers in the selected sequential GIL-held executions. It cannot establish internal OpenSSL/provider allocator frees, general leak freedom, memory zeroization, allocator exhaustion, all partial failures, provider identity/custody, overlapping concurrency, fork/subinterpreter safety, general ABI compatibility, packaging readiness, production security or performance. Broader admission holds remain unchanged.
