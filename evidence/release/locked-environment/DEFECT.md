# RELEASE-ENV-LOCK-01 — OPEN

2026-10-14 13:33 UTC. Current installed metadata in both S20 full-cell environments differs from the repository lock: pycparser3.11 vs3.0, iniconfig2.3.1 vs2.3.0. SQLAlchemy2.0.51 is the intentional second-cell override. Conditional Windows tzdata/colorama are absent. No dependency change or repeated test occurred.

Current metadata maps to the historical full-cell interpreter paths using safe package-origin.log, but does not attest historical executed bytes. Static artifact/lock/SBOM consistency PASS remains true at its declared scope; it must not be presented as installed-environment identity. All seven qualification gates remain UNKNOWN.

Exact metadata/log hashes and paths are being preserved in a separate frozen input inventory. Resolve by explicit reproducible execution-environment definition and appropriate future qualification boundary; do not silently change lock or dependencies, backdate provenance, or reinterpret prior test counts.
