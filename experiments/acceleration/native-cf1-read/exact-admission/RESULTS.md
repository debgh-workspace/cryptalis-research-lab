# Frozen exact-output native read admission

2026-10-14. Bounded PASS for the manifest below. Full DESIGN correctness admission, timing and product/backend adoption remain HOLD. No timing was performed.

## New result and its provenance

Both Python optimization modes execute the same 1,098 unique predeclared entries and compare identical complete observation arrays. The finite scope contains:

- The original 1,035 IDs, with original invocation specifications and frame fixtures unchanged. All successful wrapper returns now compare exact full text and exact type, including both complete 16-MiB texts, rather than only length/SHA-256. Existing safe failure fields and resolution traces are retained, with canonical exception-args checks, absent explicit cause and exact native-entry counts added.
- 43 explicitly manifested correction observations: table-derived relocations; policy-domain mismatches; true A/B/A scopes and NULL; same-object valid/expired/fresh-key lifecycle; decode-to-final-check expiry; post-native simulated stored-PID mismatch.
- Eight exact frozen-vector sealing comparisons and four equality-query comparisons, including exact byte output/type and resolution order.
- Four thread-caller and four event-loop-caller observations: two distinct tenant/record scopes in each representation for each caller kind.

The outputs comprise 108 exact string returns, 10 NULL returns, 12 baseline bytes returns and 968 typed refusals per mode. The 12 bytes returns belong to unchanged baseline seal/query evidence, not a candidate sealing implementation. These heterogeneous entries are not a full DESIGN coverage count.

Exact expected original text comes from independent frozen vectors or the original public input recipes (grid texts, endpoint/nil literals, maximum ASCII). The stdlib freeze explicitly confirms those full texts reproduce the original length/hash expectations, but never chooses expectations from native output. Original failure fields/traces are retained from the earlier unchanged S20 oracle; they were not newly recomputed by executing every baseline read. All additional correction expectations/fixtures retain their existing audited provenance. This is a newly predeclared exact-output oracle; it does not retroactively predeclare the old supplementary IDs or improve their historical chronology.

## Frozen sealing and query parity

The sealing check executes the unchanged S20 source in a separately loaded module namespace. Its own os reference points to a fixed-public-nonce stub, leaving canonical cf1, the shared os module and product source unpatched. It constructs descriptors belonging to that isolated module. Each seal consumes exactly one public fixture nonce and compares the entire generated frame to the independently composed frozen frame; query checks compare every term byte to the frozen term. All eight labels and four equality labels are covered.

This is synthetic reproducibility with public fixtures, never a production nonce-reuse prescription. Frozen vector provenance remains independent RFC8452 composition using OpenSSL AES-ECB and stdlib hashing, not a fully independent machine/backend implementation.

## Complete observation and negative controls

Wrapper observations compare exact return type/text or exact exception class, code, stage, retryable, effects, remedy and nonempty string operation-ID presence. Exception args must match the canonical safe template with that invocation's own operation ID; explicit __cause__ must be absent. Literal operation IDs differ intentionally. Internal __context__, __suppress_context__, arbitrary exception attributes and all traceback properties are not certified by this schema.

Every case compares complete ordered resolution arguments and a Python-observed native open_encoded entry count. A temporary call router on only the separately named research wrapper's native module reference supplies counting and bounded lifecycle hooks; the mapper and wrapper source remain unchanged, and the reference is restored in finally. Counts are entry instrumentation, not independent C-internal execution/resource counters.

Four controls in each optimization mode first observe the real candidate and verify the entire unmodified record. They then alter exactly one observed field: returned text, exact type label, failure stage, or resolution trace. All eight fail with RuntimeError("Exact admission mismatch"), expected process exit 1, and zero positive observations. Receipts retain both original and mutated records. These are downstream actual-observation controls, not changes within the native or product return channel. The original skip-term and skip-final mutant evidence is preserved separately rather than rerun here.

## Isolation, lifecycle and limits

Thread callers synchronize at a barrier and use separate public PreparedKeys for different tenant and record IDs. Event-loop callers are separate coroutines but invoke the synchronous GIL-held helper serially after yielding; their calls do not overlap, and async cancellation is not tested. No throughput or free-threading claim follows.

The 43 correction entries preserve reused PreparedKeys sequences and controlled expiry/PID hooks. These are synthetic consumption-boundary tests, not natural expiry, provider refresh, provider custody or actual post-use OS PID changes. The old actual fork and direct ABI evidence remains separately scoped; this new manifest does not repair full safe-field/traces for old fork supplements or predeclare/re-execute all 100 old ABI checks.

## Execution and review

The coordinator approved the finite scope before preparation and the independent source-only review found no blocker against the frozen files before candidate execution. See ../candidate-notes-native-read-admission-review-20261014/REPORT.md. No preparation or positive-run failure required correction. All eight negative exits are expected retained evidence.

The stdlib-only prepare/freeze steps verified old inventories and current dependencies, created cases.json exclusively, and pinned 650 inputs before any candidate import. Every execution rechecks these pins, interpreter/version/ABI, native/source/package origins and backend versions. Python is 3.12.14, cryptography 50.0.2 / bundled OpenSSL 4.0.3, and unchanged normal native binary uses system OpenSSL 3.5.7. The launcher runs negatives before positives in each mode and enforces 180-second subprocess timeouts with kill/reap cleanup; no timeout occurred. No bytecode was written to original directories.

The self-check verify_data.py uses only stdlib and confirms all current pins, original IDs/invocations/fixtures, exact observations, O0/O1 equality, exact single-field negative changes and launch signatures. VERIFICATION.json records PASS. This is data/static correspondence and a self-check, not independent historical execution attestation or comprehensive security review. verify_data.py was written after PINS freeze and is covered by final ARTIFACTS rather than pre-run pins; launch_all.py and all execution source are in PINS.

## Remaining mandatory holds

- No measured native allocation/context balance, leak qualification, complete error-queue/cipher-property failure-branch coverage, or full memory/security review.
- Observable data/final errors retain operational-versus-authentication ambiguity. Digest normalization, omitted pyca unused encrypt/copy paths, allocation ordering and differing crypto backends preclude complete fault equivalence.
- No separately queried actual provider identity or provider-isolation attestation.
- No complete repair/re-execution of the old supplementary ABI/fork schema, no actual post-decode fork or overlapping event-loop/cancellation qualification.
- Existing primitive/intermediate and full injected-fault-mapper extensions remain separately audited evidence, not rows silently added to this count.
- No provider custody, packaging/platform/ABI/supply-chain qualification, PostgreSQL/SQLAlchemy regressions, performance gate or product/backend approval.

The new evidence closes the selected original exact-text and full-predeclared-new-wrapper-oracle gaps, frozen sealing/query parity and bounded distinct-scope caller checks. It does not justify full DESIGN PASS or timing.

## Fingerprints

- cases.json: a4b192bdaaa98124960efa0bedfb7c1a6417b318143555157068b03f23bb946e
- PINS.json: 59a7e61da60f7df3eae1867bee5688040ebf9f9c8ee33df9a4802bd32a200e31
- Unchanged normal native binary: cea85e738f66122ef26751bf691f709fcc64402ae8159b27c3397d313e79e936
- Unchanged native_read.py: 4d3151148b435d7f54235b3eda864ea85e6def5cd6a4f9b5025d09bdd425a703

Detailed receipts are in evidence/, launch inventory in LAUNCHES.json, and final file hashes in ARTIFACTS.json. No product source, normal native source/binary, original evidence, database, Git state, dependencies, providers or credentials were changed.
