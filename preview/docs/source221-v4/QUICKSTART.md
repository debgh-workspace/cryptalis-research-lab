# Small public-API quickstart

**Source-checked against Integrated221; this composition is UNEXECUTED. Installed221 and exact smoke are pending.** Use only an approved disposable synthetic application. This template does not create infrastructure or confer deployment authority.

## 1. Supply the existing application and host inputs

Complete [installation binding](INSTALL.md), then supply the objects described in [host inputs](HOST-INPUTS.md). For [manifest.example.json](manifest.example.json), the existing `Customer` model has application-assigned UUID `id`, non-null UUID `tenant_id`, nullable `name` with admitted text type/C collation, and a native unique index on `(tenant_id, name)`.

`mapping` is the application's existing registry. `manifest_bytes` contains the JSON bytes, not a filename. The owner and runtime engines use `echo=False, hide_parameters=True`; runtime credentials do not own the tables or schema. No credentials or URL values are provided here.

An optional offline setup check uses the real public API:

```python
from cryptalis.doctor import doctor

report = doctor(manifest_bytes, phase="setup", mapping=mapping, engine=runtime_engine)
```

Read each `checks` entry's status, code and remedy. A successful setup inspection still has `ready=False` and `complete=False`. It does not inspect PostgreSQL, provider custody or ciphertext, and does not approve the application.

## 2. Plan without effects

```python
from cryptalis.migration import plan, apply, MaintenanceApproval
from cryptalis.sqlalchemy import attach

p = plan(
    manifest_bytes, mapping, owner_engine,
    writers=writer_inventory, search_reviews=domain_reviews,
    keys=tenant_keyrings, runtime_role=runtime_role,
    target_id=deployment_target_id,
    backfill_rows_per_second=measured_backfill_rate,
    verify_rows_per_second=measured_verify_rate,
    temporary_bytes_per_row=measured_storage_cost,
    wal_bytes_per_row=measured_wal_cost,
)
```

Use measurements for this workload. Do not copy fixture cost constants. Resolve every refusal, inspect the plan and preserve `p.artifact` outside database restore. New source221 plans default to the versioned remembered-designation profile. Do not set `preserve_cluster_designation=False`; it raises `legacy_profile_creation_disabled`.

## 3. Protect under explicit maintenance and external authority

Stop/drain every affected writer and exclude alternate writers first. The trusted deployment process must independently approve and retain the exact plan, then supply its matching PREPARED pin. Constructing a `DeploymentPin` record is not approval.

```python
approval = MaintenanceApproval(writer_exclusion_evidence, approved_pause_seconds)
progress = apply(
    p, owner_engine, keys=tenant_keyrings,
    pin=prepared_pin, approval=approval,
)
```

The default stops at `PENDING`. Keep writers stopped. Publish the exact artifact through the existing trusted host procedure, obtain its matching `ACTIVATING` pin, and call:

```python
progress = apply(
    p, owner_engine, keys=tenant_keyrings,
    pin=activating_pin, approval=approval, until="ACTIVE",
)
```

After confirmed activation, retain the authoritative `ACTIVE` pin separately from database snapshots. Lost replies require inspection of the original operation and current authority; never guess a phase. See [RECOVERY.md](RECOVERY.md).

## 4. Attach once and use admitted ORM operations

Attach before application sessions/model use, with no checked-out engine connections. Attachment does not migrate data.

```python
from sqlalchemy import select
from uuid import uuid4

sessions = attach(
    mapping, runtime_engine, lock=p.lock_bytes,
    keys=tenant_keyrings, deployment=(p, active_pin),
)
new_id = uuid4()
with sessions(tenant_id=authenticated_tenant_id) as session:
    session.add(Customer(id=new_id, tenant_id=authenticated_tenant_id,
                         name="synthetic preview value"))
    session.commit()
    found = session.scalar(
        select(Customer.name).where(Customer.name == "synthetic preview value")
    )
    assert found == "synthetic preview value"
```

This adapted example assumes a fresh synthetic value that does not violate the native uniqueness constraint. The host authenticates `authenticated_tenant_id` and authorizes the operation. Attachment does not add a general tenant filter or replace authorization. For `AsyncEngine`, await `attach(...)` and use the returned async session API.

## 5. Prove the exit before adoption

Compare the same native and attached application workloads: exact values, NULLs, result membership, ORM state, typed refusals and driver-boundary observations. Then execute approved current-data decrypt-back, package-free operation and retained encrypted-backup recovery. The exact documentation smoke remains pending; a green source suite, setup report or attach call does not prove these new examples.
