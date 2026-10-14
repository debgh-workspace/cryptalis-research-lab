# Bounded native owned-resource accounting

2026-10-14. Bounded PASS. Full DESIGN, leak/security qualification, timing and product/backend adoption remain HOLD. No timing was performed.

## Evidence

Both Python optimization modes execute the same 170 predeclared observations and produce identical complete records. The set consists of the unchanged 149 prior fault-oracle cases (including every 31 equality / 17 storage applicable selector), three valid/authenticated-wrong-term/recovery calls, and 18 direct ABI valid/refusal/recovery calls for arity, out-of-range selector and empty frame in both representations. There are 110 successes and 60 refusals per mode. Wrapper cases preserve exact safe error metadata, ordered resolution traces, one native entry, exact returned text and type; direct cases compare exact bytes or declared exception type. This is a finite ABI subset, not full direct-ABI admission.

Every observation ends with zero tracked helper-owned references and zero scratch bytes. Persistent outstanding counters survive between calls, including refusal/recovery transitions. Per-call acquisition/release/transfer counts and peak counts also match independently predeclared acquisition-site expectations. Eight EVP classes have peak outstanding count one, including sequential payload/search derivation with two acquisitions per successful equality call.

Per mode, acquisition / release-call counts are:

- EVP_MD: 246 / 246
- EVP_MD_CTX: 243 / 243
- EVP_KDF: 231 / 231
- EVP_KDF_CTX: 228 / 228
- EVP_CIPHER: 146 / 146
- EVP_CIPHER_CTX: 144 / 144
- EVP_MAC: 76 / 76
- EVP_MAC_CTX: 75 / 75
- Scratch buffers: 136 / 136
- Reserved Python bytes references: 138 acquisitions, 28 decref cleanup calls, 110 successful ownership transfers

Scratch peak requested capacity is plaintext length plus the pinned EVP_MAX_BLOCK_LENGTH value 32. Owned Python reference acquisition does not imply a fresh underlying object allocation, and transfer does not mean a free.

Four negative controls (release and transfer corruption, each in O0/O1) verify a real original observation, alter one downstream accounting field and fail with the exact accounting comparator error. These are downstream observation mutations, not native-code mutants or actual deliberately omitted frees. They establish comparator sensitivity, not complete instrumentation independence.

## Instrumentation boundary

Only the copied diagnostic C helper is changed. Successful owned acquisitions are counted; null returns are not. Matching EVP cleanup calls and scratch clear-free calls decrement the corresponding count. Result cleanup decref and successful return ownership transfer are separate. An added snapshot method returns counts to the harness. It performs its own Python allocations outside the measured helper-owned boundary. Stack arrays, borrowed immutable Python inputs, Python's internals, OpenSSL/provider internals and allocator caches are excluded.

Only per-call acquisition/release/transfer totals and peaks reset at entry; outstanding references and scratch byte counters persist. The helper remains GIL-held, and this harness is sequential. Process-global diagnostic state is not qualified for concurrent, reentrant, free-threaded or subinterpreter use.

The diagnostic selectors short-circuit at the existing finite helper stages. They do not recreate actual allocation exhaustion, EVP/provider internal partial failure, library vulnerabilities or arbitrary failure branches. A balanced counter proves the observed matching owned-reference cleanup/transfer paths reached their accounting calls; it does not prove internal allocator deallocation, leak freedom or memory erasure.

## Provenance and review

The root approved the finite scope before compilation. Independent static review reported no blocker against the frozen source/harness/manifest before compilation/execution, with 465 checks; see ../candidate-notes-native-resource-balance-review-20261014/REPORT.md.

SOURCE_PINS.json records source, harness, manifest and original inventories before compilation. PINS.json freezes 692 inputs, the new diagnostic binary, build receipt and linked dependencies before candidate imports. All original candidate, previous fault and exact-admission artifacts are preserved and currently match their pins. Builds use the existing GCC and system OpenSSL; no installs occur. Runs verify the Python 3.12.14 executable/ABI, cryptography 50.0.2 with bundled OpenSSL 4.0.3, and native OpenSSL 3.5.7 and module origins. The two crypto backends remain distinct.

The frozen launch driver uses fresh processes, fixed optimization modes and 180-second timeouts. No compile, unexpected run, or timeout failure occurred. The four intentionally failing negative processes are retained. Bytecode writing to original directories is disabled.

The pre-run-pinned stdlib verify_data.py checks all current pins, original case preservation, the acquisition-site count model, exact observations, O0/O1 parity, single-field negative mutations and launch hashes. VERIFICATION.json reports PASS. Current hashes and coherent receipts are not signed execution chronology, proof against concurrent tampering or complete supply-chain attestation.

## Remaining holds

This closes the selected measured helper-owned reference-accounting gap for these declared paths. It does not close real allocator/internal leak qualification, zeroization, complete error-queue or cipher-property branches, arbitrary provider failures, full Python allocation equivalence, all ABI/fork coverage, cancellation, concurrency, provider custody/identity, packaging/platform qualification, full security review or full DESIGN admission. No new sanitizer/leak-detector evidence is supplied. Existing operational-versus-authentication category ambiguity and omitted pyca encrypt/copy paths remain. No performance, product/backend adoption, database, Git or dependency change follows.
