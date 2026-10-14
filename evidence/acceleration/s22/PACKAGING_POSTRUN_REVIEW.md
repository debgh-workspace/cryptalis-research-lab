# Independent S22 packaging post-run review

Verdict: ACCEPT scoped packaging result. This reviewer performed data/archive inspection only: no rebuild, candidate rerun, product import, installation, runtime test, database or Git operation.

Independent actual-artifact checks:
- Two sdists are byte-identical: SHA256 7cee7fc8e265ac0a23753f18aba34a999171072bae15a006e001cc2146ed78b7.
- Direct and from-sdist wheels are byte-identical: SHA256 346eac4f4cf54bac270e25dce6f7d97cdb591ac2969a00a3b9c073a0e4a20c57.
- Against the correct S21 sdist, all 52 member names/types and 46 regular-file names match. Only cryptalis-0.1.0/src/cryptalis/manifest/compatibility.py payload changes. Every other common regular payload, including config, lock, metadata and license, is unchanged.
- Against the correct S21 wheel, all 51 member names (including directories) and regular-file sets match. Exact changed payloads are cryptalis/manifest/compatibility.py and cryptalis-0.1.0.dist-info/RECORD. Every other payload is unchanged.
- All 40 Python module bytes independently match copied source, sdist and wheel. RECORD independently has exact unique coverage, 44 correct SHA256/length rows and blank self-entry.
- Included lock exactly matches source: faae077d223037c4a7d9a54e1aafc4760cf217057eb18fbd93fc021908be343e.
- All five current pin groups independently reverify: 3 outer, 14 helper/input, 210 S21 baseline-source, 212 copied-source and 212 S22 candidate-source entries. Original S21 artifacts remain pinned and unchanged.

Receipt assessment:
- Parent reports PASS_BOUNDED_PACKAGING, all five groups successful before/after, child exit 0, leader reaped, no signals or cleanup errors, no parent errors, and restored parent file-size limits.
- Saved bounds match reviewed code: 120-second child deadline plus up to 10-second reap allowance; 2 MiB per-stream capture; at-most-8 MiB inherited soft per-file limit. These are trusted-tool controls, not hostile-code containment or aggregate disk quota. Descendant absence remains unverified.
- All eight step stderr files are empty. Verifier reports exactly missing_lock and altered_lock controls rejected, and ALL_SEVEN_UNKNOWN. Controls were source-reviewed and their receipt audited; they were not rerun by this reviewer.

No runtime result is asserted here. Same-host pinned-builder equality and source/payload binding do not establish clean-machine reproducibility, original dependency provenance, dependency drift repair, signing or release qualification. No S21 installed environment was changed. All seven product gates remain UNKNOWN.
