# Related route comparison

| Route | Current behavior by source | Proposal |
|---|---|---|
| Async normal-body exit, preparation succeeds | Native context exit/commit | Unchanged |
| Async normal-body exit, preparation fails, native rollback succeeds | Native rollback then primary re-raise | Clear retained preparation; otherwise unchanged |
| Async normal-body exit, preparation fails, rollback fails | Native secondary replaces primary | Same primary, local UNKNOWN/non-retryable metadata, fixed notes where deliverable, best-effort public invalidation |
| Async body already raised | Direct native exit | Unchanged; no adapter pre-exit preparation |
| Sync body/commit exit | Native SessionTransaction context | Unchanged; no async pre-exit preparation |
| Failed flush preparation | Existing failed-flush helper and native failed-unit transition | Unchanged; selected existing regression |
| Failed SAVEPOINT control | Existing owning-connection invalidation | Unchanged; selected whole-unit nonpublication regression |
| Optional async SQLModel | Inherits adapter transaction method behind existing exact default-off profile | No admission change; broader optional qualification remains separate |

Pinned SQLAlchemy 2.0.51 and 2.1.3 native sources were read as data. `NATIVE_SOURCE_PINS.sha256` lists those exact files. Both native transaction exits propagate secondary rollback errors. The attached primary-preserving policy is an intentional diagnostic difference mandated by Cryptalis, not a claim that native errors have the same precedence.

Public native invalidate only processes currently owned transactions. Root native close can remove its Connection before the saved rollback error is raised, so a successful later invalidation cannot prove that former physical session was closed. Fresh-checkout/data/lock evidence is indispensable, and arbitrary transport failure remains outside the proposed callback fault.
