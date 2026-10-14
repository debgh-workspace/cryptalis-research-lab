# Independent past lifecycle evidence audit

Date: 2026-10-14, approximately 14:43–14:45 UTC.
Scope: S20 inactive payload preparation and current-data reverse-policy drift evidence, reconciled against the root checklist. This is a read-only evidence audit, not a test rerun or independent security qualification. Only these new audit files were written.

## Useful finding: receipt counters need phase-aware interpretation

The SA20 S20 runner receipt reports 28 skipped. That is not the complete suite skip count. Its progress log contains 18 setup-skipped reports and 28 call-skipped reports; JUnit and the final pytest summary report 46. The checklist correctly retains 46.

The runner pass counts are 2393/2347, including 56 successful subtests in each cell. The final pytest summary separates ordinary tests: 2337/2291 passed, seven failed, and 56 subtests passed. These are consistent accounting views, not different runs. Do not copy the runner counters as ordinary-test totals or all-phase skips.

All seven S20 failed test identifiers independently equal the S19 identifiers in both dependency cells. They remain the legacy deprotection-ordinal assertions. No new failure can be inferred from these receipts, and their continued failure must not become full-suite acceptance.

## Payload preparation claim verified within its stated scope

- Both final-boundary focused JUnit records contain 114 passed, zero failed/errors/skipped; times 1.841 and 1.722 seconds. The private preparation file contributes 41 cases, with 73 affected companions. This matches the checklist's updated scope, rather than the historical 35-case prose.
- Both S20 full-suite JUnit records include the same 41 preparation cases passing.
- For the private runtime module and its test file, current S20 bytes equal the focused GREEN source snapshot and recorded before/after hashes, and equal the S20 full-suite snapshots and before/after hashes.
- Both omission receipts contain exactly six failed final-return controls, zero errors/skips. Static diff of the preserved mutation removes only the final `_binding` call. The test file is unchanged. The six cases cover final-seal source/target expiry for one/two rows and simulated PID change for one/two rows. These are controlled clock/PID observations, not actual process-fork evidence.
- The current-data transform-back case uses an inactive staging table, modifies its current target value, transforms that value back, and checks that source data/journal snapshots remain unchanged. It does not activate a new payload generation, publish a successor policy, or exercise product rotation cutover.

## Reverse-policy drift claim verified within its stated scope

- Both B7 focused receipts/JUnit records have six passes. Four are the new current-data drift cases (payload/search policy change × resume/abort); two are companion controls. Do not describe all six as distinct new drift cases.
- Both S20 full-suite JUnit records include those same four drift cases passing and 31 predecessor-consistency cases passing.
- The B7 test and deprotection runtime bytes equal their focused source snapshots and recorded before/after hashes, and their S20 full-suite snapshots and before/after hashes.
- Source inspection confirms post-protection edits, NULL changes, deletion and insertion, committed-prefix preservation on policy refusal, recovery by resume or abort/new operation, and unchanged historical encrypted backup observations.
- The B7 test explicitly stops at PLAINTEXT_PENDING. It does not perform plaintext role handoff, new credentials or external publication. Its policy-change inputs are refused; it does not establish active rotation support.

## Hash and scope accounting

OBSERVATIONS.json binds eight safe receipt sets and four selected source/test files. A null hash means that an earlier isolated candidate did not contain an unrelated later addition; it is not drift. The omission module intentionally differs from S20. No unexpected selected-file mismatch was found. COUNT_RECONCILIATION.json binds S19 failure identities and S20 progress logs.

Recorded source hashes demonstrate source stability and preserved snapshot equality, not retroactive executed-bytecode attestation. The existing installed dependency provenance mismatch, same-host recovery limits, seven legacy failures, active-rotation permission limits, and all seven UNKNOWN gates remain unchanged.

No tests.json, package-origin.json, environment files, credential files, database connections, project imports, test executions, Git operations, or network operations were used. Safe runner receipts, JUnit, source-stability inventories, progress records, a final summary line from tests.log, and relevant preserved source were inspected. No additional execution is needed to resolve this accounting question.
