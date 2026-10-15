# Actual capability and refusal matrix

**Bounded** means implemented source with the named finite evidence. It does not mean production-qualified or universal support. Integrated221 has independently accepted source suites; its installed suites and new documentation examples are pending. Transport218 evidence stays on Transport218.

| Capability | Actual boundary |
|---|---|
| Authenticated text storage, entity/scalar reads, ORM insert/update/delete, SQL NULL | Bounded admitted mappings and ORM flush routes. Application-assigned stable identity and explicit tenancy are required |
| Standard text and admitted VARCHAR/SQLModel text mappings | Compiler admission is required; arbitrary types, custom coercions and collations are not admitted |
| Equality, IN, tenant-scoped uniqueness | Declared full-width keyed terms, accepted leakage, reviewed value domain and native collation/index contract |
| IS NULL / IS NOT NULL, ordinary inequality and NOT IN | Admitted finite grammar with native NULL/empty-list semantics; not arbitrary compound NOT or field-to-field comparisons |
| Aliases, outer joins through public keys, projections, relationships, SAVEPOINTs | Finite native-versus-protected cases only. A failed scoped transaction control invalidates the unit; do not continue an ambiguous outer transaction |
| SQLAlchemy sync/async | Main source cells 2.0.51 and 2.1.3. Native 2.1-only APIs explain the 46 expected 2.0 skips; no substitute 2.0 API is promised |
| Optional SQLModel, including public async hook | Separate 38-case source evidence; this is not every SQLModel/dependency combination |
| Offline setup doctor; native planning; active diagnostics | Read-only/advisory within supplied scope. Setup does not connect. Bounded ciphertext audit requires explicit keys, opt-in and limits. Reports never confer readiness |
| Maintenance protection/resume/full verification | Bounded protocol with stopped/drained writers, byte-bounded chunks, current-value verification and separate external publication |
| Current-data decrypt-back and removal | Bounded admitted schema profiles, distinct plaintext role, explicit exposure/removal consent, package-free workload and retained-backup obligations |
| Retained native slots, comments and admitted public metadata | Finite native-property evidence. Thirteen replacement/new historical-contract cases pass in source221. No all-schema/all-metadata guarantee |
| Remembered CLUSTER designation | New source221 plans inventory original names/linkage and explicit designation. Bounded correction integrated in source. Physical heap order is not preserved or promised |
| Older retained artifacts | Parseable with conditional admission. Safe surviving-index recovery and pre-switch abort have bounded evidence. Missing retired-index history remains a hard blocker; no generic importer/repair |
| Development custody and process restart | Public local file provider; plaintext local KEK and exact retained-policy requirement. No production custody qualification |
| Exception diagnostic transport | Bounded trusted-local serialization evidence only; never load untrusted pickle or infer general distributed-execution support |
| One FastAPI/SQLModel application | Historical pinned app, zero business-source edits, 13 bootstrap plus four fixture lines, explicit configuration and private bounded delete/cascade profile. Not a public attach-only application guarantee |

## Refused or not admitted

| Operation | Required response |
|---|---|
| Protected ranges/comparisons/order, LIKE/ILIKE/prefix/contains/suffix, regex/fuzzy/full text | Refuse; no plaintext fallback or ciphertext-order substitution |
| Protected general DISTINCT/GROUP BY/aggregates/arithmetic, protected join/FK keys, other unadmitted operators | Refuse; research helpers do not admit a public capability |
| Non-text protected values, JSON/array/numeric/datetime predicates, custom protected types | Refuse until separately admitted; no silent text coercion |
| Serial, identity or database-default-generated primary keys | Refuse at plan time; assign an admitted identity before flush |
| Opaque SQL, COPY, raw-driver protected writers; general Core/bulk DML/UPSERT | Refuse guarded unsupported paths. Private experimental flags are not a public compatibility promise |
| Unknown/external writers, unsafe owner-runtime credentials or unreviewed callable SECURITY DEFINER routines | Block adoption until the actual writer/privilege/review problem is resolved |
| Online/near-zero-downtime or adaptive parallel migration | Unqualified; use the admitted maintenance procedure, with no pause-SLO claim |
| Complete root rewrap, payload-key rotation and search-key reindex | Incomplete. Preparation experiments/local primitives are not complete active workflows |
| Production AWS KMS or other production custody | Unqualified; no real-provider claim from the local implementation |
| Clean-host reproduction, broad legacy repair, other PostgreSQL majors/services, second unrelated app, Flask/Django | Open or unadmitted; separate evidence is required |

Refusal is the current safe boundary. [All 34 full-product objectives](OBJECTIVES.md), including advanced SQL, stronger privacy and broader lifecycle compatibility, remain active.
