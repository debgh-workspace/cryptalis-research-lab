# Independent inert remote checkpoint restore review

## Verdict

ACCEPT_SELECTED_26_FILE_REMOTE_CHECKPOINT_INTEGRITY_AND_DATA_JOINS.

The selected 26-file publication is recoverable byte-for-byte from private repository `debgh-workspace/cryptalis-research-lab`, immutable commit `9000743ede262529f2a725d9810d791c6a1bbfac`. All 26 complete fetched payloads match the manifest's Git blob SHA-1 identities. Total restored payload: 411,657 bytes. All restored files are ordinary single-link mode-0600 files beneath this fresh mode-0700 reviewer directory. Published source files remain inert.

This acceptance covers the exact finite selected-file checkpoint and the joins available within it. It does not mean that the environment, original runtime evidence, database, source/archive/corpus, installed packages, or all external dependencies have been restored or independently re-proved. No published test, auditor, entry, selector, launcher, project or product code was imported, compiled or executed. No database/status/test command, Git write, target environment/credential/cache read, held-capsule read or follow of an absolute runtime referent occurred. Root remains sole publisher.

## Remote provenance and exact digest boundary

The GitHub connector fetched each manifest-named path at the immutable commit with base64 encoding. Each returned SHA and complete source URL matched the requested identity; locally calculated Git blob SHA-1 (`blob <byte-count>\0<full-bytes>`) matched every manifest entry. The restore did not copy from local originals. The selected publication manifest SHA-256 is `851b17898d2ff14028c884872d3fc404963143d9351e6913591df0701b18e2e6`.

`FETCH_PROVENANCE.json` records the immutable source URLs and returned blob identities. `RESTORE_DIGESTS.json` records all 26 exact byte counts, Git blob IDs, SHA-256 values and modes. The detailed file table below repeats the cryptographic identities.

## Verified joins

- Native seal: all seven exact members match; companion seal: all five exact members match.
- Published test, entry, bootstrap, command, selection and both source-review bytes match the applicable embedded anchors. The terminal review and published auditor carry consistent native/entry/selection/test/source-review anchors.
- The root selection records SA21, accepted reviews and the V1 CLOSED_FAILURE predecessor consistently. The external V1 terminal-review digest is a reference, not independently verified predecessor evidence in this selected set.
- Exact 31 ordered expected case IDs match the finite source case grid. The complete ledger identity sequence matches 31 connections plus 184 state, two domain, three rejection and one omission record, totaling 221 records with no missing/extra/duplicate identity.
- All 184 complete state objects equal the published STATE_JOINS objects and join both expected and actual audit identity arrays. Length, supplied/received/predicted counts, gates, OIDs/formats, object root and pre-assertion status are internally consistent. State SHA-256 strings are matched across complete records; original raw native/compact payloads were not regenerated in this review.
- The states comprise 167 family, 12 full-size boundary and five omission observations. Every family state is within its recorded envelope. All six boundary pairs follow the 16,777,216-byte ceiling arithmetic, and each paired abort is three bytes smaller. The three omission underestimates are 120/123, 31/31 and 29/29 compact/native bytes.
- Domain public values, widths, order, OIDs and formats match the independently specified literals. Rejection input hashes and observed SQLSTATEs match NUL/high-surrogate/low-surrogate records. All 31 connection records have consistent PostgreSQL16/UTF8 metadata, one target digest and distinct positive PIDs.
- Ledger size is 115,686 bytes; all 221 records are newline-terminated and the largest is 611 bytes. The source-derived SELECT arithmetic is 31 + 2×184 + 2 + 3 = 404; this is not a runtime SQL trace.
- The safe tests log reports 31 passed; the audit result and terminal review report 93 passed phases and 5,124 historical checks. Their raw phase/JUnit/check artifacts are absent. This restore therefore checks consistency of those published claims without re-proving each underlying phase or historical check.
- Safe closure and resource records agree with the published audit summary. The historical closure file still says PENDING_INDEPENDENT_REVIEW; the later terminal review records its scoped acceptance. Held/null source-preparation fields are preserved rather than rewritten into fresh authority.
- All seven product gates remain UNKNOWN. No new run, product/v3 approval or renewed authority follows from these hashes.

## Key SHA-256 anchors

- entry_seal_sha256: `b872be2e11367c73c55b864fb580a2c3230b457518ba6c9e2342270719cd8bf8`
- native_seal_sha256: `f8ebb881794328c9b6054129e5966847cd37264dc80e7a21f4b71c4a10b99ff5`
- native_test_sha256: `0714ef753d9e86b55e711d09419853f0ec75693c84cb623b9a60c99222b9a2a6`
- selection_sha256: `a53e2dbd1e1fba7f919924a4361676fc06a93a694152b358bab295956973821f`
- audit_result_sha256: `977f39325b6a61a29d5d52e081c4a0e0c8227542b95ecb91f176576a9deee290`
- entry_source_review_sha256: `6a370f2f0a24fa65d26ca4c24c37c491bf7fbfa9765b09e54c62506f21fc2d64`
- native_source_review_sha256: `3b048121ed37b172ccaed6538767b9e677c2b88c0db653d443ae7eefb8876018`
- observations_sha256: `5950cdb86b0ee9e9b898effde9e709b858199e004a6f6a59d6e0c4f2997e2302`
- state_joins_sha256: `27bbb9b178e3fab6ef02cb3dfe8bd658e691a514628b7892736ed7c16778e0d2`
- terminal_review_sha256: `66be8d8b513f40dfd7620e54494c850e22cae726b8f938ce1b48c1012f4cdd00`

## Explicit unresolved external dependencies

These dependencies are outside the accepted selected-26-file boundary. None was followed, reopened, fetched beyond the manifest, or restored. `UNRESOLVED_DEPENDENCIES.json` retains the exact named source-input and pinned-input paths and identities.

1. V1 predecessor terminal review `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/reviewer-notes/abort-envelope-native-terminal-independent-20261015/REVIEW.md`, SHA-256 `14492777a41a76912c1f5d92ae473d44ac6f9aa6c6d594ed3f9f084d0340ed0e`, plus original V1 packet/entry/failed-run evidence. Its CLOSED_FAILURE binding is internally consistent; its body and original evidence are not included. The exact three-substitution V1-to-V2 delta cannot be independently rechecked here.
2. The ten entry-pinned external inputs listed below, including source221 manifest, runtime binding/guard, cold launcher, harnesses and preflight. Their hashes are inert anchors. The 221 original source payloads and 249-file / 6,577,713-byte frozen archive with original receipt are not in this restore.
3. The 19 inherited SOURCE_INPUTS provenance references, listed in the dependency JSON. One current conftest has identical published bytes/digest; that does not restore its historical source path or expand the provenance closure.
4. Progress JSONL (124 events / 93 phases), JUnit, runner receipt and accounting receipt needed to independently establish the 31 passed calls and all passed phases. The safe 31-pass log and audit summary are present.
5. Original root invocation/stdout/stderr/exit evidence, wrapper/start/stop logs, pre/post status captures and safe successful-stop evidence required to independently re-establish shutdown and run ordering. The selected closure summary is present.
6. Four runtime-binding manifests and original before/after guard outputs for 3,025 targets, 27 guard members, SA21/SA20 modules, nonproduct installed files and opaque installer metadata. No installed runtime was recovered or inspected.
7. Source-before/stability maps and 160-file runner archive, external-source maps/archive, corpus-before/after/prior maps, isolation receipt, candidate-corpus state and all 26 original corpus payloads.
8. Original auditor READ_MANIFEST.json, METADATA_MANIFEST.json and CHECKS.json needed to independently replay the reported 5,124-check historical audit. The published audit.py is restored only as inert source.
9. Interpreters, PostgreSQL toolchain/server/data directories, psycopg/pytest environment, preflight/origin/lock infrastructure, and any operational runtime configuration. Credential/environment contents, caches and held capsules remain outside scope and were not accessed.
10. Raw native JSON text and original full synthetic state payloads were not persisted in the selected ledger. This review verifies recorded fingerprint joins and arithmetic without rerunning their construction or any test.

### Ten exact entry-pinned external inputs

- `experiments/integrated221-installed-full-controls-v3-20261015/verify_runtime_binding.py`: `c84e168fd2f9dc5a5e8af943ea52d868f495b542ae00c2e9da47c470d391c861`
- `experiments/integrated221-installed-full-controls-v3-20261015/launch_cold_wrapper.py`: `fe7eb1d38cf826c79ecf201a330522f96501d4edc4d40b2f56f779df24f2acbc`
- `experiments/integrated221-installed-full-controls-v3-20261015/BINDING_SA21.json`: `669cb3c408144f597cc70de5d8c23295e26ba47f9c68888b1d986e431171cf54`
- `experiments/integrated221-installed-full-controls-v3-20261015/CANDIDATE_SOURCE_MANIFEST.json`: `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`
- `candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py`: `e5201530c7816a63e606b26352417daff6ca71aedeeccb7b569cea0edb309453`
- `candidate-corpus-wrapper-v2-20261014/corpus_artifacts_v2.py`: `4c0429a182b5b7a2f7e561892936dba89ed279583bff181b18238f50485de86f`
- `toolchain/lab_progress.py`: `673e3d41398f6be36876008f80110b313ad86553363052c8f14a25e1c47b93c1`
- `toolchain/run_baseline.py`: `a88c24fa1699ce42a091c9d2da1168ba453d4548a811d542316fe95cb833d00f`
- `repo/scripts/test_postgres.py`: `118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12`
- `experiments/abort-envelope-native-probe-v1-20261015/SHA256SUMS.txt`: `0c005d33fd00630e7b3ef986e2bbcae3e4c6cafe65b4b996b52ad514304424e5`

## Exact restored file digests

| Repository path | Bytes | Git blob SHA-1 | SHA-256 |
| --- | ---: | --- | --- |
| research/abort-envelope-native-probe-v2-20261015/PROTOCOL.md | 14214 | 25a655e1121926c166f7f3aed050035f7bbeb90d | 0dffbad803eb6b0e63b28483c198373848d38df82339602b7f177c39e9eacdbc |
| research/abort-envelope-native-probe-v2-20261015/COMMAND_ARGV.json | 3193 | ad94849d83b567f047af30e03040665c24a75fc1 | c9265b79b90d260d43bbb71f04cdbc612e687329ac5c9272c25f14299bd4ce8d |
| research/abort-envelope-native-probe-v2-20261015/EXPECTED_CASES.txt | 1304 | 8cd22fa900c4f6c423e3dd82e991762a1488dbcb | 7d7c81cb6ec1c2f413c704b1794e1a065a593fccf54b0f10770462f4a930e81c |
| research/abort-envelope-native-probe-v2-20261015/PREDECESSOR_BINDING.json | 1338 | 724818b67e5d3c5f7cc2f2fbea31e5df87bf472f | efcb7db13588876a4979e7c097c260673a5f289b6baa8b1fd6de6ee9de7551ef |
| research/abort-envelope-native-probe-v2-20261015/SOURCE_INPUTS.json | 4863 | 0b6eafe5f07efc2656a2a39a0745f8f47580830a | 40c9c0fcdf0771d651d5838b37aa94cd23ef0aa48997e53df6c3f8ba52734034 |
| research/abort-envelope-native-probe-v2-20261015/conftest.py | 1584 | eb1985d84179a74b0f1f1fa4d1dabd39879fe147 | fa521d4bec6b84320304ad59d22e7551c342d7e60f2c254c8b6495b07bdf06dd |
| research/abort-envelope-native-probe-v2-20261015/test_native_envelope.py | 17866 | 7541826e3b54cc05d9239b0b20d563ed6bb1c914 | 0714ef753d9e86b55e711d09419853f0ec75693c84cb623b9a60c99222b9a2a6 |
| research/abort-envelope-native-probe-v2-20261015/SHA256SUMS.txt | 591 | 983c72201f7dec435ec21456cf4ddb67f0aa7f58 | f8ebb881794328c9b6054129e5966847cd37264dc80e7a21f4b71c4a10b99ff5 |
| research/abort-envelope-native-entry-v2-20261015/COMMAND_ARGV.json | 2290 | 360fb963d986e452c7e7f4d9433801066647372a | 63ada3b8d11711a8ed5627a9ebc882cd6f36c635ee371c91271c53e4e484d807 |
| research/abort-envelope-native-entry-v2-20261015/README.md | 6184 | 5f5c91332bbe0f8d41e3148fe86711204105b377 | e1d5c099f928fdd5f906b793d67f32ab9fe6e609699689c7d091ac43f4e2a98e |
| research/abort-envelope-native-entry-v2-20261015/SELECTION-TEMPLATE.json | 1088 | b3fb35013baeaa02e1dc02f18c47e389cd12a7d8 | 31b2cb4c41103ec16e690d01bf7018c9cee93c352ba26038e228fb7cc37a3305 |
| research/abort-envelope-native-entry-v2-20261015/SHA256SUMS.txt | 404 | 1fec687e0e1da57224f528a5e9d83c898a9a5dae | b872be2e11367c73c55b864fb580a2c3230b457518ba6c9e2342270719cd8bf8 |
| research/abort-envelope-native-entry-v2-20261015/entry.py | 16559 | fca6899834b1abeb0c2f42d67b4ac6a2341b785f | 6aface4a47fc5d33f7592675481aea70a2f586134777acd4c6d39945ad50bfda |
| research/abort-envelope-native-entry-v2-20261015/run-entry.sh | 1365 | 530852a4e2fcfc0f0413cb59514c47f4a552bd85 | 732df7d2e7a2ee3be43764214eef3707b431227fddfefbf55e422ef0a1eaa9d3 |
| research/abort-envelope-native-entry-v2-20261015/SELECTION_SA21.json | 1604 | 41faeeec7b6c6299df4cbb78cbd2e6d3ef6d547f | a53e2dbd1e1fba7f919924a4361676fc06a93a694152b358bab295956973821f |
| research/abort-envelope-native-probe-v2-20261015/evidence/envelope-observations.jsonl | 115686 | 99098326c1212757ec5e51447045afa2ed817b6e | 5950cdb86b0ee9e9b898effde9e709b858199e004a6f6a59d6e0c4f2997e2302 |
| research/abort-envelope-native-probe-v2-20261015/evidence/tests.log | 145 | 16a401703ac1b37b1efef3dd9eaf12901b8b4af1 | 42f1c4bf9c5d0d97054b1da419264c1ccf87a45faa232bb20803a19ae03a2cc0 |
| research/abort-envelope-native-probe-v2-20261015/evidence/closure.json | 142 | a9acdec089db08294d569462bf864a3c5693e19b | 0ad936153edecbd88a65af05ad6bab47a10b6d0d40054915c2b4475ef7f261b9 |
| research/abort-envelope-native-probe-v2-20261015/evidence/wrapper-resources.json | 409 | 95b93e32385c47ce3d57dd5e8b94ef260de71d9d | 4a75f1387e03a3d3a748fc6bafc94eedf8b061fb528ff2537eb2c5c7137891cf |
| research/abort-envelope-native-entry-v2-20261015/SOURCE_REVIEW.md | 5987 | d615dcc01a1a428d0a793b8b3b8ecea26167c7c8 | 6a370f2f0a24fa65d26ca4c24c37c491bf7fbfa9765b09e54c62506f21fc2d64 |
| research/abort-envelope-native-probe-v2-20261015/SOURCE_REVIEW.md | 6615 | cb96aa121518131774588183e46f09dcd376bc7b | 3b048121ed37b172ccaed6538767b9e677c2b88c0db653d443ae7eefb8876018 |
| research/abort-envelope-native-probe-v2-20261015/TERMINAL_REVIEW.md | 15744 | d3be681e066a641fe7cf66cf4fc6c79ccea435da | 66be8d8b513f40dfd7620e54494c850e22cae726b8f938ce1b48c1012f4cdd00 |
| research/abort-envelope-native-probe-v2-20261015/evidence/STATE_JOINS.json | 131023 | 905640d5c90ad02911830e08a76daaf63a156f64 | 27bbb9b178e3fab6ef02cb3dfe8bd658e691a514628b7892736ed7c16778e0d2 |
| research/abort-envelope-native-probe-v2-20261015/evidence/audit.py | 32900 | 9580db0c8508e73ad31f40a9bca2dc59a477b281 | a768d3e7086a93b94333dcd4ff4be36091e110737f24da07d1c0ba33c79b3ea4 |
| research/abort-envelope-native-probe-v2-20261015/evidence/AUDIT_RESULT.json | 25495 | 53eb40b3379d6b88f6d580023412c9862ea0e7a0 | 977f39325b6a61a29d5d52e081c4a0e0c8227542b95ecb91f176576a9deee290 |
| research/abort-envelope-native-entry-v2-20261015/ROOT_SELECTOR.py | 3064 | 63ff74082aeae15b824720c5effcffadf81a97d0 | 851ea645a7fe09fb6f0198e3e990d8f05f646d5b61abd2ddf6e5c3bc1a2776f7 |

## Local verification artifacts

The independently authored stdlib-only data verifier completed 1,478 consistency checks. This number belongs to the restore review and is distinct from the published historical audit's 5,124 checks. See `verify_selected_closure.py`, `VERIFICATION_CHECKS.json`, `VERIFICATION_RESULT.json`, `RESTORE_DIGESTS.json`, `FETCH_PROVENANCE.json` and `UNRESOLVED_DEPENDENCIES.json`. The verifier did not invoke or import any restored source.
