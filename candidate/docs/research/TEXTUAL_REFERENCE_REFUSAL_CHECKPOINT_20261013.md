# Textual-reference refusal checkpoint

## Implemented boundary

SQLAlchemy textual references do not carry protected column lineage. The
adapter now checks every local textual-reference occurrence within its owning
SELECT scope. This prevents unsupported protected sorting, grouping, DISTINCT
ON, window and ordered-aggregate work from reaching the driver through names
that the earlier selected-column-only guard did not resolve.

Selected expressions use SQLAlchemy's FROM-only namespace. Bare outer ORDER BY
and DISTINCT ON use selected-label precedence. GROUP BY and names embedded in
expressions follow PostgreSQL input-name precedence. Nested SELECTs are checked
in their own scopes. Public alias-shadow controls retain native results.

The resolver builds the pinned SQLAlchemy compile state without rendering SQL.
It neither prepares nor caches keys, rewrites expressions, changes CF1, nor
admits additional protected capabilities. Unresolved and protected ambiguous
references fail closed. The original column-lineage guards remain in place.

## Failure evidence retained

- Initial wrapped-label C2 controls: 32 failed, 58 passed.
- TypeCoerce controls against the intermediate C2 fix: 12 failed, 18 passed.
- Independent FROM/qualified-name controls against final C2: 28 failed, 52 passed.
- Independent GROUP input-shadow controls: 2 failed, 2 passed.
- Remaining-clause controls against C3: 32 failed, 48 passed. Of those failures,
  20 established missing refusals; 12 came from the specialized mode() fixture's
  SQLAlchemy type inference and are not counted as product defects.
- Changing only that fixture to native pg_catalog.mode() produced 4 failed,
  8 passed, 68 deselected in 2.03 s. Native/public cases passed; the four protected
  cases confirmed the remaining WITHIN GROUP refusal defect.

The earlier source/test snapshots remain in coordinator evidence. The native
fixture correction does not erase or relabel the initial failed run.

## Verified finite gate

Coordinator PostgreSQL receipts were independently read without running a DB:

- SQLAlchemy 2.1.3: **284 passed**, 31.08 s, 48 warnings.
  Evidence: `c4-textual-scope-green-sa21-20261013`.
- SQLAlchemy 2.0.51 affected suite: **401 passed, 28 skipped**, 45.51 s.
  Evidence: `c4-textual-scope-affected-sa20-20261013`.
  The skips cover the two unavailable native 2.1 APIs, not failed protected cases.
- Both runs report unchanged source and external-source hashes and successful
  PostgreSQL shutdown. No failures or errors are reported.
- Pure admission checks passed 76 cases on 2.1.3 and 64 on 2.0.51, including
  protected projections without an active key operation, nested SELECT scope,
  reverse public window shadowing and comma-list ordering. These pure checks
  are additional structural evidence, not a replacement for the native oracle.

The 284-case inventory consists of 120 C2 wrapper controls, 80 FROM/qualified
controls, four GROUP shadow controls and 80 remaining-clause controls. Native
queries compare textual references against explicit column expressions;
attached public controls compare returned values, grouping results and
deterministic pages. Protected controls require
typed refusal before the driver's execution event. Table aliases and sync/async
paths are included.

Frozen runtime `src/cryptalis/sqlalchemy.py` SHA256:
`286869f5f2cf262991adea324344a5091e1e9d7994b4416464d2f799f087e2ad`.

Corrected independent clause-test SHA256:
`68cad71a86f5d7471c32a3bdafa0da72ec751530f6b451a50412aa20e109f4fc`.

## Limits

Compile-state access is specific to the pinned SQLAlchemy compatibility cells.
ORM loader/context options can be processed earlier; native loader regression
remains required. Empty-stack construction conservatively refuses ambiguous
protected FROM candidates. The finite inventory is not a proof covering custom
compilers, future SQLAlchemy syntax extensions or arbitrary SQL expressions.

This is a refusal/native-semantics correction, not a performance result or an
independent security qualification. C1 remains separate and held. Combined
installed full-suite validation and publication are coordinator-owned. Seven
legacy-layout failures remain unresolved; all seven production gates are UNKNOWN.

Primary semantic reference: [PostgreSQL 16 SELECT, GROUP BY and ORDER BY
namespaces](https://www.postgresql.org/docs/16/sql-select.html). The installed
2.1.3 and 2.0.51 SQLAlchemy `visit_textual_label_reference` and
`_label_resolve_dict` implementations define the version-specific lookup inputs.
