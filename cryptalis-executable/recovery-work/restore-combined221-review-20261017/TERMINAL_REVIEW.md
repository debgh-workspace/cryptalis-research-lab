# Independent combined221 inert restore terminal acceptance

Status: ACCEPTED_INERT_COMBINED221_SOURCE_RESTORE.

Root selected reviewed external supervisor V2 once. External capture exit is 0, child exit is 0, reason is null, leader reaped, no received signal, no group signals and no cleanup errors. Child stdout is exactly 840 bytes, hash edee3087a40470677b24dbe79bc95dda4db455496fa627ad43ec9f89c2a4f313, and parses identically to the source restore receipt. Child and external stderr are empty. Exact child argv/environment agree with selection and terminal records.

Restored source: cryptalis-executable/recovery-work/restore-combined221-20261017/run/source221. Independent metadata-first namespace audit finds exactly 221 ordinary single-link files and 21 directories, totaling 4,461,022 bytes. All files are 0600, directories 0700; no symlinks, extras or bytecode. Every source body was independently read/hash-checked as inert data against the complete final manifest e8a69b212e8a1759e7641d6bb1227a3aa728e76badd515a54421d98811e5552c. Full output manifest entries match actual name/size/hash. Output inodes do not alias any declared input, and metadata remained stable during readback. conftest was hashed only, never imported.

The same 221-member baseline map resolves in observed archive member digests. Eight exact overlays account for all differences from Integrated221; 213 entries and all 116 tests remain unchanged. The restored source is byte-identical to the accepted combined candidate, not a newly qualified runtime.

All 43 finite inputs have complete matching before/after entries. Independent current metadata and full SHA256 checks agree for every input, including controller/helper/parser, manifests, provenance, decoded parts, review bindings, original mailbox and pinned existing interpreter. Root provenance binds all 17 exact immutable remote part identities. Per-part Git blob checks and concatenated compressed archive SHA256 independently agree with 1f76f9bf50e7e757430edfe45b5ecb81afee67283675f2465c0d0b102f05822b. The reviewer did not rerun decompression or the parser: raw tar/header checks are attributed to the exact reviewed parser execution and prior accepted focused-capsule evidence. All 664 observed member identities are unique/sorted, within size bounds and total 34,721,556 bytes. Current generated source map and receipts remain ordinary data.

Original cryptalis-executable/Outputs/CRYPTALIS_FINAL.patch remains 219,914 bytes and SHA256 9b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd, with exact supervisor-before metadata and after/current equality. V1 supervisor HOLD remains preserved. Cold bytecode prefix is absent. Parser run namespace contains only source221 and its three declared data receipts.

Concrete terminal identities:
- supervisor terminal: eed09746b07e9457facee3da0255595cea95098eac5f5743b4f68bff0abb98e4
- parser receipt: ef79efc1f7f838638ae36fd9b90f26a8e9b8b33f93674fee0432e0ad314b165d
- restored source manifest: 8fb4d6fae1236cda344da7966975927141ee4c1abd20badeda93167d81c3ddb3
- member observations: 94c0404fb6d43c94b966a4e6d6ff08d5bd455b68b5f49ac255559f9afbc3b0f0

Scope: exact source-data recovery only. No product/helper/test import or execution, compilation, build, installation, database operation or repeated unit test was performed by this reviewer. The root ran only the admitted recovery controller/parser. Existing-host trust is explicit; no fresh native provenance is invented. Runtime/environment recovery, original inode/timestamp reconstruction, full qualification and tests_executed remain false. Global descendant absence remains unverified. Historical installed results remain historical; original build timeout remains FAIL; selected preview and promotion status are unchanged.

See TERMINAL_CHECKS.json for machine-readable independent counts and hashes; prior source review and ARCHIVE_SCOPE_ADDENDUM.md retain archive admission and logical-exclusion limitations.
