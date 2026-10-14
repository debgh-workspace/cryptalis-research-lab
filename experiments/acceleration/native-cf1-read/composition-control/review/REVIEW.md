# Independent source review: staged native-composition S control

2026-10-14. Source-only review. No build, candidate import, test, benchmark, PostgreSQL, network, installation, provider query/configuration, or Git operation was performed. Writes are confined to this review directory. Shell reads, JSON inspection and file hashes are evidence inspection, not candidate execution.

## Disposition

The proposed separation is structurally consistent with S: Python keeps CF1 composition and public admission; four stateless native primitives replace the corresponding primitive operations. No confirmed algorithm/composition defect was found in the inspected source. This is not compiler acceptance, execution admission, security qualification, resource/leak proof, or measurement permission. Keep execution and timing HOLD pending a separately frozen and reviewed harness/provenance/containment scope. The source explicitly acknowledges many of these gaps rather than claiming them closed.

## Positive source findings

- `staged_read.py:38-56` preserves context validation before NULL/frame work, exact immutable frame type, public frame bounds, representation and generation-shape checks, then payload/search pre-use resolution. Headers select admitted generation entries, not arbitrary custody.
- `_derive:11-23` uses the resolved material's domain, tenant, root identity and generation, including an older admitted generation. Payload info, search info, AAD and equality-message tuples remain Python; the tuple recipe agrees with S20's count-plus-length big-endian serializer.
- Storage enters SHA, HKDF, decrypt. Equality then enters SHA, HKDF, HMAC only after payload authentication. The complete term is compared with `compare_digest` before strict UTF-8/NUL handling. Final payload and search resolves precede string return (`67-78`). NULL enters no primitive and resolves active payload once. Repeating inputs does not take a cache branch.
- All four native functions check arity before argument indexing, exact bytes before accessing size/data, and private bounds before queue/resource setup. HKDF length and diagnostic selectors reject bool and integer subclasses. Size arithmetic and int conversion are bounded; the plaintext maximum is far below INT_MAX. HMAC's maximum accounts for the equality tuple's 20-byte overhead. Largest valid CF1 AAD is below the private 256-byte cap.
- SHA uses SHA256; HKDF explicitly requests EXTRACT_AND_EXPAND with SHA256; HMAC explicitly requests SHA256. All fetches and nested digest properties request provider=default, with default libctx. No provider loading or configuration change is present.
- Each call constructs fresh EVP contexts. Borrowed inputs remain owned by the CPython argument tuple while the GIL is held. Every acquired context/fetch has a common release path; scratch is clear-freed. Nonempty failed Python results are cleansed before decref. Decrypt reserves private result storage but copies scratch into it only after final success and output-size checks. Empty Python bytes may be shared; freshness must be established from execution traces, not object IDs.
- Primitive backend failures are constant-message RuntimeError; decrypt data update/final and size failures use the distinct constant data-processing marker. The wrapper translates this to the predeclared public stage policy and suppresses explicit cause display. It does not infer operational versus authentication causes from an EVP error string. That remains a stage policy, not proof of causal equivalence to P.
- Normal entry points never take a selectable fault. Diagnostic selectors short-circuit the corresponding operation and return through common cleanup. The 25 selectors total 6 SHA + 4 HKDF + 6 HMAC + 9 decrypt; 75 direct triplet entries and 54 public fault entries match their declared scope.

## Findings and admission gaps

### 1. Final search expiry is not established by the new wrapper boundary manifest

The twelve wrapper boundary records only expire resolved payload material. For equality, expected traces stop at the final payload resolution. These cases cannot prove that final search resolution occurs and refuses an expired search lease after payload postcheck succeeds. Add explicit search-only initial/final expiry cases and exact argument/order expectations to the S adapter; include post-decode and final-native-return placement where appropriate. The wrapper source contains the correct final search call, so this is a coverage/admission gap, not evidence of missing implementation.

Actual inherited-key child rejection, fresh-child material success, PID changes after work, interleaving and repeated-call state changes also require the new S harness. Existing F results cannot substitute for these observations. The pinned public-input corpus may supply cases, but a reference to that corpus is not an S execution adapter.

### 2. Fault coverage is deliberately narrower than all exit branches

Selectors do not exercise returned digest/MAC lengths, cipher key/IV property refusal, decrypt produced/tail guards, ERR_set_mark refusal, ERR_pop_to_mark failure, real allocation/provider errors, or marked/overflow queue behavior. The manifest explicitly lists these omissions. In particular, failing before an EVP operation cannot demonstrate cleanup after that operation partially modified an output or added queue entries.

Before describing fault/resource admission as complete, freeze how these branches will be observed or keep them explicitly unqualified. Resource observations must count actual acquisition/release/transfer/cleanse events for S; deriving counts from selector values alone is circular. Test actual-output mutations against the verifier, not just expected-oracle edits. The negative controls need to demonstrate that wrong bytes, wrong stage, wrong resolution/entry order, missing owned-result transfer and missing scratch clear/free cause refusal under normal and -O execution.

### 3. Error-queue preservation is limited by design

`begin/finish:45-55` uses a mark on a preexisting queue and clear on an initially empty queue, with no blanket entry clear. This is not full queue-state preservation: preexisting mark state can be consumed, bounded queues can evict prior entries, and pop failure is ignored. Six separate scopes on equality add opportunities not exercised by F's single-call results. No runtime preservation claim is justified yet. Freeze explicit initially-empty, preexisting-entry and marked/overflow observations, preserve the stated limitations, and do not call this provider isolation.

### 4. Direct ABI harness must be frozen before execution

The 114 refusal records are a useful finite starting corpus, not a complete ABI suite. Add or explicitly scope out diagnostic missing/extra arity, keyword-call refusal, selector precedence with other bad inputs, valid extrema for all admitted variable lengths, and normal-vs-diagnostic export/API checks. Valid boundary values need independently frozen expected results when the claim is successful processing, not merely absence of crash. Exact type and complete byte comparison are required; lengths/counts alone are insufficient.

Freeze read-only import origins for the separate wrapper/native module and pinned S20 dependency. `import native_primitives` is unqualified, and `from cryptalis.crypto import cf1` depends on the launcher environment. An origin check must reject stale or shadow modules rather than letting a previous F or unrelated artifact silently satisfy the run.

### 5. Harness containment/provenance is still missing

There is no supplied launcher or executable harness, as DESIGN accurately states. Before any build/import, specify exact compiler/Python ABI/header/library pins and flags, artifact-exclusive output paths, normal/diagnostic deltas and source-to-binary receipt checks. F's recorded -lcrypto command and linked-library hash do not identify a future S build's actual resolution. Check the actual built dependency and provider identities within an authorized scope rather than extrapolating from version strings.

A reviewed bounded child lifecycle must cover import refusal, expected exception, native crash, timeout, interrupted parent and malformed/missing child output. Freeze process deadlines, bounded output capture, process-group termination/escalation, wait/reap and absence of surviving descendants. Child cleanup is an admission property independent of crypto cleanup. Do not start runtime work until the specific build/run scope is selected.

### 6. Observable allocation and backend equivalence remains limited

Native result reservations are normalized, but Python argument packing, tuple creation, decoding and diagnostic creation have allocation boundaries that are not uniformly caught. SHA only catches RuntimeError; an allocation failure before entering that C operation may escape. Existing S20 likewise has uncaught regions, but equivalence across changed allocation schedules is not established. This limitation is acknowledged in DESIGN and should remain explicit.

S exposes Python-resident intermediate salts, derived keys and authenticated encoded bytes within its private composition path. They are not application outputs before final checks, but neither explicit-cause suppression nor native scratch cleansing erases Python locals, exception traceback references, immutable values or provider internals. No full zeroization claim is supported.

## Frozen expectation review

`reused-fixtures.json` is byte-identical by SHA-256 to the pinned S20 `tests/fixtures/cf1_vectors.json`: `24c918629ac10d7fb739fd02a946ecdbbcf1de4102bb353cf069cc095a3b286e`.

The 44 ORACLES records comprise two literal SHA answers, six existing primitive vectors, and 36 applicable intermediate expectations from eight CF1 vectors. `prepare_source.py` copies expected outputs from the frozen fixture; it does not obtain expected outputs from S. Its independent tuple construction agrees structurally with the serializer and the stated recipes. The reference fixture generator source describes independent RFC8452 composition using AES-ECB plus stdlib SHA/HKDF/HMAC; it was read, not run. The fixture's independence is from the S implementation, not an independently selected underlying AES implementation/provider in every historical execution.

This review checked the literal-source relationships and recipe construction, not a fresh cryptographic recomputation of every expected byte. Future harnesses must compare all actual bytes and types against these frozen constants and verify the fixture/hash before import. Full-wrapper frames, exact decoded strings, authenticated invalid text/terms, failure precedence, older generations and ordered resolves need the complete public corpus plus S-specific adaptation. Primitive intermediate success does not establish full-read success.

A small schema consistency point: wrapper success records call the AEAD entry `decrypt`, whereas public fault traces call it `payload-decrypt`. Freeze the observer naming/normalization rule so a harness does not accidentally skip or silently rewrite a trace field.

## Inspected artifact fingerprints

- native_primitives.c: 0202228f236a80ef25e14cee0eb767289e4a4d7c094eb1e03ae34ac87beded98
- staged_read.py: 0bc354865900d382ba3010a2bbde7fde79727469bf97e2b5420dfe7668e80d9e
- ORACLES.json: 4bcae01f650b3a96c0ac5e2dff2cc9503296b9411a1284d48d5e2e8c9efd0a2a
- S_BOUNDARIES.json: 090c7327df62a5d4f390b2bd4dbfdc11e923f5966b0a1dd1a7fdeaed5c0efb89

These match the inspected ARTIFACTS manifest entries. Other sources read: S DESIGN/STATUS/SOURCE_INDEX/prepare_source, pinned S20 cf1.py/keys.py and reference generator source, original native CF1 design, and the opening public-admission corpus metadata. No source was changed.

## Smallest next step

Prepare and independently review a source-only direct ABI plus wrapper harness/provenance/containment specification, including search-only expiry, real observation negatives, normal/-O verification, and explicit unresolved fault/queue/resource scope. Then ask the coordinator to select a finite authorized build/run scope. No timing, product adoption, backend attribution or database qualification follows from this review.
