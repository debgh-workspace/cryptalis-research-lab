# Independent receipt audit: proof-v1 baseline startup HOLD

Date: 2026-10-15 UTC

## Disposition

The first baseline invocation is an infrastructure/proof HOLD. It is not the expected product RED and supplies no executed remedy-regression result. Keep the failed receipt unchanged. No derivative, omission or restored variant is authorized by this audit.

The original source review remains sealed and unchanged. Its source-level conclusion did not establish that the unexecuted proof's startup assumptions would hold.

## Observed evidence

Receipt directory: `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/doctor-remedy-proof-v1-baseline-red`.

The retained stdout consists of one `harness_error` record with:

- `error_type`: `ProofRejected`
- `failure_code`: `root_must_supply_empty_environment`
- `observations_not_accepted`: `true`

Stderr is empty. The root's result records exit 2, no signal or termination reason, 0.2015460460097529 seconds wall time, unchanged checked pins and an absent bytecode prefix.

The independently inspected launcher calls `subprocess.Popen` with explicit `env={}`. Its selected arguments use the pinned Python 3.12 executable and `-I -B -S -X pycache_prefix=.../proof-v1/no-bytecode-use`. Its selected variant is `baseline-red`; the expected product RED exit would have been 1.

The first assertion inside `preflight` is `require(not os.environ, "root_must_supply_empty_environment")`. The observed failure occurs before child verification of its source/stdlib inventories, before the selection marker, before `install_product`, and before `run_cases`. Standard-library startup imports have occurred; copied product source installation and CLI cases have not.

The root result's `pins_unchanged` checks exactly three files: the `INPUTS.sha256` inventory, proof program and original review. It does not itself verify every file named in the inventory. The child's deeper input verification was not reached. Do not expand that receipt field into a full 21-input or selected-product preservation claim.

## Cause and next boundary

The empty launch mapping and nonempty child `os.environ` are compatible if interpreter startup adds a locale variable. That remains a hypothesis from this receipt. The retained output does not identify any key or value, and this reviewer did not inspect an existing environment.

A separately selected, minimal child-startup diagnostic can establish the behavior under the same pinned interpreter/flags and an explicitly empty launch environment. It must not read or inherit existing environment values or import product code. Preserve this failed v1 receipt regardless of the diagnostic outcome. Any proof change needs a new sealed packet, renewed source review and a fresh coordinator selection; do not weaken the assertion or rerun v1 silently.

## Audited hashes

- `/tmp/cryptalis_doctor_proof_root_2152.py`: `1213aecb187a342a4448ac621663e0d33c7ceddb5160e0a5a67e7c18335e8f96`
- `stdout.log`: `234588ea4a894301eb5c52e8d7ae39ff5eadce1e47752af8c2d2638c594359f3`
- `stderr.log`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `RESULT.json`: `ad00312afb69bc2bf6e415528803c7e0ebfb2171fb76271707c381c2b03e28a9`
- `selection.json`: `930fd95208dd88e52ebbc2add20101c396884fbb48c97bd90d8e804c51642383`

This audit used source/receipt reads and hashes only. No interpreter, proof, test, project import, database operation, environment inspection, cache/live-cell access or Git operation was performed by the reviewer.
