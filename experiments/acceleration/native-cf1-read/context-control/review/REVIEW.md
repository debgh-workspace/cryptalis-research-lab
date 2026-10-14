# Independent static review of D context control

2026-10-14. Scope: source/data inspection only. **HOLD for execution admission and timing; source mechanism is coherent, not a full approval.** No candidate was imported, compiled or executed. No tests, PostgreSQL, network, Git, install or provider changes were performed. Only this review directory was written.

## Findings first

1. The intended D mechanism is actually implemented. Fresh encrypt and decrypt bases are allocated and keyed per admitted non-NULL native call; the working decrypt context is freshly allocated, copied from the keyed decrypt base, then given the frame nonce with NULL key/cipher arguments. There is no retained keyed state, dummy loop/encryption, retry or alternate-backend fallback. No new source-level ownership defect was found in the reviewed delta.
2. This is a source-only package, explicitly not runnable admission. A concrete, independently reviewed launcher/build/harness and diagnostic exception adapter remain missing. Existing F receipts do not establish a D pass. Do not compile or execute on this review alone.
3. The original DESIGN's stronger causal failure requirement remains unmet. Data/final failures still become AuthenticationFailed even when an injected operational failure caused them. This is the documented source-observable stage policy, not a causal classifier. An authorized explicit policy disposition remains necessary; this review selects neither FP1 nor a measurement option.
4. A concrete path-resolution gap must be closed in the launcher: fault-plan fixture paths are `fixtures/grid-000-1.bin` and `fixtures/grid-100-1.bin`, but D contains no fixtures directory. These files currently live under candidate-native-cf1-read-20261014. Freeze the exact original fixture root and verify each declared hash; do not resolve relative to D, guess a path, regenerate fixtures, or search fallback locations.
5. The new diagnostic surface has no finite diagnostic-ABI supplement yet. The inherited 100 ABI cases target the nine-argument public helper and contain no selector cases. They do not by themselves exercise open_observed's ten-argument contract, selector exact-type/overflow/range checks, captured exception representation, or all-zero counters on invalid input. Freeze those checks before claiming diagnostic boundary admission. The source also admits unused in-range selectors; F accepts 36–40 but does not execute D sites. Therefore selectors alone are not mode evidence.
6. Paired F is specified by source macro absence and one success-counter vector, but a concrete per-build admission matrix is not supplied. D's new-site faults must not be blindly applied to F as failures. Freeze which common normal/diagnostic cases run against rebuilt F, which cases are D-only, and explicit mode discrimination with fresh counters. A named module or existing F binary does not prove paired-source provenance.

## Independently verified static facts

- All 13 entries in SOURCE_INDEX.json match current file bytes.
- Original F C SHA-256: 2926d61e43b3dc53a5fff56ab5367982c89b92b146ef9cbc47fbd2b71e5a9469.
- D C SHA-256: e31a1697ae15b7c35fec7cd43eb3055dbf6d6801978ca6ee0150d036b18fb7e2.
- Both wrappers are byte-identical: 4d3151148b435d7f54235b3eda864ea85e6def5cd6a4f9b5025d09bdd425a703.
- SOURCE_DELTA.patch is exactly the unified textual diff of original F and D, with its declared headers; no extra source delta was hidden outside that patch.
- All four plan.json manifest hashes match. Selected ID lists exactly equal their source manifests, in order, with no duplicates: admission 1,098; ABI/fork 106 (100 ABI and six fork); immediate-return expiry two; inherited faults 149.
- D's first 149 fault records and both fixture specifications equal the inherited fault manifest. Ten added triplets account for the remaining 30 records. Total 179 IDs are unique. Storage has 22 reached fault selectors and equality 36, giving 58 triplets/174 calls plus five precedence observations. Search-only faults are absent from storage.
- These facts were calculated with a standalone standard-library text/JSON/hash inspection, not by importing project code. They establish preparation consistency, not runtime correctness.

## Source mechanism and ownership

References below are to candidate-native-context-control-20261014/native_cf1.c.

- Lines 92–145 retain exact ABI/bounds checks, GIL-held borrowed immutable arguments, call-local state, fresh payload derivation and explicitly default-provider cipher fetch. Material scope/generation are trusted resolved wrapper outputs, as in F; this private ABI is not a public admission substitute.
- Lines 148–155 allocate and key encrypt_base and decrypt_base using EVP_EncryptInit_ex2 and EVP_DecryptInit_ex2. Both are real keyed provider contexts. NULL nonce here is base construction, not a skipped key setup.
- Lines 157–167 allocate working cc, perform exactly one EVP_CIPHER_CTX_copy, then initialize the nonce while preserving copied key state. Every failure immediately enters common cleanup. There is no replacement allocation/reinit recovery on copy failure.
- The retained upstream OpenSSL 3.5.7 source snapshot in candidate-notes-native-failure-mapping-20261014/openssl-cipher_aes_gcm_siv.c, lines 91–120, conditionally updates key/nonce and calls hardware initialization. It supports the intended NULL-key nonce reinitialization model; this does not prove installed binary correspondence or actual provider-copy success.
- Lines 170–198 preserve F's result-reservation order, scratch ownership, tag/AAD/data/final order, then equality search derivation/HMAC/full constant-time term comparison. Result bytes are only copied after required checks; no failed value is returned.
- Lines 200–218 free working, decrypt base and encrypt base exactly once if acquired, then the fetched cipher. Derive resources have their unchanged local cleanup. Scratch is clear-freed; local keys, term/info/AAD are cleansed; private result is cleansed/decref'd on failure. A failed actual copy still leaves owned cc scheduled for free. This is source-level owned-resource reasoning, not provider-internal leak/erasure proof.
- No global counters or secret storage were added. The static module descriptor is ordinary module metadata. COUNT and count storage are conditional on CF1_DIAGNOSTIC and disappear from non-diagnostic builds. The paired F delta still includes small source cleanup/control-flow changes (conditional non-NULL free), so use rebuilt paired F rather than silently claiming original binary identity.

## Failure policy and safe release

The wrapper is unchanged. It preserves context validation before frame handling; NULL active-payload resolution; frame/generation admission; initial payload then search resolution; strict UTF-8 and NUL checks; final payload then search resolution before return. No plaintext fallback exists.

Native failure starts as the fixed private label `backend`; lines 175–179 set `data-processing` for update/final and output-size guards; line 180 restores `backend` for search processing; a verified wrong full term uses `term`. The unchanged wrapper translates these to CryptoBackendUnavailable, AuthenticationFailed and RepresentationMismatch, respectively, with suppressed explicit chaining. New sites 36–40 are setup failures and retain backend classification. Provider strings/queue contents do not decide causes or escape via these labels.

Inherited limitations remain: native salt-hash normalization differs from S20 allocation/try boundaries; allocation order differs from pyca; pyca copy recovery is omitted intentionally; actual exception allocation failure can propagate MemoryError rather than a guaranteed fixed RuntimeError; arbitrary queue/mark preservation is not established. Source-only inspection cannot turn these into PASS.

## Diagnostic counters and observer

Counter order is exactly the eleven named fields in counter-expectations.json. Static success expectations are D eleven ones and F [0,0,0,0,1,0,1,0,0,1,1]. All seven listed D fault prefixes (36,37,38,39,11,40,12) match the placement of increments and common frees. Early derive/fetch failure counts are zero. Post-setup refusal counts equal success except result_transfer=0. Every acquired context has a matching owned free-call count. These are API-call accounting, not independent observation of provider allocator frees.

open_observed lines 226–237 uses stack-local counts, fetches exception type/value/traceback on failure, drops traceback and packages four fields, then decrefs temporary ownership. It does not normalize the captured exception. The planned adapter must handle both exception instance and unnormalized exception value, reject inconsistent observation shapes, re-raise before the unchanged wrapper mapper, and never treat the record itself as plaintext. Record allocation failure propagates; result_transfer describes return from open_impl, not successful publication of the observation record. A successful diagnostic packet must not be invented after packaging failure.

Selector failures short-circuit the target operation. In particular selector40 never produces a partially initialized provider-copy destination, and key-init selectors never execute failing init internals. Counter balance under these selectors cannot prove cleanup under real partial provider failure. Keep that distinction in receipts.

## Finite admission work still required

Before any build/run, freeze and independently review:

- Explicit authorized failure-policy disposition and execution scope; source preparation is not timing authority.
- Concrete paired F/D normal/diagnostic/mutant build matrix, complete compiler flags and macro exclusions, pinned interpreter ABI, compiler/headers/libcrypto/dependencies, S20/module origins, provider/property observations and source/binary/build receipts. Normal builds must exclude diagnostic and skip-term macros. No provider or dependency mutation.
- Exact harness/support sources and fixture roots/hashes. Enforce pins before candidate import, reject duplicates/missing/extra IDs and assert-dependent validators, and use exclusive-create receipts preserving partial failures.
- Concrete open_observed routing adapter and finite diagnostic-ABI cases. Assert value is None for every captured failure, correct exception type/value normalization, exact eleven-counter schema, and no exception type/value on success. Ensure invalid ABI counters are observed rather than assumed from normal helper exceptions.
- Both optimization modes for normal wrapper admission, two immediate-native-return expiry checks, isolated actual-fork containment, direct diagnostic vectors/faults and mapped diagnostic faults. Freeze the corresponding paired-F scope separately. Preserve independent expected text/bytes, diagnostics, complete resolution arguments/order, entry counts and precise failure precedence.
- New fault expectations must be independently anchored to the inherited setup/result-allocation oracle. Current new-site expected records match that source-derived pattern; successful D output must never become its own oracle.
- Materialize exact negative-control IDs/launch modes: wrong actual output, stage, trace, free count and copy count; disposable skip-term and skip-final-resolution mutants. Require intended discrepancies and nonzero exit in normal/-O; distinguish validator perturbations from actual source removal mutants. Preserve baseline observations before perturbation.
- Explicit source-review dispositions for unselected guards (cipher properties, mark failure, output bounds, exception construction), accepted queue scope and resource-tool limitations. Sanitizer/leak claims require separately authorized frozen containment and actual evidence; unavailable or disabled leak detection remains UNKNOWN.
- Stop on first correctness/provenance failure, retain partial evidence, and do not rerun to obtain a favorable receipt. Do not treat the 179 fault observations or any other heterogeneous counts as a full DESIGN pass.

No timing harness exists in D. Original five-arm timing, matched-backend attribution, product adoption and S20 promotion remain outside this review. D:F can eventually speak only to this wrapper's fresh context strategy and cleanup bundle, not exact pyca constructor cost or isolated backend effect.
