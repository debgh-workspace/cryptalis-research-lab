# State source221 recovery procedure

This packet extends the prior inventory without altering it. Four state test cells are terminal and accepted; actual safe-text outputs/root captures and their hashes are now listed in STATE_COMPLETED_INVENTORY.json. Existing source/control hashes are inherited from the prior inventory. No product promotion or broader qualification is implied.

## Locally tested data-only composition

The bundled restore_source221.py was run once with accepted local state V2 overlays. LOCAL_RESTORE_RESULT.json records PASS: all 221 output paths, sizes and hashes equal AMENDED_SOURCE_MAP.json (SHA256 d2ace8320a60b6cf9b7d8472ca4819efe5129f6130e800a5958951266ef2f6ff). Inputs were admitted, rehashed before/after, exact namespace checked, and outputs written as separate inert 0600 regular files. No restored Python file was imported, compiled or executed. The local-tested-source221 directory is a validation output only; do not publish its 221 duplicate bodies.

## Root-owned remote continuation

1. Root retrieves the two published state V2 overlay bodies from an immutable commit and verifies exact remote readback/provenance. Supply them in a fresh ordinary workspace directory under src/cryptalis/sqlalchemy.py and src/cryptalis/_sqlalchemy_transactions.py. No credential, dependency or environment bodies are needed. Record immutable commit, exact remote paths, fetch method and observed hashes separately.
2. Expected sqlalchemy.py SHA256: bd36700fd6ee58afdad9b90943ce5b119967fe5ebde14d1f4cacd26c2a8160f1. Expected _sqlalchemy_transactions.py SHA256: 676e87d50468129de692de6ed86f020ae248cf1601d4dda2b94f791e901da415.
3. Review and pin restore_source221.py from this inventory. Use the unchanged command form below, replacing only the explicit overlay directory and fresh output path with the verified root-owned paths. Both must be absolute normalized workspace paths; output must be a new path under persistence-recovery-20261013. Preserve errors and partial outputs rather than retrying the same output.

python -I -B /workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/cleanup-state-recovery-20261017-0132-simba/restore_source221.py --overlay-root ABSOLUTE_ROOT_SUPPLIED_REMOTE_OVERLAY_DIRECTORY --output ABSOLUTE_FRESH_RECOVERY_OUTPUT --provenance root-supplied-remote-bytes

4. Retain the exact argv, exit status, stdout/stderr and immutable fetch receipt. The script hard-pins the complete frozen baseline map and amended map, requires exactly the same two changed paths, metadata-admits the entire finite source set before body reads, validates no symlink/hardlink leaves and UTF-8, rehashes every input, applies only two overlays, verifies exact 221-file namespace/full hashes, and rechecks input metadata/hashes. It does not authenticate remote provenance itself.
5. Independent review must reconcile the real remote acquisition and completed reconstruction before a remote-overlay recovery claim. The claim is reverified previously recovered frozen base plus newly fetched remote two-file overlay, not wholly new full remote/environment recovery. Dependency reproduction, clean host, database/native release, installation/full-suite and external qualification remain unestablished.

Current remote-byte restoration status: PENDING root-supplied bytes. Locally tested reconstruction is complete.
