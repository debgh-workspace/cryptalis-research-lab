# S12 read-only doctor integration boundary (not implemented)

Reconciliation at2026-10-13: a bounded static scanner already exists in manifest/compatibility.py and plan.compatibility_report(). The missing capability is a unified doctor CLI/API and comprehensive dynamic coverage, not the absence of all source inspection. S11 corrects two stale advisory claims before this integration.

## Reuse rather than rebuild
- Product declaration parser: parse_protection_declaration.
- Native pre-adoption dynamic admission: compile_protection, which owns a fresh REPEATABLE READ/READ ONLY transaction, verifies transaction_read_only, and never reads application values. Host writer/value-domain declarations remain attestations rather than proof of all writers.
- Supplied-source report: existing bounded compatibility_report, never import or execute the application source.
- Existing active-layout checks are separate: check_attachment/check_deployment inspect pins/journals/roles. Do not run the plaintext compiler against active encrypted schemas and report expected bytea as corruption. Never call attach merely to diagnose: attach changes mappings and installs guards.

## Proposed first executable slice
A doctor API accepts manifest bytes plus explicitly supplied registry/engine/writer inventory; no connection strings in output and no automatic plugin/module imports. Static CLI accepts a bounded declaration file and explicitly reports dynamic checks NOT_INSPECTED. It must not claim full doctor completion. Dynamic API composes existing read-only admission, returning sanitized finite checks, proposed-lock digest and existing advisory compatibility report. Do not return plan DDL, source literals, credentials, rows or keys.

Every report must distinguish checked/rejected/unavailable/not-inspected; report phase and evidence scope. No overall secure/ready/PASS badge based on partial inspection. Ciphertext authentication, production provider custody, complete writer coverage, actual query routing and all seven qualification gates remain UNKNOWN until specifically inspected with their required authority. Empty source findings do not prove compatibility. No automatic grants or repairs.

## Required independent acceptance evidence
- Real native PG16 schema pass and incompatible/default/generated schema refusal.
- PostgreSQL-enforced read-only write-injection refusal, including caller AUTOCOMMIT engine; exact rows/catalog/schema state unchanged.
- No query against application values in pre-adoption mode; compare captured query set and independent row snapshot.
- Supplied source never executes/imports; no secret literals, URLs or driver message bodies in diagnostics.
- Malformed manifest, missing host evidence, wrong mapping, access failure and ambiguous lifecycle mode remain visibly incomplete.
- CLI malformed options, missing/oversized/symlink paths and broken output retain existing bounded IO discipline.
- Clear behavior for active encrypted layout; reject unsupported diagnostic mode rather than silently applying plaintext schema criteria.

This draft does not authorize new credentials, new clusters, production providers, mutation, or crypto/cache changes.
