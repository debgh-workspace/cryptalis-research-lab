# Independent post-run declared-license inventory review

Verdict: ACCEPT the scoped evidence inventory. No candidate rerun, product imports, builds, DB or Git actions were performed in this review.

All 73 immutable input pins reverify, and the emitted pin map exactly equals the manifest. stdout SHA256 01e04feb4b9053418e0504ffb05d7610b20f99975c41066f0270e19a0369f67b matches the parent receipt; stderr is empty. Parent receipt records exit 0, 0.16162795100535732 seconds and unchanged inventory. This reviewer audited saved data, not the live execution.

Independently checked:
- Eight name/version pairs exactly match reviewed expectations and lock versions. pycparser 3.0 remains sourced from pinned unpacked cache, separate from installed 3.11.
- All 12 base64 notice payloads decode byte-for-byte to their pinned origin files. All 12 notice SHA256/lengths and local RECORD rows were independently verified using shell hashing and literal row comparison.
- Three vendor SBOM files and all 15 bundled libraries also match their reported SHA256/lengths and local RECORD rows. Vendor counts independently agree: Rust 39 components/39 license fields; OpenSSL 1/0; auditwheel 10/0. Fifteen library files are not represented as fifteen fully licensed or conclusively mapped components.
- Exactly three named controls report rejection with the source-reviewed reasons: malformed_vendor_sbom, missing_notice, notice_hash_mismatch. No control replay was performed.
- Both environments' emitted current metadata paths/hashes and version headers match their input files. Current pycparser 3.11 and iniconfig 2.3.1 remain explicitly distinct from lock 3.0 and 2.3.0. SA20 SQLAlchemy 2.0.51 is the intentional override; SA21 is 2.1.3. Each emitted observation has 13 relevant dependencies; each frozen directory inventory has 14 METADATA files including Cryptalis, correctly excluded from that dependency observation.
- Frozen before-inventory hashes reverify for both 14-METADATA sets and 15-library set. Prior source inspection observed no symlinks; the parent reports identical pre/post inventory and no-symlink checks.

Missing tzdata 2026.5, absent Windows-conditional tzdata/colorama in current cells, native notice incompleteness, platform-variant incompleteness and historical-execution identity NOT_ESTABLISHED remain explicit. Local RECORD consistency does not authenticate original downloaded wheel bytes. Declared expressions/notices establish neither legal compatibility nor compliance. Directory scanning remains bounded to the verified unchanged snapshot, not general hostile-tree enforcement. All seven product gates remain UNKNOWN.
