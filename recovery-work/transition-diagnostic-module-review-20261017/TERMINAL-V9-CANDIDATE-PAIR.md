# V9 candidate and diagnostic pair acceptance

Disposition: ACCEPTED for genuine-module TransitionFailure constructor diagnostics and monitored preservation. Baseline and candidate were each selected once by root in separate processes. This audit only read source/evidence and rehashed admitted files; no target rerun, import or DB operation occurred.

Packet seal: `f25ab88131cf6d44385cef7294dd36b352c1bddabaf8eff90070854c6629fec0`.
Runner SHA256: `fef2d0c90d25622e704717f64cee9744be2835922e255eb08403a1409c41cf0c`.
Source review: `46103dd1457a2e6dd852c400d2728d9ceba2a3b5abb117ed530094b398af2425`.
Accepted baseline terminal review: `d3bf6661d146f2ed9c8dd2427c3456ef907d9d47bdceffcc302bf63170693300`.

## Actual candidate

Capture: `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/transition-module-candidate-v9-20261017-1433`.
Child exit0, outer aftercheck exit0, empty stderr, PASS_REAL_MODULE_DIAGNOSTICS, candidate variant, primary null,20 cases,644 preservation PASS and absent cache.
Stdout189068 bytes SHA256 `c974b4fa63736dee6753dcb802abe5527aca7477baad50ea536f155e5a4235b2`.

Baseline capture: `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/transition-module-baseline-v9-20261017-1429`.
Baseline stdout187620 bytes SHA256 `291747562a510534fc31aa703e4f532793d7dd1a59c250be336488bb64ffeb81`.

## Independently checked exact pair delta

Compared all20 candidate records against the previously independently reconstructed baseline records, using separately stated literal approved remedy strings. Exactly these six messages differ:

- operation_aborted:omitted_defaults
- operation_aborted:context_cleanup
- journal_identity_mismatch:omitted_defaults
- journal_identity_mismatch:context_cleanup
- database_effect_requires_inspection:omitted_defaults
- database_effect_requires_inspection:context_cleanup

For each, the sole difference is insertion of its exact approved remedy immediately after the existing common sentence and before any cleanup suffix. The operation_aborted remedy preserves the old journal/artifact and disclaims forward-successor integration. The identity-mismatch remedy forbids deleting/relabeling/replacing a journal to make a plan fit. The database-effect remedy distinguishes acknowledgement failure from rollback/completion and disclaims blind repetition or an implemented native ambiguous-COMMIT reconciler. Full strings match the sealed three-entry proposal exactly.

All remaining14 records are byte-for-byte equivalent as decoded field values: six existing remedy codes plus one unknown code, each in two argument forms. Every nonmessage field across all20 records is identical: ID, code, operation_id, sqlstate, cleanup_errors, effects and retry. Cleanup order and UNKNOWN formatting remain exact. The sealed runtime also checked exact class, RuntimeError inheritance and args before recording each case. Optional arguments are genuinely omitted in omitted_defaults cases; explicit-None variants were not separately exercised. Cleanup records are input data, not actual rollback/close operations.

Pair fact for packaging: 20 baseline constructor cases plus20 candidate constructor cases, with6 expected message-only differences and14 unchanged records. This is not40 distinct lifecycle scenarios, not a repeat of the prior extracted-class mutants, and not DB/native transaction qualification.

## Origins, wrappers and native bindings

All17 product and245 dependency origin pairs join exact admitted hashes. Candidate product paths equal baseline paths after only `/views/baseline/` to `/views/candidate/` substitution. All16 non-migration product hashes are identical. Migration baseline hash is `94344b2f98e0969d9f8b3d41cc9dca6e7d01a5e785a5b3af33431c41e55d2014`; candidate hash is `1d806f3f70ce9ae191871a75d372f7acdef4e35aaf7d63b0a8cbdadd03ade01b`. The runner checks the exact three-entry source delta before import and binds the actual module/spec/class/constructor filename to the selected view.

The245 dependency-origin records equal baseline exactly. The two deprecation-wrapper receipts equal baseline exactly: ciphers.algorithms and ciphers.modes, with pinned checked original-module origin and None wrapper spec. The four native names remain cython_runtime, _cython_3_3_0, _openssl.lib and _openssl; typing aliases remain typing.io and typing.re. Primary-null success after20 cases means the sealed postcase wrapper/raw/class/utils, native owner/lib/type, registry identity and origin/shape assertions completed. This is verified control-flow evidence, not independent memory inspection or native creator/build provenance.

## Closure and envelope

Reconstructed exact644-input union equals every reported PASS key:509 dependencies,86 views,43 originals and6 controls/seal. Independently metadata-admitted the whole set, read with O_NOFOLLOW and verified every hash, then checked all captured tuples unchanged. All91 packet members match the seal. Cache remains absent.

Candidate outer before/after six-control hashes are byte-identical, SHA256 `2a17db1bccf75e500a36a61a54f0fff6a163ab1ba4c1d373fd57d29260e912cf`; all six current hashes were independently verified. This set includes the accepted baseline terminal review in addition to packet seal, runner, source review, original final patch and Python. Metadata ledgers are identical, SHA256 `c4abf7abd99d89c7138c3b8041008e654c538ee2b5fe659313494ec69776ef4f`. Both91-member packet receipts match, SHA256 `0eae1f4f70912e9589b3ef57bc10a4983b4d418ec70b5914d7f72f7352e07087`. Child per-file runtime tuples are not serialized; its PASS ledger and this independent current audit are distinct evidence.

INVOCATION.txt762 bytes SHA256 `f4dd73a74083053ccf84325cbed0901f496b813b52a9ae8431dd2de7e94286f9` binds candidate, exact packet seal/cwd, selected Python, -I -B -S, absent pycache_prefix and clean four-variable environment including PSYCOPG_IMPL=binary. limits.txt802 bytes SHA256 `4648330265ce92518154458975457ffc7626ceeeaa0b893befb68880e92bafc9` records CPU30, VM1048576 KiB, file512 KiB, core0. Declared wall60/grace2 and stdin /dev/null match the accepted envelope. Output is below the256 KiB JSON and512 KiB per-file caps.

## Packaging scope

The three-remedy diagnostic proposal now has accepted baseline/candidate genuine-module constructor evidence in the declared same-host pinned509 profile. Preserve this pair, the source packet and all V4–V8 failed attempts. No further compatibility rerun is required by this result.

This does not adopt or publish the candidate into a selected artifact, qualify migration behavior, exercise a real transaction/pool/ambiguous COMMIT, call DB or application/key-provider APIs, or resolve broader UNKNOWN gates. Native OpenSSL provider initialization remains inside the explicitly trusted native-loader boundary. No native syscall sandbox, vendor provenance or complete linkage isolation is asserted.
