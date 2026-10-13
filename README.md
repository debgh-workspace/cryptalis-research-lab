# Cryptalis research laboratory

Private research repository. Original Debrato2005/cryptalis stays read-only; its 15-message mailbox is preserved unchanged.

## Current working candidate

`candidate/` contains the integrated experimental S7 source, tests, examples and documentation. S6 normalizes malformed protection-plan rejection; S7 accepts positive finite measured rates only in explicit transition-artifact estimate fields, leaving manifest numeric grammar unchanged. Integer artifacts remain compatible; older readers refuse new fractional artifacts. S8 public-table binding remains separate under experiments/s8-public-binding pending qualification. The root `CRYPTALIS_BUILD_CHECKLIST.md` is the authoritative current ledger. Seven legacy-profile assertions still fail; no production gate is qualified.

Installed S7: SQLAlchemy 2.1.3: 1725 passed, 7 failed; 2.0.51: 1707 passed, 7 failed, 18 native-version skips. Full logs and source inventory are in `evidence/20261013/`. Reproducible wheel/sdist and build report are in `experiments/s7-rate-estimates/artifacts/`. Wheel SHA256: 19efd5eafede07616c45c21be491fe85206f52cd0c1ada53fa76dee8ab2ea6e8.

## Verified recovery baselines

S5 full checkpoint: concatenate/recover the archive with `python checkpoints/s5/restore.py /path/to/new-location` using Python 3.12+. It verifies 3579 entries. The frozen archive retains S5, older candidates, research, evidence, master inputs and original mailbox. All parts were downloaded from GitHub and restored in a separate directory. This is same-host byte recovery, not a fresh database or clean-machine qualification.

`history/` preserves the complete original Git bundle with part hashes and instructions. All seven parts were read back byte-for-byte; the original bundle also passed local bundle verification and a separate no-checkout clone. No original commits were rewritten.

Never commit private keys, credentials, runtime homes or live databases. Use only authorized isolated PostgreSQL databases and the unchanged dual-role preflight. New test credentials/fresh cluster qualification remain subject to explicit approval.

Older workspace evidence beyond the recovered S5 archive remains separately inventoried and is not claimed completely published. This repository is not a production deployment or release.
