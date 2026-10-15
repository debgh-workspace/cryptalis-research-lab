# Narrow paired restore V3 source preparation

V3 fixes only required-directory classification after the preserved V2 failure.
It is unexecuted restore source for independent review. No actual paired restore,
publication, network, product/runtime/test/build, database, environment or live
origin operation occurred. The bounded checks below executed only copied
name/type helper functions against synthetic ordinary file/directory metadata.

## Immutable source and minimal change

- V2 source SHA256: `25a09641fe61a49d212fa8ce90f99a3d65af006ea394969d306da8c15086eee7`
- V3 source: `restore_authenticated_paired_v3.py`
- V3 bytes: 243,303
- V3 SHA256: `60b7666952832ac2e1aba155d70cc1cb38c02968d71a5352c0e3281381640c59`
- `V2_TO_V3_MINIMAL.diff` SHA256: `2f14425231244e293352bf99ff3b16ec1c7858e1b6756e94b4fd81a4f13c8667`

There are exactly three changes:

1. `OUT` names the fresh `async-cleanup-full-source-additive-remote-paired-restore-v2` root.
2. `verify_tree` obtains each entry's actual `lstat` result before context-aware name validation.
3. New `validate_restored_entry_name` admits the exact required directory
   `logical-workspace/workspace/cryptalis-executable/toolchain` only if `lstat`
   shows an ordinary directory and its exact name belongs to the expected
   directory closure already computed from accepted file names. Every other
   entry uses the unchanged generic name gate. Unexpected directories are
   rejected before further processing.

The exception never permits a regular file at the directory name, another
prefix, a case variant, an arbitrary sibling or child, or any new toolchain
origin. The two previously accepted exact inert leaf exceptions are unchanged.
Existing mode0700 directory and mode0600 single-link regular-file checks,
readbacks and final exact file/directory closure checks remain in force.

AST comparison confirms all old functions other than `verify_tree` are exactly
unchanged, including `safe_name`, `nameset`, archive admission, body validation,
paired reconstruction, authentication, I/O safeguards and `main`. All existing
assignments except `OUT` are unchanged. This retains every part/member identity,
limit, count, provenance requirement, base checkpoint pin, the exact 355+516
member admission and 2,386-record restore map, source reconstruction, inert
nested-body rules and all qualification boundaries. No archive or live source
was opened by this V3 authoring helper. No restored or archived code ran.

## Bounded synthetic checks

`test_name_type_classification_v1.py` contains literal copies of only four name
helpers and two deny sets from the new source. The source preparation receipt
pins those copies. It does not import, execute or call the actual restore
program, archive decoder, authentication or product code.

The harness creates one ordinary inert file and one real empty directory in its
own new preparation subdirectory, obtains real `lstat` results, and derives an
expected directory closure from the two exact accepted leaf names plus one
ordinary fixture name. All 18 classifications passed on the first attempt:

- Exact required directory admitted with observed directory type and closure membership
- File-at-directory and absent closure membership rejected
- Both exact inert leaf files retained; neither leaf accepted as a directory
- Arbitrary toolchain sibling/child, unprefixed parent, case variant and extra prefix rejected
- Ordinary expected file/directory retained; unexpected directory rejected
- Raw phase, environment and traversal names remain rejected

Two additional direct checks confirm `safe_name` still rejects the output
parent and unprefixed parent as ordinary file names. No symlink was created and
no exploit test was performed. Source preparation and synthetic runs both exited
0 on their first attempts. Their sources, logs and exits are preserved.

`SYNTHETIC_CLASSIFICATION-v1.json` records all individual results.
`SOURCE_PREPARATION-v3.json` records the structural/source comparisons; its
historical status says tests pending because it was written before the separate
successful harness run. `FINAL_CONTINUITY-v3.json` binds the final source and
successful results. `REVIEW_ARTIFACTS.sha256` seals all files here except itself.

## Execution remains gated

Preserve all prior 43 preparation files, the original seal, V2 source and the
failed suffix-v1 output. `RESTORE_V2_INCIDENT.md` records the exact failure and
the limitation that the original tool-returned streams were not saved as raw
local logs. No success is inferred from the partial output.

Before any retry, independently review this exact V3 source and minimal diff,
verify the original actual-readback provenance and external commit pins, obtain
separate execution authority, confirm suffix-v2 is absent, and recheck the exact
reviewed source hash. Only the coordinator may run the actual restore. All five
existing required CLI arguments and their authentication meaning are unchanged.
This preparation performs no retry and does not publish or relabel any bytes.
