# Supervisor attribution correction (2026-10-14)

The frozen V2 preparation describes supervisor_v2.py as a “verbatim copy” of the composition-control supervisor. That description is not an accurate identity claim against the current composition-control source and must not be used as transferred review clearance. The V2 files remain untouched.

Compared current files:
- This slice's frozen supervisor_v2.py: SHA256 e5e69f622989ba1815ed6e4b2cfd289a577764e8681c2e5aa439f00504849ef6.
- candidate-native-composition-control-20261014/supervisor_v2.py as read for this correction: SHA256 d7960256071bfe5a8a75f3453df0c3ebf51017a446ec1fd09d235088e9481c7c.

SUPERVISOR_COMPARISON.diff contains the exact current comparison. This slice's copy additionally retains cleanup errors for signals/reaping/pipe/selector cleanup, sets a cleanup-error reason when appropriate, and explicitly records descendants_verified_absent=False. It attempts process-group termination and reaps the direct child; that does not establish that every possible descendant is absent.

The creation command read the composition file and wrote these local bytes, but no separate contemporaneous source digest/revision was retained at the copy operation. Therefore this erratum does not claim a historically proven source revision or that today's other file equals the source as it existed then. The independently frozen local digest above is the authoritative identity for this slice.

Independent review must assess this slice's pinned supervisor implementation in its own right, including error receipt preservation and termination limits. No candidate execution occurred. The attribution correction changes no oracle, fixture, candidate code, cache, frozen manifest or historical outcome.

## Subsequent source reconciliation

The composition worker reported that its v2 filename briefly contained a correction, then the original v2 was restored and the correction was separately versioned as supervisor_v3.py. A fresh SHA256 and byte comparison independently verifies that the CURRENT candidate-native-composition-control-20261014/supervisor_v3.py equals this slice's pinned supervisor_v2.py byte-for-byte, with SHA256 e5e69f622989ba1815ed6e4b2cfd289a577764e8681c2e5aa439f00504849ef6. This reconciles the current source identity and explains the worker-reported filename history; it does not manufacture a contemporaneous historical digest. Review this local pinned implementation independently, or cite the exact current matching v3 digest rather than today's original v2 name.
