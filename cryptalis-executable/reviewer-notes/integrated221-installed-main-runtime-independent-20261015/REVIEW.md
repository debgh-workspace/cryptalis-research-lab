# Integrated221 installed-main runtime source acceptance

Decision: ACCEPT_SCOPED_INSTALLED221_MAIN_RUNTIME_SOURCE, 2026-10-15 UTC.

The exact V3 main runtime route and finite freeze are accepted for root's separately selected installed-SA21 run after actual stage binding and quiescence checks. SA20 requires the genuine accepted terminal review of that installed-SA21 run before its separate binding and selection. Optional runtime is outside this acceptance. The reviewer executed no wrapper, prepared helper, project import, collection, test, installation or database command.

## Accepted exact controls

Packet: experiments/integrated221-installed-full-controls-v3-20261015.
Seal: experiments/integrated221-installed-runtime-preparation-20261015/MAIN_V3_PACKET.sha256, SHA256 179e6c8ba812be83116852a6b6ce087d1444557a655e54f5c3760763fd1d61b4. All 30 declared members match.

- ENTRY.sha256 (27 members): 2825dc1673d149c612d424b3bb1d5c757dd5cf65cf1aa64d0a5f173618fda9d0
- INPUTS.sha256 (3024 targets): 67785c91814ecfde44d54852f572d51de9dc2d908c6521e5c62a6680d281d37d
- POSTINSTALL_CLEARANCE.sha256 (112 targets): 9c2ec000ce886bb904c702f783f769cf44aef8ce3b3caba7ee345439e558f472
- launch_cold_wrapper.py: fe7eb1d38cf826c79ecf201a330522f96501d4edc4d40b2f56f779df24f2acbc
- verify_runtime_binding.py: c84e168fd2f9dc5a5e8af943ea52d868f495b542ae00c2e9da47c470d391c861
- assemble_stage.py: dfacbf88e0ffb2e8d34fda355874cfa945d9b0f5140cc9ebbe01daa121ff071a
- run-full-sa21.sh: 4dc0cd2751a0ac8bb6b885ae5a746d188a966b47f18489c158e1d5935f9a99f3
- run-full-sa20.sh: 0b6d30904a1d2fd84a09222ea3d85c4bf914b735221f4c006d221230ee4d7972

Main actual payload review 8b8f86122846f5edfdececf448d4e94b3c8470a73d8275b853c3d73291d25e9d and HANDOFF.json 959b57005e36693f9d1b7f0e8e441d1f96693c5f66d83cd71ebc6d79a8010e7f were independently read and hash-checked. Actual wheel remains dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6; source221 manifest remains 202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520. Actual accepted source-SA21/source-SA20/packaging/payload reviews are bound by roles, not replaced by file existence.

## Complete finite installed identity

After metadata admission, all 3024 unique manifest-union target hashes match current bytes. There are 2506 hashed ordinary installed files, including all 2402 nonproduct files, rather than only the selected 42 convenience pins. Complete dependencies, startup files, metadata and entry points are included. Independent exact namespace checks establish SA21 111 directories/1255 regular files/four links and SA20 113 directories/1253 regular files/four links. Each cell has one exact product-owned uv_cache.json installer marker checked through metadata only and excluded from all payload reads/hashes. No .pyc, __pycache__ or .pytest_cache path exists in the admitted cells. Both full namespace schemas and ordinary/nonproduct maps are unchanged from reviewed V1 to V3.

Product modules match all 43 source runtime modules and the actual wheel. Complete installed RECORD integrity and inode isolation rest on the accepted actual payload audit; runtime pins include the accepted RECORD and all ordinary product payloads. Interpreter aliases/endpoints are explicitly bound, and all installed aliases remain exact. The wrapper's installed-candidate probe asserts package origin under the selected installed sys.prefix and outside candidate source, with source byte equality. PYTHONPATH excludes candidate src in installed mode. This is a bounded entry-origin and file-identity check, not continuous imported-code attestation.

## Bytecode routing and preserved wrapper behavior

The additive launcher requires -B before importing the wrapper's dependencies. It admits and hashes the exact wrapper regular source path, reconstructs its script path/argv context, and uses runpy.run_path with a non-__main__ name. This loads the wrapper .py source rather than consulting a wrapper module-name bytecode cache. It retrieves main and ENV from that namespace, verifies both main's globals and loaded run_baseline share that exact ENV, requires its original four-key schema and adds only PYTHONDONTWRITEBYTECODE=1. It invokes main exactly once. No test arguments, role probes, plugin routes or subprocess hooks are changed.

Wrapper, corpus helper, baseline runner, progress plugin and dual-role preflight identities remain unchanged. Their existing bounded startup/import limitation remains explicit; this acceptance is not a complete stdlib/host process map. Wrapper child Python processes receive the shared fixed ENV; package-capable test subprocesses inherit its bytecode suppression. The two existing native deprotection workers at test_deprotection.py:299/306 use -I -S, intentionally ignore PYTHON* settings and assert Cryptalis is unavailable. Root explicitly selected that package-free exception; possible stdlib cache behavior lies outside the cold installed-cell proof. Their test code and assertions remain unchanged.

The runtime guard admits exact directories, regular names and aliases before any expanded installed hashing and repeats after the wrapper. Every new cache or other unlisted installed path fails closed. No cache body, raw phase JSON, ambient environment, secret or credential was read by this reviewer.

## Stage and execution gates

The data-only assembler may be selected separately under pinned Python -I -B. It requires external ENTRY/INPUTS/POSTINSTALL hashes, this report's actual hash and explicit coordinator semantic-verdict confirmation. It admits packet/reviewer files, does not expand INPUTS payload reads and creates only fresh stage binding/clearance files. SA20 additionally requires the actual accepted installed-SA21 terminal path/hash/verdict. Root must verify that predecessor's semantic scope; a generic ACCEPT token alone is not such proof. Failed binding outputs are not overwritten.

Each root entry takes exactly one actual binding digest. Guard identity is checked before interpretation; before-pins, source221/packet archive, one unchanged guarded wrapper invocation, and independent after-pins follow. A nonzero wrapper exit is preserved; a successful wrapper cannot hide a post-pin failure. Root is sole database executor, with external quiescence, exact entry capture, independent before/after pg status and 26-corpus restoration checks. Existing lock, role preflights, explicit stop and corpus wrapper remain mandatory. Entry never chains another stage.

SA21 destination is evidence/integrated221-installed-full-sa21-v3-20261015 and packet/run/sa21; SA20 equivalents use sa20. Both were absent during source review. Shell and JSON routes agree. Compared with V1, shell differences are only packet paths, guard digest and the required fresh evidence destinations. Test selection, preflight/wrapper logic and argument tails are unchanged. Both exact outcome TSVs, MAIN2684_NODE_IDS.txt and SA20_SKIP_ALLOWLIST.json equal the accepted full-source controls byte-for-byte. Required outcomes: SA21 2684 ordinary PASS, zero failure/skip; SA20 2638 ordinary PASS and exactly 46 documented native-version skips; 56 passing subtests separately in each. No historical seven-failure or exit1 waiver is admitted.

## Preserved incidents and limits

V1 is held for its newly introduced unqualified wrapper module-cache execution path; V1_HOLD.md SHA256 c823a7dcf5d5a889150f6b22352f44a09a0360c508b50205538ebd9e1bcc7b61 remains. Author V2's missed relative constants were caught statically and preserved; V3 corrects both guard/binder packet roots. No helper or runtime was executed in those attempts.

Reviewer chunk2a8358 failed its normalized shell comparison because it omitted the required fresh V3 evidence destination. Root authorized inspecting that exact diff and correcting only that comparison. The SA21 and SA20 differences were inspected; corrected chunk155be0 passed with no test-selection, role-preflight, wrapper logic or expectation changes. Chunkcdfe64 independently passed all 3024 ordinary hashes and unchanged maps. These comparison failures are retained, not retroactively claimed as initial passes.

This admits exact main source/runtime selection conditions, not a runtime result, optional stage, promotion or release. Same-host copied dependency provenance and startup limits remain; original dependency artifacts are unavailable for clean-host proof. All seven broad product gates remain UNKNOWN. Live reviewer read boundary is closed; root may bind and select SA21, then request independent terminal audit before any SA20 run.
