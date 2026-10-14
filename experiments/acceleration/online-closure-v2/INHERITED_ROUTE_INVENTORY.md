# Inherited API inventory: online closure V2

Status: source-only disposition, not executed evidence. This inventory covers exactly the 14 methods defined on EnumerationLab in the frozen 201-file V2 candidate. It does not classify every possible future subclass method or arbitrary dynamic invocation.

Source aliases below are relative to `candidate-online-closure-v2-20261014/tests/`:

- Base: `_online_enumeration_lab.py`
- CF1: `_online_cf1_lab.py`
- Child: `_online_cf1_process_lab.py`

## All 14 base methods

| Base method and lines | CF1 dispatch/disposition | ChildFrameLab dispatch/disposition | Boundary |
|---|---|---|---|
| `__init__`, 28-39 | Override at CF1 90-93 creates fixture crypto, then base owner setup. | Inherits base owner setup. Not the admitted reconstructed-worker route. | Creates schema/source/native rows as owner. Outside concurrent preparation admission. No authorization to invoke it follows from this inventory. |
| `connect`, 41-46 | Inherited. | Inherited. | Opens owner connection and sets session search path/timeout; checks isolation. No source/dirty/staged mutation. This is session setup, not a claim of zero SQL. |
| `reconstruct`, 49-64 | Override CF1 147-153 reopens durable identity, prepares fresh local crypto state, then reads the expected pin without a write-admission lock. | Override Child 45-50 reopens durable identity and reads expected pin without a write-admission lock. | Durable identity/inventory/pin inspection only. Unlocked phase inspection does not admit worker writes. No provider restart qualification is implied. |
| `close`, 66-68 | Inherited. | Inherited. | Owner-controlled schema destruction. Outside concurrent worker admission; not authorized by packet preparation. |
| `install_capture`, 70-100 | Override CF1 95-108 calls base capture setup in a transaction, changes empty staged shape and installs exact pin plus initial PREPARING domain. | Inherits base owner capture setup; unsupported reuse is outside the reconstructed CF1 worker protocol. | Owner-controlled setup, not an admitted worker route or a durable writer guard. Capture implementation is unchanged. |
| `write`, 102-113 | Inherited. | Inherited. | Intentionally performs native/source mutation outside preparation admission. Capture remains unchanged. The worker barrier does not exclude this source-writer path. |
| `seed`, 115-119 | Explicit override CF1 140-144 opens a transaction and calls shared locked pin/PREPARING admission before base production. | Explicit override Child 52-56 does the same. | Admitted producer. No nextval/dirty effect precedes shared admission in these overrides. |
| `page`, 121-146 | Explicit override CF1 155-158 admits before inherited inventory locking/advancement. | Explicit override Child 58-61 admits before inherited inventory locking/advancement. | Admitted producer. Base 137 calls self.seed, which dispatches through each class's admitted override. |
| `claim`, 148-151 | Inherited. | Inherited. | Read-only dirty/source query; it neither retires tokens nor stages data. A claim does not itself authorize later installation. |
| `install`, 153-168 | Override CF1 160-183 checks operation, prepares keys, then takes shared locked pin/PREPARING admission before dirty-token FOR UPDATE and atomic frame staging/retirement. | Explicit override Child 63-65 immediately raises FixtureRouteUnsupported. | CF1 admitted installer; Child unsupported route refuses before any SQL/transaction call in its method body. |
| `drain`, 170-174 | Inherits read-only queue iteration and self.claim/self.install composition. self.install resolves to the admitted CF1 override. | Explicit override Child 67-69 immediately raises FixtureRouteUnsupported. | CF1's initial queue read is not write admission. Child never reaches inherited iteration or installation. |
| `finish`, 176-180 | Inherits read-only inventory check and self.page/self.drain/self.oracle composition. Preparation effects dispatch through admitted CF1 overrides. | Explicit override Child 71-73 immediately raises FixtureRouteUnsupported. | CF1 is an old foreground-schedule helper, not a closer, paused finisher or durable success certificate. Child never reaches inherited inventory reads or page production. |
| `oracle`, 182-195 | Override CF1 185-201 opens separate read-only observer, inspects pin, and compares native/source against independently decoded CF1 frames after scheduled writers stop. | Inherits plaintext observer, which names staged.v and is not a CF1 terminal verifier. | Inspection, no write route. Child schema incompatibility is not closure evidence. The approved closing path is not this inherited oracle. |
| `snapshot`, 197-199 | Inherited. | Inherited. | Read-only table inspection. Capturing or publishing returned raw rows is not authorized by this packet. |

## Additional paths required to understand dispatch

- Child `_require_pin` at 42 aliases the exact CF1 helper at 110-120. The helper selects operation identity, expected pin and phase together; lock=True adds FOR SHARE and requires PREPARING. The unlocked form permits inspection only.
- Child `install_presealed` at 75-97 checks operation and frame type, enters a transaction, and calls the shared locked helper before dirty-token locking, frame staging and exact-token retirement. V2 leaves this path unchanged.
- Child module `_child_worker` at 107-135 reconstructs and invokes install_presealed inside the acknowledged outer transaction. The nested installer context does not establish an earlier terminal COMMIT. The unchanged after_commit acknowledgement follows the outer transaction return. No worker was spawned here.
- CF1 `preparation_worker_barrier` at 122-138 selects pin/phase FOR NO KEY UPDATE, requires PREPARING and yields while its transaction is open. It is only the cooperative-worker barrier. It has no phase write, source lock, durable guard, paused finisher, publication or closure certificate.
- Fixture crypto helpers, process orchestration helpers and context-manager setup/teardown are not additional EnumerationLab methods. This inventory does not grant authority to invoke them.

## V1 finding and V2 disposition

The V1 source review correctly identified normal inherited Child install/drain/finish reachability outside shared admission. V1 successful inherited staging was never established: the plaintext ON CONFLICT clause refers to v after CF1 setup renames the column to frame. The provisional NULL/tombstone-success observation was explicitly corrected. No executed V1 bypass, successful phase transition or race is claimed.

V2 defines all five preparation methods directly on ChildFrameLab: admitted seed/page and immediate-refusal install/drain/finish. Each refusal method's only executable statement is a fixed FixtureRouteUnsupported raise. This resolves the exact inherited-route source objection without introducing plaintext CF1 staging or a PAUSED bypass. The independent V2 review reaches the same source-only conclusion.

Explicit base-class calls, arbitrary owner SQL, monkey-patching and unsupported setup reuse remain outside the cooperative protocol. No admission wrapper converts owner-only fixtures into deployment-wide writer exclusion.

## Checks and limits

The eight prepared source methods were not run. Their hard-coded base inventory detects a newly added base method if later executed, but does not automatically classify new subclass methods or prove arbitrary control flow. Selected AST/order assertions cannot substitute for native runtime schedules.

Durable closure, guard/runtime-role mapping, capture/handoff, rotation/provider authority and complete final verification remain open and approval-blocked. All seven gates remain UNKNOWN.

