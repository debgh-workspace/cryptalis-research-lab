# Declared component-license inventory: source-only packet

Status: NOT RUN. Independent source review is required before one finite standard-library-only run. No product import, package install/download, subprocess, database, Git action, historical SBOM modification, or legal assessment.

## Frozen scope

`inputs.sha256` binds 73 files: verifier/config/mismatch record, current S20 lock, two historical package-origin logs, local metadata/RECORD/notices, three upstream vendor SBOMs, and 15 psycopg-binary bundled libraries. `inventory.py` reads files and emits a single JSON receipt; it never writes files. Notice bytes are preserved losslessly as base64 with origin paths, lengths and SHA256. Upstream license expressions are copied, not inferred.

Eight exact lock-version components are represented. Seven use current SA21 environment metadata; pycparser 3.0 uses the specifically pinned unpacked cache directory. Installed pycparser 3.11 is retained only in the separate current-environment observation and never substituted for 3.0. Twelve declared notice files include SQLAlchemy AUTHORS. tzdata 2026.5 is not available in the checked release-lab or unpacked-cache distributions; it remains explicitly missing, with its Windows-only lock marker recorded. No other-platform archive coverage is claimed.

Each selected component METADATA, notice, vendor SBOM, and bundled library is checked against its local RECORD hash and size. Only explicitly selected RECORD members are read: arbitrary RECORD paths are never followed. Local RECORD is not an independent trust anchor, downloaded wheel digest, signature or legal conclusion.

The three vendor SBOMs are retained as separate upstream declarations. The cryptography Rust SBOM contains license fields. The cryptography OpenSSL inventory and psycopg-binary auditwheel inventory omit license fields. No license is assigned to a native library based on filename, package metadata, or a nearby notice; completeness is UNKNOWN. The verifier hashes the 15 bundled library files without loading or executing them.

## Separate current-environment discrepancy

`environment-mismatch.json` records current pycparser 3.11 versus locked 3.0 and current iniconfig 2.3.1 versus locked 2.3.0 in both identified environments. SA20 SQLAlchemy 2.0.51 is the intentional compatibility-cell override; lock/SA21 is 2.1.3. All nine runtime-union and six test-only package names are checked, including absent Windows-conditional tzdata and colorama. Historical package-origin logs identify the environment paths; current metadata is not retroactive evidence of historical executed code or dependency bytes.

## Finite validation proposal

After review, one Python >=3.12 invocation using `-I -B` suffices. Capture stdout/stderr to new evidence paths. Positive inventory plus exactly three in-memory negative controls: malformed vendor JSON, missing notice bytes, altered notice bytes. All require specific refusal reasons. Verify input hashes before and after. No builds, pytest, imports from these distributions, optimization-mode repeat, performance test, or test rerun is proposed.

All seven full gates remain UNKNOWN. Original artifacts and SBOM remain unchanged. Separate static artifact-to-lock/SBOM equality is not invalidated or expanded by the current-environment discrepancy.
