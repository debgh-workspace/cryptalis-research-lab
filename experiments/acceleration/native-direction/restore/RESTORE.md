# Native direction probe restore boundary

Verified on 2026-10-14 in the existing isolated environment only. This does not qualify another machine, library build, ABI, provider, or product backend.

1. Fetch native_direction.c, test_direction.py and validate_direction_explicit_pinned.py from experiments/acceleration/native-direction at commit def66ac68180cc2d68d518f55078ca2a56338895.
2. Restore these files beneath a fresh root at cryptalis-executable/candidate-native-direction-probe-20261014. Restore the public cf1_vectors.json fixture from the verified S20 remote archive into sibling candidate-accel-payload-integrated-20261014/tests/fixtures. Verify every source hash against the receipts.
3. Create the probe's evidence directory. From the fresh root, execute the recorded compiler command in canonical-build-receipt.json. Use the recorded existing headers/compiler/libcrypto; do not install or silently substitute dependencies.
4. Verify binary SHA-256 393cf26a573870a9e7e1d3b12a3196528f9301f840214dbc05d84e1cb37575ed before any native import. The initial alternate-path build is retained: CPython assertion macros embed the source pathname, which changes the binary and build ID. Matching the relative source path in the fresh root restored byte identity without changing source or flags.
5. Run validate_direction_explicit_pinned.py with the existing pinned venv path, without resolving its interpreter symlink. It enforces cryptography50.0.2/OpenSSL4.0.3 and source/binary hashes before loading, uses explicit checks, and refuses existing output paths. The fresh restore passed76checks with optimize=0.

Keep restore-build-receipt.json (initial mismatch), canonical-build-receipt.json (corrected identical build), canonical-validation-receipt.json, and the fresh explicit validation receipt. Never overwrite original experiment files or reinterpret the original timing's unrecorded optimization flags. No database or product runtime was changed by restoration.
