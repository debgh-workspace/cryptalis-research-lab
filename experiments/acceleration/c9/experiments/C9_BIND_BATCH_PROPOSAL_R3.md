# C9 decision proposal: one synchronous IN-bind batch

Status: PROPOSED, no runtime changes. This narrows the earlier exploratory
C9_FUNCTION_SCOPE_PROPOSAL.md. It is the proposal submitted for coordinator
review. The earlier document remains as an unimplemented blocked alternative.

## Existing boundary, and the precise change needed

Current `_sqlalchemy_search.rewrite_search` creates a SQLAlchemy expanding
bind. `_SearchValue.process_bind_param` receives one element at a time. There is
no whole-IN invocation around which to reuse a function-local derived key.
Retaining one on that scalar processor would create a longer lifetime and is
rejected. Rewriting plaintext into terms earlier in rewrite_search would move
crypto ahead of later admission checks and is also rejected.

The bounded integration option is a private `_SearchTerms` TypeDecorator with
`ARRAY(LargeBinary)` implementation and `cache_ok=False`. Its single synchronous
process_bind_param receives the entire concrete tuple, computes all terms,
and returns a list of bytea/NULL values. It retains only the same existing
operation keys/descriptor/tenant already captured by `_SearchValue`; **no derived
key is retained on the decorator**. The derivative code path lowers supported
positive IN to `substring(payload,15,32) = ANY(:terms::bytea[])`. PostgreSQL gets
the same full-width terms. Fixed substring constants, tenant scope and generated
node permits remain. No user ANY-expression or other grammar is newly admitted.

For a first experiment, optimize only exact tuple inputs with 2–20 members,
whose members are exact str or None. Every list, empty, singleton, missing/required,
nonconcrete, invalid-typed and larger input keeps the existing expanding-bind
path unchanged. SQLAlchemy may coerce a literal .in_(tuple) into a list; that
case remains baseline. Explicit late-bound tuple values are the intended cell. NOT IN and scalar equality also keep the existing path.
These are optimization eligibility checks, not new query refusals or plaintext
fallback. Separate placeholders per occurrence and shared-name ambiguity checks
remain as they are. Bind processing stays at its existing pipeline position; every admission
stage remains. In particular check_cursor still performs its check afterward. No derived key crosses a process_bind_param return.

The ARRAY callback rechecks the actual input. It does not use rewrite-time
eligibility as authority. Materialize the input at bind time using the native
expanding algorithm's falsy-empty branch and flat list comprehension (not a
container constructor that adds length-hint hooks). If the actual value is no
longer an eligible immutable tuple, use original per-element equality_term
without KDF reuse. The emitted SQL remains ANY; the callback cannot change back
to expanding IN. Therefore exact empty/NULL and invalid/member/iterable failure
equivalence is a mandatory gate, including altered generated binds. No values
are frozen early during rewrite. Arbitrary concurrent mutation/host event
extensions are not newly qualified by this plan.

Changing SQL shape to ANY is a real implementation change. Bytea-array adaptation,
NULL/empty semantics, fixed-index compatibility and native error behavior need
proof; they are not assumed from the source resemblance. No runtime patch is
authorized by this document alone.

## Function-local crypto mechanism

Introduce a private bulk-query-term helper, not a new public crypto API. Factor
only equality_term's existing validation/resolve body into a private helper
whose term computation can be supplied internally. Public equality_term keeps
its signature, semantics and default `_term`; open_text, seal_text and payload
key derivation remain byte-for-byte unchanged. Do not refactor their shared
`_term` hot path for this query-only optimization.

The bulk helper owns local `search_key` and `material_seen` variables. It loops
over the finite input, using the original per-item validation body. The callback
is reached only for non-NULL items, after the original search-material resolve.
On its first call it computes the exact existing search HKDF using original
salt/info bytes and stores the derived bytes locally. On subsequent calls it
requires the same exact material and fixed descriptor, then performs the same
HMAC algorithm and tuple encoding. The original final resolve still runs for
every item, including NULL. No HMAC/term/plaintext result memoization occurs.

A finally block clears scope-owned key/material/callback references on success
or BaseException before returning the complete list or propagating failure.
The local helper cannot be returned, suspended, yielded or reused. No new
ContextVar, global, processor, PreparedKeys or Keyring cache is introduced.
Existing bounded root caching remains unchanged. Python bytes/tracebacks still
do not provide verified zeroization; clearing references is not such a claim.

For L input members, K non-NULL members, the expected query work is:
- Original and candidate: 2L `_resolve` calls, in the same before/after sequence.
- Original and candidate: K HMAC calls, all existing per-item field/tenant/text checks.
- Original search HKDF: K. Candidate search HKDF: 1 if K>0, otherwise 0.
- Payload HKDF, open_text, returned-row checks: unchanged, outside this helper.
- A second invocation must derive again; no hit survives an invocation.

The term key depends on admitted root/context and field, not plaintext or row.
Reusing it under these fixed inputs does not change CF1 terms, headers or frames.
Per-item resolve calls still enforce absolute expiry and PID/context checks.
No time or provider failure can renew a lease. Failed derivation is never cached.

## Exact first test slice, before timing

Prepare the following in this separate S18/C8-based copy. Use existing public
fixture roots, frozen vectors and independent stdlib HKDF/HMAC reference. No
worker DB calls. Product changes wait for coordinator approval.

1. Query-term equivalence: public equality vectors; mixed None/empty/Unicode/
   composed/decomposed/trailing-space/duplicate values; list and tuple sizes
   0,1,2,20,21. Compare exact bytes or None with the independent reference and
   original per-item helper. Input shape eligibility must not change failures.
2. Guard/count trace: capture purpose/generation and field/tenant validation
   counts without key values. Compare the original sequence exactly, including
   two resolves per NULL. Confirm K-to-one HKDF reduction only within one batch,
   no cross-batch reuse and no new payload derivation.
3. Lease failure trace: expiry before first element, between elements after a
   warm local key, during first HKDF, during later HMAC, and immediately before
   the final original resolve. Require original typed failure and no returned
   partial list; scope cleanup must execute. Use deterministic fake clocks only
   in the pure test, then one real short-lease case if approved.
4. Context/PID: wrong domain/tenant/field, absent or changed generation, different
   PreparedKeys/material, and inherited fork PID. Warm local state must not
   bypass any refusal. Separate independent thread invocations remain isolated.
5. Backend/cancellation cleanup: first derive failure, HMAC failure and injected
   BaseException/CancelledError all close local state; a later fresh invocation
   derives again and succeeds. Injected exceptions are not async DB evidence.
6. Mutation sensitivity: removing final resolve, preserving state across calls,
   reusing mismatched material or suppressing cleanup must fail the exact tests.

After pure proof, coordinator-owned native PostgreSQL tests compare supported
IN's exact ordered rows and projected TRUE/FALSE/UNKNOWN values against native
IN, using independent driver `= ANY(text[])` as a second oracle. Include NULL
left side, empty, all-NULL, mixed NULL, duplicates, late/shared named values,
repeated predicates, aliases, two fields/tenants, scalar/entity projections and
public-ID pagination. Include before_execute mutation of original list inputs:
growth from 20 to 21, clearing, invalid members, and shared named lists. They
remain on the baseline route. Also replace a generated tuple bind before
processing with another tuple, list, empty value, invalid member or iterable;
any differing native outcome is a blocking failure, not a new refusal. Check existing fallback cases and unsupported-expression
refusals before driver execution. Compare custom/generic EXPLAIN shapes without
forcing index use. All original admission/key/security regressions must remain.
These are existing positive-IN contracts, not new ANY or query capabilities.

## Benefit limit and performance decision

This mechanism saves **query-side K−1 derivations only**. It does not save the R
returned-row search derivations. C8 measured 20 query derivations for IN-20 and
286 more for its hot text projection. Therefore this is a much smaller candidate
than whole-result sharing. No 11.5–13.1% end-to-end saving is implied.

If equivalence passes, predeclare one paired baseline/candidate benchmark using
exact C8 runtime as baseline, both pinned dependency cells, fixed IN-20 miss and
hot IDs-only workloads plus IN-20 hot text, equality-hot text and point controls.
Both baseline and candidate use the same explicit late-bound tuple inputs; this
is a new finite lowering experiment on frozen C8 runtime, not a C8 rerun.
Untimed checks must independently observe the intended ANY array path and K-to-one
derivation before timing. Literal-list controls must still show the original
expanding route. A benchmark that measures fallback only is invalid. Use the same public
fixture and existing warm Keyring. Seven alternating blocks, ten warmups and
forty retained samples per cell is the proposed fixed schedule. Proposed finite
criterion: at least 5% median reduction and 6/7 favorable blocks for both primary
IN-20 IDs-only workloads on both dependency versions; no more than 10% median
regression on any control. Alongside this internal relative gate, retain the
absolute added-p95 targets of 3 ms for equality and 8 ms for IN-20 versus the
independent native workload. Report both IDs-only and returned-text IN-20
separately. Passing the internal gate does not qualify product performance. The coordinator must approve this exact gate
before timing. A failed gate is retained without lowering thresholds or retrying
for a favorable result. C1 and C5 remain held regardless of C9 outcome.

## Explicitly blocked alternative

Returned-row reuse would need a bounded function that owns multiple row decrypts.
Ordinary SQLAlchemy execute(), all(), fetchmany(), iterator and close lifetimes
do not provide that one boundary in current source. A key stored on `_ReadText`
or a Result would be a lazy lifetime cache. Do not implement it. Do not insert
implicit eager materialization, change streaming/native errors, or describe the
standalone batch exploration as a product optimization.


## Frozen timing arithmetic clarification (R3)

Timing may begin only after equivalence and mutation gates pass and coordinator
review clears the exact frozen implementation. Every dependency cell uses five
workloads: IN-20 miss IDs-only, IN-20 hot IDs-only (the two primary workloads),
IN-20 hot text, equality-hot text and point text (three controls). Each of seven
blocks runs all five in this fixed order. Within each block use variant order
(native, expanding baseline, candidate) for even zero-based block numbers and
its reverse for odd blocks. Each variant/workload/block has exactly ten retained
warmup observations followed by forty retained measured observations. There are
5,250 executions per dependency cell: 1,050 warmups and 4,200 measured. Raw start,
end, elapsed wall/RAW/process/thread clocks, row/native checks and run order are
retained. No cProfile runs, filtering, retries or posthoc exclusions.

For each variant/workload, compute seven measured wall-time block medians, then
the median of those seven medians. Relative reduction is 100*(baseline-candidate)
/ baseline using those two aggregate values. Favorable blocks count strict
candidate block median < baseline block median for the same block. Both primary
workloads must improve >=5% and have >=6/7 favorable blocks on both versions.
Each control's aggregate candidate/baseline ratio must be <=1.10. A failed
condition is a failed internal gate. Do not average versions or let one workload
compensate for another.

Report absolute added-p95 separately: nearest-rank p95 (rank266 of280) of all
measured candidate observations minus the same independently measured native
workload's nearest-rank p95. The target is <=3ms for equality and <=8ms for each
IN-20 projection; record all nominal PASS/FAIL values and any anomalies unchanged.
These absolute targets do not replace the relative gate; neither set alone
qualifies product performance. Report native and original baseline medians/p95
for context. All observations remain available if clocks disagree or run fails.
