# Independent S25 packaging artifact audit

Verdict: PASS_INDEPENDENT_ARTIFACT_AUDIT.

Actual wheel SHA256:42150bab589fcb80083dafb8bd34186c5040776950fa1f5b04b11a43c1e3b36c.
Actual sdist SHA256:4800ce1a8e21685d063daf84882e36885759b2b30bcd3c3ad43c6a688b2299ba.

The independent standard-library data audit in audit_artifacts.py completed successfully and wrote ARTIFACT_AUDIT.json. It did not invoke the target verifier, imports, build backend, installer, test runner, DB or remote operations.

Rechecked all240 PACKET,3 outer,45 frozen-input,214 baseline,216 candidate and216 derivative manifest entries. Both build-copy scoped inventories exactly equal the216-file clean source and original candidate. Baseline artifact pins remain matched. Two sdist bytes are identical; direct and roundtrip wheel bytes are identical.47 sdist files and46 wheel payload files have safe unique paths; tar contains only regular files/directories and ZIP no encryption/special members. Extracted tree has no symlinks and matches every sdist byte/path. Tar member timestamps are0 and wheel timestamps1980-01-01 00:00:00.

Archive deltas exactly match the plan: only _sqlmodel_support.py and sqlalchemy.py change in the sdist; those two plus RECORD change in the wheel. No archive path additions/removals. All41 runtime modules equal clean source and sdist/wheel bytes. RECORD has46 unique coverage rows,45 valid SHA256/size entries and empty self fields. License and lock bytes match source; lock hash matches plan; original and normalized packaging configs match. Missing/altered lock rejection is retained in the successful verifier receipt, with unchanged reviewed implementation; this audit did not re-execute its negative controls.

Parent receipt status PASS_BOUNDED_PACKAGING, child exit0, no reason/errors/cleanup errors, leader reaped. Both complete integrity groups passed.120-second configured deadline,2MiB per captured stream and8MiB regular-file limit match review; original parent limits[-1,-1] restored. Captured byte counts/hashes independently match; all per-step stderr files empty; every run regular file within8MiB. Receipt does not provide elapsed wall measurement or independent descendant-absence proof; no such claims are made. Bounds remain cooperative per-child/per-stream/per-file, not aggregate quotas or hostile containment.

This clears the packaging artifacts for use in separately reviewed installer freezing. It does not authorize installation/runtime or establish installed provenance, independent-host reproducibility, dependency archive provenance, or any of the seven UNKNOWN qualification gates. Optional routing null binding must only be materialized in a separate finalized packet after its copied-environment audit and exact-command review.
