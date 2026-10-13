# S8 physical mapping resolution experiment

Status: separate prototype; integration awaits both installed dependency cells and real-application confirmation.

Preserve the manifest-first public API. Native unqualified public table mappings require physical resolution on the original runtime connection search path before lifecycle inspection narrows that path. Collect candidates read-only, validate the protected deployment, then freeze only ordinary direct public tables inside compiled schemas. Protected models remain exclusively bound from the authenticated lock. Public table resolution never grants DELETE authority: private table allowlists, grammar, same-schema constraints and locked effect inventories remain required.

A missing native resolution is not permission to guess the manifest schema. Other schemas, views and unsupported mappings remain outside this correction. Runtime schema/name drift is refused. Attachment freezes names, not a new general OID authorization contract. Existing per-operation cascade OID/lock checks remain unchanged; broader concurrent owner-DDL qualification is still open.

Alternatives: retain explicit per-table application edits (known working but integration cost); broad schema_translate_map (changes more behavior and does not govern literal SQL); wire proxy (separate deployment and trust model). This prototype is the smallest tested host-adapter correction, not a claim of universal superiority or novelty.

Evidence: native child/cascade RED2FAIL2PASS; corrected source99PASS;6 async paired cases plus2 absent-resolution refusals PASS. Removing only the new schema/name drift check makes both targeted tests fail. First installed2.1.3 full suite1760PASS7FAIL314.69s; second cell pending. No production gate is promoted.

Primary references: https://www.postgresql.org/docs/16/ddl-schemas.html and https://docs.sqlalchemy.org/en/20/core/metadata.html .
