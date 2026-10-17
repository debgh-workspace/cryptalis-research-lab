# V9 genuine-module baseline: terminal acceptance

Disposition: ACCEPTED for the selected baseline's 20 TransitionFailure constructor diagnostics and monitored preservation only. Root ran this baseline once. This independent audit performed no product/module execution or rerun. Candidate remains separately selectable and unproven.

Capture: `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/transition-module-baseline-v9-20261017-1429`.
Packet SOURCE seal: `f25ab88131cf6d44385cef7294dd36b352c1bddabaf8eff90070854c6629fec0`.
Runner: `fef2d0c90d25622e704717f64cee9744be2835922e255eb08403a1409c41cf0c`.
Source review: `46103dd1457a2e6dd852c400d2728d9ceba2a3b5abb117ed530094b398af2425`.

## Actual result and exact oracle audit

Child exit0, outer aftercheck exit0, empty stderr, PASS_REAL_MODULE_DIAGNOSTICS, variant baseline, primary null, case_count20. Stdout187620 bytes SHA256 `291747562a510534fc31aa703e4f532793d7dd1a59c250be336488bb64ffeb81`.

Independently reconstructed and compared all 20 complete JSON case records, including IDs, full literal messages, operation/sqlstate, cleanup arrays, effects and retry. The ten codes are operation_aborted, journal_identity_mismatch, database_effect_requires_inspection, six existing remedy codes and unknown_diagnostic_code, each with genuinely omitted optional arguments and with fixed context/two cleanup records. The three proposed new codes correctly have no remedy in baseline; all six old remedies and the unknown fallback are exact. Cleanup order and UNKNOWN formatting are exact. The reviewed runner also asserted exact exception class, RuntimeError inheritance and args before appending each record. No sensitivity mutants were repeated.

This does not add explicit-None constructor variants: omitted-default calls are genuinely omitted, while the context form supplies fixed values. No actual rollback/close operation occurs; the cleanup records are constructor input data.

## Actual loaded bindings and postcase checks

All17 product and245 dependency origin records join exact admitted path/hash entries. cryptalis.migration is bound to the V9 baseline view and SHA256 `94344b2f98e0969d9f8b3d41cc9dca6e7d01a5e785a5b3af33431c41e55d2014`. The reviewed runtime checks enforce real selected module/spec, class module and constructor filename. These are genuine module constructor cases rather than AST extraction.

Exactly two deprecation wrapper receipts occur: cryptography.hazmat.primitives.ciphers.algorithms and cryptography.hazmat.primitives.ciphers.modes. Each records its pinned original-module path/hash, checked_original_module ownership and wrapper_spec_is_none=true. The other two allowed static callers were not enrolled or imported by the checker. A primary-null success after all20 cases entails that the reviewed postcase utils/class, wrapper/raw identity, registry and shape/origin assertions completed.

The four embedded native names are exactly cython_runtime, _cython_3_3_0, _openssl.lib and _openssl; trusted typing aliases are exactly typing.io and typing.re. Success entails that their reviewed initial and postcase identity/shape checks completed, including the pinned extension-owner/raw-lib relation and actual type(lib) check. The report does not serialize object addresses or complete object state; this is control-flow evidence from the sealed runner, not independent memory inspection or native-creator proof.

## Exact preservation audit

Reconstructed union of509 dependencies,86 view leaves,43 originals and6 controls/seal equals all644 reported preservation keys, each PASS. Independently performed complete current metadata admission, O_NOFOLLOW hash reads and a final stable-tuple comparison; all644 match their expected hashes with unchanged metadata. All91 source-manifest members verify. Cache path remains absent.

Outer before/after five-control hash ledgers are byte-identical, SHA256 `bf149ec72ead838f445c4c11ded42d2926e87f390d3d25f471a6cd01746bf5f2`, and all five current hashes rechecked successfully. Outer metadata ledgers are byte-identical, SHA256 `bb51c700d51eadabcd2862af0c9a50d0b8e2b103c94fa5269caf890b88965614`. Both91-member packet receipts are identical, SHA256 `0eae1f4f70912e9589b3ef57bc10a4983b4d418ec70b5914d7f72f7352e07087`. Child runtime per-file tuples are not serialized; its PASS ledger is distinct from these outer tuples and the independent current audit.

INVOCATION.txt761 bytes SHA256 `72e22be319ea21a03ff8a4981426621fc3168f377e21f8e3414289a1dc0b6bda` binds exact V9 cwd, baseline seal, Python, -I -B -S, absent pycache_prefix and only LANG/LC_ALL/TZ/PSYCOPG_IMPL=binary. limits.txt802 bytes SHA256 `4648330265ce92518154458975457ffc7626ceeeaa0b893befb68880e92bafc9` records CPU30, VM1048576 KiB, per-file512 KiB, core0. Invocation declares wall60/grace2 and stdin /dev/null. Stdout is below both the256 KiB runner JSON ceiling and external512 KiB file ceiling.

## Next separate selection and limits

No baseline rerun is needed. If root selects candidate, use the same sealed V9 packet, host/environment/cwd/flags and outer bounds with only variant argument `candidate`, a fresh capture, renewed before/after admission and this accepted baseline kept immutable. Compare candidate's20 records with baseline: only the six records for the three new remedy codes may gain their exact approved remedy text; remaining14 records and all other fields must agree.

Scope remains the three-message diagnostic proposal under the existing trusted same-host stdlib/native-loader boundary, including native OpenSSL initialization. No DB, real transaction/pool behavior, migration executor, application/key-provider API or lifecycle scenario was exercised. No vendor provenance, syscall confinement, complete native linkage or resolution of the broader UNKNOWN gates is established. Preserve all V4–V8 failures as historical evidence.
