# Independent V11 runtime first-attempt audit

Decision: HOLD, setup/import failure before product import or test collection. Closure evidence is accepted; no correctness result is accepted. No rerun was performed by this reviewer.

## Binding

Runtime derivative: reviewer-notes/tenant-fastpath-v11-runtime-supervisor-v1-20261017, SOURCE seal 4bea837a9301b44d1403e8bd069ea939bc6d714137b8fc048c364239283d5727. All three source members were rehashed and match. External attempt: attempt-001; outer envelope: outer-001.

V11 packet: experiments/tenant-fastpath-no-db-packet-v11-20261017. PREPARED remains 0ee0e251481d6bd01e5eda6dbf67e3e568c25ed643570c565c635ae3fdc2f7a2; ALLOW remains 17413de2a8f341f221355e288b1fef3d0e8f759912d5dfbd0366be93d18cbb17.

## Distinct failures

1. Primary child setup failure: ImportError, “unadmitted module origin or namespace package: importlib.resources.readers”. The traceback runs from harness/run_correctness.py's import pytest through _pytest/assertion/rewrite.py. The exact origin finder refuses that module. No missing host body was read by this reviewer.
2. Secondary child final-origin failure: AssertionError, ('missing_spec', 'typing.io'), raised by module_origins in child.py's finally block while handling the first exception. Both errors survive in chained stderr, but the second becomes the child's terminal exception. It must not be substituted for the primary setup diagnosis.
3. The external supervisor reports primary_failure=AssertionError when its own successful-child assertion rejects child exit 1. This generic supervisor classification is not evidence of a product assertion failure.

Pinned harness source places import pytest before import cryptalis.sqlalchemy, other product imports and collection. The traceback therefore supports pre-product/pre-collection failure. There are no case results or differential conclusions; 468 remains a declaration, not an observed count.

## Actual attempt and cleanup

Only SA20 baseline correctness was selected. Its exit is 1; no SA20 candidate, reducer, SA21 child or later step ran. The child receipt reports leader observed before cleanup, owned-group cleanup before reap, ownership_lost=false, received_signal=null and no cleanup errors. The in-memory child history exactly matches that receipt. Outer receipt reports supervisor_exit=1; external TERMINAL is HOLD.

Stdout is 13,250 bytes containing exactly one BOOTSTRAP_ORIGINS_JSON line, with no DIFFERENTIAL_JSON or collection report. SHA256 d194daf24d5bbf323c8f369bbe72c19bbda2822a8ff19d2c556564142a4feae0.
Stderr is 2,719 bytes containing the two chained errors above. SHA256 22dc3e1eba08090a7916fed231eb49bb634e0ec7b0adb6ed0fda3730a896637e.
Combined capture is 15,969 bytes and agrees with the child receipt.

## Independently checked preservation

Reconstructed the runtime monitored union from accepted PREPARED original_inputs/closure, PREPARED/ALLOW controls and exact external SOURCE members. BEFORE.json and AFTER.json have exactly the same 5,411 expected identities; every metadata/hash entry is PASS and every before/after stat tuple matches.

Freshly metadata-admitted the entire 2,566-file materialized input/control set before rehashing its bodies. All digests still match the accepted map. Independently checked full output namespace using only declared directories: exactly those 2,566 leaves plus four results leaves (sa20-baseline.json, .stdout, .stderr and CLOSURE_FINAL.json). No extra directory or leaf was accepted. External and output CLOSURE_FINAL.json agree, contain exactly one child history, report unchanged=true, no closure failures and PASS for all five copied branches.

Bytecode prefix, python312.zip, PREPARE_FAILED.json and results/RESULT.json are absent. No accepted materialized input or sealed source was changed. Original host/donor live bodies were not reread; their complete before/after execution receipts were independently audited.

## Next boundary

Preserve this failed attempt, V11 materialization and all sealed sources. A successor needs separately evidenced, finite admission for required missing stdlib origins and an explicit policy for legitimate synthetic aliases such as typing.io, grounded in accepted source rather than blanket missing-spec permission. Child error handling should retain primary setup/test failure separately from final-origin failure. Neither this diagnosis nor closure acceptance authorizes guard relaxation, another run, additional unknown-body reads or a correctness/performance claim.

Review used inert source/control/receipt reading and finite actual copied-file hashes. No target runtime/product execution, test, DB or Git action occurred during this audit.
