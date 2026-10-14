# Online closure: isolated source preparation

Status: PREPARED, NOT IMPORTED, NOT RUN. This is a partial experimental correction, not a reproduced bug or verified fix. No product source, installed environment, database, trigger, role, provider, remote or Git state changed. Coordinator alone owns promotion/execution. All seven qualification gates remain UNKNOWN.

## Exact new question

Can every cooperating preparation producer and stage writer be admitted only in PREPARING under the same operation-row SHARE lock, while a non-key closing lock can drain those workers without conflicting with capture foreign-key KEY SHARE? Source supports this hypothesis. PostgreSQL behavior has not been newly observed.

The retained D3/D4/D5 source has no closer, phase column or durable maintenance guard. It is therefore impossible to correct an existing final-catchup/switch method in this fixture. Product maintenance already has distinct writer-pause/full-verification/publication obligations; this candidate does not weaken or replace them.

## Candidate delta

Fresh derivative: candidate-online-closure-20261014. Base: candidate-accel-online-cf1-convergence-20261013, including its D5 exact source manifest. Two inherited files change; every other inherited byte remains identical.

- `_online_cf1_lab.py`: lab-only constrained phase column initially PREPARING; shared pin query also reads phase, and every lock=True admission rejects any phase other than PREPARING; explicit direct seed producer admission; a separately named preparation_worker_barrier holds FOR NO KEY UPDATE, validates identity/pin/PREPARING, then yields while its transaction remains open.
- `_online_cf1_process_lab.py`: direct inherited page and seed paths also obtain the common locked admission. The existing presealed installer already uses that helper. Its stage/retirement SQL is unchanged.
- No phase-changing function, source writer fence, guard, controlled paused finisher, publication, switch, trigger or history/WAL access is added. Barrier return does not claim closure. The phase column reserves PAUSED and PAUSED_VERIFIED names from the proposal but no code can legitimately produce those states yet.

The common helper's unlocked use remains inspection only. Reconstructing a paused fixture can inspect its pin; it does not admit any stage or inventory write. Key preparation still precedes database admission in the ordinary installer and does not extend a lease. No bypass parameter selecting PAUSED is exposed.

## Source path inventory

CF1 page -> locked pin/phase -> inherited page -> overridden seed -> locked pin/phase -> inherited seed. Direct CF1 seed has the same gate. CF1 install -> locked pin/phase -> dirty token FOR UPDATE -> stage -> token retirement, inside one transaction.

D4 page/seed now use the same admission; install_presealed already takes it before dirty/stage effects. Child reconstruction is read-only. The D4 spawn path reuses ChildFrameLab and therefore the same helper. Base EnumerationLab remains frozen and unqualified for direct use as a CF1 worker. Explicit base-class invocation and arbitrary owner SQL can bypass cooperative interfaces and remain excluded, not newly secured.

Capture inserts dirty rows referencing operation(id); it takes no explicit operation SHARE. No key columns change. FOR NO KEY UPDATE versus SHARE/KEY SHARE compatibility is the pinned PostgreSQL-source inference recorded by the proposal, not installed-server attestation.

## Remaining full closure objective, not optional scope

Before any closure claim, a reviewed actual closer must hold the operation non-key lock, drain admitted workers, acquire deterministic source locks, establish fresh READ COMMITTED visibility, install and verify the durable native/runtime writer guard, atomically set PAUSED, and commit. Reconnecting preparation workers must then refuse with valid dirty tokens still present. A distinct controlled finisher must drain byte-bounded residual work and perform full current native/source/independent-decoded membership, value, NULL, context and tombstone verification under the durable pause before recording PAUSED_VERIFIED. Failed/interrupted closure must preserve atomic guard/phase state; failed final work must retain PAUSED and stay unpublished.

The source fixture has only owner connections; the existing product guard explicitly depends on owner/DDL writer exclusion. A guard copied into this fixture cannot prove nonowner runtime reconnection coverage. The coordinator must establish how existing provisioned roles and reviewed guard semantics map to the fixture before implementation. No new credentials, role grants or trigger authority can be inferred.

Required inputs: explicit resolution of pending capture/handoff permission Sentinel_f9407ee631c081d1a92fb471b6262b6f; approved source-writer coverage and owner/DDL exclusion; exact durable guard reuse/installation boundary; admitted phase/finisher contract; unchanged final full-scan and separate external publication obligations. Fresh cluster, live provider, rotation and external qualification approvals remain separately pending. No near-zero pause budget or publication qualification follows from this work.

## Deciding evidence and fixed bounds

`test_online_closure_source.py` contains six source-structure methods, one with six path subcases. It reads/AST-parses source only; it never imports the fixture, loads a provider or connects to a database. These checks are prepared but NOT RUN. They can detect source regression in the intended gates/lock spelling and preservation of capture/oracle bytes. They cannot detect PostgreSQL races, deadlocks, transaction wait order, runtime guard behavior, stale snapshots, or complete closure. String/AST assertions are intentionally narrow and are not a substitute for the native oracle.

After independent review, the coordinator may decide whether to execute those source-only checks using the standalone file, outside candidate pytest/conftest collection. No new baseline run is requested. Omission mutations, if later authorized, must use additional isolated copies and retain all failed receipts.

Full future native packet is the existing proposal's eight groups: row-lock compatibility; pending native writer; stale normal/presealed workers with valid tokens; already-admitted worker commit/rollback; runtime reconnection; handoff rollback atomicity; paused restart/complete bounded drain; failure after durable pause. Reuse that packet rather than repeating D5 empty snapshots. Exact schedules and parameterized instances still need freezing after the missing closer/guard implementation exists. No sleeps/retry-until-pass; explicit terminal outcomes and raw stage/queue snapshots are mandatory.

## Retained evidence and checkpoint

D3 handoff: 24 cases per dependency cell; atomicity control and split-retirement failure retained. D4 worker process-loss: 12 cases per cell, research branch checkpoint 4135805673b2e7c9976959c4383bae39681d2eab, with encryption/provider supervisor surviving and acknowledged COMMIT boundaries only. D5: 10 cases per cell, JUnit 1.278/1.136 seconds, no closure authority. Recovery state's online checkpoint still points to D4; D5 manifest and local receipts are the exact later source/evidence basis. No unverified D5 remote commit is invented. Historical source/evidence remains unchanged and is not rerun.

The root checklist's latest bounded integration is S25, not this older research fixture. S25 serial installed tests are coordinator-owned. Current recovery state contains older descriptive fields alongside current S25 run markers; the authoritative checklist and actual evidence determine scope.

Source proposal: reviewer-notes/s24-related-online-repos-20261014/PROPOSAL.md and SOURCES.json. Prior boundary review: reviewer-notes/s23-online-followup-20261014/source-review.md. Contract: inherited docs/lifecycle.md maintenance, phases, full terminal verification and online-final-scan clauses. No public upstream code was copied.
