# ORM workstream A2: public UPDATE fault boundary

Owned tree: candidate-accel-orm-faults-20261013. Frozen A1 and S16/S17 trees were not edited by this worker. Coordinator owns all database sessions, Git/publication and integration. All seven production gates UNKNOWN.

## Outcome

Confirmed and corrected one native compatibility defect: ordinary public bulk UPDATE DBAPI errors were incorrectly converted into failed-ORM-flush state. The minimal correction exempts DBAPIError only in the inner native invocation catch. Existing provider/cancellation cleanup and outer async result quarantine remain intact. No new operation or effect is admitted.

## Final source and checks

- src/cryptalis/sqlalchemy.py: ef764a712b60c6c33e694937ed23ce56f21b8374f081d276b0f076310a9d3b89
- tests/test_private_public_update_faults.py: b02b835db801c7b0bc735323ea91e058ed8d2bc1e3408b39604ea1aa280281e6
- Actual coordinator final SA2.1.3: 20 PASS, 8.15 s.
- Actual coordinator final SA2.0.51: 20 PASS, 7.90 s.
- Exact final runtime/test bytes independently match both archived source snapshots. Both runs report source unchanged and successful server stop.
- Original overflow RED: 4 FAIL, 2.15 s.
- Outer-exemption mutant: 2 FAIL, 1.23 s, exact root/SAVEPOINT quarantine assertions; final restored source passes.
- Thirty-five actual private DELETE controls passed in an earlier combined SA2.1 run against the final runtime; three A2 fixture failures made that combined cell fail. No separate final SA2.0 DELETE claim here.
- Worker checks: AST and pure imports/parameter inventory on both pinned versions, with DB connection entrypoints disabled. No worker DB runs.

## Scope and artifacts

Twenty controls cover real overflow, real autoflush IntegrityError, unavailable/expired-renewal providers, real preparation task cancellation, and explicitly synthetic exceptions after successful native result completion. The latter tests outer quarantine; it does not reproduce a natural driver-finalization failure. Independent raw protected-storage, lock, pool and same-session recovery observations remain strict.

Changed artifacts: runtime file, new fault-test module, this progress file, docs/research/PRIVATE_PUBLIC_UPDATE_FAULTS_20261013.md, A2_BASE_RECEIPT.json and A2_FAULT_VERIFICATION_RECEIPT.json. The research document and JSON retain exact prior failed-harness boundaries and all nine coordinator receipts. No historical legacy assertion changed.

## Next boundary

Local runtime/tests remain frozen. Coordinator reports the minimal correction integrated into S17 and its full installed run underway; this worker makes no full-suite or promotion claim. No further A2 implementation is queued. Keep private public UPDATE off by default.
