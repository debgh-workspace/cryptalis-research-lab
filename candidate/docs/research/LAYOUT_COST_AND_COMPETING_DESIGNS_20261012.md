# Layout cost and competing mechanisms, 2026-10-12

## Measured before correction

Each candidate ran three sequential repetitions on2,000 synthetic rows using the same independent all-row CF1 decoder, PostgreSQL16.15 and installed SQLAlchemy2.1.3 cell. The legacy drop/rename median protect+publish time was6.324 s, client CPU3.324 s, cluster WAL4,434,128 bytes, retained relation+indexes827,392 bytes. Prospective two-statement in-place medians were6.383 s,3.447 s,5,409,208 bytes and1,310,720 bytes. This is not measured downtime or peak temporary disk; WAL is cluster-wide and sequential cache/order effects are uncontrolled. All12,000 decoded row observations matched.

Hypothesis: rewriting while the staging column still exists keeps a second payload in the new heap; subsequently dropping the staging column does not immediately reclaim its physical bytes. The PostgreSQL documentation explicitly distinguishes logical column removal from physical reclamation. The separate combined-rewrite candidate changes only each type-conversion/staging-drop pair into one ALTER statement, retaining full verification, transaction locks, snapshot exclusion and exact native metadata checks. Initial13 search/metadata/VARCHAR roundtrip cells pass. The installed wheel repeats these13 and adds three2,000-row cost repetitions, all exact. Combined-rewrite medians:6.215 s, client CPU3.233 s, cluster WAL5,051,608 bytes, retained relation+indexes786,432 bytes. The retained space reduction is40% versus separate in-place statements; cluster WAL falls6.6% but remains13.9% above the legacy baseline. No statistically established speed advantage is claimed. Both installed selections now pass124 cases (SQLAlchemy2.1.3 and2.0.51), including provider failure, key expiry, phase resume and seven lost-COMMIT-reply points. These are selected tests, not a full-suite or security qualification.

## Prior art and design implications

PostgreSQL documents that type changes commonly rewrite a table and indexes; multiple ALTER actions can share one pass. Rewrites need temporary disk and are not MVCC-safe for older snapshots. This is established database engineering, not a novel cryptographic result. Snapshot fencing remains mandatory. [PostgreSQL16 ALTER TABLE](https://www.postgresql.org/docs/16/sql-altertable.html)

MongoDB Queryable Encryption documentation describes a snapshot-exfiltration threat boundary, excludes persistent attackers with query transcripts, does not guarantee native uniqueness over randomly encrypted values, and places restrictions on changing encrypted field/query configurations and existing collections. These are documented trade-offs, not an executed comparison or proof that Cryptalis is stronger. Cryptalis must disclose its retained exact equality/frequency leakage and its own narrow SQL/DDL scope. [Official limitations](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/limitations/)

CipherSweet recommends collision-bearing blind indexes with application-side verification; long exact indexes expose repeated plaintexts. Its public BlindIndex implementation exposes configurable bit length and transformations. This confirms that reduced index precision is a design option, not a newly discovered primitive. For Cryptalis, client filtering would need independently verified aggregate, uniqueness, LIMIT/OFFSET, transaction and concurrency semantics before admission. No shorter-index runtime replacement is made here. [Official FAQ](https://ciphersweet.paragonie.com/faq), [public BlindIndex source](https://github.com/paragonie/ciphersweet/blob/master/src/BlindIndex.php). Source was read at the mutable master URL; no immutable competitor revision or runtime benchmark was captured.

All seven production gates remain UNKNOWN. No provider change, new leakage opt-in, commit or promotion.

Physical relation size is not a secure-erasure claim. WAL, backups, old pages and storage-layer copies require their own retention/custody policy.

## Final bounded validation

Installed SQLAlchemy2.1.3:124 PASS;2.0.51:124 PASS (191 deselected each). Installed Python3.14.8/SQLModel0.0.47/FastAPI0.141.1 replay: native58 PASS; protected58 bodies PASS plus1 bulk teardown ERROR; package-free58 PASS before and after removal;36 exact independently decoded backup rows. Separate two-table, three-field, two-tenant lifecycle preserves post-protection edits and SELECT * order/values. Evidence:combined-rewrite-installed-sa21-20261012-0942, combined-rewrite-installed-sa20-20261012-0942, combined-rewrite-installed-fastapi-20261012-0946.

Unchanged original mailbox:15 commits, base2ff72ea4fe7871f31a9fabbbf63f19a5cc714e43, SHA2569b725abc6cc9baa86d98f88ac076f3beb67cc596dbe6d7c7d06b2eda8512e6cd. Experimental delta is separate. No new commits or pushes.
