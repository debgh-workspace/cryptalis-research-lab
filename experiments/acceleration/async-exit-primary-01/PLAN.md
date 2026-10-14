# Deferred RED/GREEN plan

All commands are proposals. None has been executed by the preparer. The coordinator alone may run one reviewed command block at a time through the unchanged dual-role preflights and exclusive-lock corpus-v2 lab wrapper. Stop for independent terminal audit between every block. No cluster/credential changes, imports outside that wrapper, install, network action, remote publication or checklist edit is authorized by this packet.

## Frozen trees

- RED: `candidate-next-unblocked-correctness-red-20261014`: all 216 S25 files unchanged, plus exactly one new test file.
- GREEN: `candidate-next-unblocked-correctness-20261014`: the same new test, and exactly one changed runtime file versus S25.
- `BASELINE_SOURCE_MANIFEST.json` is the exact original 216-file S25 manifest. `BASELINE_sqlalchemy.py` preserves the original runtime file. RED and GREEN each have a complete 217-file manifest and SHA256 listing. `SOURCE_DELTA.patch` is the exact baseline-to-GREEN delta.

## Selected nodes and sequence

`NEW_NODE_IDS.txt` lists all 22 planned parameterized nodes, derived statically from literal pytest parameters, not a pytest collection claim:

- 8 paired native/protected root/SAVEPOINT cases with provider or injected cancellation primary failures.
- 2 protected failed-invalidation cases with explicit UNKNOWN and later laboratory rescue.
- 2 real suspended-provider task-cancellation cases.
- 4 custom/unavailable exception-note cases; primary identity and cleanup attempts must survive unavailable output.
- 2 pending-only/no-SQL cases with successful native cleanup and retained-preparation clearing.
- 4 related sync native/protected body-error exit cases whose native secondary-error policy must remain unchanged.

`REGRESSION_NODE_IDS.txt` lists 24 existing nodes: successful async root/nested cleanup, real cancellation, failed SAVEPOINT whole-unit quarantine, and early failed-flush rollback/invalidation controls. No original assertion is edited.

Execute RED SA2.1, audit, RED SA2.0, audit, GREEN SA2.1, audit, GREEN SA2.0, audit. RED selects only the new 22 nodes. GREEN selects all 22 plus the 24 existing regressions. Source reasoning predicts primary replacement in the 12 protected double-failure cases and stale preparation in the root pending-only case; these are predictions, not reproduced outcomes. Any different failure, collection problem, timeout, failed cleanup or origin mismatch requires diagnosis. Do not relabel all failures as the intended RED, weaken assertions or proceed automatically.

## Evidence requirements

Before and after each block verify `INPUTS.sha256` and `PACKET.sha256`. Capture unchanged preflight, candidate source origin, all source snapshots, exact node IDs/outcomes, wrapper/runner exits, server stop, and all 26 original corpus restorations. The selected early-flush module has an autouse corpus writer; corpus-v2 isolation is mandatory even when its selected methods add no corpus entries.

A separate-process source-origin check does not continuously attest to every import. No aggregate source or installed result follows from these selected checks. If the focused correction passes, full current main and optional SQLModel regression, independent review, packaging and installed qualification remain separate coordinator-owned decisions.

## Bounded cleanup and ambiguity

The fixture owner Engine gets a fixture-lifetime public begin listener setting transaction-local lock_timeout=1s and statement_timeout=5s. This includes independent observation and schema teardown. Lock evidence uses a tighter local 100ms lock timeout. Async task/session/engine cleanup awaits are explicitly bounded to 5 seconds each. Cleanup faults are removed before laboratory rescue. The helper records fixed cleanup-stage notes without replacing an earlier failure; if there was no earlier failure, cleanup failure fails the test.

These bounds prevent the proposed intentional callback faults from silently turning into an unbounded teardown wait. They are not a hostile-driver guarantee: asyncio timeout depends on cancellation cooperation, and the unchanged wrapper's process bound/server shutdown remains required. Failed bounded cleanup means STOP and inspect the existing lab. No automatic retry, backend termination, fresh cluster or credential substitution is proposed.

Ordinary protected failure cases inspect native transaction/pool state and independent stored values plus row-lock acquisition before any test-driven rescue/close/dispose. The nested case includes a flushed outer prefix; fresh checkout/commit must still see only the original committed row. Native controls and failed-invalidation arms explicitly rescue before these observations and retain that weaker evidence boundary.

The seven historical acceptance failures and all seven production gates remain unresolved/UNKNOWN.
