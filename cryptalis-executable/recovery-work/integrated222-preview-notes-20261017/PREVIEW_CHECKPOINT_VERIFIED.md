# Combined222 preview checkpoint

Status as of 17 October 2026, 15:56 UTC: a reproducible, privately recoverable wheel with narrowly tested installed behavior. This is an additional checkpoint; it does not replace the previously selected preview or authorize production use.

## Artifact identities

- Wheel: `cryptalis-0.1.0-py3-none-any.whl`, 141,600 bytes. SHA256 `898e2548a0943d3d718aec7e2c2346d434b3131ef68c1cfe243ae9b7d8a390c8`.
- Source distribution: `cryptalis-0.1.0.tar.gz`, 151,115 bytes. SHA256 `1d647b06f61550b2220937c4642926b91ff16afb3ef5be3a031d23c2b4084a9c`. This artifact is local only; its upload remains unapproved.
- Full source composition: 222 files, 4,469,599 bytes. Manifest SHA256 `486f900e78cf426f33a5fba71a8d4e992657572c5af10254ec7602c0c707ae5d`.

Version remains 0.1.0, so use the full wheel hash and checkpoint path to distinguish this build. Relative to the preceding diagnostic wheel, runtime changes are confined to `cryptalis/manifest/compatibility.py` and `cryptalis/migration.py`, with the corresponding RECORD update. The changed documentation and added regression test remain in the full source composition; they are not included in either distribution archive.

## What has been checked

- Five offline builds completed successfully: two identical source distributions and three identical wheels, including a wheel rebuilt from the source distribution. Archive contents, all 43 runtime modules, RECORD digests, source copies and extracted-file preservation passed independent review.
- A fresh wheel-materialized prefix contains 48 wheel files and 509 separately copied, pinned existing dependency files. The original dependency files and earlier prefixes were preserved.
- Two independently reviewed runs passed against genuine modules in that fresh wheel prefix: five legacy/diagnostic constructor cases and four compatibility-report tests. They checked actual installed origins and preserved the fixed input files. These nine cases do not constitute a full test suite or a native database regression.
- A separate actual offline `uv --target` installation has now returned 0 with all 298 declared inputs preserved. Independent terminal review accepted the actual installation: exact 50 output files, 49 RECORD rows with 48 digests, generated launcher and all 298 original inputs. The earlier argument-conflict attempt remains preserved as failed. It uses `--no-deps`: normal dependency resolution and installation are not tested. Generated installer metadata is deliberately suppressed; forbidden metadata bodies are not read.
- The actual generated-launcher `--help` check passed and was independently accepted: SystemExit 0, six exact installed module origins, zero third-party imports, all 50 outputs and all 349 original inputs preserved. It executes the generated script body under explicitly selected Python and import paths. OS shebang execution, shell PATH discovery and portability were not tested.

## Download and recovery

The wheel and four accompanying evidence/manifest files are stored in the private repository at immutable commit `38c627a3123a9f3bdb10e45cbafa2f0516d71889`:

[Private wheel checkpoint](https://github.com/debgh-workspace/cryptalis-research-lab/blob/38c627a3123a9f3bdb10e45cbafa2f0516d71889/preview/artifacts/integrated222-v2-20261017/cryptalis-0.1.0-py3-none-any.whl)

Repository path: `preview/artifacts/integrated222-v2-20261017/cryptalis-0.1.0-py3-none-any.whl`. Access requires the private repository's existing permissions. The remote bytes were retrieved and restored into a fresh local file, then matched against the exact size/hash above without execution. This verifies artifact recovery, not a clean machine or complete environment restore.

Paths below are relative to the existing authorized workspace `/workspace/scratch/cb28ee9f5f4a`:

- Verified remote restore: `persistence-recovery-20261013/combined222-wheel-remote-restore-20261017/cryptalis-0.1.0-py3-none-any.whl`; its `RESTORE_RECEIPT.json` records the immutable commit and byte match.
- Original accepted build: `cryptalis-executable/recovery-work/integrated222-offline-package-controls-v1-20261017/run/direct-wheel/cryptalis-0.1.0-py3-none-any.whl`.
- Actual full source tree: `recovery-work/integrated222-v2-20261017/source`.

The source distribution and a self-contained combined222 source capsule are not published by this checkpoint. Do not infer that the wheel alone restores documentation, tests, dependency provenance or a runnable environment.

## Reversible evaluation and remaining holds

Keep the downloaded wheel and its hash record together. Any further approved evaluation should use a new empty, versioned scratch prefix and the reviewed fixed controls; do not overwrite an existing prefix, change the selected preview, alter a system environment or point the checkpoint at production data. The separate prefix leaves existing artifacts and the prior selection untouched. It does not recreate older prefixes lost in the workspace rollback. No database migration or rollback is part of this checkpoint.

Results rely on the existing pinned host Python/uv and previously admitted dependencies. They do not establish a clean-host install, original dependency/vendor provenance, production readiness, or provider/DB/native transaction behavior. The native 48-case regression involving up to 68 fixtures remains on its separate fixture-permission approval hold.

All 34 objectives remain in scope; this checkpoint does not mark them complete. All seven qualification gates remain UNKNOWN: G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE. Earlier failures and unrelated performance holds remain retained.

## Exact terminal evidence

- Actual offline installation review: SHA256 `8c375cb6177be671ea8c93abd1d5e3ef32a20bb0f5acfff1c87cc46630d6e735`.
- Actual generated-launcher review: SHA256 `9ef9f740f44a6d6ee0516f4ad60435553a58a2bada66fa2ca9b91b3f9816b098`.
- Separate read-only research helpers passed 68 progress-state and 39 column-projection recording-connection cases. These helpers are not included in this wheel and do not authorize recovery or validate actual PostgreSQL state.
