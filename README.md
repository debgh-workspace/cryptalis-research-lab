# Cryptalis research laboratory

Private research repository. Original Debrato2005/cryptalis stays read-only; its 15-message mailbox is preserved unchanged.

## Current working candidate

`candidate/` contains integrated experimental S12 source, tests and documentation. S6 normalizes malformed-plan diagnostics; S7 supports bounded fractional measured-rate artifacts; S8 resolves and freezes eligible native unqualified public table mappings. S9 bounds planner numeric rejection without changing estimate formulas. S10 reduces temporary tuple serialization allocations without changing wire bytes or key lifetime. S11 corrects stale source-scanner UUID/default-DML diagnostics; runtime admission is unchanged. S12 adds bounded pre-adoption doctor diagnostics (see candidate/docs/doctor.md). Complete role/provider/ciphertext diagnostics remain open. The root checklist is authoritative. Private DELETE/cascade opt-ins and locked inventories remain required.

Installed S12: SQLAlchemy 2.1.3:1803 passed,7 failed; 2.0.51:1785 passed,7 failed,18 native-version skips. The seven legacy-layout assertions remain open, unchanged. Last real-app check on S8: pinned FastAPI:58 native +58 protected +58 package-free before removal +58 after removal pass, each zero failures/errors/skips, without upstream source edits or per-table schema assignments. Explicit C collation,13 bootstrap/4 fixture lines and operator grants remain. Seven-user/seven-item synthetic recovery matched exactly. No production gate is qualified.

Artifacts: experiments/s12-doctor/artifacts/. Wheel SHA256:db6e83817fd4bad3e9be8f98b9aebbbc5641ac38f09e64e94ab11be84b77e332. Source inventory and same-host179-file composite recovery receipt: evidence/20261013/s12-source-manifest.json and s12-recovery-receipt.json. Prior S5/S6/S7/S8/S9/S10/S11 checkpoints remain in history. Integer artifacts remain compatible; older readers refuse S7 fractional artifacts.

## Verified recovery baselines

S5 full checkpoint: concatenate/recover the archive with `python checkpoints/s5/restore.py /path/to/new-location` using Python 3.12+. It verifies 3579 entries. The frozen archive retains S5, older candidates, research, evidence, master inputs and original mailbox. All parts were downloaded from GitHub and restored in a separate directory. This is same-host byte recovery, not a fresh database or clean-machine qualification.

`history/` preserves the complete original Git bundle with part hashes and instructions. All seven parts were read back byte-for-byte; the original bundle also passed local bundle verification and a separate no-checkout clone. No original commits were rewritten.

Never commit private keys, credentials, runtime homes or live databases. Use only authorized isolated PostgreSQL databases and the unchanged dual-role preflight. New test credentials/fresh cluster qualification remain subject to explicit approval.

Older workspace evidence beyond the recovered S5 archive remains separately inventoried and is not claimed completely published. This repository is not a production deployment or release.

S10 synthetic 8MiB encoder traced peak:16,777,664 to8,388,864 bytes. Same-session paired IN2 medians improved modestly in both dependency cells; point/equality effects varied. No general speedup, process-RSS, tail-latency or production performance qualification.
