# SQLAlchemy storage attachment

**IMPLEMENTED:** bounded sync/async text attachment; research prototype.
All seven gates remain **UNKNOWN**. Production-provider and independent production-security qualification remain incomplete.
[Status](status.md) owns revision-bound tests and the corrective row-isolation evidence.

The adapter prepares row-bound CF1 frames before SQL and keeps ORM attributes as text or NULL.
Read projections carry field, tenant and row context. Authentication precedes value release.
Host-requested primary-key constraints must match returned identity. Unsupported forms fail before SQL.
Async key preparation runs before synchronous hooks. Protected SELECT caching is disabled.
Unprotected SELECTs retain native caching.

Use the [product protection transition](walkthrough-migration.md) before attachment.
Bounded current-data decrypt-back and removal are implemented for admitted schema profiles through `cryptalis.deprotection`; they are not limited to empty targets.
Follow the [recovery/removal guide](https://github.com/debgh-workspace/cryptalis-research-lab/blob/d952c505a4666266019e32f27c77f93edd5151ca/preview/docs/source221-v4/RECOVERY.md) with the exact forward/reverse artifacts, current external pins, maintenance and plaintext consent, and a distinct plaintext runtime role.
Removal also requires actual package-free workload and retained encrypted-backup recovery evidence. Those are host attestations, not checks performed by the removal API.
The exact public quickstart/backup/restore/removal smoke remains unexecuted; generic legacy repair, clean-host recovery and complete lifecycle qualification remain open.
Supply a trusted compiler lock, admitted tenant keyrings and an engine with parameter logging hidden.
Attach before sessions or model use. Close existing connections first.
Supply the exact approved plan and its current authoritative ACTIVE pin after confirmed activation.
Missing or stale authority must remain a refusal; do not fabricate a pin to bypass the check.
The deployment tuple does not create or approve authority. Use the restricted runtime engine.
The host authenticates tenant scope and authorizes queries; attachment adds no tenant filter.
Assign row IDs and declared tenant values before flush. A Python default does not replace assignment.

```python
from cryptalis.sqlalchemy import attach

sessions = attach(
    Base.registry, runtime_engine, lock=plan.lock_bytes,
    keys=tenant_keys.__getitem__, deployment=(plan, active_pin),
)
with sessions(tenant_id=authenticated_tenant) as session:
    session.add(Customer(id=app_assigned_uuid, tenant_id=authenticated_tenant, note="text"))
    session.commit()
# AsyncEngine: await attach(...); use async with and await Session methods.
```

The AsyncEngine note applies to supported ordinary SQLAlchemy mappings. Default async SQLModel
attachment remains refused; do not enable private flags as an adoption workaround.

Storage-only locks reject protected search. [Equality/IN/uniqueness](walkthrough-search.md) require declared capabilities.
Opaque SQL, COPY, protocol handles, Core/bulk writes and unsupported expressions reject.
Direct/grouped AND lookups and scalar primary-key IN capture explicit requested IDs.
Callable defaults, tuple/transformed identities and ambiguous bind forms reject before SQL.
Primary-key lookups in HAVING or JOIN ON also reject for protected reads.
Explicit public bind overrides retain native values. Compiler-generated override names reject.

Run from the project root. The wrapper reloads both private credential files and probes both roles.
It ignores inherited URLs, prints safe failures and stops if either probe fails.

```bash
.venv/bin/python scripts/test_postgres.py -- -q tests/test_sqlalchemy_adapter.py --tb=short
```

Runtime CRUD and tested persistent DDL/ownership denials have bounded PostgreSQL 16 evidence.
Independent writers can bypass attachment. Changed ciphertext rejects; valid replay, nullable NULL
substitution and row deletion do not establish freshness, authenticated presence or completeness.
The host must exclude unsupported writers. Production custody and deployment enforcement remain UNKNOWN.
