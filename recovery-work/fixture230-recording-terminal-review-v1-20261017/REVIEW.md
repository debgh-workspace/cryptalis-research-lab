# Independent actual fixture230 recording terminal review

Decision: ACCEPTED_RECORDING_19_ON_MATERIALIZED_230. Root selected the accepted invocation once; this reviewer performed only data inspection and hashing, with no rerun or target import.

Capture: persistence-recovery-20261013/fixture230-recording-v1-20261017. Both child and external aftercheck exits are 0; stderr is empty. Exact captured INVOCATION.json is byte-identical to the independently accepted admission packet, SHA256 26de90f91cbb80cdd85597b3a12cafc661b422b61f4ea8b34efa73945a6cab85. The runner seal remains 9879217a68b075b0868a35fa8a427f87f250cf9380a28687b8db4f707f1e9fbf. Source recipe review: recovery-work/fixture230-runtime-admission-review-v1-20261017/REVIEW.md, 5034 bytes, 510fb355cf8aa2be2da9e8f0d246487be93e7ecfa015a2fb7d035261d3a24b82.

## Actual cases and source binding

The complete report has status PASS_FIXTURE_HARDENING_RECORDING, variant combined, primary null, case_count 19 and admitted_count 863. Its ordered case records exactly match both the sealed literal driver and the prior accepted recording result:

- test_preflight_refusal_precedes_engine_or_mutation: indices 0–2, original bad_at values 0, 1, 3.
- test_successful_preflight_before_owner_engine: index 0.
- test_unacquired_schema_never_dropped: indices 0–1, create_collision and commit_ambiguous.
- test_owned_schema_cleaned_after_body: indices 0–2, None, RuntimeError and KeyboardInterrupt.
- test_full_fixture_acquisition_cleanup_boundaries: indices 0–9, owner_acquire, runtime_acquire, registry_acquire, mapping_setup, create, commit, create_all, runtime_dispose, mapping_dispose and owner_dispose.

Every record is PASS. The unchanged driver checks genuine pytest parameter declarations and invokes the original test functions and full fixture module directly. Their literal event assertions cover preflight-before-mutation, no cleanup after failed/ambiguous CREATE, acquired handle cleanup ordering and once-attempted disposal. This does not add a full exception-chain assertion or prove live PostgreSQL behavior.

The report binds manifest fa86e1917f631f8d7698faf444b993f412b27bf5ffa39e251392e91d7152c740 and actual materialization receipt e36828e3c95502e26d2cfaf0b45c031c387c2d404719683e39e9e4cebad0cd28. Source root is recovery-work/fixture230-materialized-v1-20261017/source. Its accepted actual-copy review remains 4673 bytes, SHA256 27ee27473795b95752d157192b16073b89fd3b15c37daf16544b3819403c0e09. All 230 source entries, including the 48-runtime map and both target tests, are admitted and preserved. Actual runtime loaded 23 product modules; admission of 48 runtime files does not mean all 48 were imported.

## Origins and continuity

Independently joined every final product origin/hash to the current materialized230 runtime map and every dependency origin/hash to the exact 625-dependency map. Observed final totals are 23 product and 353 dependency origins. Dependency origin records equal the prior accepted recording result. Native identities are exactly cython_runtime, _cython_3_3_0, _openssl and _openssl.lib; typing aliases are typing.io and typing.re. Two cryptography deprecation wrappers retain the checked original algorithms/modes module hashes and the accepted wrapper-spec policy. Their records equal the prior accepted result. Success follows the frozen runner's prebound identity checks and complete postcase sys.modules rescan; emitted native names do not independently prove vendor provenance or linkage completeness.

Reconstructed the exact 863 inner keys: 230 source leaves, 625 dependencies, six runner controls, runner SOURCE seal and actual receipt. Every preservation result is PASS and every expected digest agrees with root's concrete before map. Reconstructed the exact 893 outer keys from the sealed 887-path base plus admission packet four members/seal and independent source review; it exactly equals the captured before map.

All 893 external after rows have pass=true and final_metadata=true. Independent metadata-first current checks, bounded nofollow reads and a final full metadata pass verified every original seven-field identity and SHA256. No omitted or enrolled paths were accepted. Cache absence is reported true and the fixed bytecode path remains absent. The earlier startup HOLD stdout is still byte-identical to a6cfad8fbab3e8cde1fe47f418d3a24d9127ec1b9627163efdc051f0c7fb5eca.

## Limits, exact evidence and scope

Captured limits show CPU 30 seconds, virtual memory 1048576 KiB, core 0 and file size 512 blocks. Exact argv retains timeout 60 seconds with TERM and 2-second kill-after, canonical bash and inner env -i four-key reset before Python -I -B -S. These are process/per-file bounds, not a global descendant-absence or aggregate monitor claim.

Complete stdout is 235029 bytes, SHA256 1f0020b4b3b06a510ca4efd982edfe68a9cd4cf40d75abd903620d87f03bde77, below the 262144-byte report cap. Before receipt: 434728 bytes, d7b3658f169cc50ad0d7bf90779b821e4c490702ad47f05423138aeade57f185. After receipt: 188083 bytes, a894c3a750c750bea126b800dad891b0b575814756cbf3f240f66ce490c527bb. CHECKS.json retains exact hashes/sizes of all selected raw capture evidence; audit.py is the independent data-only audit.

metadata_validated, successor_authorized and mutants_repeated remain false. This is a fresh integrated230 recording-only 19-case result with genuine module imports and trusted host/native initialization. It is not a pytest session, native SQLAlchemy search execution, DB/ACL operation, full suite, installed-wheel test or package build. Public38 transfer and packaging retain their separate gates. No existing source, selected controls, failed capture or owned runtime was modified by this review.
