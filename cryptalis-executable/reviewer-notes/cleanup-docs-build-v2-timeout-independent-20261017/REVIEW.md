# Combined packaging V2: independent timeout-boundary review

Decision: PRESERVE_FAILED_BUILD_RUN; FIVE_COMPLETE_ARCHIVES_ELIGIBLE_FOR_SEPARATE_INERT_VERIFICATION.
This is not whole-build PASS or final packaging acceptance.

The actual parent-receipt.json status is FAIL, child reason timeout, child exit -9 after the 120-second wall bound. Recorded SIGKILL targets the owned group while leader_reaped=false; final leader_reaped=true, cleanup_errors empty, parent file-size limits restored. descendants_verified_absent remains false and is not upgraded by this review. Before/after all six integrity groups agree: packet247, outer3, inputs1929, baseline221, derivative221 with213 original unchanged, candidate221. Host-after exit is0; outer exit is1.

All five build log files name their expected output and all five build stderr files are empty. Shell set-e ordering and creation of empty verification.json/verification.stderr place the reached stage at verifier after roundtrip-wheel. These are completion indications for preceding commands, not invented numeric per-build exit receipts. The verifier produced no completed result; neither its internal stopping point nor complete verification can be inferred.

Independent bounded data-only archive checks confirm:
- Both sdists are complete/readable, directly byte-equal,150623 bytes each, SHA2568850a20e997e998862c7d44273bcaf8e1cf6022d108f59f04f123731ae7af334.
- All three direct/repeat/roundtrip wheels are complete/readable and directly byte-equal,141155 bytes each, SHA256e1f9af85ce3c4e2bc6458d6bf3c1163e227cb2e09fea7365b4d6f7ef52bca28b.
- Complete49sdist/48wheel file inventories match policy. Bounded gzip expansion and TAR member type/path checks precede member reads; ZIP metadata bounds and reads/CRCs establish payload readability. This boundary review does not replace the full canonical archive-header/parser audit required for final acceptance.
- All43 runtime payloads hash-match selected source. Exact comparison against pinned accepted doctor archives permits only _sqlalchemy_transactions.py and sqlalchemy.py in sdist, and those two plus RECORD in wheel. Every other payload is equal, including packaged metadata/config/license/README.
- All48 RECORD rows cover the wheel;47 hash/size entries validate; self row is empty; exactly the two runtime rows differ from doctor.
- All49 current extracted payloads equal the sdist. Rehashed1105 declared leaves across five preserved source trees; every source hash and final metadata tuple remains unchanged. Existing artifact metadata remained stable across this audit. Source conftest was hashed only.

Safe projection CHECKS.json records exact artifact paths, sizes, digests and receipt identity. Parent receipt SHA2565cd5f156971ec8dbeef712ee9fc10f0ca1794a85ca93d76d427a046a9ca2b726. Live host/tool bodies were not reopened; host identity is supported only by existing entry receipts.

Recommended next step: preserve the failed run, its original120-second limit and all completed artifacts. Review/select a separate bounded inert verification-only continuation after fresh metadata/hash admission and genuine quiescence. Bind these five output identities and original packet/clearance/failure evidence; write new receipts exclusively. Reuse the exact approved verifier/parser without rebuilding or changing sealed inputs. Original FAIL must remain distinguishable from any later verification result.

No rerun, rebuild, product/helper import, installation, DB/status, Git, private/credential/marker/pyc read, promotion or publication occurred. No broader source/runtime/native/installed/full-suite/clean-host qualification follows. Seven UNKNOWN gates remain unchanged.
