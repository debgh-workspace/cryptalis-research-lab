# Independent r2 native packet post-run review, v1

2026-10-14. Safe receipt and file-hash audit only. The coordinator owned all execution and database actions. This reviewer did not read raw environment-bearing tests/package-origin/readiness/start/stop JSON.

## Result

SCOPED GREEN verified for the frozen r2 eight-case native/transaction packet in both cells:

- SQLAlchemy 2.1.3: 8 passed, 0 failed/errors/skipped; pytest 5.90 s, JUnit 5.897 s.
- SQLAlchemy 2.0.51: 8 passed, 0 failed/errors/skipped; pytest 6.56 s, JUnit 6.565 s.

Each JUnit case list exactly matches all eight planned IDs, including the calibrated early-refusal reservation discriminator. Each progress stream contains 24 passing setup/call/teardown reports. The four native case records are IDENTICAL in each cell, with eight completed native/lifecycle paths and twelve all-true shape/comment/current-value observations, including all four lifecycle removals.

Both source-stability maps (153 entries) and external-test maps (3 entries) are unchanged. Both runner receipts contain 152 source/test hashes matching the frozen candidate manifest; all 214 candidate manifest entries still match current bytes. For each cell, all 26 prior corpus files match both archived backup and current primary bytes. Isolation reports show restoration true with no errors, archived changes or deleted files. Safe readiness logs report preflight success and safe shutdown logs report server stopped. The coordinator reported wrapper/preflight/stop exit codes zero; raw JSON was deliberately not read to re-check those environment-bearing fields.

## Boundary

The r2 native results remain valid at this exact source/test boundary. A pending r3 parser-performance correction is separate work and neither erases these observations nor inherits their result without matching inputs and appropriate re-execution. This review does not clear that correction, constructor/envelope controls, full suites, compatibility, lost-COMMIT replies, crash durability, production custody or any release gate. The historical RED receipts remain separate preserved evidence.

The early-refusal test passed against the reviewed r2 guard; static counterfactual analysis shows omission of reservation or the guard would fail its expected refusal. No mutation execution was performed. The tests establish the bounded smaller-cap refusal/rollback path, not production-scale capacity.

## Evidence pins

- Frozen INPUTS.sha256: `3139aa00e119c999c9b027695cd0c2d089d154ff721b73e38ef4326d832a9b52`
- Candidate source manifest: `f60c533cd016eee96c2045ddd3efe95633aaf07b2df5761bc2b6bcd695c32741`
- Reviewed commands: `e8854547af9db3a4ebde8dcaef8c1565e19adbf3105ee90da49834ae6aa8d033`
- SA21_RECEIPT_AUDIT_v1.json: `cb7ae15cf3f23fa93d75d6c95593c5f15fb321b4ddcb44ec75b0c2fd9771ebbf`
- SA20_RECEIPT_AUDIT_v1.json: `845dfc3db1597834d65e28797eb27f8f3602b18551da60478f07c27d3d175fd7`
