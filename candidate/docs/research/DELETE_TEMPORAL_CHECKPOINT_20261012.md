

## 2026-10-12 ordinary public DELETE and temporal catalog slice

Candidate chain: native-delete -> delete-catalog -> delete-temporal (all isolated, uncommitted).

Real upstream FastAPI native suite: 58 PASS. Protected full_name with baseline integration: 57 PASS, 1 call failure, 1 teardown error; both refuse public Item bulk deletion. Private Item opt-in alone remains refused because upstream mappings are unqualified. Explicit schema qualification in the external lab shim passes target selection; it exposes two independent refusal causes: native compiled-cache reuse fails exact inventory statement identity, and standard temporal columns fail inventory type whitelist. Disabling cache only on internal inventory calls removes the former; leaves temporal refusal.

Six finite temporal metadata cases on real PostgreSQL 16.15 provide RED (six failures in catalog parent) and GREEN (six passes in temporal candidate): date, timestamp, timestamptz, time, timetz, interval. Each uses two committed ID-selected DELETEs, exact affected-row counts and native remaining-value comparison. This admits metadata for plain public columns only; it does not implement encrypted temporal search or general interval predicates. Exact pg_catalog base-type and other inventory checks remain.

Conservative namespace alternative: qualify mapping schema in external lab setup. This costs two mapping-integration lines and does not solve general unqualified adoption. Ambitious alternative remains native-resolution/OID binding with version-pinned proof; not implemented in this reconstructed source. Do not relax namespace checks to make the app green.

Private opt-in adds one line; external qualification adds two lines beyond original six integration lines: actual prototype integration is nine lines plus four fixture lines. Historical harness JSON reports six because its static counter did not include added lines; use this corrected scorecard. Upstream application sources remain unchanged. No claim of six-line fully working production integration.

Sources inspected 2026-10-12: https://docs.sqlalchemy.org/en/20/core/connections.html (scoped compiled cache options); https://www.postgresql.org/docs/16/datatype-datetime.html (native temporal types). Official docs establish mechanics, not this prototype's security. Native source and observed repeated execution establish the cache-identity issue.

Residual: private bulk DML is off by default, with known broader invocation-authority qualification incomplete. No general feature promotion. Role preflight and durability retained. All production gates UNKNOWN. Next: real-app temporal result, cross-version tests, omission controls, installed-artifact repetition, complete protected-app uninstall, and second app.
