# Durable inactive payload preparation: next isolated slice

Status: PROPOSED SOURCE DESIGN ONLY. No source, tests, database, provider, or Git changes were executed by this design pass. This document does not change a canonical product contract.

## Decision

Yes. A test-only PostgreSQL preparation/journal experiment can fit the existing approved host authority. The approved A4 lifecycle investigation already includes isolated rotation work; the selected lifecycle already requires one PostgreSQL journal, atomic chunks, inspected resume, and a separate deployment publication effect. The experiment below adds no policy acceptance or active representation switch. It uses only the existing coordinator-run PostgreSQL 16 fixture, existing owner/runtime roles, public synthetic key fixtures, and new test-owned tables. Root alone executes database work and decides integration.

No additional product policy decision is needed for that exact experiment. A passing experiment would establish durable **inactive preparation at one explicitly identified source revision**, not product rotation. Active generation admission/publication, changes to deployment authority, capture-backed online work, new roles or credentials, another cluster, real KMS calls, key retirement, and production execution remain outside this proposal.

The concrete next question is: after a process dies or a COMMIT reply is lost, can a fresh process inspect the original operation, reuse every committed ciphertext byte, and either prepare the remaining exact source prefix or refuse safely?

## Current evidence and important gaps

- The S20 base has 208 non-cache source/test/document files. This pass computed inventory SHA-256 dca9fc0d76ded56f5d0479bdb26abb2210105dfbc02c4ce2e76b80a952d7d952. The inventory algorithm and complete file map are in PROVENANCE.json.
- S20's crypto/_payload_rotation.py and its test file are byte-identical to the final B8 candidate. Module SHA-256: eb1117e9f03710bcd04d4139c181930102573c5f3de7f9167a7178c2660c295e. Test SHA-256: eb841213900dd279efbfcbc47c18c99e5fa714308f594f65e3aa335c71be481a.
- B8's final evidence records 114 affected tests passing in each dependency cell. Removing only the final binding check makes all six final-return expiry/PID controls fail in each cell. The historical 35-case scope description precedes the current 41 B8 cases.
- B8 authenticates exact source-generation frames, requires distinct payload roots/generations, preserves exact search context/material and terms, applies byte/row limits, and returns only a complete immutable batch. It performs no SQL or provider calls.
- B8's native test stores a complete result in an inactive table and checks current edited values. It does not journal chunks or prove process-death/lost-reply recovery.
- Existing migration._scope hashes membership, not source frame bytes. It cannot establish the source revision required here. Existing migration/deprotection phases, _state, _save and _executor accept operation-specific authority and schema contracts. Reusing them with fabricated protect/reverse plans would be incorrect.
- Existing process-worker and lost_commit_reply fixtures provide useful fault mechanisms. Their old outcomes do not prove this new experiment.
- All seven full production gates remain UNKNOWN. S20 still has its seven known legacy-profile failures. This design does not reclassify either fact.

## Narrow experiment boundary

1. One already-protected synthetic source relation, one selected protected field, and one exact tenant per operation. UUID and signed-int64 primary-key profiles are separate fixture cases. Storage-only and packed equality are separate cases. No multi-model rotation executor.
2. The source is created by the existing authorized fixture setup before the measured preparation operation. Its generation-1 application binding and original journal remain unchanged throughout preparation. The generation-2 policy exists only as an explicit inactive argument using public fixture roots.
3. A separate test-owned staging relation and one test-owned journal store ciphertext and nonsecret evidence. No plaintext, unwrapped key, provider credential, key-cache state, SQL bind value, or raw provider exception is persisted in these objects or diagnostics.
4. Reconstruct the local public fixture provider in each independently executed worker. Do not fork to inherit keys, serialize PreparedKeys, or write raw-root caches. This proves fresh-process functional preparation only, not external provider custody or fresh-machine recovery.
5. Root uses the unchanged lab wrapper, exclusive lab lock, and both role preflights for every run. A failed preflight stops the run. No alternative database or role is substituted.
6. The experimental source admits at most 64 selected rows and 4 MiB aggregate source-frame bytes. These are deliberate lab bounds, not a product limit or performance claim. Count and size checks occur under the same table lock before returning source frames. Per-batch bounds retain B8's stricter actual row/byte accounting and maxima. Tests use small multi-chunk fixtures.

## Proposed new files, in a fresh derivative only

- experiments/payload_rotation_journal.py: test-only operation artifact validation, source census, journal inspection, atomic preparation, and inactive terminal verification. Imports unchanged B8 and existing crypto types. No package exports, entry points, wheel inclusion, attachment hooks, or public migration API changes.
- tests/test_payload_rotation_journal.py: frozen native/failure oracles in TEST_MATRIX.md. Observes tables independently and uses an independent decoder/reference path rather than trusting the experiment's status result.
- tests/payload_rotation_journal_worker.py: independent executable worker, public fixture reconstruction, selected fault barriers, and safe bounded receipts. Receives a nonsecret operation artifact path; database access uses only the existing coordinator-provisioned fixture environment.

No executable file is supplied by this design pass. Root should first create the RED tests in a new source derivative; implementation follows the actual RED result. Preserve the complete 208-file S20 base.

## Artifact and authority inputs

Use a versioned, canonical, nonsecret preparation artifact kept by the test runner outside PostgreSQL. Its digest binds:

- Format and kind: an explicitly experimental inactive-payload-preparation format, never protect or deprotect.
- Random operation UUID; host-supplied target UUID; the observed existing database/role binding; exact source schema, relation OID and identity; selected field/descriptor/codec and tenant; native typed key ordering.
- Original source operation UUID, source plan/lock digest, externally supplied current source pin, and an exact digest of the original source journal row. The source pin is a fixture host assertion, not package-provided authentication.
- Exact source and target KeyPolicy fingerprints, including selected payload/search generations, provider IDs, root IDs, wrapper-context identities and sealed-wrapper hashes. The target policy is authorized for inactive preparation only. Root generation or policy publication is not an operation step.
- Source and target reader/descriptor identities and the pinned implementation inventory. A new process checks its loaded module origins and relevant module hashes against the supplied artifact. Do not treat a restored journal as the source of this expected revision.
- Scope definition, selected source membership/count/content commitment, source catalog commitment, original generation/search representation, configured row/byte bounds, and the test's explicit maintenance/pause acknowledgment.
- Exact journal/staging object inventory and expected owner/ACL facts. Names are bound identifiers, not SQL fragments.

The host supplies current authority inputs again for every start, resume, and terminal inspection. Compare them to the artifact before any target-row or journal mutation. A changed artifact using the same operation UUID refuses. A different operation UUID is not permission to adopt the old stage.

Do not use transaction ID, xmin, WAL LSN, wall-clock time, maximum key, or a human revision label as proof of the selected row version. They do not replace the exact content commitment below.

## Exact source revision and cursor evidence

A source revision is explicitly scoped to the selected field, exact tenant membership, native row identities, current source frame bytes/NULL, source metadata, and host authority inputs. It is not a global business-row revision or an authenticated freshness claim.

Under an EXCLUSIVE source-table lock, stream selected rows in native PostgreSQL primary-key order. Retain typed cursor values: UUID canonical strings decoded back to UUID, or canonical decimal signed-int64 values decoded back to int. Reject booleans, codec changes, mixed encodings, noncanonical cursor text and overflow. A NULL frame still has a real row identity and advances the cursor.

For each row, form a canonical nonsecret record with tenant UUID, record codec, canonical record ID, explicit NULL/non-NULL discriminator, and SHA-256 of exact non-NULL frame bytes. Hash the canonical record. Compute the source stream commitment over an explicitly length-delimited canonical scope header, the ordered fixed-length row hashes, and a final exact row count. Use existing canonicalization and hashlib; this is test evidence encoding, not a new ciphertext/cryptographic protocol. NULL and empty text never share the same record encoding.

Keep the whole-source membership/count commitment and content commitment separate. Rehash the complete bounded source on every resume and before every new batch, under the lock held through that batch's commit. This deliberate small-fixture cost avoids introducing persistent capture, revision triggers, online log permissions, or an unproved efficient freshness shortcut.

Any changed member, deletion, tenant move, source-frame rewrite (including a valid fresh reseal of the same value), descriptor, relevant source schema fact, original journal row, or current pin refuses the original operation. Do not rebase, reset the cursor, replace committed targets, or silently start a new operation. Changes to public fields are outside this field revision; the experiment never writes those fields and separately asserts preservation of the baseline source observations.

SHA-256 commitments detect disagreement under their collision assumption. They do not make a malicious owner/database authoritative or prevent an owner from consistently rewriting all evidence. Same-context replay/freshness and restore provenance remain canonical threat limits.

## One journal and one inactive staging relation

These are test-only tables, not a migration of the product _cryptalis_journal schema.

Journal logical columns:
- operation_id UUID and entry_number nonnegative bigint form the primary key.
- plan_digest is exactly 32 bytes.
- entry_kind is OPERATION for entry 0 or BATCH for positive entries.
- evidence is a strictly validated, versioned JSON object.

Entry 0 holds the exact operation binding, phase PREPARING or PREPARED_INACTIVE, expected source revision, derived progress summary, and any terminal verification receipt. Each positive entry holds one immutable committed-batch receipt: ordinal, cursor_before, cursor_after, ordered identity count/commitment, exact source row commitments, target-frame commitment, logical byte total, and declared policies/descriptor binding. A batch is never represented solely by a last key or count.

Staging logical columns:
- operation_id UUID, record_id in that profile's native UUID/BIGINT SQL type, tenant_id UUID, batch_number bigint, source_row_commitment 32 bytes, and nullable target_frame bytea.
- Primary key (operation_id, record_id). The operation has exactly one field/tenant; validate that identity explicitly.
- Validate ownership and effective ACLs. Runtime/PUBLIC must gain no stage or journal write/DDL/ownership access and no new grant is issued. Unexpected default grants or role reachability refuse; do not repair permissions automatically.

Fixture setup creates exactly the inventoried new objects and rejects a same-named existing relation. Object OIDs/definitions/owners/ACLs are subsequently checked. Do not search for and adopt a similar staging table. Do not create triggers, routines, extensions, new roles, or capture infrastructure.

The original active source journal row, source frames, source indexes/constraints/triggers/owners/grants, original deployment pin, and active attachment configuration are read-only throughout this operation. Whole-schema evidence reports the two intentional new tables rather than pretending that no catalog object changed.

## State machine and transactional algorithm

PLANNED is only the outside-database artifact. Persisted phases are PREPARING and PREPARED_INACTIVE. No ACTIVE, ACTIVATING, PENDING-publication, switch, contract, retirement, or accepting-successor phase exists. Errors are observations; do not overwrite good progress with a fabricated success/failure phase.

1. Validate artifact/current host inputs and loaded revision. Open a dedicated existing-owner connection with parameter redaction, finite lock timeout and synchronous_commit on. Reuse the existing connection cleanup discipline; invalidate/close the physical session so a session advisory lock never returns to a pool.
2. Acquire the existing cooperating maintenance advisory-lock identity for the one source table's model set. The key must not include operation UUID, so a second operation over the same scope cannot bypass it. This serializes cooperating local executors only. Do not reuse migration._executor by constructing a fake MigrationPlan.
3. Begin a transaction, acquire the source-table lock, and inspect bound catalog/role/current-source facts. Check complete source count/size before fetching frames. Recompute its exact source revision. Startup authority and writer exclusion remain explicit host responsibilities; the table lock does not survive process death.
4. For a new explicitly requested start, create the operation entry only when all expected objects and identities match and no operation row/stage exists. A resume requires the original operation entry. Missing or one-sided restored operation state refuses; it never self-authorizes reconstruction.
5. Independently inspect all committed batch markers and staging rows. They must form the exact contiguous prefix of the current source under the artifact's batch bounds: first cursor absent, each next cursor equal to the previous end, exact member/order/count, exact source commitments, exact recorded target commitments, no orphan rows/markers, no duplicated/reassigned members and no phase/counter discrepancy. Reauthenticate the stored target frames with fresh admitted fixture keys and compare decoded values and exact search header/terms against the source. Never call seal for an already committed member.
6. Select only the next ordered bounded prefix. Source-frame size selection happens before payload transport; a first row that cannot fit refuses instead of appearing as end-of-stream. Pass an immutable tuple to unchanged B8. Validate its full returned identity list and all policy/descriptor binding again.
7. Recheck both prepared-key bindings before target DML. Insert all inactive target rows, add their BATCH entry, and conditionally update entry 0 from the exact inspected progress. Require the expected affected-row counts. Repeat the existing private binding check immediately before the explicit commit. Any SQL, crypto, expiry, PID or receipt-validation failure rolls back this whole chunk. Earlier committed chunks remain exact.
8. Commit one chunk. A lost or failed response is UNKNOWN until fresh inspection, even if an internal counter had advanced. Successful stream output is not durable evidence.
9. When the next prefix is empty, perform a full locked terminal scan. Prove exact source/stage membership in both directions, all row values/NULLs, exact target generation, unchanged search terms/representation, correct descriptors, journal/stage consistency and unchanged original source binding/catalog. Then update entry 0 to PREPARED_INACTIVE with its exact verification receipt in that transaction.
10. Return an explicitly inactive receipt only after its commit succeeds. Repeated terminal inspection revalidates current source and stored targets before returning the same receipt; a later changed source is a mismatch, not proof that the earlier preparation remains current.

The final local lease check is a process-side observation, not an atomic guarantee about a later server COMMIT timestamp or instantaneous provider revocation. No key is used after expiry. A committed target ciphertext stays inert if its prepared-key lease later expires. Fresh inspection renews material only by an exact provider-backed preparation of the same allowed policies, never by extending an old PreparedKeys deadline.

## Crash and lost-reply classification

- Before a chunk commit: a dead session's transaction rolls back. After the original backend/transaction is terminal and the scope lock is acquired, the previous marker prefix is still the authority for inspected progress. Absent next marker plus no next target rows permits preparing that uncommitted next chunk again. Its new ciphertext may differ because the uncommitted bytes were never published.
- After a chunk commit or a discarded COMMIT reply: matching marker plus exact stored target/source evidence means reuse the committed bytes. Prove with a seal-call spy that resume does not reseal that prefix.
- Original transaction still live: the same session advisory lock cannot be acquired. Return a pending/inspection-required outcome. Marker absence cannot establish rollback. Never forcibly terminate another process to make the outcome convenient.
- Marker and rows disagree, source revision differs, current target identity/pin is unknown, or journal format is unsupported: refuse dependent writes and retain evidence. Do not repair/delete/recreate state automatically.
- Crash after terminal commit but before output: fresh inspection returns the same PREPARED_INACTIVE receipt after revalidation. It never activates generation 2.

The trusted-current-primary and PostgreSQL durability assumptions remain explicit. This does not claim global exactly-once execution, failover-loss recovery, forged-journal resistance, deployment-wide writer exclusion, or cross-service atomicity.

## Safe failures and observations

Use existing sanitized TransitionFailure/CryptoFailure boundaries or an equally safe experiment-local typed wrapper. Proposed stable experiment codes include preparation_source_revision_changed, preparation_identity_mismatch, preparation_journal_inconsistent, preparation_unknown_layout, preparation_source_row_too_large, preparation_executor_busy, and preparation_outcome_requires_inspection. Preserve actual SQLSTATE when available; never include row values, frame bodies, terms, URLs or raw provider text.

Every failure receipt names the original operation, attempted batch, last independently observed committed prefix, whether the original transaction is terminal/unknown, and the next safe inspection. A failure or broken output channel does not become a successful partial preparation. Cleanup failure is additional evidence and must not hide the primary failure.

## Completion and next authority boundary

The experiment is complete only when the finite matrix passes on SQLAlchemy 2.1.3 and 2.0.51 through unchanged existing-role preflights, committed-prefix bytes survive fresh-process resume, deliberate omissions make the relevant oracles fail, source/runtime files and active bindings remain unchanged, and root has reviewed the exact receipts. No benchmark target is included.

A later product slice would still need a reviewed operation artifact integrated with the canonical single journal, maintenance writer exclusion, active generation/reader admission, full source-target/constraint proof, separately authorized database/deployment publication, current-data compensating rollback, and retained-backup/provider evidence. Do not infer permission for any of those effects from PREPARED_INACTIVE.

## Source references

- Base docs/lifecycle.md: Maintenance and ownership; Plan and phases; Changes and rotation; Restore and authority loss; Recovery behavior; supported deployment candidate.
- Base docs/security.md: trust boundaries; provider/policy custody; public failure contract; threat limits.
- Base docs/decisions.md: selected journal/lifecycle/current-authority choices and owner amendment A4/A5.
- Base src/cryptalis/crypto/_payload_rotation.py; tests/test_payload_rotation_preparation.py.
- Base src/cryptalis/migration.py: _policy, _connection, _executor, _state, _scope, _backfill_chunk; src/cryptalis/deprotection.py: _state predecessor binding.
- Base tests/migration_commit_proxy.py and tests/test_migration.py: terminal lost-COMMIT-reply and independent worker controls.
- Final B8 candidate B8_PAYLOAD_PREPARATION_SCOPE.md and B8_FINAL_BOUNDARY_PROVENANCE.json.
- persistence-recovery-20261013/b8-final-boundary-results.json; root CRYPTALIS_BUILD_CHECKLIST.md current S20 and pending-authority entries. Their exact inspected hashes are recorded separately.
