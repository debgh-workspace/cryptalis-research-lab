# Pure38 V3: independent terminal evidence review

Decision: ACCEPT_BOUNDED_SYNTHETIC_PURE38_RESULT_ONLY.
Output: persistence-recovery-20261013/forward-aborted-successor-pure-v3-vectors-v1-root-20261016.
External controller capture: persistence-recovery-20261013/pure38-controller-root-20261017.
Controller seal: 072f256d7c965f5a65d0b557404cbe859e07b0f9aae23bb729bee6b2cdf119df.

Independently parsed and reconciled the entire actual stdout object against EXPECTED_RESULT.json fixed fields, using canonical JSON equality to retain boolean/numeric distinctions. All 38 ordered result objects match: 10 ordinary, 26 exact refusals, two disclosed boundary limitations. Every pass/input-unchanged flag is true; failure list is empty. All six authority flags are exactly false. Loaded module list is 38 sorted unique names within the exact 472-name admitted stdlib map.

All 495 admission-before and admission-after records are identical, with matching actual metadata tuples, expected sizes, expected hashes and observed hashes. Exact key set is 490 original pins plus five controls. Original source/vector namespaces are unchanged; independently rehashed all their declared members/seals and all five controls and matched current metadata to receipts. This reviewer reconciled all host-file receipts but did not repeat all host-file body hashes after the run. Current source/vector/control readback is data-only.

Exact argv/cwd/four-key environment match the immutable recipe; shell=false, 10-second deadline and 131072-byte combined bound are recorded. Controller exit 0; child exit 0; 11,626 stdout bytes; empty child stderr and empty outer stdout/stderr; elapsed 0.13318493199767545 seconds. No child error or cleanup error. Terminal after/oracle/namespace/absence/owned-child-terminal checks are true. Output contains exactly the nine declared receipts. Bytecode and python312.zip routes are currently absent.

exit-and-limits.json has intermediate status HOLD because it was written before final admission/oracle checks. It is not the terminal verdict. terminal.json reports PURE38_OBSERVED_PENDING_INDEPENDENT_REVIEW; the independently checked evidence above supports this review's narrowly bounded acceptance.

Evidence SHA256:
- stdout.json: 93fe65bb2de8bc9b80074b5ce7228d4026300024d48e6507135c0ad3a7c2b88f
- terminal.json: 664082abfee544fbf8cbc85c466f1d37d88deefa271ae0c2888cc2121987f719
- admission-before.json and admission-after.json: cc5f3072cf379ee22122a2b9939013bb8c1fee0b9d57ddfde50177bdbc932086

No rerun, controller/component import, compilation, DB/status, Git, private/credential/pyc read or product promotion occurred in this review. This is synthetic pure-component evidence only. Full journal/nested-state decoder, genuine historical producer compatibility, stable native key/snapshot/membership, row transfer/reservation, ACL/catalog/locks/journal mutation, retry/closure/publication authority and full lifecycle remain unestablished. The two limitation cases disclose those boundaries and do not close them.
