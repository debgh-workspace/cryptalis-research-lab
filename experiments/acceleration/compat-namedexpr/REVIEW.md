# NamedExpr independent post-run review

2026-10-14 UTC. No blocking evidence discrepancy for publishing this narrow, separate S21 derivative with its explicit limitations. It is not merged into frozen S21. This assessment is not a publication action or a release qualification. All seven gates remain UNKNOWN.

## Independently reconciled results

- evidence/compat-namedexpr-red-20261014: 17 failed, 3 passed, zero skipped/errors, 0.18 seconds. All 20 setup and teardown phases pass. Terminal summary, actual JUnit testcase outcomes, and progress call outcomes agree.
- evidence/compat-namedexpr-green-sa21-20261014: 118 passed, zero failed/skipped/errors, 1.86 seconds.
- evidence/compat-namedexpr-green-sa20-20261014: 118 passed, zero failed/skipped/errors, 1.80 seconds.

Each GREEN contains exactly 20 new NamedExpr cases, 56 existing string-binding cases, 28 existing compatibility-report cases, and 14 doctor cases. JUnit and every progress phase agree on 118 passes. No subtest inflation or setup-stage skips appear.

RED excerpts demonstrate false imported-query attribution: the scanner reports core_dml_refused_if_attached with CONDITIONAL_REFUSAL where rebound_query_binding with UNRESOLVED is expected after an assignment expression. The fixed visitor scans the RHS first, then invalidates the target, preserving the positive RHS/reimport controls while correcting later attribution. The prior source-only review describes conservative scope and comprehension limits; those limits remain.

## Lineage and stability

All 150 source-before inventory entries match their current candidate roots independently, and each run's before/after maps are identical. Both GREEN inventories are identical. RED-to-GREEN changes exactly one inventoried file: src/cryptalis/manifest/compatibility.py. The new test bytes are identical across RED and both GREEN cells. Existing tests are not weakened.

All 210 frozen S21 preparation hashes still match the original S21 candidate after these runs. Compared with that frozen inventory, the NamedExpr derivative changes only compatibility.py; its new NamedExpr test is separate. S21's published integration and installed-focused claims must not be silently reassigned to this derivative.

Safe package-origin logs verify imports from the respective isolated RED/GREEN source directories. Source-root receipts identify the intended source candidate and unchanged preflight. Readiness logs record successful dual-role PostgreSQL preflight. This is focused source-overlay evidence, not installed-artifact qualification or a full-suite run. Dependency cell labels do not alone attest historical installed versions.

## SHA-256 identities

- Frozen S21 / RED scanner: 4d42e25714eed40dfb3c27d10239705855d6ffe963a5ef642de7511f85abe460
- GREEN scanner: 15d7030053b1d0a5acee9d81f7a9ffa8ae7b81b5e73271d7dcd83dca3d9dcc7c
- Identical new tests: 05b69558fd5b72781f81f63c48ba1c46f6307f4b2f0cc0e6d653d7735dbb2eef

No tests were rerun and no database, Git, environment, or credential operations were performed by the reviewer. No tests.json or package-origin.json was read. No candidate or prior review was edited. Only this new report was written.
