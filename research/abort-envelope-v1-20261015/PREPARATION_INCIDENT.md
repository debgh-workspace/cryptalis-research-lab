# Preparation incident: checksum list resolved from the wrong directory

On 2026-10-15, during source-only v2 preparation, the final read-only command
sha256sum -c ../SHASUMS.txt was invoked with working directory
experiments/aborted-successor-envelope-v1-20261015/correction-v2.

The v1 list contains names relative to its own parent directory. sha256sum
resolved those names against correction-v2 instead. The check exited 1 and
reported FAILED open or read / No such file or directory for:

- SPEC.md
- envelope_reference.py
- test_envelope_reference.py
- NATIVE_PROTOCOL.md
- JOURNAL_VALIDATOR.md
- INPUTS.md

This was a wrong-working-directory preparation error. It was not a hash
mismatch, permission denial, product execution, test run, database failure, or
evidence that any original file had changed. Earlier commands in the same
shell call successfully wrote/read the new v2 seal; no checksum retry occurred.

The worker reported the exact issue to root. Root then independently verified
all six original v1 leaf hashes against v1 SHASUMS.txt with SHA-256
4273ed617d0fd76d075e62f7648b8c721b705bc7fed059139e0a47deac5b472d,
and reported that all matched at 17:52 UTC. That result is root's independent
readback, not a worker retry. Root instructed continued sealed v2 source review
without execution and confirmed no new user approval was needed.

All original v1 sealed files and both v2 sealed deliverables remain unchanged.
This incident note is an additional preparation record, outside both existing
leaf seals. No product or execution claim follows from the incident or readback.
