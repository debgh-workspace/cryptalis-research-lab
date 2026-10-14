# Explicit native fault oracles

2026-10-14. Bounded PASS; full DESIGN correctness, timing, product/backend and provider admission remain HOLD.

## Result

149 uniquely predeclared cases pass with Python optimization disabled and enabled. All 31 diagnostic sites run in equality mode and the 17 applicable payload/cipher sites run in storage mode. Each site has a valid/fault/recovery sequence on the same PreparedKeys instance (144 observations). Five additional cases check bad tag alone in each representation, result-reservation refusal before bad tag in each representation, and bad tag before equality search derivation. There are 96 exact returned-text successes and 53 full safe-diagnostic refusals per positive run. Both modes reject one actual-record stage corruption and one actual-record resolution-trace corruption. No timing was taken.

## Repair to the original harness

The original fault adapter replaced _native_encoded and copied its exception mapping. This harness leaves that function and the full read wrapper unchanged. For each call it replaces only the separately named research wrapper's native_cf1 module reference with a call router. The router calls the original diagnostic binary's open_fault for a selected site or open_encoded for a normal call. It has no catch or mapping logic. Thus actual RuntimeError categories traverse the unchanged mapper, decode boundary and final checks. The original module reference is restored in finally; no product module import/function is replaced.

Expected categories are frozen from the source-policy study: pinned pyca process_data failures become InvalidTag, and canonical S20 translates that to AuthenticationFailed. Setup/AAD and implemented derive/MAC faults are assigned the bounded backend policy. Diagnostic field literals come from canonical S20 keys.py, not native_read or its output. cases.json is generated without any crypto/candidate imports. fault-sites.json supplies only diagnostic selector names, not expected categories. The source snapshots and mapping report are pinned.

Every failure compares exact class name, code, stage, retryable, effects, remedy, nonempty string operation-ID presence, suppressed explicit cause, complete ordered resolution arguments and native-call count. The exception's args also must equal its canonical safe message template with that invocation's own operation ID. Operation IDs are intentionally not compared between invocations. Internal __context__ and arbitrary exception attributes are not certified absent; the RuntimeError is suppressed through from None. No returned bytes/string is accepted on a fault.

Successes compare exact str type and 'abcdefg', pre/post resolution order and one native entry. The manifest pins all expected observations before execution. Receipts also record exact selector-entry traces, independently checked against the manifest by verify_data.py. These are Python entry observations, not native resource/event counters. Same-group PreparedKeys objects are cached and reused across each valid/fault/recovery sequence, while traces are cleared per invocation.

The negative controls first verify a real observed fault against the frozen full record, then change only stage or trace and use the same exact comparator. These are actual-observation downstream mutations, not native return-channel/product mutants. Their purpose is to demonstrate rejection of discrepancies the old class-only checks ignored. Each negative launch completes one valid precursor before the intended refusal; those successful precursors are not advertised as a failed whole positive suite.

## Provenance

freeze.py verified the existing diagnostic build pins before freezing; every run verifies all 633 retained pins before imports. Pins include all existing original-candidate files, original binary/dependencies and stage-policy source snapshots, plus freeze.py, run.py and cases.json. The later launch_all.py driver and verify_data.py are covered by final ARTIFACTS.json, not the pre-run PINS.json; run.py is the pinned execution/verification boundary. No new native build, source edit, dependency install, PostgreSQL, Git or product change occurred. PYTHONDONTWRITEBYTECODE=1 prevented new bytecode in original directories.

Pinned diagnostic binary SHA-256: feaa6db110763c6089bc3dd8bc72f59077cb61d748d785c16cbfc23267dfa0ab. Runtime checked Python 3.12.14 and CPython ABI, native source/module origins, OpenSSL 3.5.7, and cryptography 50.0.2 with bundled OpenSSL 4.0.3. Current hashes and consistent receipts are provenance evidence, not signed historical execution attestation or provider identity attestation.

verify_data.py uses only stdlib to verify all pins, manifest IDs, complete record equality, O0/O1 parity, exact entry selector traces, launch hashes, intended negative failure signatures and single-field mutation, and AST assertion absence. VERIFICATION.json records PASS. Original artifacts are untouched and remain currently matching.

## Limits that remain

The finite injected selectors short-circuit explicit native stages; they do not reproduce actual EVP internal allocator/provider failures, process aborts, partial failures or every native branch. Native data/final failures deliberately retain pyca's observable authentication category, including its operational-cause ambiguity. This does not establish a causal EVP failure discriminator.

The helper omits pyca's unused encryption base and copy/reinitialization fallback, and has a different allocation schedule. Result reservation preceding authentication is tested only at the specified research boundary; full pyca allocation/copy equivalence is not claimed. Payload digest failure normalization is a bounded native policy; the source study explicitly notes S20 salt hashing lies outside its HKDF catch. These injected native-only calls are not proof of matching every Python exception under real allocation exhaustion.

Recovery demonstrates subsequent correct output, not resource balance, leak freedom, zeroization, error-queue preservation or concurrency/cancellation safety. Full original supplementary metadata repair, comprehensive failure-branch completeness, measured resource accounting and other admission gaps are outside this slice. Frozen sealing/query parity and complete prior exact-text coverage are not added here. No full DESIGN PASS, performance claim or product/backend adoption follows.

## Key hashes

- cases.json: 9834ecae4a1084e70dcae6cba1eb4836d244737c4a6eab5f1a0cb5852e425a5a
- PINS.json: b5dd84eb734d945c1c9216b3177e8eae2889b74ee239ad6e7d367c6ae8c3a10f
- run.py: 6745ee6375efea9f16a4e7e5ddbc16a059c266b6688e92a024d69a20e7f67448
- LAUNCHES.json: d6a062ecb0782fb25c2b53497dc8aabc15162e22d3a16c72915eec47300d0558
