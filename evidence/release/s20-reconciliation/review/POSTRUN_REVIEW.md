# Independent S20 post-run data review

Verdict: ACCEPT for the bounded artifact/lock/historical-SBOM consistency result only. No candidate rerun or product imports were performed by this reviewer.

The immutable script and manifest retain their reviewed hashes; all 51 manifest inputs reverify. The emitted input_pins map exactly matches the manifest. stdout SHA256 is 16f811c8c22112bf66c7489caf203dea84afe3a4cc6500bfdbe0e6c1e914d920, matching receipt.json. stderr is empty. The parent execution receipt records exit 0 and 0.10504771600244567 seconds; this reviewer did not independently observe process execution.

Data cross-checks:
- 40 current Python source files match source-before.json byte-for-byte by SHA256, and no source symlinks were observed. Parent receipt records unchanged source after execution. Prior archive listings/source review corroborate the bounded 40-module scope.
- The wheel RECORD independently contains 44 sha256-bearing entries, consistent with the reviewed complete coverage/hash/size algorithm and emitted result.
- Runtime union matches all nine expected package/version pairs. Test-only union matches all six expected package/version pairs. These remain separate from the declared uv_build range.
- Historical SBOM independently contains nine components and 302 distribution references. An independent awk/jq comparison of component-name/URL/hash triples exactly matches all 302 corresponding runtime lock entries. This does not validate downloaded dependency bytes.
- All six expected controls appear in order, rejected=true, with the reviewed named reasons: malformed_sbom, missing_wheel_license, altered_sdist_license, dependency_version_mismatch, dependency_edge_mismatch, missing_record_row. Source review establishes that they mutate inputs in memory, independently of the generated receipt; this audit does not replay them.
- sdist_has_lock=false agrees with the archive inventory. The lock remains an external pinned release input. The historical SBOM has zero component license fields, independently counted. MIT notice preservation implies no transitive-license review.

Limits: the recursive source read is bounded by the verified unchanged 40-file snapshot and no-symlink observation, not general hostile-tree/allowlist enforcement. This is not a secret-content scan. Platform-marker union, including tzdata, is not an installed Linux inventory. No native vendored-library completeness, vulnerability triage, signing/publisher identity, historical executed-bytecode provenance, resolved builder identity or clean-machine reproducibility is established. All seven product gates remain UNKNOWN; no full release qualification follows.
