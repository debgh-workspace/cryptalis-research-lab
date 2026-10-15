# Search cost follow-on: direct JSON projection

Date: 2026-10-15. Status: source/data research only; implementation and execution await root selection.

## Recommendation and concrete question

First select a fresh SELECT-only PostgreSQL/psycopg compatibility experiment. It must establish the result-OID and custom-loader boundary before selecting a product derivative. The eventual isolated, one-token product hypothesis is to change `pg_catalog.jsonb_build_array` to `pg_catalog.json_build_array` at selected Integrated221 `src/cryptalis/sqlalchemy.py:221`, with its arguments and receiving `_ReadText` unchanged. No public behavior equivalence is established by the small edit size.

Question: does avoiding transient PostgreSQL JSONB construction and conversion back to JSON text reduce the fully consumed protected equality/IN hot-text cost, while preserving exactly the existing decoded three-slot payload/record/tenant contract?

This is a small server-side representation experiment, not a proposed search-privacy change or a claim that the absolute budgets will pass. Expected gain is UNKNOWN. Existing evidence suggests the bulk of returned-row CPU remains in CF1; this experiment must be allowed to fail once without expansion or favorable reruns.

Selected source: `candidate-cluster-retained-integrated-v2-20261015`, 221-file manifest `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`. Selected `sqlalchemy.py` SHA256 is `28cf5c4991aae1cb4f3baf6a5630b30d675cb2308e842ce09fd6a04ddaaf5a88`. Do not change CURRENT_CANDIDATE, the preview artifacts, or any old observation.

## What the retained evidence actually says

The objectives remain added p95 at most 3 ms for point/equality, 8 ms for IN-20, and isolated protected-column-plus-equality-index storage at most 2 times the matched plaintext column and its equality index. Do not replace these with whole-relation space or query-only latency.

There is no uniform historical FAIL across all these targets:

- The 2026-10-08 bounded warm synchronous million-row receipt retained at `final-export/docs/_reset/slice4-performance.json` records an isolated storage ratio of 1.4928, with 155,785,600 native bytes and 232,556,224 protected bytes. It used unique 53-byte synthetic identifiers, one tenant, and native name B-tree versus protected tenant/full-term B-tree. The documented point/equality/IN added-p95 values were 2.336/2.561/3.005 ms. These are earlier bounded passes, not current Integrated221 or deployment qualification.
- C7 is a different, storage-only full-scope scan. All four size/version overall cost gates failed. At 1,000 rows, equality added-p95 was 31.954440/30.605295 ms on SA21/SA20; at 10,000, 314.329899/367.896602 ms. The SA20 1,000-row IN nominal pass of 2.425702 ms is preserved; its native p95 was 41.954158 ms. Full-scope scanning must fetch and authenticate every non-NULL row even for misses. Its linear work cannot be repaired by a projection micro-optimization, and no timing/completeness privacy claim follows.
- C9 actually reduced query search derivations from 20 to 1 and used ANY, yet both primary IDs-only relative improvement gates failed on both cells. Returned text still paid per-row authentication, derivation, and materialization. Hot-text added-p95 remained IN 14.971709/16.416346 ms and equality 7.758017/8.670194 ms. These observations do not prove one causal explanation for the misses. The native bind/default cache-order gap remains separate and open.
- C10 specialized two fixed `_term` framing calls. Its hot-text median reductions were 2.055/2.231 percent on SA21 and 2.541/1.565 percent on SA20 for IN/equality, below the frozen 5 percent requirement. Added-p95 was IN 14.035163/14.005799 ms and equality 8.824318/9.201093 ms. Both absolute and relative gates failed in both cells. Point controls were only descriptive under that protocol, at 2.013211/1.850602 ms added-p95; they cannot rescue the primary failures.

C8's retained finite summary attributes approximately 82.7–83.4 percent of instrumented fetch CPU to inclusive `open_text`. For 143 equality rows and 286 IN rows, fetch elapsed medians were about 4.23–4.63 ms and 8.32–8.55 ms respectively. Profiling is not latency, nested costs overlap, and those observations are not a current full-adapter benchmark. This limits expectations for a server-only change; it does not show the server cost is zero.

The selected `_ReadText` and `_Payload` classes are AST-identical to S20. Selected `cf1.py` and `_sqlalchemy_search.py` are byte-identical to the inspected predecessor. `keys.py` differs in diagnostic reduction behavior, while `tuple_bytes` and `_resolve` remain AST-identical. These facts permit source-path attribution, not transplantation of old performance results onto Integrated221.

The 2× storage objective remains a current qualification gap rather than a newly measured failure: C9/C10 do not supply current isolated storage measurements. CF1 equality adds 74 frame bytes before database tuple/index accounting, and the full-width term is indexed; length/distribution/index shape matter. This projection change leaves physical stored bytes and indexes unchanged and cannot close the storage objective by itself.

## Source mechanism and exact edit boundary

All following paths are relative to selected source:

- `src/cryptalis/sqlalchemy.py:140–180`: `_ReadText` has `impl = JSON`, checks a list of exactly three elements, distinguishes missing outer-join rows, parses record/tenant, applies expected point/tenant checks, bounds and decodes the hex frame, then calls `open_text`.
- `:183–223`: `_Payload` keeps raw bytea inaccessible as public output. `column_expression` obtains record and tenant from mapped row columns, uses the stable table UUID for single-tenant scope, constructs the array, and type-coerces it to `_ReadText`.
- The only candidate product change is the function name at `:221`. Keep `encode(..., "hex")`, argument order, `LargeBinary` coercion, operation ownership, `_ReadText` construction, labels/lineage, and uncached protected compilation unchanged.
- `src/cryptalis/crypto/cf1.py:181–222` remains byte-identical: expected context, frame bounds, generation resolution, per-record derivation, AEAD, search-term recomputation/constant-time comparison, strict text decoding, and final key checks remain.
- `src/cryptalis/crypto/keys.py:278–285` retains per-use policy/PID/expiry checks. No new root/derived-key/plaintext/result cache or changed lease exists.

Primary PostgreSQL source provides a concrete mechanism. In tag REL_16_15, `json_build_array_worker` writes a JSON string directly into a StringInfo and returns text; the public array builder supplies `absent_on_null=false`. `json_out` returns that stored text. The JSONB builder instead builds a Jsonb value, and `jsonb_out` serializes it through JsonbToCString. This is a real implementation difference, not measured saved time. Both builders preserve the supplied NULL elements. See [json.c](https://raw.githubusercontent.com/postgres/postgres/REL_16_15/src/backend/utils/adt/json.c) and [jsonb.c](https://raw.githubusercontent.com/postgres/postgres/REL_16_15/src/backend/utils/adt/jsonb.c), plus [PostgreSQL 16 JSON function contracts](https://www.postgresql.org/docs/16/functions-json.html).

No JSONB operator, index, storage type, order, or comparison is needed on this ephemeral array. Its admitted elements are hex text, native UUID or int64, and UUID/text tenant identity. Arbitrary JSON objects, floating-point values, duplicate object keys, and JSON-path semantics are not admitted new operands.

The main new observable is the result PostgreSQL OID: JSONB 3802 becomes JSON 114. Default driver equivalence is plausible and independently source-reviewed, but per-OID custom psycopg loaders can differ. This is a mandatory admission gate, not an assumed equivalence. A new compatibility exclusion cannot be invented merely to permit this optimization. Engine-level shared JSON deserializer behavior, sync/async routes, and exact integer preservation must be checked in both dependency cells. If the supported contract includes OID-specific customization whose behavior differs, this candidate needs a separate design decision or must be rejected.

## Why this is a new, bounded hypothesis

C7 changed the search workflow to full scan. C9 changed query material derivation and SQL operand representation. C10 changed Python CF1 tuple assembly. This candidate changes only the server's construction of a short-lived result envelope. It leaves search selection, query terms, returned-row crypto, Python parsing, and storage unchanged.

The previously researched fused native CF1 extension is a different, larger mechanism with its own outstanding admission/timing decisions. Do not repeat or subsume it here. Likewise, do not combine this proposal with a binary envelope, base64, key reuse, new backend, ANY route, or compilation caching.

A binary envelope was considered and deferred. It would require a new parser, separate record/tenant/payload presence flags and NULL tests, and new serialization bounds. It would not automatically halve network bytes: psycopg defaults results to text, and requesting binary results changes the format for every returned column. A bytea result can therefore still travel as hex. This one-token JSON change avoids that larger compatibility surface. [Psycopg binary result documentation](https://www.psycopg.org/psycopg3/docs/basic/params.html#binary-parameters-and-results).

## Public implementation comparison

CipherStash's current public EQL documentation describes JSONB-backed encrypted domains with functional index terms, including HMAC-256 equality terms. It is evidence for separating database index work from client decryption, not proof that JSONB is the best transient transport wrapper for Cryptalis. Its type, KMS, key lifetime, index and cryptographic contracts differ; none are imported here. [EQL indexes](https://cipherstash.com/docs/reference/eql/indexes).

The actual public `cipherstash/benches` `benches/exact_v3.rs` source inspected through GitHub uses `LIMIT 1`, prepares encrypted operands outside the timed loops, and has separate execute-only and execute-and-decrypt loops. Those numbers cannot qualify Cryptalis's 143/286-row complete-consumption workloads. Preserve a matched native comparator and timed boundaries rather than borrowing headline speed claims. [Inspected benchmark implementation](https://github.com/cipherstash/benches/blob/main/benches/exact_v3.rs).

Public-source provenance limit: PostgreSQL links are pinned to the REL_16_15 release tag. The fetched CipherStash benchmark page used `main`, with a web-cache age of about two months; its immutable commit was not exposed. Direct history/raw fetches returned cache misses. It is an inspected implementation example, not a verified latest-HEAD or immutable-source qualification. Current vendor docs and repo landing pages were checked on 2026-10-15. No external service, API integration, paid resource, downloaded package, or third-party code was executed.

## Independent native comparison and prerequisites

### First slice: read-only constructor and loader characterization

The smallest new run does not import Cryptalis or use a product fixture. Through the existing unchanged role preflights and exclusive laboratory lock, use bound synthetic operands in SELECT/VALUES expressions. Return the typed operands alongside both array constructors. No CREATE/INSERT/UPDATE/DELETE/DDL, fixture grants, new role, extension, provider call or protected-data mutation is needed. Root must still review the exact source, command, environment identity and stopped-boundary closure before selecting this run.

Freeze these controls before execution:

- Four admitted combinations: UUID or bigint record, native UUID or single-tenant text tenant. Opaque synthetic bytea lengths 0, 1, 74 and 1,024 cover empty/nonempty transport; no CF1 key or validity assumption is required to compare builders. Full CF1 bounds remain for the later product gate.
- Native NULL payload, record and tenant positions, including all-null and present-record/null-payload forms. Both builders must retain list length three and positional None values. This read-only gate characterizes transport; it does not independently prove `_ReadText` application behavior.
- UUID zero/nonzero and bigint minimum/maximum, -2^53-1, -1, 0, 1 and 2^53+1. Compare exact Python int types/values against independent typed native outputs.
- Default psycopg loading, connection-local shared `set_json_loads`, SQLAlchemy engine `json_deserializer`, and deliberately different per-OID JSON/JSONB custom loaders. Isolate custom registrations to fresh connections, never global adapters. Observe callbacks and outputs for each OID. A deliberate differential loader should demonstrate the difference; do not relabel that expected characterization as public compatibility PASS.
- Sync/async connections in each existing SA21/SA20 dependency cell. Record actual server OIDs, cursor formats, decoded types and outcomes. An explicitly separate binary-cursor control may compare both standard types; it must not change default application cursor behavior.
- Negative oracle controls must make an actual observed type/value/NULL-slot/OID mismatch fail the independent comparator. Expected answers come from typed native columns and independent data logic, not either JSON builder or a candidate helper.

The output should distinguish default/shared-decoder equality, intentional per-OID custom-loader divergence, exact native integer/UUID/NULL correctness, unsupported routes and unrun cases. A nominal test-process exit is not product equivalence. Do not attach timing thresholds to this characterization or turn its elapsed suite time into a speed claim.

If root also selects a native-cost diagnostic in this first packet, keep it a separately declared SELECT-only phase: one, 143 and 286 synthetic rows; fixed public opaque-byte lengths; original JSONB builder, JSON builder and typed-native-output control; identical actual inputs, complete fetch/close, alternating order and retained individual samples. Freeze sizes/repetitions and clock/CPU accounting before execution. Use generated SELECT inputs rather than tables or grants. The typed multi-column control diagnoses constructor/serialization/driver work and is not the protected application cost denominator. This phase can decide whether a later product experiment is justified; it cannot establish authenticated read gains, index performance, storage qualification or the 3/8 ms application targets.

### Later source candidate, only after root review

Before timing, a new source-isolated correctness packet must bind native, unchanged Integrated221, and the one-token derivative. Do not use the candidate as its own expected-output oracle.

1. A separate native psycopg oracle returns typed payload bytes, UUID/int64 record and UUID/text tenant from a synthetic fixture. Independently form the expected three logical values. Compare both PostgreSQL array builders after actual driver decoding, including exact Python types and lengths. Use nil/non-nil UUIDs, int64 minimum/maximum and values beyond JavaScript's exact-integer range, present NULL payloads, empty text, Unicode, boundary-sized frames, absent outer joins, malformed context and wrong expected tenant/record cases.
2. Both builders must preserve each of the three positions. A present row with SQL NULL payload still reaches `open_text(None, ...)`; a missing outer-join row retains the separate `record is None` branch and its single/multi-tenant checks. Do not coalesce the whole result, drop NULL elements, or convert all fields to text.
3. Compare scalar/entity/aliased/labeled/duplicate projections, relationships, lazy iteration, streaming and pagination with independent native values. Compare ordered sequences directly, never sort to hide an ordering difference. The earlier `tests/profile_sqlalchemy_search.py:247–254` sorts its comparisons and is insufficient by itself for that property. Keep unsupported DISTINCT/ordering refusals before driver execution; JSON's absent comparison operators must not become their accidental replacement. Use unchanged current source tests at `tests/test_sqlalchemy_adapter.py:134,170,213,616,691,742,842,1129`, `tests/test_sqlalchemy_search.py:198,266,488`, `tests/test_sqlalchemy_outer_nulls.py`, and `tests/test_sqlalchemy_ordering_labels.py:70,120`; freeze their actual version-specific inventory rather than promising a guessed count.
4. Assert unchanged primitive/use counts for M non-NULL query operands and R returned non-NULL protected values: terms M+R, search derivations M+R, payload derivations R, opens R, key resolutions 2M+4R, generic CF1 tuples 3M+6R in BOTH protected variants. Preserve corruption, expiry/fork, cancellation, cleanup, wrong-context, NULL, bound/default and no-plaintext-to-driver controls. No check is removed to obtain a gain.
5. Verify actual cursor SQL changes only the admitted array-constructor call, with unchanged predicates/order/index use, row counts and independent answer hashes. Check returned OID and the actual selected JSON loader, including shared engine JSON deserialization. A per-OID custom loader mismatch must stop admission or be resolved under an explicit pre-existing compatibility contract, not concealed by a test-specific override.

The frozen C10 route is a useful design ancestor, not an executable approval for this candidate:

- `candidate-accel-term-framing-20261014/tests/profile_c10_timing.py`, SHA256 `81c1fc50eaa8698e94bab5406f2cf10a9822a6b6fc4de2f559a2eed79f4fcf23`.
- `.../tests/test_c10_postgres_gates.py`, SHA256 `bdf912dc2bbbdc111a914266af856dc0aaa82560b0d7ed64d9274c24e3c24ef7`.
- `.../experiments/C10_TIMING_PROTOCOL.md`, SHA256 `37e8854cf795b612250f7c18a727a175ac888515b69e2515a86e95f02f665c01`.
- Current fixture definition: `tests/single_tenant_public_cascade_fixture.py:6`, requested with 1,000 rows, `unique=False`, `public_table=False`.

A new version must replace S20/208-file and C10-CF1 identity assumptions with the selected 221-file baseline and one-token adapter delta, and use unchanged tuple counts. It needs a new independently reviewed finite input manifest, collection, command, safety prerequisites and root selection. Old C10 approval files or successful execution status do not authorize it. Neither old source/runtime results nor old source hashes count as current derivative evidence.

If correctness clears, preserve the existing five workload shapes: IN20 miss IDs 0 rows, hot IDs 286, hot text 286, equality hot text 143, point text 1. Retain seven alternating variant-order blocks, 10 warmups plus 40 measured samples per block, complete execute/fetch/close timing, all observations, independent native driver oracle, normal GC, resource/clock records, no data selection and no unchanged rerun. The suggested mechanism admission remains the earlier 5 percent median-of-block-medians and six-of-seven favorable blocks in BOTH hot-text primaries, with no more than 5 percent aggregate control regression, separately in both dependency cells. This is a proposed predeclared protocol for root review, not a newly approved product SLO. Keep the absolute 3/8 ms budgets as separate gates.

No timing claim follows if only server SQL microtime improves. A safe diagnostic of the two array constructors on identical typed ciphertext rows may explain a result, but cannot replace fully authenticated end-to-end primary results or a native baseline. Do not introduce an unbounded payload sweep or another benchmark suite without a distinct reviewed question.

## Authority and stopping conditions

Completed here: finite metadata-first source and archived safe-summary reads; standard-library data extraction, AST comparisons and hashes; primary public source research; independent source review. No product import/test, DB access, install, Git action, current environment/cache/corpus inspection, credential access, rawphase-body read, source mutation, or selected-preview change occurred.

Root may next select source-only preparation of the SELECT-only constructor/loader characterization packet. Only root should admit its later serialized laboratory run through the unchanged approval/role/cold-source/corpus/stop boundary. Any product derivative follows separately after the OID/custom-loader gate and source/command review. No provider, new access, new DB, fixture privilege, production, upload, or promotion authority is implied.

Stop on a semantic/loader/context/error/check-count mismatch or a failed frozen cost gate. Preserve the failed evidence. Do not weaken privacy, length/NULL context, key lifecycle, or declared budgets; do not expand this candidate to rescue it.

## Artifacts

`EVIDENCE_EXTRACT.json` contains the selected numeric observations, source-function equality checks and hashes of 23 finite local inputs. Its initial SHA256 is `6330aa188265fccdfc3ab9122fb495b1eef8e66c0f1e223aaa596fc940e83f80`. Historical receipts and failed experiments remain unchanged. Independent source findings and their exact additional primary links are preserved in `independent/REVIEW.md`.
