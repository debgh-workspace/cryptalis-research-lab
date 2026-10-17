# Minimal additive publication selection: 40 files

Use SECOND_BENCHMARK_ADDITIVE_INVENTORY.json, not the earlier272-file superset, for the requested small additive publication. It lists38 existing files with exact sizes/SHA256, plus this README and the additive inventory itself:40 files total. Existing payload is1,409,617 bytes. No source, capture or archive was repackaged and no Git write/publication was performed here.

## Exact additive set

The inventory's files array is the explicit38-path payload list:

- Seven changed benchmark members: SOURCE.sha256, benchmark.py, reduce.py, VIEWS.json, PLAN.md, CORRECTNESS_BINDING.json and candidate sqlalchemy.py.
- Sixteen raw stdout captures, indices0–15.
- Ten capture-root entries: CAPTURE_MANIFEST.json, reducer/stdout.json, resources-before.txt, resources-after.txt, QUIET_WINDOW.txt, reducer/exit.txt,0/exit.txt,0/stderr.txt,schedule-elapsed.txt,schedule-exit.txt.
- Four independent reviews/recomputations: successor benchmark source review, second benchmark terminal review, successor candidate correctness terminal review, second benchmark recomputation JSON.
- The exact one-line candidate.diff from fallback-order-v1.

Publish only these38 plus this README and the additive inventory if root selects. The272-file full inventory is a local audit aid and is not part of this40-file set. No duplicate baseline tree is included.

## Exact immutable dependencies, verified by remote text comparison

Repository debgh-workspace/cryptalis-research-lab:

1. Commit de70fdd0e747051d29d883bddb4ffd5820491840, recovery-work/search-next-slice-20261017/runner-v2/DEPENDENCIES.json, SHA2566e46df3839a262b6855efba632c1a0445685a9469f93ea049ba36e14d5422823. Restore these identical bytes as successor DEPENDENCIES.json.
2. Commit a7d75f002b40c757705d4de509ba577a5452c85e, recovery-work/search-next-slice-20261017/benchmark-v2/WORKLOAD.json, SHA256c518ceb007b13587dc429bcf892da848d19a03ebbb45557eaa8e227dcca75119. Restore identically as successor WORKLOAD.json; thresholds/counts remain unchanged.
3. Commit194ace1c5c9e6da8bf795847603e441e93b0ad00, recovery-work/search-next-slice-20261017/runner-v2/views/candidate/src/cryptalis/sqlalchemy.py, SHA2565393819f2f312b9196bd2ffe185713d7d8ce6487eeb0b55b1b4e50cc7baa8395. This is the predecessor for the one-line delta, not the successor. Successor full file is included in the additive set at SHA2565ec115163c8c53ba01c34613a9140b4506cd3a38a8280224ea9c21f032743f6a.

## Reconstructing omitted source views honestly

The source views are not claimed to exist as individually published remote files. Restore source221 by the already accepted focused-archive+overlay relationship recorded at commit e980e4a19a86ed1cc9c199075495726aeac3354a, cryptalis-executable/recovery-work/restore-combined221-20261017/run/RECEIPT.json. Archive parts commit2b5124c47e6b3188f22282af547bdc330eca8abb; compressed archive1f76f9bf50e7e757430edfe45b5ecb81afee67283675f2465c0d0b102f05822b; raw tar8e6c5233a98295872d30cd45bb5c79c27dda6e233ba20eb87497436c8caac50d; overlay commit eed4482d824c87004c6df280a038f0b24ac17d8d; combined221 manifest e8a69b212e8a1759e7641d6bb1227a3aa728e76badd515a54421d98811e5552c.

The additive inventory retains the exact admitted remote input paths/hashes from restoration INPUTS.json, plus85 explicit target-to-restored-source aliases with per-file sizes/hashes. All85 aliases were compared locally byte-for-byte. Copy only those43 baseline and42 unchanged candidate source bodies, then use the newly included candidate sqlalchemy.py. Together with seven changed packet members and the two immutable remote controls, this reconstructs all94 packet files without publishing duplicate views. Verify the complete93-member SOURCE.sha256 seal d176ed1773d01d731dca7c8406a04ed552e692ba6ae159ae36c962a57a7daeec afterward. No restoration operation was performed for this inventory.

## Reduction and receipt restoration

The64 manifest inputs consist of16 distinct raw stdout bodies plus48 empty-stderr/zero-exit/zero-after-exit bodies. The additive set includes actual0/stderr.txt (empty) and actual0/exit.txt (ASCII0 plus newline). The inventory records46 exact hash/size-verified aliases for the other identical members. These are byte-preserving restorations of previously reviewed receipt bodies, not fabricated new execution evidence. Retain explicit alias provenance; do not describe the aliases as separately transported receipts. Reducer exit1 is included separately. The original exact CAPTURE_MANIFEST.json can then be verified and arithmetic reduction reproduced from its full64-file read set. No reducer rerun is selected here.

This minimal set does not individually publish all16 invocation/resource/metadata receipts or the full successor correctness packet/raw capture. Their independent reviews are included; the omitted original bodies remain local and their omission must be disclosed. A complete raw-control-receipt transport would exceed40 files. The selected40-file set is sufficient for raw timing arithmetic, exact source reconstruction and preserved review conclusions, not independent reconstruction of every historical resource-control observation.

All absolute paths remain bound to /workspace/scratch/cb28ee9f5f4a. Relocation needs a separately reviewed versioned binding; do not silently edit frozen controls while retaining old seals.399 dependency/native bodies and host runtime are excluded; reconstructing source and data does not recreate or authorize execution of that environment.

No private environment dumps, credentials, Git internals, caches, bytecode, dependency bodies or DB data are in the proposed plaintext set. Result remains integrity accepted/performance HOLD28flags; all128 samples are retained. No speedup, promotion or causal predecessor-versus-successor claim follows.
