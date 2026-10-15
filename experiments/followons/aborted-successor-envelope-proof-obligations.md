# Narrow prerequisite: terminal-state envelope and physical journal validator

Status: exact source-derived proof obligations, NOT IMPLEMENTED / NOT RUN. This supplements the sealed REVIEW.md, whose hash is 1cc67af070f5ca7a2a8aa36647f150b62b4da585c2d9ef5875ab6355f5525fc0. The next selected slice should implement and independently test these prerequisites in isolation before enabling v3 execution.

## Decisive simplification

A forward or reverse ABORTED row can only be produced before switch. The active_schema member is added at switch, after the safe-abort boundary. Therefore a terminal-ABORTED history budget must cover the exact pre-switch state family, not every later active representation. Do not apply the proposed terminal-history cap indiscriminately to current ACTIVE/DEPROTECTING rows or all historical APIs.

A successful safe abort changes only phase to the shorter string ABORTED. It does not append observations, refresh schemas, rewrite guard metadata, add verification, or add lineage. This invariant makes an expansion-time reservation possible. Preserve it in v3; do not append an abort receipt or terminal self-digest to the row.

## Exact current state fields and growth

Selected source: candidate-cluster-retained-integrated-v2-20261015.

Forward expansion (migration.py:667-672):

    phase = EXPANDED
    models[table_id] = {
        scope: {count: N, membership: SHA256 hex},
        cursor: null,
        rows: 0,
        chunks: 0,
        schema: exact expanded _facts observation,
        guard: exact expanded _guard_facts observation
    }

v3 adds only its already-approved fixed-size aborted_forward summary at the top level. It is immutable for the operation.

Forward growth (migration.py:690-740, 847-848):

- Each committed nonempty backfill chunk replaces cursor with str(last primary key), increments rows by returned row count, and increments chunks once.
- scope, schema and guard are never rewritten before switch.
- BACKFILLED changes only phase.
- The explicit VERIFIED checkpoint adds verification = {table_id: 64 lowercase hex characters} for every model. Reverification does not append history or individual row results.
- Direct switch may compute the same verification map, but its active_schema additions and PENDING state commit after the safe-abort boundary.
- abort (888-900) preserves every member and replaces only phase with ABORTED.

Reverse expansion (deprotection.py:319-323):

    phase = EXPANDED
    layout_version = 101
    models = the same progress shape above, observed on reverse staging
    source_operation_id = canonical 36-character UUID
    source_plan_digest = lowercase 64-character SHA256

Reverse growth (352-378, 469-470):

- cursor, rows and chunks grow as above; other model members remain fixed.
- Verification compares current values but adds no verification map to the journal.
- VERIFIED changes only phase.
- active_schema is first added by reverse switch at 419; PLAINTEXT_PENDING/ACTIVE cannot be safely aborted.
- reverse abort (484-506) changes its phase to ABORTED and the separate source phase from DEPROTECTING to ACTIVE in the same transaction. It does not add fields to the aborted reverse row.
- If v3 adds a current reverse-history summary to its state, include that exact immutable summary in the initial reservation. No such field exists today and none is required merely to preserve existing reverse source-link semantics.

The fixed schema and guard observations are not assumed small. Their actual bytes must be included. guard contains the captured trigger facts plus all noninternal trigger inventory, including trigger definitions, function source, owner/schema/name strings and proconfig. Existing schema-only 4 MiB reservation is not a complete journal-state bound. Reverse expansion currently has no corresponding whole-state budget at all.

## Conservative expansion-time envelope E

Construct a size-only deep copy of the exact proposed pre-switch state after native expansion observations have been collected, but before the expansion transaction commits or inserts an externally usable row. The copy is never stored as observed state.

In E:

1. Retain exact scope/schema/guard and exact immutable source/lineage members.
2. Replace phase by BACKFILLED, length 10, the longest possible pre-switch phase. ABORTED is length 7; EXPANDED and VERIFIED are length 8.
3. For every model, replace cursor by 36 simple ASCII characters. Admitted UUID cursors have length 36. The selected compiler is not UUID-only: compiler.py:288-292 admits BigInteger/int8 as int64-be/v1, model admission at 374-376 permits it, and migration.py:569 dispatches the cursor decoder by record codec. Its signed primary-key string has at most 20 characters, so the same reservation covers both. The real cursor remains null or the exact admitted codec's value.
4. Replace rows and chunks by 9007199254740991, the longest 16-digit admitted counter, or by the initial scope count N if the narrower verified invariant below is selected.
5. For forward, add the full verification map, with exactly the admitted model keys and one 64-character simple ASCII hex string per model. For reverse, do not invent a verification field.
6. Require canonical depth within the existing nesting bound. Later mutable members contain only scalar values and the one fixed-depth verification map, so they cannot exceed this reservation's nesting.

Admission requires both:

- len(C(E)) <= 16 MiB, where C is the exact canonical encoder used for terminal-state hashing;
- PostgreSQL's native UTF-8 byte length of E cast to jsonb then text <= the chosen 16 MiB transfer limit.

The native length can be observed on the same intended connection using a parameterized read-only scalar expression over E, before expansion commits. Measure octet_length(convert_to(parameter::jsonb::text, 'UTF8')), not character length and not the UTF-8 length of Python's differently spaced JSON. This is an observation of a size-only value, not a persisted invented catalog fact. The runtime proof must establish this exact PostgreSQL 16 serialization behavior; a Python-only test is insufficient.

Why E dominates a legal aborted row: all variable member names and container structure are present; mutable strings consist of unescaped ASCII with lengths no larger than the placeholders; mutable integers have no more digits; an absent verification member is smaller than the reserved full map; all other members are identical. Native jsonb output ordering does not change encoded length. ABORTED is shorter than every legal pre-switch phase. Thus abort cannot create a newly oversized terminal row once this initial envelope is admitted.

If E exceeds either budget, fail and roll back the expansion transaction. The old native representation and predecessor journal survive unchanged. Do not first commit expansion and then discover the failure at abort or successor planning.

Do not make a new canonicalization/size check an abort gate without this earlier admission proof. Historic v0/v1/v2 operations retain their current abort behavior. An already-aborted historical row that is too large for this successor prototype is a read-only successor-scope refusal; it is not permission to alter that row or block the old safe-abort path.

## Necessary state-machine invariants

The existing code does not itself establish every counter/type bound. The narrow proof slice must specify and enforce them for newly admitted v3 operations:

- Expansion scope.count is an exact nonnegative integer within 0..2**53-1. membership is canonical SHA-256. Exact model keys equal the artifact's model set.
- cursor is null or an exact canonical UUID/signed-int64 decimal string matching the admitted record codec. Do not use arbitrary artifact/native free text as a cursor.
- rows and chunks are exact nonnegative bounded integers; bools and floats are refused. Under the supported stopped-writer model, each nonempty chunk advances its cursor, rows <= N, and chunks <= rows. After selecting the next bounded rows, compute the proposed rows/chunks/cursor and validate them before any UPDATE or other incrementing chunk effect. Existing source only validates chunk_size <= 5000 and chunk_bytes; it does not impose the proposed counter maxima, so this is a new v3-only invariant, not a claim about old code. If unexpected membership growth would violate it, refuse before the chunk write and preserve the last admitted state so safe abort remains available. If another later check fails after SQL, transaction rollback must preserve that same state.
- Validation failures during later chunk work must not grow or overwrite the previously committed state. Counters are progress, not permission to skip full membership verification.
- Fixed members are unchanged. Whole-state shape is closed to the current pre-switch family; no ad hoc timestamps, errors, receipts, per-row results or ever-growing debug lists are added.
- For new forward states, verification is absent or the exact fixed table-to-digest map. For new reverse states, no such map is present under the current format.
- A current ACTIVE/DEPROTECTING source row follows its own existing schema/state checks. It is not an ABORTED history row and must not accidentally inherit this narrower field set.
- Unknown or corrupt historical state never receives an inferred missing member. Old-format producer source compatibility still requires exact frozen-producer review before admitting those historical shapes.

The implementation should derive E from the same admitted state fields the executor will write. A generic rule that merely checks current state size on each _save does not prove future abort remains possible.

## Physical journal validation before exact-rowset proof

The authenticated artifact currently names the journal schema/table, not a historical journal OID or primary-key index name. Do not invent those identities or claim historical absence. Validate current physical safety and preserve observed identities through the new operation.

The narrow validator should accept only the actual original CREATE TABLE shape:

- ordinary permanent local table, not a view/materialized view/foreign/unlogged/temporary/partitioned relation or inherited child; no RLS/FORCE RLS;
- exactly three live columns in expected order: operation_id built-in uuid NOT NULL; plan_digest built-in text NOT NULL; state built-in jsonb NOT NULL; no generated/identity/default expressions or unexpected column metadata affecting writes;
- one nondeferrable, validated primary key on operation_id alone, backed by the expected ordinary unique btree UUID semantics, valid/ready/live, with no predicate/expression/include change; no extra uniqueness/check/foreign-key constraints or extra user indexes;
- no user rewrite rules or user triggers, and no unexpected inheritance, policy, dependency or external object requiring cascade;
- exact planned maintenance owner and current existing runtime permission checks, including membership/admin paths and journal writes. The original owner and runtime SELECT grant are compatible. No new ACL repair or grants.

Use schema semantics rather than guessing the auto-generated PK index name or TOAST OIDs. Internal PK/TOAST dependencies are expected. Distinguish them from external dependencies; fail closed if classification is unknown. Read-only monitor grants are not historical evidence, and broad current grant assumptions must not replace the existing runtime-role checks. Root should select an explicit current ACL admission policy before widening beyond the exact fixture.

Perform this validation and history/row-count inspection under the same acquired table/journal locks immediately before mutation. A valid physical primary key is what makes count plus a complete no-repeat chain sufficient for exact membership. A row-level lock alone does not exclude a new operation inserted after inspection.

## Minimum isolated proof slice

Keep v3 execution disabled until all of these have a deciding result:

1. A pure envelope constructor covers every actual forward/reverse pre-switch field and every mutable transition listed above. Independent expected encodings verify max-width counters, UUID/int64 cursors, full verification map, Unicode/control-character fixed metadata, nested guard/proconfig content and exact byte/depth edges.
2. Native PostgreSQL 16 confirms actual jsonb text sizes are dominated by E across each reachable pre-switch state and each abort. A near-budget expansion either rolls back completely or every later legal abort stays within both budgets. No role/helper changes are needed for this state-size proof.
3. A test deliberately adds an unreserved state field or removes the verification/cursor/counter reservation and demonstrates that the independent proof detects the omission. An over-budget attempt after committed work must retain the prior state and remain abortable; no test may count a blocked abort as safe refusal.
4. The physical validator accepts the actual historical/current journal shape without fabricated OIDs/names and refuses independently mutated table/column/PK/RLS/rule/trigger/dependency/owner/runtime-privilege shapes before effects. Mutation execution and restoration require separately admitted fixture authority; this review performs neither.
5. Prove old-format safe abort is unaffected and completed-old-abort idempotence still works after a later successor. Only after these prerequisites should the full successor/lineage/reverse slice be enabled.

No execution result is claimed. No selected source, test or document was changed. This note used additional finite ranges from the same already-pinned migration.py and deprotection.py; the original input hashes remain applicable.
