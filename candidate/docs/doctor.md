# Bounded read-only doctor

Status: bounded diagnostic implementation through S14; exact source and installed evidence below. This is a partial implementation of OBJ-DX-02, not completion of the full doctor objective.

## Static CLI

`cryptalis doctor protection.json --json`

This accepts the product `cryptalis.protection/v1` declaration, using the CLI's existing bounded file reader. It checks declaration grammar only. It does not discover or import application code, open a database, obtain credentials, inspect provider custody, authenticate ciphertext, or repair permissions.

Exit status:3 means a valid but incomplete diagnostic report;2 means a rejected declaration or invalid input;4 means existing CLI I/O/unavailable-output failure. A zero-success exit is deliberately not returned for incomplete qualification. JSON includes `complete:false`, `ready:false`, and an explicit status per check. Plain output includes check names/statuses and static failure codes. A readable report is not deployment authorization.

## Explicit host API

```python
from cryptalis.doctor import doctor
report = doctor(
    manifest_bytes,
    mapping=existing_registry,
    engine=existing_native_engine,
    writers=approved_writer_inventory,
    search_reviews=approved_search_reviews,
    sources={"app/queries.py": reviewed_source_bytes},
)
```

Use the default mode before protection on a native schema. Active mode requires the separate explicit inputs below. The dynamic path reuses the compiler's synchronous psycopg/PostgreSQL16 admission in its own REPEATABLE READ/READ ONLY transaction. It does not call attach or activate, change mappings, migrate data, or apply generated DDL. Source inspection reuses the bounded compatibility scanner and retains its PARTIAL/NOT_INSPECTED coverage. Writer completeness and small-domain reviews are supplied host assertions.

Pre-adoption checks: declaration grammar, bounded native schema/mapping/compiler admission, and supplied-source advisory compatibility. Pre-adoption roles, production provider and ciphertext checks remain NOT_INSPECTED. A proposed lock digest is a change detector, not an authentication signature. No application values or keys are read by this diagnostic mode. Database failures return sanitized SQLSTATE only; invalid metadata is omitted. Source literals and driver exception bodies are not copied into reports.

The caller supplies trusted engine/registry objects. Read-only database transactions do not sandbox host callbacks, prevent every physical disk write, or establish complete writer inventory. PostgreSQL also permits writes to existing temporary tables in read-only transactions. Independent production gates remain UNKNOWN.

## Evidence

Initial76PASS2.81s. Expanded169PASS6.24s including existing compiler/scanner/CLI tests. Removing only compiler read-only enforcement/assertion makes both new ordinary/AUTOCOMMIT write-refusal controls fail; exact compiler bytes restored, then14 doctor tests PASS0.43s. This mutation uses a zero-row DELETE against disposable synthetic tables; it does not mutate customer data.

Repeated offline wheel SHA256:db6e83817fd4bad3e9be8f98b9aebbbc5641ac38f09e64e94ab11be84b77e332. Forty RECORD entries verify;36 installed runtime modules byte-match. Installed full suites:1803PASS/7FAIL/0SKIP305.74s (2.1.3),1785PASS/7FAIL/18SKIP309.25s (2.0.51). The seven legacy-profile failures and two fork warnings remain. Source hashes unchanged.

Primary sources: https://www.postgresql.org/docs/16/sql-set-transaction.html and https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#setting-read-only-deferrable .

## Active metadata/role inspection (S13)

Call `doctor(manifest_bytes, phase="active", engine=planned_runtime_engine, deployment=(host_authenticated_plan, current_external_pin), mapping=existing_registry, sources=reviewed_sources)`. The mapping/source arguments are optional for metadata inspection. The declaration must match the plan and the pin must be ACTIVE and bind its exact digest. An owner engine is refused. Invalid/missing inputs, stale pins, catalog drift, read-only failures and malformed state remain rejected or unavailable. No privileges are repaired.

The inspector reuses the admitted lifecycle attachment checks inside its own read-only transaction. A successful roles check covers the planned runtime role's effective privileges and routine policy at that snapshot, not complete discovery of every external writer. Journal/pin agreement is not cryptographic authentication of the pin's origin. Provider and, without the explicit S14 opt-in below, ciphertext checks remain NOT_INSPECTED; complete/ready remain false. It never calls the maintenance verifier or bypasses its approval requirement. The static CLI continues to inspect only declaration grammar.

S13 installed focused suites157PASS on each dependency cell; source hashes unchanged. Last full-suite baseline remains S12; S13 full suite NOT RUN. All seven independent gates remain UNKNOWN.

## Explicit bounded ciphertext observation (S14)

Add `audit_ciphertext=True, keys=existing_trusted_resolver` to the active host API. Defaults are `audit_row_limit=1000` and `audit_byte_limit=16777216`. Limits must be strict integers in1..10000 and1..67108864 respectively. The static CLI does not obtain keys or enable this observation. Supplying keys without explicit opt-in is rejected before database access.

The active schema/role inspection runs first. Within the same REPEATABLE READ/READ ONLY transaction, the audit reads only row/tenant identities and payload columns, then authenticates visible non-NULL CF1 cells with the existing plan-bound tenant policy and bounded key lease. It does not read the old plaintext source columns. No new cryptography, key cache or credentials are introduced. Keys for tenant policies absent from the compiled plan remain refused, consistent with the existing runtime contract.

Row and cumulative byte limits apply across all model tables. The byte budget uses the existing SQL-side conservative projection cost; it excludes metadata queries and the identity-only lookahead probe, so it is neither total transferred bytes nor a process-RSS bound. Row/byte bounds do not bound elapsed time, provider latency, lock waits or server work. A remaining row beyond a bound produces PARTIAL. An identity-only probe distinguishes an exact end boundary from incomplete coverage. Reports include counts and static codes, never plaintext, row identifiers, frames, keys or provider exception text. A trusted host callback is outside the database read-only sandbox.

CHECKED means only that the observed non-NULL cells authenticated at this snapshot. It cannot prove NULL substitution, absent rows, same-context replay/freshness or complete external membership. Any generation admitted by the exact key policy may authenticate; this is not active-write-generation readiness verification. A fixture that deletes a row and replaces all remaining frames with NULL deliberately demonstrates this limit. Provider custody remains NOT_INSPECTED. `ready` and `complete` remain false. This operation never calls the maintenance verifier, changes a journal/pin, or issues a lifecycle certificate. Existing transition approval requirements remain unchanged.

Source evidence: initial missing-API regression3FAIL; expanded audit90PASS after correcting one test SQL expression (the failed setup is retained). Removing authentication causes1FAIL; removing the byte bound causes1FAIL. Exact restoration and added boundary controls:19PASS. Independent CF1/native-value oracles cover multiple tables, fields and tenants. Repeated wheel SHA25643c98cb0128c0a8cfda090febc8f485bd9b4883f3c9c047aefd155fe263ac080;37 installed modules byte-match. Full installed suites:1831PASS/7FAIL/0SKIP315.40s on2.1.3;1813PASS/7FAIL/18SKIP315.98s on2.0.51. Same seven known legacy-profile failures; source hashes stable. Six later snapshot/projection/READ ONLY/global-row/empty-data controls pass separately on each installed cell, without runtime changes. The isolation-level mutation fails and exact restoration passes. Full-suite acceptance remains open.

AEAD's interface does not itself provide anti-replay, consistent with RFC5116 section1.2: https://www.rfc-editor.org/info/rfc5116/ . This is an established limitation, not a novelty claim.
