# Independent compatibility binding review

Date: 2026-10-14 UTC.

## Decision

No blocking finding for publishing the narrow advisory-source-scanner derivative. This is a bounded diagnostic correctness correction, not runtime feature admission, production readiness, or comprehensive Python name resolution. All seven release gates remain UNKNOWN.

## Reviewed delta and static constraints

Candidate: `candidate-compat-binding-20261014`, derived from `candidate-accel-payload-integrated-20261014` (S20). Within the 148-file executable/test/build inventories, only `src/cryptalis/manifest/compatibility.py` changes and `tests/test_compatibility_string_bindings.py` is added. Existing tests and build inputs are unchanged. RED uses the same new tests against the unchanged S20 scanner; RED-to-GREEN changes only the scanner.

The helper recognizes ExceptHandler.name, MatchAs.name, MatchStar.name, and MatchMapping.rest. Function locals include these string targets, including nested patterns, without descending through nested function/class scopes. This prevents inherited SQL/model identities from being used even before a local binding executes.

Exception types are inspected before alias invalidation. Handler bodies follow entry invalidation, and the alias is removed again at exit, including when a body explicitly reimports the same name. Match subjects are inspected before capture invalidation. Captures are invalidated before guards and bodies, between sibling cases, and after the match. Wildcards bind nothing. The regression cases preserve outer scopes, defaults, explicit subsequent imports, nested patterns, and unrelated-name controls.

The union of possible match captures deliberately sacrifices precision: a genuine call on an unaffected branch can be omitted. This is conservative unresolved analysis, not proof of compatibility. Pre-existing broader control-flow and class-method lexical-scope limits are not redesigned. Coverage remains PARTIAL, authority ADVISORY_NOT_AUTHENTICATED, staging_required true, and effects NONE; diagnostics do not echo source literals.

## Independent evidence audit

Only safe source, tests.log, readiness.log, package-origin.log, source-root.json, source-before.json, source-stability.json, external-source-before.json, external-source-stability.json, candidate-corpus-isolation.json, and progress.jsonl were read. No tests were rerun; no database or Git commands were executed. No tests.json, package-origin.json, environment, or credential files were read. Candidate files were not edited.

- `evidence/compat-binding-red-20261014`: tests.log reports 55 failed, 1 passed in 0.33 seconds. Progress events independently contain 56 passing setups, 55 failed calls, 1 passing call, and 56 passing teardowns. No skipped events. All 56 cases are from the new test file. Failure excerpts show the intended false diagnostic attribution on S20.
- `evidence/compat-binding-green-sa21-20261014`: tests.log reports 98 passed in 2.20 seconds. Progress independently contains 98 passing setups, calls, and teardowns, with no failures or skips.
- `evidence/compat-binding-green-sa20-20261014`: tests.log reports 98 passed in 1.79 seconds. Progress independently contains 98 passing setups, calls, and teardowns, with no failures or skips.
- Each GREEN call inventory is 56 new binding regressions, 28 existing compatibility-report cases, and 14 existing doctor cases.
- All three source-root receipts identify the expected isolated candidates and report candidate_override and preflight_unchanged true. Package-origin logs identify the matching candidate source and report verified true. Both tests.log and readiness.log record passing PostgreSQL preflight.
- All 148 source-before entries independently hash to the current corresponding source root. Source-stability before/after maps match exactly in each run; both GREEN inventories are identical.
- External-source inventories are empty; their stability success does not establish additional external-source coverage. Candidate-corpus isolation receipts record no archived corpus outputs and primary_receipts_restored true. No corpus result is claimed by this slice.
- SQLAlchemy cell names above are receipt-directory labels supplied by the runner/root. The safe logs reviewed here do not independently attest installed dependency version numbers. The unchanged-wrapper claim is recorded by source-root receipts and root testimony; this audit did not separately hash the wrapper against a prior trusted wrapper snapshot.

## Final SHA-256 identities

- S20 / RED scanner: `60c725dd0e7c567c579ea444beea2f80e32d27e7a8ccfb2d0938f668fda69099`
- GREEN scanner: `4d42e25714eed40dfb3c27d10239705855d6ffe963a5ef642de7511f85abe460`
- New regression test file, RED and GREEN: `fea21ff5374d165112d4370514fbdd430f708db96635e0aea2d4f9aff22f1ed8`
- Existing compatibility-report tests, unchanged: `1d220fa656af7d2120440572b60d7a2388ecac7c075dd8a59372f2722f62910b`
- Existing doctor tests, unchanged: `8a546981a1d154fd39245cf5cdee773a64c6d191a2905aa18a84a459aa711f20`

Publication should preserve this exact lineage, selected-test scope, RED evidence, conservative-analysis limits, and UNKNOWN gates. This review authorizes no new publication action by itself and makes no claim about a full-suite run.
