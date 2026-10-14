# Backend identity and benign queue observations

2026-10-14. Bounded diagnostic result, pending independent data audit at authoring. No timing or product admission.

## Result

The separate diagnostic build succeeded with no compiler diagnostics. The 36 predeclared cases passed in each of Python optimization modes 0 and 1, using the same C -O2 binary. Both processes exited 0 with empty stderr. Each mode rejected both downstream comparator controls (queue entry removal and provider-name corruption). There were no failed launches or retries.

All six actual top-level fetch slots were observed on successful equality calls: payload SHA2-256, payload HKDF, AES-256-GCM-SIV, search SHA2-256, search HKDF, HMAC. Every recorded fetched method reports provider name `default`. All source fetch/property requests remain `provider=default`, including nested SHA256 properties, but these observations do not independently identify the internally fetched nested digests.

Fetched AES-256-GCM-SIV properties: key length 32 bytes, IV length 12 bytes, block size 1 byte, mode 65541 (0x10005), flags 3211285 (0x310015). These are method-level getter results, not a complete property-query string or provider custody proof. Observed names are captured in 64-byte buffers; arbitrary long provider names are outside this fixture scope.

Runtime version: OpenSSL 3.5.7 9 Jun 2026. Pinned linked libcrypto SHA256: 8bb5f3fdffe280d4453eb79a4663c2c47af70b7c247fe2e94e2da703cee1fd3d. Diagnostic binary SHA256: 905ded3b0af88e149b9896255a5d0edf3f52a0763b4336b39ac28c52dc80b2b9. Header/compiler/link dependency pins and exact commands are in PINS.json and build/build.json; loader provenance is not hermetic runtime mapping attestation.

Per mode there are six successful exact encoded-byte observations and thirty exact private RuntimeError refusals. Each of twelve action/representation combinations is exercised with 0, 1 and 2 unmarked public sentinel entries. Before/after ordered error code, source file, line, function, public text data and data flags match exactly, including empty queues and absence of additional entries. Sentinels are ERR_LIB_USER reasons 100 and 101, not actual provider faults. Existing injected selectors short-circuit own call sites; they do not simulate internal provider failures. Bad-tag and wrong-search-root cases use only frozen public CF1 inputs.

## Meaning and limits

This records actual fetched top-level identity and cipher properties and supplies finite ordinary-unmarked-entry evidence for the copied helper. It does not prove arbitrary queue capacity, exhaustion behavior, other-thread state, preexisting mark preservation, ERR_set_mark-failure branches, property-rejection branches, memory/leak freedom or every provider failure. Getter instrumentation is additional work inside the diagnostic call. No unchanged normal-binary run is part of this slice. Public Python wrapper mapping is not requalified by direct private ABI observations.

Classifier policy remains open for coordinator/owner selection; private `data-processing` remains an observable stage label, not an authentication-versus-operational cause diagnosis. Full DESIGN, timing, product adoption and security/custody qualification remain held.

Only the new observation directory was written. Original C/wrapper/product sources and binaries were preserved and pinned. No provider load/configuration/security-setting change, install/dependency update, credentials, service, PostgreSQL, Git or benchmark occurred. Supported implicit default fetch behavior was used. No preparation rerun after freeze.

## Evidence

- SCOPE.md and cases.json: frozen 36-case scope and expectations
- native_cf1.c / prepare.py: additive copied-source instrumentation and preparation recipe (do not rerun)
- build/build.json and launch-build.json: compilation and linkage receipts
- results-O0.json / results-O1.json: complete observations and rejected controls
- launch-O0.json / launch-O1.json: bounded process outcomes
- ../candidate-notes-native-backend-observation-review-20261014/REVIEW.md: pre-execution static review
- ERRATUM.md: preexisting-mark historical-claim correction
