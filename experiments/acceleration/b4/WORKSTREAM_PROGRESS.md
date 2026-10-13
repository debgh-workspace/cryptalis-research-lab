# Legacy exit-reader safety derivative

Updated 2026-10-13 13:55 UTC. Coordinator alone executes PostgreSQL and publishes.

## Scope and provenance

Coordinator approved a separate complete retained legacy-safety derivative.
All 326 source files copied from frozen candidate-public-types-strict are
byte-identical. LEGACY_SAFETY_PROVENANCE.json records every original file hash.
Label: legacy-safety-b4-20261013. Packaging version remains 0.1.0; no packaging
assumption or artifact format is changed. This label is provenance, not product
admission. No mixed S14/S16 runtime module overlay is used.

Current legacy protection format cryptalis.transition/v1 and reverse staging
layout 2 remain unchanged. Historical assertions and their source remain intact.
Original legacy, frozen S15 bridge, B1 and B2 are unchanged. No database was
started or contacted by this worker. No credentials, cluster or role changes.
All seven production gates remain UNKNOWN.

## Concrete source finding and finite RED

The legacy deprotection._state validates its own reverse digest/layout/phase and
external pin but returns without checking the stored predecessor identity/digest
link or the predecessor's continued DEPROTECTING state. Later abort/remove checks
do not cover resume or the reverse row's source link. This is the same concrete
invariant as B2, not a new legacy layout interpretation.

The exact B2 test file is reused byte-for-byte (31 cases): six predecessor/link
faults across four genuine compiled reverse phases; four healthy reconstructed-
artifact resume controls; exact old-abort idempotence after a new reverse starts;
changed-link abort and active-removal refusal with exact snapshots, followed by
fixture-only exact link restoration and healthy recovery. Current native edits
and independently decoded public-root backup frames remain the oracles.

First run this file and the ten original tests/test_deprotection_ordinals.py
cases against the unchanged copied legacy runtime. Expected RED is a hypothesis,
not an executed result. Preserve the failing snapshot before adding the minimal
B2 check. Product artifact formats, ciphertext and plaintext layout, full verify,
source expiry, role handoff and publication semantics must remain unchanged.

Proposed coordinator-only selection through unchanged lab_session.py and
scripts/test_postgres.py:

    --candidate-root candidate-accel-legacy-safety-20261013 \
    --evidence evidence/b4-legacy-predecessor-red-20261013 -- \
    -q tests/test_reverse_predecessor_consistency.py \
    tests/test_deprotection_ordinals.py --tb=short -ra

Static compilation only is permitted for this worker. After RED, the candidate
must be unfrozen before any runtime or test change. No new proof is claimed by
historical ten-case legacy ordering results.

## Explicit current-target bridge prerequisite

Coordinator approved a new copy of the S15 parent/child experiment, parameterized
by a required explicit target source/interpreter pair. No bridge copy is added
yet. The coordinator must choose the final frozen qualified current successor;
S16 is not automatically selected while its ORDER BY review remains open.

The new child must be an independent process/package with complete installed
runtime module-set/byte equality to the selected target, using the unchanged
fresh dual-role preflight. Preserve explicit plaintext consent, current-data
edits, same table OID, full native values/order/types/indexes, package-free checks,
old encrypted backup reader and stale-restore refusal. Preserve the existing
role handoff exactly; no new credential, account or implicit reader admission.

Frozen source references (must remain unchanged):
- ../experiments/test_legacy_to_retained_bridge.py:
  de707a226f300b26896799a9f0ab7119e33537c4ba3a5d1694bc412cce7d7381
- ../experiments/test_retained_bridge_child.py:
  4cadd8e9b9c2d9a8f3d0ec09a1c9f4fe72d54b050a956709e7422c03d19ef166

No transparent online upgrade, automatic artifact conversion, new provider,
production recovery or complete legacy compatibility claim follows this slice.

## Confirmed RED and minimal defensive correction

Coordinator reports evidence/b4-legacy-predecessor-red-20261013: 26 FAIL /
15 PASS in 20.61 seconds, exact source archived and PostgreSQL stopped. All ten
historical legacy cases and five healthy B2 controls pass. The 24 inconsistent
resume cases and two changed-link abort/removal cases fail as predicted.

Applied only the exact B2 entry check to legacy deprotection._state, after the
existing ABORTED early return and phase/pin admission. An active reverse now
requires its original source identity/digest link plus a matching predecessor
row/digest in DEPROTECTING. Refusal uses existing source_state_changed. No repair
or phase interpretation is added; valid old completed aborts remain idempotent.

The separate legacy artifact formats, staging layout 2, migration runtime,
original assertions and package version are unchanged. Bridge files are not yet
added. Static compilation PASS. Frozen for the same 41-case coordinator gate.

## Corrected 41-case result and explicit-target bridge copy

Coordinator reports 41 PASS in 17.72 seconds; exact source preserved and server
stopped. This establishes the 31 predecessor/recovery controls plus ten
historical assertions for the selected legacy cell. It does not yet qualify
all crash/lost-reply or the new bridge target.

Added only new files under tests/bridge_lab. legacy_bridge_parent.py and
retained_bridge_child.py are opt-in filenames outside default test discovery.
The parent requires --bridge-target-source and --bridge-target-python; no
candidate name or interpreter default is inferred. The coordinator will select
the final frozen qualified current successor, presently pending S17 qualification.

A probe child runs the selected candidate's unchanged dual-role preflight and
checks its installed runtime before legacy fixture lifecycle work. The source
runtime module set, bytes, test helper bytes and runner digest are pinned. The
child requires exact installed module-set and byte equality, matching helper
origins, one installed cryptalis package for every loaded cryptalis module, and
the exact requested interpreter. Source and installed binding are rechecked
around child lifecycle work. Child logs and binding manifests get per-case names
in the coordinator evidence directory, so the text/VARCHAR cases cannot replace
each other's receipts.

The copied bridge retains the original two text/VARCHAR cases, explicit
plaintext consent, existing-role handoffs, current legacy edits, independent
old-frame decoding, encrypted dump/recovery, full native values/order/types/
indexes, same table OID, package-free operations, current target rejection of old
artifacts, and latest removed-pin rejection of an old protected restore. It is
still a maintenance plaintext bridge, not an in-place format upgrade.

Eleven source-only binding tests cover absent source/interpreter inputs, selecting
the legacy package as current, changed preflight, source/helper/runner drift,
and changed/missing/extra installed runtime modules. Their fake package fixtures
never launch an interpreter; actual installed-package proof remains in the child.

## Remaining finite gates and freeze

Python syntax compilation PASS for every new bridge file. No pytest or database
execution by this worker. All original 326 files still match provenance except
the one approved deprotection._state correction. Original ten legacy assertions
and frozen S15 files are unchanged. Bridge execution waits for coordinator's
explicit target/interpreter selection.

Recommended affected legacy gate before exit-reader qualification:

    -q tests/test_reverse_predecessor_consistency.py \
    tests/test_deprotection.py tests/test_migration_snapshot_boundary.py \
    tests/test_varchar_lifecycle.py tests/test_deprotection_ordinals.py \
    tests/bridge_lab/test_bridge_binding.py --tb=short -ra

Expected selection: 31 + 52 + 9 + 4 + 10 + 11 = 117 cases. This includes actual
SIGKILL at all five reverse phases, uncommitted second-batch death, seven lost
COMMIT-reply cases, exact prefix retention, old-abort/new-operation idempotence,
removal/backup/restore, stale snapshots, provider outage/expiry and VARCHAR native
semantics. Use both existing SQLAlchemy cells as the coordinator schedules them.

Explicit future bridge selection (two outer cases, each with isolated probe,
roundtrip and restored-old-database refusal children):

    -q tests/bridge_lab/legacy_bridge_parent.py \
    --bridge-target-source /absolute/path/to/qualified/current/candidate \
    --bridge-target-python /absolute/path/to/matching/installed/venv/bin/python \
    --tb=short -ra

Every runtime and test change is frozen for coordinator review/serial execution.
The target selector is not authority to accept a current policy or stale worker;
all existing lifecycle approval and publication guards remain in force.
