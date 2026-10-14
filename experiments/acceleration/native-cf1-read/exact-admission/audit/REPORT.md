# Native read admission: independent preexecution review

2026-10-14. No blocking defect found for the declared finite scope. This is permission to consider execution under the coordinator's authorization, not an execution result or production qualification. No candidate import, native test, PostgreSQL, build, dependency installation, Git action or shared-product edit was performed by this reviewer.

## Frozen object

- cases.json SHA-256: a4b192bdaaa98124960efa0bedfb7c1a6417b318143555157068b03f23bb946e
- PINS.json SHA-256: 59a7e61da60f7df3eae1867bee5688040ebf9f9c8ee33df9a4802bd32a200e31
- 1,098 distinct ordered cases: 1,035 originals, 43 correction observations, 8 seals, 4 queries, 4 thread callers, 4 event-loop callers.
- 2,131 stdlib/static checks passed; detailed checks and reviewed source hashes are in verification.json.

Source freeze was coordinated with the author; candidate execution remained held during this review. Any subsequent source/manifest changes require re-review.

## Oracle and provenance

Original case inputs, fixture inventory and case order are preserved exactly. Original failure metadata/traces are preserved and strengthened with native-entry count and exception-argument/cause observations. Original success values are now exact text/type, reconstructed from public vector text or the original named fixture recipes. Static comparison of generate_cases.py confirmed grid, endpoint, nil and maximum-length recipes. Reconstructed values agree with historical byte lengths and digests. This is newly frozen exact-output provenance, not retrospective repair of historical chronology.

Correction cases retain their exact expectations and native counts, with exception checks added. Seal/query expected bytes come from fixed vector records, rather than executing the candidate to construct expectations. The seal path loads unchanged S20 source under a separate module name, constructs that module's descriptor class, and assigns only its own os reference. The fixed public nonce never replaces the shared os module or canonical cf1 module. There is no candidate seal implementation.

The recursive equality oracle compares complete dict keys, list order and exact Python types; missing or extra metadata and bool/int equivalence cannot silently pass. Success observations admit only exact str, bytes or NoneType. Byte results are serialized to hex with an independently checked bytes type tag. Failure metadata, nonempty string operation ID, canonical exception args, explicit cause absence, complete resolution trace and native-entry count are compared.

## Controls and shared state

Each of four named controls first verifies the unmodified observation, then changes only its selected downstream observation field (text, type tag, stage or trace). launch_all.py requires exit 1, FAIL, RuntimeError, exact mismatch message, verified original and no accepted positive observations. These controls demonstrate downstream oracle sensitivity. They are not native-return-channel, real exception-class or primitive fault mutants.

The runtime temporarily replaces the wrapper's native module reference with a counting/router shim, preserves the mapper, and restores the reference in finally. The shim calls the actual unchanged native function. Its PID/decode expiry actions are explicit research-only case hooks. Per-call data and counters use threading.local. Thread fixtures get separate key objects, while sequential correction cases intentionally reuse only their specified scope/lifecycle objects. Observed traces are deep-copied. No contamination route was identified within this schedule.

## Execution bounds and limits

launch_all.py runs each of ten finite cells in a fresh child process with a 180-second timeout; subprocess.run kills/reaps the child on timeout. A timeout receives a separate exclusive failure receipt. Thread startup has a 10-second barrier; normal executor shutdown joins workers. A blocked native call is ultimately bounded by the outer process timeout, not by ThreadPoolExecutor itself. The inspected runtime does not create child subprocesses.

The two event-loop tasks yield once and then invoke a synchronous reader. They verify two distinct coroutine callers, not overlapping async native execution, cancellation, task-local reentrancy or scheduler stress. Thread barriers align entry attempts; they do not prove native overlap or arbitrary interleavings, particularly with GIL-held native work. These limitations were confirmed with the author.

Fresh-process execution bounds shared module/router state to a cell. The isolated module retains its nonce stub until process exit; it is not the canonical module. Pin checks precede candidate imports and enforce source paths, runtime identity and backend strings. This is not provider-custody attestation, a proof against concurrent filesystem tampering, or complete dependency closure.

## Gates retained

No execution result is claimed here. Full DESIGN admission, timing, cancellation, resource/leak accounting, exhaustive failure branches, ABI/fork supplemental repair, operational-cause disambiguation, platform/provider custody, full source/security audit and product/backend qualification remain HOLD. No production or general concurrency claim follows from this finite review.
