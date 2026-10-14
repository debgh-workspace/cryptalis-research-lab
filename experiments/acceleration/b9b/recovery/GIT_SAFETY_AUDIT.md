# B9B exact-archive Git-safety content audit

Archive SHA-256: 801f535dc76f378ea232d84c1365a71e52f34e63c50abc7a25107c21d7a2ba48
Archive unchanged: YES. Bytes: 930828.

## Inventory and provenance

- 232 regular UTF-8 archive members, no duplicate names, traversal paths, links, devices or binary/nested archive members.
- 213 source files exact to the designated B9B candidate: 209 byte-identical entries from the 210-entry inherited source manifest; one changed frozen experiment; three added profile metadata/test files.
- All 9 independent-review hashes match. All 231 non-manifest members match the embedded manifest.
- 13 exact safe evidence files: root-provided b9a-b9b-verification-results.json plus junit.xml, tests.log, source-stability.json and external-source-stability.json for B9B RED-SA21, GREEN-SA21 and GREEN-SA20.
- 2 independent review files; 2 original mailbox/checksum files; manifest and restore instructions.
- Historical mailbox contains 15 commits and retains SHA-256 9b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd.
- No tests.json, package-origin.json, environment dump, private credential file, .git, virtual environment or cache included/read.

## Redacted sensitive-marker review

- 2 credential-shaped URLs, both nonfunctional public source-test fixtures. Files: tests/test_attachment_engine_preflight.py line 24 and tests/test_doctor_setup.py line 84. Both use a fixed synthetic username and reserved invalid.example host. Source do_connect sentinels prevent connections. Values are omitted here and redacted in JSON.
- 3 additional PostgreSQL URL literals have no password, use the same reserved hostname, and are protected by a do_connect sentinel in experiments/manifest_setup_fastapi_models.py lines 47-49.
- 0 private-key format markers, 0 recognized access-token formats, 0 JWT-shaped values.
- 162 environment credential references are variable names/private filenames, not resolved values. Referenced private files were not opened.
- 51 broad sensitive-assignment pattern occurrences reviewed as test model fields, diagnostic redaction markers, explicit wrong-password negative-test markers, dynamic environment references, CLI argument declarations, assertions, or manifest scan prose. No operational credential assignment was identified.
- Public crypto structural/scalar vectors are exact inherited source fixtures. The mailbox/evidence contain no credential-shaped URLs, private-key headers or recognized tokens.

GIT_SAFETY_AUDIT.json enumerates all 232 members with exact hash, byte count, original path and comparison result; every pattern finding has file/line, line hash, classification and redacted matched value.

## Authorization and limits

Parent supplied verbatim owner authorization for engineering/tests/checkpoint commits and pushes only to private debgh-workspace/cryptalis-research-lab, preserving checkpoints/source evidence, using small batches and remote verification; secrets must never enter Git. This report only documents content provenance and observed scan results. It does not override the prior reviewer denial or itself authorize publication. Root owns any same-operation retry; this worker uploaded nothing.

Static scanning is not exhaustive proof that arbitrary content contains no secrets. No database use, test execution, Git commands or credential reads occurred. Run source-stability receipts exclude the experimental module; worker freeze, current bytes and independent-review hashes are separate point-in-time provenance, not continuous runtime attestation.
