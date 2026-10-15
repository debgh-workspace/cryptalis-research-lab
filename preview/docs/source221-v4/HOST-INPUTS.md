# Explicit host inputs

**Source-checked template; UNEXECUTED.** The host supplies these objects. They are not new Cryptalis helpers or implicit authority.

## Mapping, writer and domain review

Use the existing registry/model and the manifest's stable domain/table/field IDs. The public synthetic example IDs are 501, 502 and 503; its tenant is 504. Assign independent stable identities to another deployment. Do not regenerate identities at startup.

```python
from uuid import UUID
from cryptalis.manifest.compiler import Writer, WriterInventory, SearchReview

DOMAIN, TABLE_ID, FIELD_ID, TENANT = (UUID(int=i) for i in range(501, 505))
writer_inventory = WriterInventory(
    complete=True,
    writers=(Writer(TABLE_ID, "synthetic preview app", "sqlalchemy",
                    evidence="approved disposable fixture's inventoried ORM writer"),),
)
domain_reviews = (
    SearchReview(FIELD_ID, False, "reviewed synthetic names; declared leakage accepted"),
)
```

These evidence strings are examples of fixture assertions, not proof about an application. Replace them with actual reviewed evidence before use. `False` means `small_domain=False`; never use it to misclassify an enumerable sensitive domain. Inventory background jobs, direct drivers, SQL/COPY routes and external writers. Excluded routes need real enforcement. Declaration alone does not stop them.

## Development-only keys

The public `FileDevelopmentKeyProvider` stores a plaintext local KEK. It does not provide production custody, same-user isolation, authenticated file provenance, a backup service or verified zeroization. Do not use test-suite public deterministic roots for private data.

One-time creation requires an explicitly approved owner-controlled private path and a recovery plan. This code is **not executed** and must never become a startup repair fallback:

```python
from cryptalis.crypto import (
    FileDevelopmentKeyProvider, KeyContext, KeyPolicy, Keyring,
    KeyUnavailable, create_root,
)

provider = FileDevelopmentKeyProvider.create(approved_custody_path)
wrappers = tuple(create_root(provider, context) for context in (
    KeyContext(DOMAIN, TENANT, "payload", UUID(int=506), 1),
    KeyContext(DOMAIN, TENANT, "search", UUID(int=507), 1),
))
policy = KeyPolicy(DOMAIN, TENANT, wrappers, 1, 1)
ring = Keyring(policy, {provider.provider_id: provider})

def tenant_keyrings(tenant_id):
    if tenant_id != TENANT:
        raise KeyUnavailable()
    return ring
```

The resolver is synchronous, including for async attachment. Retain the exact provider file and complete policy through the approved host store before protection: domain/tenant IDs, each provider identity, each complete `KeyContext`, wrapped bytes and active generations. The store/serializer is a host integration dependency, not supplied by this example. Do not put custody files, credentials or policy recovery material in source control or public evidence.

On restart, reopen the same file and load the exact retained `KeyPolicy` from that store:

```python
provider = FileDevelopmentKeyProvider.open(approved_custody_path)
policy = retained_policy
if (policy.domain_id != DOMAIN or policy.tenant_id != TENANT
        or any(w.provider_id != provider.provider_id for w in policy.wrappers)):
    raise KeyUnavailable()
ring = Keyring(policy, {provider.provider_id: provider})
```

Rebuild the resolver in each fresh worker. Do not inherit providers/keyrings across a fork. Missing/corrupt custody is a hard stop: recover the exact approved copy and policy, never generate replacements. A failed create can leave a partial file; inspect it before any approved retry.

## Engines, measurements and authority

- Supply the existing mapping; an owner maintenance engine; a separately provisioned non-owner runtime engine/role; and a distinct plaintext runtime role for reversal. Engine logging settings are `echo=False, hide_parameters=True`.
- Supply a stable authorized nonzero UUID `deployment_target_id`, measured positive backfill/verification rates, integer per-row temporary/WAL costs, and an approved pause. Estimates exclude some drain, index/DDL and publication delays.
- Supply actual writer exclusion evidence and explicit maintenance, plaintext and removal approvals. Evidence-record constructors do not approve their own actions.
- Retain an authenticated current plan/pin outside database restore. The database journal cannot select current authority.

The real record shape is `DeploymentPin(p.target_id, p.operation_id, p.digest, "PREPARED")` from `cryptalis.migration`. Use it only after host approval of that exact identity. Forward authority progresses through PREPARED, ACTIVATING and ACTIVE. Reversal has its own operation/digest and PREPARED, PLAINTEXT_ACTIVATING, PLAINTEXT_ACTIVE, REMOVING and REMOVED handoffs. No automatic publisher is supplied.

An administrator reviews role/grant work separately. `p.runtime_role_template("cryptalis_runtime_new")` only prints a template for a new NOLOGIN role. It does not provision credentials, repair existing privileges or authorize grants.
