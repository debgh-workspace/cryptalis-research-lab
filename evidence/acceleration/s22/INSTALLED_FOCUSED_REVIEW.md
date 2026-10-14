# S22 installed-focused independent data audit

2026-10-14 15:52 UTC. No tests or database execution by this reviewer.

Both receipts, terminal summary lines and JUnit records agree: 351 selected cases passed, zero failures/errors/skips; exit 0; SA21 5.07 seconds, SA20 5.52 seconds. The complete selected case identities are identical across cells. Compared with each S21 focused run, there are exactly 98 added passing cases (20 NamedExpr, 78 statement-binding) and no removed cases.

The package-origin logs identify the disposable S22 installed environments, outside source. Independently rehashed all 40 .py modules in each installed package: exact equality with the 40 S22 source modules and the wheel's 40 modules. Wheel SHA256 346eac4f4cf54bac270e25dce6f7d97cdb591ac2969a00a3b9c073a0e4a20c57 matches the frozen installation plan. This checks installed module bytes, not the entire dependency environment or historical executed-bytecode identity.

All 151 runtime/test/config entries per run match the source-repository snapshot, before/after hashes and S22 prepared pins. Before and after inventories are equal. All 212 current source files match the prepared S22 manifest. Role-preflight receipts report successful checks for both existing roles, with prefixes 76053d5b/a38ab71b.

For each run, all 26 pre-run corpus backups match their manifest and current shared bytes. Current matching filename sets exactly equal each pre-run inventory. Both isolation reports have no archived or deleted outputs, no errors, and restoration true. Thus no new corpus artifact attribution or semantic classification follows from these focused runs. The safe stop logs confirm server stopped; root reports stop exit 0. Environment-bearing stop JSON was not opened.

This verifies the selected installed-focused matrix only. The full S22 suites are source runs, not full installed-suite evidence. Existing seven legacy failures, dependency provenance limitations and all seven UNKNOWN qualification gates remain unchanged. No tests.json, package-origin.json, environment-bearing JSON, credentials or private-home files were read.

AUDIT.json preserves exact case identities, module hashes, source checks, restoration checks and safe evidence hashes. Available for further assigned work.
