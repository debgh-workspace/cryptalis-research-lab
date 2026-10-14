# Optional S20 source-release lock hardening

SOURCE ONLY, NOT RUN. Root authorized preparation; independent review and execution authorization are still required. Original S20 and its artifacts remain untouched.

## Exact delta

`source/` preserves all 208 non-cache S20 files. Only `pyproject.toml` changes, by appending a `[tool.uv.build-backend]` section with `source-include = ["uv.lock"]`. Original and derivative inventories are separately frozen. No runtime, requirements, test, license or lock bytes change.

This is an optional source-release self-containment improvement. Existing approved policy requires recorded locked inputs but does not mandate the lock be embedded in an sdist. The externally preserved lock already supports the narrower existing release packet. This work does not resolve the current installed-dependency-versus-lock discrepancies.

## Actual builder choice and evidence

Use the exact uv 0.12.23 executable SHA256 abdc39eab8b4ad341dca91f3823a23a343fae94bdb22ebdd9e91694415206f2f through its direct `build-backend` commands. This makes backend selection explicit: the backend is bundled in the same pinned binary, not dynamically resolved from the broad build-system range. Local uv distribution METADATA declares0.12.23; an execution-time `--version` check must agree. No claim of a locally available Rust backend source tree or source-to-binary provenance is made.

The cached standalone uv_build0.12.12 Python shims/binary are different artifacts and are NOT used. They must not be substituted. The original S20 logs say wheel-from-sdist; original generic launcher chose uv. This plan records its own exact builder rather than retroactively asserting original launch resolution.

`build-plan.json` freezes a clean allowlisted environment, fresh local HOME/cache/tmp, offline mode, UTC and SOURCE_DATE_EPOCH=0. Existing archive inspection observes tar epoch0 and wheel1980-01-01; that is not old launch-environment provenance. No inherited environment dump or credentials are read or recorded. A verified local Python executable is pinned for standard-library extraction and verification only; no distribution imports occur.

## Finite commands and stopping rule

`run-after-review.sh` is the exact proposed launcher. It refuses existing output, verifies pins, copies derivative source into two new roots, performs exactly two direct sdist builds, one direct wheel build, and one wheel build from a freshly extracted new sdist. It captures each stdout/stderr separately, then runs the artifact verifier and after-integrity checks. No package resolver, installation, downloaded build dependency, subprocess from package source, Git, database, or PostgreSQL test is requested. First failure stops, preserving artifacts/logs; no alternate backend or retry is authorized.

The direct backend is read-only with respect to source. Its exact proposed subcommand forms follow the available PEP517 shim's `uv build-backend` argument construction; execution has NOT yet checked them on this pinned binary. If refused, stop rather than changing the command silently.

Acceptance: new sdist bytes identical twice; exact lock bytes added; old/new source sets208 with only stated pyproject delta; sdist payload adds only uv.lock plus both rewritten/original pyproject changes; every other sdist payload member unchanged; direct/from-sdist wheels byte-identical to original S20; all40 module bytes, metadata/license and44 RECORD hashed entries unchanged. Two in-memory negatives independently remove or alter the lock and must fail for their exact reason.

No runtime tests are justified for unchanged wheels. Same-host packaging equality is not independent clean-machine reproducibility, signing, complete source-to-binary provenance, dependency drift repair or release qualification. All seven gates remain UNKNOWN.
