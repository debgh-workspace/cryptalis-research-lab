# S20 release evidence reconciliation: source-only review packet

Status: NOT RUN. No build, product import, database call, dependency installation, Git action, or external request is proposed. All seven full qualification gates remain UNKNOWN.

## Existing evidence reconciled

- `evidence/s20-payload-preparation-20261014-artifacts/report.json` records repeated same-host offline wheel/sdist identity, 44 hashed RECORD entries, and 40 runtime modules. Existing wheel digest a46e527484daaf4621831f395af8d8193716220a24106c5d6d0d983a16a9cbb7; sdist dd4b0f44c0b0114b56c5d57637ff79e159ce6c65e1c9e71fbdd2843aabb495c6.
- `checkpoints/CP29-license-distribution.md` records the already-corrected historical license omission, positive/negative archive tests, and nine-component CycloneDX export. Do not rebuild or repeat that historical experiment.
- Current S20 and `release-lab/license-source-1` have byte-identical pyproject.toml, uv.lock, and LICENSE. Existing wheel METADATA declares MIT and LICENSE; both existing S20 archives contain the exact source notice, SHA256 7f5a6a6ca9e6e2d6e75ec8530612396f3eebd2659c79a6ca123bf30a933f23df. These were read-only shell inspections, not script results.
- Historical SBOM is `evidence/w9-license-fix/runtime-sbom.json`. Its nine-component union includes Windows-only tzdata; it must not be relabelled an actual Linux installed-dependency inventory. It has no component license fields; no transitive dependency-license review is implied by retaining Cryptalis's MIT notice.
- Existing S20 sdist has no uv.lock. The lock is an external pinned release input, not an archive-contained reproducible build guarantee. Build requirement `uv_build>=0.12.12,<0.13` is a declared range, not a resolved builder identity.

## Contract and intended finite result

The approved blueprint `cryptalis-mandate-inputs/CRYPTALIS_FINAL_REVAMP_BLUEPRINT(1).md`, lines 6030, 6081, and 6219, requires exact artifact/input binding, SBOM/notice/provenance distinction, explicit completeness limits, and independent qualification. Checklist OBJ-OPS-01 and G-RELEASE remain incomplete.

`reconcile.py` reads only the 51 pinned files, plus its checksum manifest, parses archives without extracting or importing their contents, and emits one JSON receipt to stdout. It verifies artifact digests, source payload equality, metadata/direct dependency declarations, archive notices, complete RECORD coverage/hash/size, the nine-component union runtime lock closure including requested psycopg binary extra, six test-only dependency versions, declared build requirement, historical SBOM graph identity, and every SBOM distribution URL/hash against the current lock. It does not evaluate platform markers as a runtime installer.

Six in-memory negative controls: malformed SBOM JSON; missing wheel license; altered sdist license; mismatched dependency version; mismatched graph edge; missing RECORD row. Each must reject for its named reason. No original files are mutated. Before/after input hashes must match.

Run only after independent source review, from a verified standard-library Python >=3.12 using `-I -B` and capture stdout/stderr in new evidence paths. This source preparation does not authorize execution. No pytest/build/runtime suite repeat is needed. One normal run is sufficient; no optimization-mode repeat or benchmark is proposed because validation uses explicit conditions rather than assert.

The result can close a bounded artifact-to-existing-SBOM consistency gap. It cannot close native vendored-library inventory, dependency license compliance, vulnerability triage, signing/publisher identity, historical executed-bytecode provenance, clean-machine reproducibility, known seven legacy failures, or any full qualification gate.
