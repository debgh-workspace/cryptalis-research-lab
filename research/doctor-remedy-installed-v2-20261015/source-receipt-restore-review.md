# Accepted independent six-file supplement restore

Date: 2026-10-15 UTC

## Result

All six selected RED/GREEN evidence files were independently fetched through the read-only Git connector at exact commit `1e2d6e0b516bed6876671c2166da1631b603406d` in `debgh-workspace/cryptalis-research-lab`, decoded from base64 without text transformation, and restored under this fresh review directory's `restored/{red,green}/` directories.

For every file, a complete byte comparison against the retained local original passed. The independently computed Git blob ID matched the connector's returned blob SHA. All six restored files are regular, single-link files with mode 0600; their fresh directories have mode 0700. Total selected restored content is 21,410 bytes.

The immutable repository prefix is `research/doctor-remedy-source221-20261015/`. No default branch or moving ref was used.

## Six exact files and SHA-256

- `red/RESULT.json`: `11cdd211f6e4640c0e015b4b2c154d54b21d9106db970a46851058dec4046350`
- `red/BOOTSTRAP_ROUTE.json`: `e775bd2fb8703651bcfec405aaca45afdd7ebe03fbc4b0d95434e61616ea56ab`
- `red/REVIEW.md`: `a4817e237d082eee340232126e4b9cc27683a776ca5017aa3632ce7afca80483`
- `green/RESULT.json`: `808af0f7b532f821215138827196c11488372261fe505290f4926c5f4520214b`
- `green/BOOTSTRAP_ROUTE.json`: `910cad939b2947a81699deeb69f8dae658691b767dbfaf29d78a0d9ce6c7acf5`
- `green/REVIEW.md`: `1632e84f5b85fddfeafe165489598895ea9e699514fa17207e49b9ce7a250368`

The two RESULT and two bootstrap files were compared with the corresponding `persistence-recovery-20261013/doctor-real-red-v2-root` and `doctor-real-green-v1-root` originals. The reviews were compared with the respective accepted independent terminal-review files. Existing original files were read only and not modified.

`CONNECTOR_RECEIPTS.json` records the repository, exact commit, immutable URL, returned Git blob identity and comparison destination for each read. `RESTORE_RESULTS.tsv` records byte counts, verified blob IDs, SHA-256, mode and byte-comparison results. `RESTORED.sha256` seals exactly the six restored payloads.

## Scope

This establishes only the selected six-file published supplement's byte-identity and inert restore closure. It is not complete source221, package, test-evidence, dependency or environment recovery, and it does not make referenced-but-unrestored artifacts available. The RESULT files retain their original PENDING_INDEPENDENT_REVIEW text; the separately restored accepted reviews retain their original verdicts. No receipt content was synthesized or upgraded.

No restored content was executed. No test/helper/import, database/status command, shell Git command or publication occurred. Only the six requested immutable connector reads, inert local writes, file metadata checks, byte comparisons and hashes were performed.
