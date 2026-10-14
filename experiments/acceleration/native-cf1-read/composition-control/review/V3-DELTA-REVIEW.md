# S v3 focused delta review

2026-10-14, approximately 11:53 UTC. Static source and hash inspection only. No build, candidate/harness import, test or run.

## Disposition

The v3 correction closes the blocking source findings in V2-REVIEW.md for attempted compiler/runtime work. No remaining source-review blocker was identified for the coordinator to select a finite, explicitly bounded build/run scope. This review does not itself authorize execution or establish runtime success. Original full DESIGN, timing, causal backend equivalence, fork qualification and product-adoption gates remain open.

## Verified corrections

- guard_v3 hashes precisely the manifest bytes it parses, returns that digest, and rejects a different manifest when the captured digest is supplied later. Build, launch and successful-entry runtime paths capture an anchor once and use it for post-checks. No guard rewrites files or refreshes expected pins.
- build_v3 and launch_v3 wrap attempted compiler/child work in try/except/finally. Their finalization performs the anchored pin/cache check even when bounded raises, a child fails, output is absent/oversized/malformed, or negative acceptance fails. Primary errors and integrity errors are preserved separately, with integrity failure overriding acceptance.
- build/launch reject missing dont_write_bytecode before importing local guard/supervisor modules. run retains its explicit interpreter/optimization/ABI/-B checks and child receipt finalization. Incorrect argument/collision/initial-integrity rejection occurs before candidate work; these early rejections need not be portrayed as completed test runs.
- supervisor_v3 records signal/reap/pipe/selector cleanup failures independently, attempts remaining cleanup, and marks cleanup errors as failure. Direct-child reaping and group-termination attempts are separate from descendant absence; descendants_verified_absent is explicitly false. This is an honest bounded process-group scope, not verified absence of intentionally escaping descendants. Receipt filesystem failure remains a fail-closed external error rather than a promised persistable receipt under every OS failure.
- v3 reuses unchanged expected data, suite runtimes and observed C source. No outcome-derived expectations or additional candidate behavior were introduced. v3 build/output paths are separate from v2. freeze_v3 excludes future v2/v3 build output from preexisting input pins and includes the preserved v2 artifact manifest and governing snapshot.

## Independently inspected hashes

- PREBUILD_v3.json: 1b7facb755f993473f9ec033d0699dff949125f1f377e66d437899eb2b4b92ad
- guard_v3.py: bf15a6c1134917a48816ef96435652f4406c48687a5f943d52ef8c7f1d1f9a19
- build_v3.py: 06845aec9978cbf02d1b38c19380203bebfeac83303d0ad8d3a529807d66e486
- launch_v3.py: 741688a3e0d8ee0ac5fe44cd50f39964b6716998d40ae5f91044ba3d5d0cfa80
- run_v3.py: 76f4a343f13781cbfee0d7f29cb4c035ee55a951fecbe61e433306ed8ce050e7
- supervisor_v3.py: e5e69f622989ba1815ed6e4b2cfd289a577764e8681c2e5aa439f00504849ef6

These match HARNESS_ARTIFACTS_v3.json. Unselected branch, queue, provider, actual allocation/partial EVP, leak/zeroization and broader containment limits described in V2-REVIEW.md and HARNESS_v3 remain in force. Normal/-O negative controls and positive cases remain future observations, not results of this review.
