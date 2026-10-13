# B7 final evidence and next executable rotation prerequisite

## Verified B7 result

- SA21: 6 PASS in 3.97 seconds; SA20: 6 PASS in 3.35 seconds.
- Each source-path gate has four new policy-drift/recovery cases and two unchanged controls.
- Candidate import origins, unchanged dual-role preflights, all recorded source/test
  hashes, exact JUnit cases and successful shutdowns were independently rechecked.
- All 204 inherited S19 files and 39 runtime modules are unchanged.
- Test SHA-256: `22c0d97956346dd606abdf1de88e1d605917741868b3f0fe45aeeaa6f188eeb5`.
- Safe receipt SHA-256: `55ddf18802eb194e5ca340933ffb465d1189550ee4cc841c4b54fb6ed0f7715e`.

A changed payload or search policy after a committed reverse chunk is refused
before its provider is used or further SQL is emitted. Exact current ciphertext,
native catalog facts and journal state survive refusal. Original-policy resume
preserves the durable prefix; abort retains current values and permits another
application edit before a fresh fully verified reverse. Original retained frames
remain readable with their original public-fixture reader.

This proves existing reverse-operation safety. It does not implement rotation.
The interruption is a typed policy refusal between commits, not new crash or
lost-COMMIT evidence. Catalog comparison covers recorded trigger definitions and
enabled flags, not function-body bytes. Seven historical legacy-profile failures
and seven UNKNOWN production gates remain unchanged.

The frozen candidate preparation notes retain their historical PENDING wording;
this final note and the receipts supersede it only for this six-case gate. No
frozen candidate file was edited and no test was rerun during receipt review.

## Next actual executable prerequisite: inactive payload re-encryption

The next slice should produce real replacement CF1 frames, rather than add more
refusal-only tests. Proposed scope, subject to coordinator review before edits:

1. Add one private, side-effect-free payload-rotation batch preparation function
   in a NEW S19-derived candidate. It receives immutable expected row contexts,
   current source frames, explicit source/target policies and a byte budget.
   It reuses the existing authenticated decoder and CF1 sealing primitives.
2. Admit exactly a payload-generation transformation. Domain, tenant, field and
   record identity stay fixed; the search root, search generation and equality
   terms stay exact. Validate the intended source generation even when a reader
   inventory also includes historical generations. The new payload root must be
   distinct and explicitly selected; headers cannot select custody.
3. Authenticate and decode each current source value, then reseal with the target
   payload generation and fresh nonces. Return an immutable **inactive batch**
   only after every item succeeds. Inputs and retained backup frames remain
   unchanged. Bound input/output/decoded logical bytes and preserve existing
   lease expiry/fork/provider-failure rules; never extend a source lease.
4. Establish independent target-frame correctness for storage-only and equality,
   NULL/empty/Unicode, both admitted record codecs, and multiple tenant contexts.
   Assert changed payload generation, exact unchanged search terms, and exact
   independent decoded values. Inject a late bad source frame and source/target
   expiry: neither may yield a partial batch. Test a changed current target value
   transformed back with explicit prior reader material so a stale snapshot
   cannot satisfy the expected value. This is local transformation feasibility,
   not rollback authority or crash-atomic publication.

That is engineering within the approved separate rotation work, using public
synthetic material. It requires no active policy, grant, credential, provider
service or new host authority. Exact validation/API shape needs review before
implementation; no new runtime file has been written by this task.

## Remaining path to complete rotations

Inactive batch preparation alone is not the objective. The following integration
work remains explicit: operation-bound source/target artifact and reader inventory;
reuse the existing durable journal/maintenance exclusion for atomic shadow rows
plus progress; real interruption/lost-reply resume preserving committed target
bytes; full native/current-value and metadata verification; compensating rollback
from current post-switch data; then the separately approved database/pin cutover.
Search rotation is a distinct subsequent implementation: new terms and indexes,
resealed authenticated headers, exact query/uniqueness parity and no mixed-generation
uniqueness gap. Root rewrap remains a third separate workflow.

The only host-choice blocker at publication remains the concrete existing release
operator/system and its enforceable old-worker termination/reconnect exclusion
procedure. Required proof covers both switch boundaries, interrupted publication,
stale pins and uncertain-effect inspection. Do not invent a permanent token/trigger
authority, revoke old backup readers, or infer credential permission to remove that
blocker. Actual remote-provider behavior and independent security review remain
separate qualification requirements.

## Recovery overlay

The four-file plan contains the unchanged new test, full base provenance, safe
combined receipts and this final note. It is not a standalone source archive.
Restore all 204 S19 files against B7_PROVENANCE.json before adding the test. The
original B7_ROTATION_PREREQUISITE.md and WORKSTREAM_PROGRESS.md remain frozen in
the local candidate; their scope is summarized here. No runtime module changes.
