# Four negative controls and pair summary

Disposition: ACCEPT ALL FOUR OBSERVED NEGATIVE-CONTROL KILLS, within the same-host SA21 scope. Together with independently accepted baseline and candidate captures, the finite literal correctness and specified mutation-sensitivity prerequisites are satisfied. No timing, product promotion, database or wider qualification follows.

Packet runner-v2 seal: 4747b053405eafe60a656f95adda95ea483bc3d3cfd676570517206d0e85059c.
Captures: persistence-recovery-20261013/search-new-sa21-{mutant-stale,mutant-tenant,mutant-point,mutant-null}-20261017-1323.

## Per-capture independent checks

Each has exit.txt=1 and after-exit.txt=0; one terminal JSON, correct variant, status HOLD, tests_run25, no primary type/stage and no test errors. HOLD is the expected mutant correctness outcome, not a bootstrap failure. In each capture the closure key set exactly matches its selected 43-file view, 399 dependencies and six controls; all448 entries PASS. All25 method names occur in each stderr ledger. Packet-before/after and control-before/after compare identical; hash receipts contain only OK. Each reports absent pycache prefix, also absent at review time.

- mutant-stale: five failures. Required test_literal_rebind_tenant_reject_old fails because the operation does not raise AuthenticationFailed. Four single-tenant real-CF1 subcases separately fail exact exception classification (InvalidContext instead of AuthenticationFailed). This is the intentionally behavior-changing old-text/rebound-self mutant, not identity-gate removal alone.
- mutant-tenant: ten failures. Required test_literal_wrong_tenant and rebind-old observer tests fail because tenant checks were bypassed. Eight real-CF1 subcases fail exact AuthenticationFailed classification against KeyUnavailable or InvalidContext. These are operation assertion failures, not test errors or import failures.
- mutant-point: three failures. Required test_literal_wrong_point, test_literal_rebind_points and the additional UUID-record point case fail because the required AuthenticationFailed is absent.
- mutant-null: 21 failures. Required test_real_cf1_context_matrix fails in all eight combinations at the first defective-material NULL check: KeyUnavailable was required but no exception was raised. Thirteen additional observer/method failures detect returning None instead of invoking open_text. Later checks within an already-failed subcase are not claimed to have run; the required real-NULL negative control is nevertheless directly established.

The exact-error helper thus preserves the distinction between wrong operation behavior and genuine setup/import/test errors. No mutant kill is inferred solely from nonzero exit or closure failure.

Root's post-run coordinator classification initially accepted the first three controls, then rejected null because its required-method comparison used an exact name suffix without allowing unittest's explicit subtest parameter suffix. This is a preserved postcheck classification error, not a child test or closure failure, and no test was rerun. Independent review matches the exact method identity test_real_cf1_context_matrix and the eight enumerated equality/uuid_record/single Boolean parameter tuples. It does not accept arbitrary name substrings, unrelated failing methods or any errors. All eight matching null traces fail the literal KeyUnavailable assertion at runner line190 because the operation incorrectly returned normally.

## Resource and entry records

Every capture includes its own exact INVOCATION.txt with selected variant, absolute runner-v2 cwd, clean three-variable environment, stdin /dev/null, timeout TERM60s/kill-after2s, pinned source seal and Python -I -B -S with absent pycache prefix. Readbacks agree: CPU30, VM1048576 KiB, file512 KiB, core0. Two independently capped512 KiB capture files imply at most1 MiB combined; there is no active aggregate monitor. Observed stdout/stderr sizes respectively:

- stale: 73,769 / 15,721 bytes (89,490 combined)
- tenant: 74,366 / 27,830 bytes (102,196 combined)
- point: 73,425 / 6,132 bytes (79,557 combined)
- null: 75,075 / 23,100 bytes (98,175 combined)

stdout and stderr SHA256 respectively:

- stale: 42ec0a3609d789952c00d96b606eb376d6bf626b8db81d96a830664ce3c838cd; 294c16bac1798eae7db9154a92c42e64e6c1b3f80169549e8a12e70aa4d386d2
- tenant: 731af793b249dab2f285a432fe95016fbf8a0bda7139d7ffedf0083a319d231c; 67c3efa9df86a6a87765ddb07b3ae7ab0a5af60177b278ed11b5544777e10db6
- point: f09886e53ab9d882518f8e8d5ecb3e7c4c543acef81073dcf2db441f230bb443; 190e37f0f7dbcb4312b469940df2613261dc0f6aad43d1ba314cdff20b11ba49
- null: 81d10f9f34712099ddb15cbb15773df15ced6156154fa7f4b60ebecef5d2709e; 77dd1c0206d1fdaed7dd69fd96b4a639bd464102aeab885bcd49022d1c3eeb06

## Pair interpretation and remaining limits

Baseline and candidate separately passed the same25 source-bound methods against literal expectations, including actual CF1 with synthetic pre-admitted key material. These four captures establish sensitivity to the specified stale substitution, omitted tenant check, omitted point check and early real-NULL return. This finite result does not prove every possible mutation or input safe, nor cross-host/runtime compatibility.

The baseline's historically recorded4 MiB per-file limit did not enforce the originally proposed1 MiB combined bound; its separate acceptance retains that explicit limitation. Candidate and mutant receipts use512 KiB per-file limits. Do not silently homogenize these resource histories.

Trust remains the existing-host interpreter/stdlib/native-loader boundary. No vendor/native provenance, full loader inventory, hostile-native sandbox, provider preparation/custody, SA20, installed-artifact, DB or performance qualification is added. Any timing experiment requires its own reviewed source/protocol and explicit selection; these unittest durations are not product performance data.

Reviewer performed read-only capture/source inspection, hashes, comparisons and JSON-data reconciliation only. No reexecution or source mutation.
