# Forward progress V2: independent terminal acceptance

Disposition: ACCEPTED ACTUAL RECORDING-CONNECTION / LOCAL-PROGRESS INSPECTOR RESULT.
Root selected the run once. This review parsed and hashed existing evidence only; it did not rerun/import/compile the target or execute SQL/DB work.

Capture: persistence-recovery-20261013/forward-progress-v2-20261017-1528.
Packet SOURCE.sha256: 96e0473ec83634c04402706fbae983dfc937338e1c5b97c0b531c2f4fa093ede.
Source acceptance: recovery-work/transition-diagnostic-module-review-20261017/FORWARD-PROGRESS-V2-SOURCE.md, SHA256 8f61bdf34af8880c5c0bda6497bf7f2053651cb31fb30d87e02b6b1046e0d866.
stdout:164447 bytes, SHA256 98b2db09594a54b575ecb4fecd8c5fc0ba7f429977be987e83e56152ece1ad64.
stderr:0 bytes. Child exit0 and external aftercheck exit0.
Terminal status PASS_FORWARD_PROGRESS_RECORDING_INTEGRATION; primary null; variant combined; cache_absent true; metadata_validated=false; successor_authorized=false.

## Exact oracle audit

Independently reconstructed all 68 ordered, unique case IDs from the reviewed literal source cases, without importing or executing them. The existing JSON has exactly one PASS record for each and no additional/failure record:
- 14 roundtrips for initial/partial/complete EXPANDED, BACKFILLED, VERIFIED, PENDING, ACTIVE, three ABORTED forms, empty VERIFIED, one above2**53 count, and signed64 minimum/maximum cursors.
- One serializer-only DEPROTECTING case and one canonical UUID cursor roundtrip.
- Three independent literal profile roundtrips and one exact literal profile-set contract.
- 40 fixed-code negative mutations covering counter exact types/inequalities, cursor canonical forms, table/member/context identity, unsupported profile/kind/codec, phase-specific members/completeness, verification and digest membership, and container/scalar subclass refusal.
- Six actual _state refusal controls: missing operation identity, ordinary ABORTED, wrong-pin ABORTED, stale ACTIVE, DEPROTECTING forward read and behind-pin state.
- Two actual _save refusals for rowcount0 and rowcount2.

Each positive executes the pinned genuine migration._save with exact SQL and operation/digest parameters into the recording object, decodes its JSON and asserts equality/input preservation. Successful actual _state paths use ABORTED allow_aborted=True/PREPARED, ACTIVE/ACTIVE, or other supported ahead-of-PREPARED states. DEPROTECTING is intentionally serializer-only and independently refuses forward read. Both marker-write failures require the exact TransitionFailure code journal_marker_write_failed and original operation ID, one recorded statement, unchanged input and decoded serialized equality.

Positive inspection asserts exact frozen/slotted scalar result, both false authority flags and unchanged inputs, then mutates separate copies to check no retained mutable state. Negative inspection requires exact ProgressShapeError/code/args and unchanged input. Existing terminal records retain fixed ID/status only, not SQL payloads, exception bodies or serialized state; these details are established by the sealed per-case control flow and PASS assertions, not reconstructed from nonexistent per-case raw receipts. No source-code mutant run is claimed; negative input mutations are actual cases.

## Closure and origins

Reconstructed the exact 560-key union:509 selected same-host dependency leaves,43 actual combined222v2 runtime leaves,seven packet controls and SOURCE.sha256. Terminal preservation equals that exact key set with all values PASS. Independently admitted all current finite files by ordinary-file metadata, then rehashed each with O_NOFOLLOW and required stable device/inode/mode/link-count/size/mtime/ctime tuples. All expected hashes matched. This current independent observation complements the sealed runner's before/after checks; runtime per-file tuples were not serialized and cannot independently be reconstructed.

All17 reported actual product origins join the actual combined222v2 runtime map; all245 dependency origins join the509 map. The target migration hash remains34ef8d914cdaf6f22c2297661fda7c04f16a83b71061be1ac5510a03caa6f33b. The two pinned local inspector/case module origins and function filenames are asserted before/after by the sealed runner; they are not separately dumped as an origin map.

Closed native bindings report cython_runtime,_cython_3_3_0,_openssl.lib,_openssl, with trusted typing.io/re aliases and the two actually loaded algorithms/modes deprecation wrappers. Primary-null successful control flow establishes completion of the existing identity/shape/owner relations and dependency-origin postchecks; this review does not independently inspect process memory or establish native creator provenance.

Outer five-file hash and metadata ledgers are byte-identical before/after; each current outer hash was independently verified. They bind the source seal, runner, source review, original final patch and exact Python executable. Seven packet-member check ledgers are byte-identical and all OK. Actual invocation uses the selected four-key environment, isolated/no-site/no-bytecode flags, exact packet cwd/cache path and source seal, stdin/dev/null. Limit receipt confirms CPU30s, virtual memory1048576KiB,file512KiB,core0; invocation records wall60s/grace2. The bytecode path remains absent.

## Scope and remaining gates

This qualifies actual Python _save/_state serialization/readback/refusal plumbing with an explicit recording connection and the isolated read-only local-progress inspector. The connection never reaches PostgreSQL; no transaction, commit/rollback, JSONB representation, row lock, native cleanup, catalog state, ciphertext access or recovery material was observed or changed. Synthetic opaque historical metadata stays unvalidated. Counter/cursor shape does not prove membership, cross-table reachability, authenticated provenance or current external authority.

The trusted same-host stdlib/native-loader and OpenSSL initialization boundary remains explicit; no clean-host, race-free confinement or vendor-provenance claim is made. No operational wiring was added and no successor/destructive action is authorized. All broader lifecycle/native/authority UNKNOWN gates remain unchanged. V1 and all earlier evidence are preserved; no repeat is needed for this accepted slice.
