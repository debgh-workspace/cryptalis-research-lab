# S21 installed-focused independent evidence review

2026-10-14 UTC. This is separate from the immutable full-source review and its AUDIT.json. Data for this review is in INSTALLED_FOCUSED_AUDIT.json to avoid replacing that prior audit.

## Result

Both installed-focused cells reconcile with no blocking evidence discrepancy:

- evidence/s21-installed-focused-sa21-20261014: 253 passed, zero failures/errors/skips, 5.11 seconds.
- evidence/s21-installed-focused-sa20-20261014: 253 passed, zero failures/errors/skips, 5.00 seconds.

Terminal summaries, JUnit suite attributes, all 253 actual testcase elements, and progress setup/call/teardown outcomes agree. Each phase has 253 passes; there are no excess subtest calls or hidden setup-stage skips. The selected testcase IDs are identical across cells.

The exact selection is 56 string-binding cases, 132 maintenance-budget cases, 28 compatibility-report cases, 14 doctor cases, 18 migration-audit cases, 3 deprotection cases, and 2 CLI cases. This totals 253 and covers the requested bounded selection. Exact IDs are retained in the companion audit.

## Installed provenance and source stability

Package-origin.log identifies site-packages/cryptalis/__init__.py in the corresponding release-lab/s21-installed-v2-20261014 environment, records installed=true, byte_matched_modules=40, and verified=true. The expected source is candidate-s21-correctness-20261014/src, not an alternate source candidate. As a separate current-state check, this reviewer hashed all 40 candidate Python modules against the matching installed package paths in each environment: no mismatches. This current observation supplements, rather than replaces, the execution-time wrapper receipt.

Both source-root receipts identify the intended source candidate and unchanged preflight. Readiness logs record the passing dual-role PostgreSQL preflight. Each 149-file executable/test/build inventory has identical before/after maps, and every source-before hash independently matches the current candidate. External-source inventories are empty and establish no additional coverage.

The existing S21 integration review established that the role preflight script and test conftest are byte-identical to accepted S20/source-lock inputs. No runner source was changed by this reviewer. Package-origin receipts support the stated installed execution boundary; this review does not independently reconstruct all dependency installation provenance or prove historical dependency versions from directory labels.

## Limits

These are installed-focused results only, not a full installed suite. The separate full-source suite still has seven known failures. No new runtime capability, production readiness, complete compatibility, or release qualification is established. All seven gates remain UNKNOWN. Remote composite restoration is outside this review and remains the root's separate verification responsibility.

No tests, database commands, Git commands, or candidate edits were performed by this reviewer. No full test JSON, package-origin JSON, environment, or credential files were read. Prior full-source and scanner review artifacts remain unchanged. The companion audit records exact case IDs, counts, origins, current module/source comparisons, and hashes of safe evidence files.
