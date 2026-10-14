# S23 acceptance evidence add-on: independent publication review

Date: 2026-10-14 UTC. Disposition: PASS, DATA-ONLY PUBLICATION REVIEW. No blocking concern found in the exact archive below. Publication authority and remote readback remain the coordinator's responsibility.

Archive: `CRYPTALIS_S23_ACCEPTANCE_EVIDENCE_ADDON_20261014.tar.xz`

Bytes: 87,856

SHA-256: `7fd2bc7e4df3dfae16747f737dd1b410862e4dd80ce14a5c2a629fbe0b3799cd`

## Integrity and reference completeness

The independent data-only extraction contains exactly 150 unique regular relative files: 139 explicitly allowlisted evidence files and 11 metadata files, totaling 2,037,817 uncompressed bytes. All inventory and payload-manifest sizes/hashes match. The 149-entry payload manifest plus its own member exactly cover the archive. No symlink, special member, unsafe path or duplicate member was admitted. No archived script, test or product module was imported or executed.

The 1,283-path reference map is complete and internally consistent. This review independently reconstructed its union from the included inventory, manifest post-run audit, four runs' source/runner/external/prior-receipt inventories, and comment audits. There are no missing/extra paths, conflicting hashes or digest discrepancies. Every current safe target was separately byte-hash checked.

Reference classifications are exact:

- 139 included at their original paths
- 1,036 references to exact members of the frozen S23 source capsule
- 108 byte-identical aliases of included evidence

The referenced source capsule is independently checked as 1,750,488 bytes with SHA-256 `41c756d905f84f4754208ba4d27bda87621ab88d0bac58fcf421c7bbcbf50870`. Its exact 213 source members match the retained preparation manifest, whose SHA-256 is `42f17eb0f1a95063dbb15069df906dc0e53595601201af64a4c73fb7a03152b2`. No full source tree is duplicated in this add-on.

The sixteen recorded external/historical targets remain references only. Their contents were neither opened for this review nor included in the archive. This add-on depends on the separately retained source capsule; it is not a standalone source or operational-environment backup.

## Outcome and history preservation

Archived JUnit, runner receipts, logs and captured summaries agree:

| Family | Cell | Retained result | Runner exit |
| --- | --- | --- | --- |
| Generated setup | SA21 | 2 PASS, 0.82 s | 0 |
| Generated setup | SA20 | 2 PASS, 0.74 s | 0 |
| Object comments | SA21 | 3 FAIL / 1 PASS, 2.70 s | 1 |
| Object comments | SA20 | 3 FAIL / 1 PASS, 2.67 s | 1 |

All four source/external inventories are stable within their recorded scope, and each run retains its exact 26-entry restored prior-corpus evidence. The comment case receipts exactly match the included independent audits. Native controls preserve comments. The three commented lifecycle cases retain shape/current values but fail comment equality at PLAINTEXT_PENDING, with removal NOT_REACHED. The absent-comment case reaches REMOVED. The serialized booleans do not distinguish a missing comment from changed comment text, and this review makes no stronger assertion.

Manifest V1 source/hash and its original observer finding remain preserved alongside V2, its diff and passing post-run evidence. The executed V2 test remains `b851385a2f663e4faff36890efe8420b2b4416f0a0b68aa555f20210cc967b00`.

All eight comment V1 files match the V1-preservation record. The executed comment V2 test remains `fb6c4eb1abffc05c9705f15c9b8a8cb34d93da3141a2638938d143f053506272`. Its three-failure history is retained without a claimed remedy. Pending/preparation documents are historical snapshots, not replacement terminal outcomes.

## Publication safety and limits

All 150 members are UTF-8 textual source/evidence/metadata. The archive excludes raw environment-bearing test/origin/readiness/start/stop JSON, named credential files, private-home contents, installed runtimes/dependencies and caches. An independently applied bounded scan of all members found no private-key block, credential-bearing URL, AWS access-key identifier or recognized provider-token pattern. This is not universal proof against arbitrary unrecognized secrets.

The two manifest version observations remain explicitly pre-run identity evidence. Comment version strings remain pinned in-test observations. Neither implies an unchanged full dependency environment. Test source is included only as evidence; none was executed during this review.

No network, Git, database, credential, test or restored-code action was performed. The add-on preserves focused acceptance and confirmed RED evidence. It supplies no operational restore, passing comment correction, full-suite/installed qualification, external-provider qualification or release qualification. All seven full gates remain UNKNOWN.

`DATA_AUDIT.json` records all checks, exact member identities, reference counts/completeness, retained run outcomes and explicit non-execution limits. Fresh data extraction is retained under this review directory.
