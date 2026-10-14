# Independent D-only v3 receipt audit

2026-10-14. Data-only audit: read JSON/source bytes and hash files using standard-library code. No candidate imports, builds or reruns. Only this additive note written.

## Result

Bounded PASS for all eight declared v3 D launches: four positive PASS and four EXPECTED_FAIL. No audit mismatch found.

- D-normal positive: exactly 241 ordered observations under O0 and O1.
- D-diagnostic positive: exactly 374 ordered observations under O0 and O1.
- Positive observation records are exactly equal across optimization modes for each build.
- D-normal negative: exactly 101 ordered observations, target frozen/uuid-storage-unicode, path value.
- D-diagnostic negative: exactly one observation, target vector/frozen/uuid-storage-unicode, path value_hex.
- Each negative has child FAIL, exit 1, exact intended RuntimeError, original_verified true, exact frozen mutation path and a separately reconstructed literal-00 actual mutation. Controller status is EXPECTED_FAIL only with clean final integrity.

Independently reconstructed expected observations from CASE_SELECTION and ADDITIONAL_EXPECTATIONS rather than relying on child PASS: all D-normal ABI/full-read actuals match their exact frozen expectations; all diagnostic vectors, observation ABI records, direct counts/errors and wrapper public+nested native records match. Comparison is type-exact, recursively over dictionaries/lists. All unmodified negative-prefix observations and the negative target's saved original match the same frozen oracles.

## Integrity, lineage and supervision

Execution freeze SHA-256 remains 12fdaed70806d9979a8fe9865b7405d7c55032f045ff6b864222b49aa70e7e99. All 17,210 pinned file hashes and all 76 preserved v2 artifact hashes match current bytes. Shared cache inventories match.

Every supervisor/child anchor agrees, child receipt hash matches its recorded binding, and controller/child integrity lists are empty. Exact argv and child environment match the frozen plan. Before/final private-cache records are empty and child private directories are currently empty.

Each child explicitly records the original build anchor 1a56f94e6f30cf448070038647c092fbaba10071919eca9f22f59f44b9f4f4f1. Adopted build receipt paths and hashes, binary paths/hashes and actual v2 freeze bytes match the approved lineage. No build substitution or rebuild occurred in v3.

Before/final mapped-library paths and hashes match the frozen resolved map and current files; libasan and libubsan are present. Loaded module origins are pinned or equal the exact adopted binary. The newly pinned ABI helper is admitted without changing origin checks.

All eight supervisors report no timeout/stream-cap/other reason, empty stdout/stderr, confirmed leader reaping, empty cleanup errors and no process-group signals. Receipt evidence does not independently prove absence of escaped descendants or stress coverage of exceptional supervision branches.

## Preserved chronology and scope

The original v2 D-normal negative controller remains FAIL and its child FAIL_INTEGRITY. Its seven unexecuted v2 D siblings still have no supervisor receipts and remain NOT RUN. The sixteen accepted T/S v2 runs remain preserved byte-for-byte; v3 did not repeat them. Combined finite evidence is the sixteen accepted T/S v2 launches plus eight accepted D v3 launches, alongside the separately retained failed v2 D attempt.

This closes only the declared finite address/undefined-behavior experiment. Leak freedom stays UNKNOWN after the historical LSan clean-control fatal exit 23; detect_leaks=0 does not qualify leaks. No exhaustive allocation/fault proof, sanitizer coverage of uninstrumented CPython/provider internals, actual-fork extension, timing claim, database/product adoption or full DESIGN closure follows.
