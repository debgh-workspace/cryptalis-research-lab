# Startup diagnostic source review

Date: 2026-10-15 UTC

No blocking source issue found for the two separately selected, finite diagnostic children. No execution was performed by this reviewer.

Reviewed packet: `experiments/preview-doctor-dx-slice-20261015/startup-diagnostic-v1`.

- `startup_probe.py` SHA256: `c5d5b86cbc1da6641ea3acced87d3cc436d72e5daab5b76e8a8066852dcd1ec1`
- `RUN_PLAN.md` SHA256: `31e7ee4cda70b339f269889adfe162ca36f6bf20ad54c82c336f43d2a6b4533d`

Both hashes match the stable handoff.

The source requires isolated, no-site and no-bytecode flags, the exact fresh bytecode-prefix path and one of two explicit modes. Invalid selection exits 2. It imports only `sys`, `json` and `os` directly and contains no product import, subprocess, explicit file write, retry or proof launch.

The two admitted launch mappings are exactly `{}` and `{"LC_ALL": "C.UTF-8"}`. Root must supply these fresh mappings without merging or inheriting its environment. The child reads its resulting startup environment to compute exact equality against the selected fixed map and that map plus known `LC_CTYPE=C.UTF-8`. It emits only sorted key names and two booleans. No environment values are emitted. This source review did not inspect an existing environment.

There is no unbounded application loop. The child relies on root for interpreter/source hash checks, exact command and working-directory selection, absent-prefix checks before/after, a five-second wall deadline and 16-KiB output bound per child. These are execution conditions, not properties enforced inside this short source.

Select one diagnostic at a time and retain stdout, stderr and actual exit. Accept the proposed locale explanation only if the two exact patterns in the run plan are observed. Any different output or process failure is HOLD. Do not change proof-v1 or its failure receipt. A corrected proof packet requires separate preparation, sealing, review and selection after both observations are accepted.

This review establishes source suitability for the narrow diagnostic only. It does not establish Python's actual startup behavior, a product RED/GREEN outcome or authorization to execute a proof variant.
