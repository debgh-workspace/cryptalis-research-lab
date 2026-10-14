# Statement bindings post-run and S22 composition review

2026-10-14 UTC. No blocking discrepancy found for retaining the narrow derivative and its focused evidence. All seven gates remain UNKNOWN. This is not a full-suite or installed-artifact qualification.

## Reconciled focused evidence

- compat-statement-red-20261014: 64 failed, 14 passed, zero skipped/errors, 0.42 seconds; 78 passing setups and teardowns.
- compat-statement-green-sa21-20261014: 196 passed, zero failed/skipped/errors, 1.99 seconds.
- compat-statement-green-sa20-20261014: 196 passed, zero failed/skipped/errors, 2.01 seconds.

Terminal summaries, actual JUnit testcase outcomes, and setup/call/teardown progress events agree. No subtest inflation or setup-stage skips occur. Both GREEN selections contain exactly 78 statement-binding, 20 NamedExpr, 56 string-binding, 28 compatibility-report, and 14 doctor cases.

RED excerpts demonstrate false Core DML attribution after loop-target rebinding where an unresolved rebound diagnostic is expected. The same new tests pass after the reviewed correction. Existing positive/negative controls remain included. No tests were weakened or changed between RED and GREEN.

All three 151-file source-before inventories match their current roots independently, and each before/after map is identical. GREEN inventories are identical. The sole RED-to-GREEN inventory difference is compatibility.py, from 15d7030053b1d0a5acee9d81f7a9ffa8ae7b81b5e73271d7dcd83dca3d9dcc7c to ba8ce979234426f0e16961fa065fd54dda7bceb50c7019e2bc5e11b33d092920. The new statement-test hash is f5a20b9a49ce5dc0c36199d41a0811ef8115bdd5c58685052fe33b89dd787cbd.

Package-origin logs verify source imports from the intended isolated candidates. Source-root receipts record unchanged preflight, and readiness logs record passing dual-role preflight. These are source-overlay focused results; dependency cell labels alone do not attest historical version provenance.

## S22 preparation composition

All 212 hashes in persistence-recovery-20261013/s22-source-preparation.json match candidate-s22-scanner-20261014. All 210 frozen S21 preparation entries are retained. Only compatibility.py differs; tests/test_compatibility_namedexpr.py and tests/test_compatibility_statement_bindings.py are added. All three overlay files are byte-identical to the reviewed/executed statement derivative. Every frozen S21 preparation hash still matches S21; no existing test, runner/preflight, packaging configuration, or other module is changed by this composition.

Preparation-manifest SHA-256: 0ba8dca89209dab18d222c5d2b35c56795443911516ac53bc08162d8a06cf3b1.

This verifies preparation composition only. It does not transfer the isolated focused results into a claim that S22's combined full suite or installed artifact passed. Those results need separate review.

## Review boundaries

The companion POSTRUN_AUDIT.json records exact counts, safe evidence hashes, origins, source comparisons, and composition checks. The first audit script assumed the older manifest key sha256 and stopped on KeyError before writing; the observed S22 schema uses source_sha256. The reviewer reported this, received continuation authorization, and corrected only the audit's read key. Candidate and manifest bytes were not altered.

No tests, database commands, Git commands, or source edits were performed. No tests.json, package-origin.json, environment, or credential files were read. Only these separate review artifacts were written. Conservative advisory/PARTIAL analysis limitations from STATIC_REVIEW.md remain; no complete Python analysis or release admission is claimed.
