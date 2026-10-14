# S22 SA20 full-suite and real capture/restoration audit

2026-10-14 15:48 UTC. Data-only review. No project execution, database work, Git/network calls or shared-source edits.

## Result

The recorded run is 2577 ordinary passes, seven failures, 46 skips, two warnings and 56 successful subtests in 404.29 seconds. Test exit remains 1 because the seven legacy failures remain. Exact case-level comparison to S21 SA20 shows 98 additional passing cases, zero removed cases, unchanged failure identities and unchanged skip identities. This is not a clean full-suite acceptance or a qualification-gate pass.

The runner's 2633 pass count includes 56 subtests. Its 28 skipped count covers call-phase skips; 18 setup skips bring the total to 46. The final pytest summary and progress-phase counts reconcile. No changed expectations or removed failed/skip case is hidden by the count increase.

## Source identity

All 212 entries in the prepared S22 source manifest match the current candidate. The candidate contains exactly those 212 non-cache files. Relative to S21: only src/cryptalis/manifest/compatibility.py changes, and two test files are added. There are no source removals.

All 151 runtime/test/config entries captured by the wrapper match the prepared pins, their copied source-repository bytes and both before/after inventories. The inventories are identical. Documentation/other source files are covered by the 212-file manifest comparison, not represented as separately captured runtime snapshot entries. Source equality is not retroactive executed-bytecode attestation.

The original preflight runner remains byte-identical. The safe readiness log and runner receipt report successful SELECT 1 for both roles with expected hash prefixes 76053d5b/a38ab71b. The frozen versioned wrapper/helper/source packet still matches its reviewed pins. This checks preserved artifacts, not a new preflight or database connection.

## Actual wrapper capture/restoration

All 26 files in prior-corpus match prior-corpus-manifest.json. Each corresponding current shared file independently matches the exact pre-run bytes, and the complete shared filename set across both capture patterns equals the original set. There are no unaccounted added or missing matching files at observation time.

One changed output is preserved under candidate-corpus:
master-s4-compatibility-flush-corpus-v1-sa2.0.51.json
SHA256 1b4a276ccf14da6f352b4bfc12fbac8f2550cb01bcab67d9bc5fe8fd42dbc02e.

Its bytes match the isolation receipt and differ from the prior/restored shared version (faec6d27c3fa9223484869f4d7b52687f26ecadc71c78c03b9e4e8ad4b37b859). The isolation report records no deleted files, no errors and restoration true; all stated restoration checks were independently recomputed. Unchanged receipts were not relabelled as newly emitted outputs.

The safe stop log says server stopped. Root reports postgres-stop exit 0; this audit did not open the environment-bearing stop JSON to independently read that exit field.

## Limits

This establishes a real run's archive/restoration behavior beyond the earlier filesystem fixtures. It does not classify current corpus semantics, relabel older shared observations as S20/S21 evidence, prove cryptographic/security qualification, or close the seven historical failures. Only the explicitly changed archived output is identified as captured by this run; byte-unchanged files do not establish whether their producers executed.

No tests.json, package-origin.json, environment-containing start/stop/readiness JSON, credential files, private-home files or live databases were read. AUDIT.json records per-file hashes, exact outcome delta and input evidence digests. All seven qualification gates remain unchanged.
