# Native CF1 complete-read public-fixture prototype

2026-10-14. IMPLEMENTED and bounded correctness VERIFIED as described below. Full DESIGN correctness admission, timing, and product admission remain HOLD. No performance measurement was run.

## Artifacts and implementation

`native_cf1.c` implements stateless payload SHA256/full HKDF, exact AAD, AES-256-GCM-SIV decrypt, then search full HKDF/HMAC-SHA256/full 32-byte comparison. Fresh contexts are fetched and freed per call. The GIL stays held. Native scratch is cleansed, with no whole-process erasure claim. `native_read.py:open_text_native` is separately named and keeps unchanged S20 context/frame ordering, NULL behavior, exact admitted-generation material resolutions, strict UTF-8/NUL decoding, and final payload/search resolutions. S20 source was imported read-only; no product monkeypatch, source edit, cached key/result, key-provider service call, database, Git operation, install, or new dependency was used.

The native stage classifier intentionally maps setup/derive/AAD/result-allocation/MAC errors to CryptoBackendUnavailable and data/update/final returned errors to AuthenticationFailed. This preserves the selected observable policy, not operational-cause discrimination. A provider operational failure at data/final may therefore appear as AuthenticationFailed. No provider error strings are parsed. Omitted pyca unused-encrypt and copy/fallback calls, allocation ordering differences, and salt-digest normalization preclude full fault equivalence.

`static-review/REVIEW.md` records independent source-only review before compilation: no certain source-level blocker for the authorized bounded correctness build/run. The reviewer noted unnamed diagnostic selectors (9/19/20/29) are accepted as no-ops; tests use exactly the 31 named manifest sites. Error-queue mark handling does not preserve preexisting mark metadata and depends on the documented queue-capacity assumption. This is not complete security or memory-safety qualification.

## Recorded checks

- Normal native build: 1,182 explicit checks PASS with Python optimization flags 0 and 1; ordered IDs are identical.
- Diagnostic build: 1,246 explicit checks PASS with optimization flags 0 and 1; ordered IDs are identical. The additional 64 checks are all 31 named fault-site refusals and recovery calls, plus two allocation/tag/search precedence cases.
- ASan + UBSan diagnostic build: the same 1,246 checks PASS, empty stderr, halt-on-error enabled. Leak detection was disabled; no leak or allocator-balance qualification follows. The system OpenSSL/Python binaries themselves were not rebuilt with sanitizers.
- Six expected-failure controls: comparator wrong-value check, removed final resolutions, and removed term comparison; each tested at flags 0 and 1. Every control failed with its exact expected mismatch and zero passed checks. The comparator control runs before candidate work; it is not an end-to-end wrong-decoded-output perturbation. The skipped-term source switch is only in a disposable mutant binary; the skipped-final function is separately compiled from research-wrapper text. Neither changes product imports.

The frozen baseline case manifest contains 1,035 cases and 89 frame fixtures. Its cases comprise 8 independent CF1 vectors; 606 one-bit-per-byte frame mutations; 92 frame-shape/generation cases; 64 representation/record/tenant/text-grid cases; 8 NULL cases; 48 input-type and 28 record-type refusals; 48 context cases; 40 key/admission cases; 24 resolution-expiry and 8 NULL-expiry cases; 40 named precedence cases; 6 int64 endpoint cases; 2 nil UUID record+tenant cases; 2 exact 16-MiB cases; 2 over-bound cases; 6 invalid UTF-8/NUL content cases; 1 valid-AEAD wrong-term case; and 2 shape-valid opposite-representation cases. Expected outcomes were computed using unchanged S20 before native candidate import and frozen in `cases.json`. They include exact safe exception metadata and exact resolution traces; operation IDs must be present rather than identical.

The normal 147 supplementary checks cover two thread callers, two event-loop callers, an interleave of storage/equality in the same tenant/record, valid/invalid/valid reads, actual fork-inherited PreparedKeys rejection and fresh-child public-material success, after-native expiry for storage/equality, private ABI type/length/arity/tuple bounds, and 32 unchanged equality-term comparisons. The interleave is NOT distinct-tenant/record A/B/A evidence. Synthetic PreparedKeys fixtures test consumption only, not provider admission/custody. Expiry is controlled fixture replacement, not a real provider lease race. Async tests do not qualify database cancellation.

## Pinning and environment

The executable launch path is `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python`, kept without resolving its symlink into another environment. Python is 3.12.14, cryptography is 50.0.2, and the oracle backend is OpenSSL 4.0.3. Native builds use GCC 14.2.0 and system OpenSSL 3.5.7 with explicit `provider=default` fetch properties. These are different backends. No pure backend/context attribution or backend-product approval is claimed.

Each launch verifies 585 source, fixture, interpreter, installed cryptography, compiler/header, binary and dynamic-dependency hashes before native import (590 for sanitizer dependencies), enforces package/backend versions and import origins, records optimization/ABI/executable values, rejects existing output files, and uses explicit checks rather than `assert`. Source-derived expected supplementary IDs are enforced in the frozen harness, but are computed after execution and were not enumerated in the pre-run JSON case manifest. This remains a full-DESIGN protocol gap. Hashes are provenance consistency checks, not signed execution attestation, reproducible-build proof, or an atomic defense against concurrent replacement.

Two precompile provenance attempts failed because a guessed GCC `cc1` path was absent. Both failed directories preserve the old driver and failure record. `gcc -print-prog-name=cc1` then identified the existing executable; only the driver path changed, and new build directories preserve successful attempts. Native source and wrapper did not change after static review. A later `cat | head` preview printed a broken-pipe diagnostic; it was not a failed build or validation.

## Full DESIGN gaps and disposition

Do not start timing based on these receipts. At minimum, the selected implementation lacks the DESIGN's six standalone native primitive-vector oracle entries, diagnostic intermediate salt/key/AAD/header inspection, separately manifested supplementary IDs, distinct-tenant/record A/B/A isolation, and verified allocator/leak balance. The full independent inventory is in `evidence-audit/AUDIT.md`. Further gaps include exact text/UTF-8 expectations (the current observer compares length/SHA-256), frozen-vector sealing/query/intermediate parity, table-derived descriptors and policy-domain mismatches, cross-scope concurrent callers, same PreparedKeys lifecycle reuse, native invocation counting, distinct decode-boundary expiry, complete supplemental error metadata/traces, additional error/property branches, and end-to-end wrong-output perturbation. The diagnostic fault adapter duplicates the wrapper mapping and checks only the resulting class; it does not independently verify injected errors through the production-equivalent mapper. The existing broad grid/byte-mutation evidence does not replace a missing named requirement. Product provider, packaging/ABI/platform qualification, independent human review, PostgreSQL/SQLAlchemy regression, and full end-to-end performance remain outside this task.

## Primary fingerprints

- `native_cf1.c`: `2926d61e43b3dc53a5fff56ab5367982c89b92b146ef9cbc47fbd2b71e5a9469`
- `native_read.py`: `4d3151148b435d7f54235b3eda864ea85e6def5cd6a4f9b5025d09bdd425a703`
- `cases.json`: `e3c8faa46bc4e5eb0742ea3a3793c1c390519f2f057227e28176d7162c76881c`
- Normal native binary: `cea85e738f66122ef26751bf691f709fcc64402ae8159b27c3397d313e79e936`
- Diagnostic native binary: `feaa6db110763c6089bc3dd8bc72f59077cb61d748d785c16cbfc23267dfa0ab`

Receipts: `build-03-normal/build.json`, `build-04-diagnostic/build.json`, `build-05-skip-term/build.json`, `build-06-sanitizer/build.json`, and `evidence/*-01.json`. `evidence/final-integrity-01.json` rechecks all run pins and ordered-ID equality after validation.
