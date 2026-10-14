# B9B: bounded inactive preparation profile RED

Status: TESTS PREPARED, NOT EXECUTED. Root owns all PostgreSQL runs, GREEN acceptance, promotion and publication. No generation-2 publication is proposed.

## Frozen base and delta

Base: `candidate-durable-payload-journal-20261014`.
- Module SHA-256: `18de8f736a3fba717c1ed399a98d289a42e6d94e660234642563c363645b7edd`
- B9A R3 test SHA-256: `21edf18c18056a02f6afc15a34fe768172e098b0ddff2c49a9623584d6bb8a19`
- `PROFILE_BASE_HASHES.json` records every 210 inherited non-cache file, including the 208-file S20 base and the two B9A additions. All remain byte-identical. No runtime/module, inherited test, wrapper, dependency, canonical document or source edit.
- New executable file: `tests/test_payload_rotation_profiles.py` only. New records: this matrix and the base hash manifest.
- Static Python AST parse succeeds. No import, pytest collection, test execution, PostgreSQL command or Git command was performed by this worker.

## Contract and deciding scope

Owners: `docs/decisions.md` approved app-assigned identity and storage/equality scope; `docs/lifecycle.md` Changes and rotation; original `candidate-notes-durable-rotation-20261014/TEST_MATRIX.md` P1/R1; reviewed `candidate-notes-durable-preparation-review-20261014/NEXT_SLICE.md` same-journal B9A contract. B9A intentionally admitted UUID/equality only. B9B extends only the three remaining profile combinations, with unchanged UUID tenant, single model/field, external source authority, generation-1 active attachment and generation-2 inactive target. Existing B9A 16 cases and unchanged B8 controls remain companion gates, not new coverage claims.

Six deciding cells, with explicit pytest parameter IDs:

| Selector | Parameters | Future deciding result |
|---|---|---|
| `test_profile_current_values_same_journal_inactive` | `uuid-storage`, `bigint-equality`, `bigint-storage` | Nine native ordered current rows, five exact batch receipts, independent full decode, exact membership/NULL/text types and header/term parity, source frames/catalog/pin/source journal unchanged, one journal, generation-1 attachment intact, repeated terminal inspection has zero seals and zero mutations. |
| `test_profile_restart_preserves_committed_prefix` | same three | Real SIGKILL after first committed chunk, observed backend termination, independently reconstructed PUBLIC keyrings in fresh exec workers, unchanged first two target frames and first receipt, only remaining seven identities sealed, full parity, fresh terminal inspection performs no seals or mutations. |

All six currently expect uncaught `PreparationFailure` with `code == 'unsupported_profile'` from `bind()` -> `_authority()`. These are positive future-contract tests, without xfail, skips, caught-rejection success, monkeypatch admission or altered frozen expectations. Root must inspect the traceback/code. Collection/setup/fixture failures or a different rejection are not the intended RED and require fixture diagnosis before GREEN.

Root selectors:
- `tests/test_payload_rotation_profiles.py::test_profile_current_values_same_journal_inactive`
- `tests/test_payload_rotation_profiles.py::test_profile_restart_preserves_committed_prefix`

Use only the unchanged existing-role `scripts/test_postgres.py` workflow. Repeat accepted GREEN plus affected frozen companions in SQLAlchemy 2.1.3 and 2.0.51. This file does not supply credentials or a substitute runner.

## Independent fixture and oracle

The new file creates its own native SQLAlchemy mapping and disposable schema using the existing owner/runtime fixture identities and PUBLIC provider. BIGINT columns remain native PostgreSQL OID 20 / exact Python int; UUID columns remain OID 2950 / exact UUID. There is no database-default or identity generator, integer-to-UUID adapter or string-backed identity column. Generation-1 setup is the ordinary previously authorized synthetic protection/publication path. Stage and journal receive no new grants.

Nine rows are inserted in reverse native order. BIGINT covers -2^63, negatives, zero, positives and 2^63-1. Both extreme IDs have non-NULL authenticated payloads. UUID covers a low and maximal UUID. Before rotation planning, attached runtime updates a value, deletes a row and inserts a different row; the independent expected map differs from the historical map. NULL, empty text, Unicode and trailing-space text survive.

The decoder independently implements the public CF1 tuple/HKDF/HMAC/AEAD framing recipe. BIGINT record bytes use the specified tagged signed eight-byte encoding, independently of product `_record`; storage uses a 14-byte header and equality a 46-byte header. The oracle never treats storage nonce bytes as search terms. It verifies exact signed native order and canonical decimal journal identities/cursors, including boundary values.

Logical-byte receipts are checked independently: 24 identity bytes for BIGINT/UUID tenant versus 32 for UUID/UUID; non-NULL contribution is `3 * frame_length - 42` for storage or `3 * frame_length - 74` for equality. Every batch has an exact two-row cap and 4096-byte bound. This checks profile-dependent accounting, not new exact-fit/oversize fault coverage; the unchanged B8 and B9A byte-boundary controls remain required.

The frozen B9A worker's `finish` action has a four-step cap, insufficient for this nine-row case. Instead this test uses its existing one-step action in at most five fresh workers after the committed prefix (four remaining chunks, then terminal verification). Every worker uses the frozen containment/output/cleanup harness and reconstructs its own provider/keyrings. No worker or module modification is required to collect the RED.

## Implementation hazards exposed by static inspection

Removing the first admission check alone is insufficient. Artifact admission also restricts UUID/equality; stage layout and source checks fix native UUID IDs; persisted cursor/member validation assumes UUID strings; logical accounting fixes equality overhead and 32 identity bytes; source/target header generation checks must distinguish storage search generation zero from equality generation one. A future implementation must bind these distinctions to the compiled descriptor and native relation, not infer authority from journal data or weaken canonical tuple/budget, current-pin, single-journal or final-lease checks.

No new key scheme, provider, cluster, roles, credentials, product CLI, active generation-2 policy, production recovery guarantee or global exactly-once claim follows. The six cells do not repeat the whole 48-cell original proposal across profiles or claim all its remaining faults covered. Stop after root records the exact RED and reviews the next implementation boundary.
