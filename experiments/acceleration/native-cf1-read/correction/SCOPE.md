# Native CF1 correctness correction slice

2026-10-14. New isolated public-fixture correctness slice. Original prototype files, binaries, source hashes, receipts, failures, and audits are immutable inputs. No native recompilation, old test rerun, performance measurement, product source change, product monkeypatch, dependency install, database, Git, or key-provider service access is authorized here.

The finite predeclared manifest selects 43 positive/refusal observations and one expected-failure actual-output negative control, each at Python optimize=0 and 1:
- Eight recomputed table-derived descriptor relocations, all representation/record/tenant combinations.
- Sixteen policy-domain mismatches, valid and malformed frame, all eight modes.
- Six genuine tenant-and-record A/B/A reads, storage/equality; two NULL observations in the same sequences. Research-wrapper counters check one native call per non-NULL successful read and zero for NULL.
- Six lifecycle observations: same PreparedKeys succeeds, its existing material is expired, same frame/same PreparedKeys refuses, then freshly constructed public PreparedKeys succeeds; both representations.
- Three expiry injections after successful strict decode but before final resolution: storage payload, equality payload, equality search.
- Two simulated PID changes immediately after native return, both representations.
- One actual native-returned string is changed before the downstream strict comparator. This run must exit with the exact mismatch, not PASS. Before changing it, the fixture's actual output is verified exactly. Both O0/O1 must reject the changed returned value.

Every observation compares exact text or full safe exception fields (class, code, stage, retryable, effects, remedy, operation presence) and exact resolution trace. Operation identifiers are required but never compared byte-for-byte. The expected records, case IDs, exact UTF-8/text values and fixture hashes are frozen before the first candidate execution. Correctness observations enforce the complete ordered list.

Synthetic public PreparedKeys and controlled expiry/PID mutation qualify consumption-boundary behavior only. Post-decode injection uses a research-only bytes subclass whose decode calls strict built-in decoding then expires the selected material; the real C helper still returns exact bytes. The hook is installed only in the separately named research wrapper and always restored. PID change is simulated; the original evidence's actual fork test is not rerun. These are not provider-custody, threading-race, async-cancellation or memory-erasure proofs.

Full DESIGN correctness and all timing remain HOLD: this slice does not add primitive/intermediate-value diagnostics, native allocator/leak accounting, full native fault-mapper parity, packaging/platform/provider qualification, or product admission. Existing stage/cause ambiguity, omitted pyca calls, and different backend limits remain unchanged.
