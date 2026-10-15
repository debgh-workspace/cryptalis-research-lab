# One declaration, explicit host inputs

The example is the concrete JSON form of the existing `tests/test_migration.py::application` declaration: domain 501, table 502, field 503, model Customer, tenant column tenant_id. These are public synthetic example identities. Use stable independently assigned identities for a real evaluation; do not regenerate them at each startup.

| Member | Meaning |
|---|---|
| schema | Exactly `cryptalis.protection/v1` |
| profile | Exactly `cf1` for this preview |
| routine_allowlist (optional, top-level) | Array of distinct lowercase 64-hex SHA256 reviewed-routine digests; default `[]`. A digest is not permission or proof of review; retain the corresponding independent routine review and admission evidence |
| domain_id | Nonzero canonical lowercase UUID identifying the protection domain |
| models[].model | One unambiguous existing mapped model name, not a module to import |
| table_id / field_id | Distinct stable nonzero canonical UUIDs |
| tenancy | `{"column":"tenant_id"}` or `{"single_tenant":true}`; not both |
| fields[].name | Existing ordinary mapped column attribute; not a relationship or context key |
| protect | `true` |
| queries | `[]` for storage only; admitted equality/unique intent as shown |
| accept_leakage | Explicit matching accepted query leakage; do not add search implicitly |

All model/field arrays must be nonempty. Query and leakage arrays reject duplicates. `unique` implies `equality`: even `queries:["unique"]` requires `accept_leakage:["equality","unique"]`. For storage only, both arrays are empty. Stable IDs are distinct across the complete declaration, including the domain. The parser accepts only its documented object members. Declaration validity is not native schema admission. The compiler returns separate canonical lock bytes; do not invent or hand-edit that lock. Protection/reverse artifacts and publication pins are additional protocol records, not a second field-configuration language.

Equality permits admitted IN queries. Uniqueness is within the declared tenant scope. Preserve native semantics: the historical searchable-email application explicitly selected C collation before schema creation. This is an adoption decision, not permission to silently change the collation of an existing application. Planning must refuse an incompatible native schema. The example fixture uses `Text(collation='C')` and a native unique index on `(tenant_id, name)`.

The host separately supplies:

- `WriterInventory` with every writer and exclusion evidence; completeness is a host assertion.
- `SearchReview` per searchable field with the value-domain decision and leakage evidence.
- Admitted key policy/provider resolver, outside the database and public manifest.
- An owner maintenance engine and a restricted runtime engine.
- A trusted deployment target, current artifact/pin authority outside database restore, measured rates/costs and maintenance approval.

No secret, password, private root or KEK belongs in this manifest. Do not substitute the public deterministic roots in the test suite for custody.
