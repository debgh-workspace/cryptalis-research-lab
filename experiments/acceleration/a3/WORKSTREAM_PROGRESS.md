# A3: ordinary ORM optimistic versioning

Status: test-only S17 derivative, four cases PASS on each pinned version; runtime and test bytes remain frozen.

## Contract and bounded acceptance

- `docs/compatibility.md` admits ordinary native ORM CRUD semantics. Manifest mapper compilation (`src/cryptalis/manifest/compiler.py`, `_compile_model`) does not exclude integer `version_id_col` mappings. Native DELETE admission (`src/cryptalis/sqlalchemy.py`, `_native_delete_rows`) explicitly retains the version bind.
- The explicit versioned-mapper refusal in `_experimental_public_update.py` applies to private bulk UPDATE. This test does not opt into or change that capability.
- Blueprint B-ORM-17 identifies optimistic concurrency as unexecuted research. This four-case schedule is bounded evidence, not its full concurrency qualification and not a malicious-replay freshness guarantee.
- Four native-differential cases: sync/async times stale ordinary UPDATE/DELETE. Both Sessions load version 1; the winner commits version 2. The stale flush must raise the exact native `StaleDataError`, preserve the native failed-unit/identity-map state, and leave the winner's physical bytes untouched. Explicit rollback must recover the same Session; fresh UPDATE reaches version 3 or fresh DELETE removes the row.
- An independent owner connection and existing independent CF1 decoder inspect stored winners and retry outcomes. The version mapper is established before table creation and planning; there is no post-plan mapping or schema mutation.

## Files and provenance

- Source: frozen `candidate-accel-integrated-r2-20261013` (S17), 195 inherited files verified unchanged by `A3_BASE_RECEIPT.json`.
- Added executable file: `tests/test_sqlalchemy_optimistic_versioning.py`.
- Added receipts: `A3_BASE_RECEIPT.json`, `docs/research/A3_OPTIMISTIC_VERSIONING_CORPUS_20261013.json`, `docs/research/ORM_OPTIMISTIC_VERSIONING_20261013.md`, this progress file.
- Test SHA-256: `f319a0ab2e5569d050a236c6285359c9dce3c4a5cb6be3134aa07a11c8717a7a`.
- Runtime SHA-256: `fc2f7a7c983370f7c81874b56ec8e511532d226fc962bc0c8939b38d4daadfbe`.
- No runtime, historical test, Git, role, credential, or cluster changes.

## Actual validation

- SQLAlchemy 2.1.3 and 2.0.51: AST parse and module import PASS with psycopg connection entrypoints disabled.
- An attempted pytest collect-only on each version was correctly refused by the unchanged mandatory PostgreSQL preflight hook (exit 4). No marker was injected and no bypass was attempted. Do not count collection as PASS.
- Coordinator database results: SQLAlchemy 2.1.3, 4 PASS in 1.78 s; 2.0.51, 4 PASS in 1.47 s. Both passed unchanged dual-role preflight, retained stable source, and stopped cleanly. No database execution by Agent A. Exact archived runtime/test bytes were checked against this candidate.
- Exact test arguments: `tests/test_sqlalchemy_optimistic_versioning.py -q --tb=short` (four parameterized cases).
- Existing S17 seven legacy-profile failures remain outside this slice. All seven production gates remain UNKNOWN.

Next task: coordinator publishes the bounded eight-cell corpus supplement and test-only evidence. No runtime correction or new integration is needed. Broader optimistic-versioning qualification remains open.
