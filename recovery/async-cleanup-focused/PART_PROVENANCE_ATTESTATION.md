# Exact local part provenance attestation

2026-10-15 UTC. Decision: **PASS_LOCAL_PART_PROVENANCE_FOR_ALREADY_AUTHORIZED_EXACT_PUBLICATION**.

All eleven local parts independently match the contiguous byte ranges below of the accepted 1,029,680-byte `CRYPTALIS_ASYNC_CLEANUP_RECOVERY_20261014_v1.tar.xz`, SHA-256 `1c6f9900389f61826d1f1d427a0bfc94e5f3cc20fee0f758281b928a896129af`. Each actual length, SHA-256, and Git blob ID matches `parts/MANIFEST.json`. Git blob IDs were calculated directly as SHA-1 of `blob <decimal length>`, a NUL, and the bytes; no Git operation occurred. Concatenating parts 01 through 11 is byte-for-byte identical to the accepted archive. The associated full per-part identities are in `part-provenance.json` and `part-provenance.tsv`.

| Part | Start, inclusive | End, exclusive | Bytes |
|---|---:|---:|---:|
| part-01.bin | 0 | 96000 | 96000 |
| part-02.bin | 96000 | 192000 | 96000 |
| part-03.bin | 192000 | 288000 | 96000 |
| part-04.bin | 288000 | 384000 | 96000 |
| part-05.bin | 384000 | 480000 | 96000 |
| part-06.bin | 480000 | 576000 | 96000 |
| part-07.bin | 576000 | 672000 | 96000 |
| part-08.bin | 672000 | 768000 | 96000 |
| part-09.bin | 768000 | 864000 | 96000 |
| part-10.bin | 864000 | 960000 | 96000 |
| part-11.bin | 960000 | 1029680 | 69680 |

The exact 2,964-byte manifest has SHA-256 `95283f84eebc99775c574a6c2bc6c832c20bd9cedbe0edffdc5f4109adb24ca8` and Git blob ID `7c12ae61f986c0a8b81e135fe9ce60c7f13253ef`. The intended, already-authorized publication scope supported by this attestation is exactly these eleven parts plus this manifest under `debgh-workspace/cryptalis-research-lab`, path `recovery/async-cleanup-focused/parts/`. This review grants no additional publication authority and performs no upload.

The accepted archive's 516 regular members and complete 217-file source identity inherit the independent frozen review at SHA-256 `cedb958ec9a873b49d8d6baa96bc55c348cd076d4840fd54fda3b22dc09d983a`. The restore source's complete 516-member size/hash map was independently compared with the pinned frozen manifest and exact allowlist, with exact equality and no forbidden member names.

The accepted bounded scan covered 514 files / 9,052,576 bytes, with a 2,097,152-byte per-file limit and 33,554,432-byte total limit. It excluded its own report and the final frozen manifest. The seven pattern categories, two accepted synthetic-fixture dispositions, and zero unresolved findings are preserved. Disposition source SHA-256: `640f4a4727d588a5f5b03d11941d9e482b2430dfecc12f4252a4850589c3a022`. No matched values are reproduced; no new secret scan was performed. This bounded result is not proof that every possible secret is absent.

Local staging remains local staging. This attestation is not an authenticated remote readback receipt, does not establish a remote commit, and does not support replacing actual remote bytes with local parts for restore. All seven qualification gates remain UNKNOWN; historical seven failures retain their unresolved prior disposition; full-matrix and installed qualification remain separate and pending.
