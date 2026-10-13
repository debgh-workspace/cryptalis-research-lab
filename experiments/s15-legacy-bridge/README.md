# S15: bounded legacy maintenance bridge

## Status and result

VERIFIED only for the owned synthetic Text and VARCHAR(64) fixtures, using the complete preserved legacy package and separate installed S14 interpreters. Two parameterized journeys pass per SQLAlchemy cell:2.1.3 in6.04s;2.0.51 in5.61s. The nested current interpreter runs its unchanged dual-role preflight too. Runtime source is unchanged; this is a compatibility/recovery experiment, not an automatic upgrade feature. S14 remains the integrated runtime.

Sequence: genuine legacy ACTIVE data with newer protected/public edits → explicit maintenance deprotection → distinct-role plaintext publication → actual package-free workload → legacy metadata removal → separately compiled S14 plan → retained-native protection and authenticated reads → S14 deprotection/removal → restore old encrypted legacy dump → reject that restore under the latest S14 REMOVED pin while independently decoding the retained backup.

Independent observations: current values, visible SELECT* names/order, native types/typmods/collations and index definitions match. Original table OID survives the transition journey; the final destructive test-fixture restore naturally creates new objects. Physical suffix attnums are not preserved by the legacy copy/drop mechanism. Both crypto layouts independently decode to expected latest values. Current package-free CRUD was tested before its removal; legacy package-free CRUD was tested both before and after its removal.

## Required boundary

- Exact version-pinned legacy source, its independently current ACTIVE plan/pin, keys and retained reader.
- Existing approved owner and distinct runtime roles; explicit fixture operator handovers use only those roles. No role/credential creation.
- Writer exclusion, snapshot draining and maintenance approval.
- Explicit plaintext-at-rest consent. Plaintext may enter WAL/backups; this is not online/transparent and makes no erasure claim.
- Legacy suffix admission remains strict: only its admitted text/VARCHAR columns and metadata. Do not strip comments, ACLs, constraints, indexes or dependencies to force admission. Generic legacy metadata repair remains open.
- Complete legacy removal is required before fresh S14 planning; never relabel artifact format/digest or combine modules from different package closures.
- A host must validate its real workload and retained backups before actual production removal. The synthetic test's attestation identifies a retained dump and already-verified reader; the physical restore occurs at the end and is not independently authenticated by the removal API.

The first child failed because the harness omitted the existing hide_parameters=True engine contract. Correcting the harness preserved the refusal; no product check was weakened. Initial failure logs are retained.

## Restore/run layout

Recover the S5 archive and verified S14 candidate overlay in an authorized lab. Keep legacy candidate-public-types-strict complete. Place the two archived experiment files in that lab's experiments/ directory (not one nested s15 subdirectory), matching the recorded original layout. Install the already-verified S14 wheel in a release-lab environment with the selected pinned dependency cell. Keep its candidate source at candidate-ciphertext-doctor-20261013 for byte-origin checks. Do not copy credentials into Git or provision a new cluster implicitly.

Run from the lab parent via its existing repo/.venv/bin/python and toolchain/lab_session.py, selecting --candidate-root candidate-public-types-strict and the appropriate S14 installed --python interpreter, with a unique --evidence directory and pytest target ../experiments/test_legacy_to_retained_bridge.py. The outer process uses the complete legacy source; current children discard that source path, validate installed S14 bytes and invoke the unchanged current scripts/test_postgres.py. One coordinator holds the shared lab session lock.

The S14183-file recovery remains unchanged. The two S15 helper hashes are in s15-source-manifest.json. Same-host helper byte recovery was checked; no fresh-machine/cluster restore claim is made. All seven production gates and the seven unchanged legacy-profile assertions remain open.
