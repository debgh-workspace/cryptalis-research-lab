# R3 post-run verification

R3 completed all 17 differential methods: PASS, 8.470 seconds, exit 0.
R2 timed out at the first near-max reverse method after the coordinator's 120-second
limit (exit 124); the remaining 16 were not observed. These are paired bounded
runs, not a ratio benchmark or a measured per-method performance comparison.

The current manifest and all 214 candidate source hashes match the frozen receipt.
All oracle and test hashes also match. The 17 r3 method ASTs are identical to r2;
assertions and fixtures were not weakened. Evidence hashes are recorded in
POSTRUN_R3_VERIFICATION.json. Original receipts and logs remain unchanged.

Source inspection explains a plausible cost reduction: r2 fetched source.operation_id
in each history iteration, reparsing the full source JSON each time; r3 reuses a
constructor-local UUID. No profiling attribution is claimed.

This review read logs and checked source hashes and ASTs only. It ran no tests,
product imports, database operations or Git commands and edited no product source.
Results establish synthetic parser/helper boundaries only; compiler/catalog
admission, native PostgreSQL and lifecycle correctness remain unverified.
All seven product gates remain UNKNOWN.
