# Preexisting mark semantic observation supplement

2026-10-14. Prepared source only. No compilation, native import or execution authorized by this document. Completed unmarked package remains unchanged.

## Property being tested

The observable property is preservation of a known, test-created mark stack across the copied helper, as judged by later supported public operations. This is not direct introspection of hidden per-entry mark counts. Public APIs expose distance to the nearest mark and the effects/status of consuming it. Consequently, the observation necessarily changes the test-owned mark/queue state after the helper returns. There is no claim to inspect arbitrary marks without disturbing them.

For each fixture, public setup installs sentinel A then B and one of four configurations: mark B once; mark B twice; mark A once then append B; mark A then append B and mark B. Initial marks use ERR_set_mark and require return 1. Queue entries have the same fully public data as the preceding unmarked fixture. All setup starts with an empty queue verified by queue_seed; no unrelated caller queue is cleared.

Following the own helper call, record oldest/newest endpoints. Repeatedly append public sentinel C, record ERR_count_to_mark, call ERR_pop_to_mark, and record endpoints again. After a frozen finite number of steps, drain and record all remaining entries. The final no-mark pop must return 0 and empty the queue for preservation cases. The drain is observation/cleanup of test-owned data, not production queue policy.

Endpoints are explicitly endpoints: a single-entry queue has duplicate oldest/newest records; an empty queue has none. They are not represented as a complete hidden queue snapshot. Distances, pop statuses, endpoints and final drain jointly form the exact semantic trace. Earlier unmarked full-entry evidence is not silently upgraded to marked-state introspection.

## Independent frozen trace oracle

Expected behavior derives from the public setup/probe operations, with distinct no-helper baselines; it is not collected from helper observations. Pinned OpenSSL 3.5.7 source previously inspected by the coordinator uses per-entry mark counters. This makes two marks on B observably consumable twice. No assumption of mark loss is built in.

After appending C, each tuple below is (distance, pop status, remaining sentinel sequence); endpoints in JSON are derived from that stated sequence:
- B once: (1,1,AB), (3,0,empty)
- B twice: (1,1,AB), (1,1,AB), (3,0,empty)
- A once, B unmarked: (2,1,A), (2,0,empty)
- A once and B once: (1,1,AB), (2,1,A), (2,0,empty)

The no-helper baseline for each configuration must match the exact preserved trace. Each configuration also has two active negative controls: explicitly consume one mark or add one extra mark before probing, without invoking the helper. Each must both differ from preservation AND equal its separately predeclared exact altered trace. This checks sensitivity to both loss and spurious retention; an arbitrary exception or unrelated mismatch does not count as a valid negative control.

## Finite matrix and bounds

60 predeclared cases: 4 positive baselines, 8 negative controls, 48 helper observations (four mark configurations times the existing twelve representation/action recipes). Helper recipes: storage success/bad tag/fault1/fault10/fault17; equality same plus wrong search root/fault30. Public frozen Unicode CF1 vectors only. Exact encoded bytes or exact private RuntimeError arguments are required. No new faults, providers, cryptographic inputs, wrapper mapping claims or classifier decisions.

There are at most two preexisting test sentinel entries, at most two preexisting marks in positive cases, three after the extra-mark control, and at most three simultaneously queued test-created entries including C. Probe loops are fixed at two or three steps, never until exhaustion. Native/internal error queue entries are not counted as a proven capacity bound, but no test induces queue exhaustion or resource exhaustion. The copied helper remains unchanged except inherited call-local observation and added public fixture methods. Ordinary helper queue cleanup is not replaced.

After static review, proposed execution is one separately built diagnostic C -O2 binary at Python optimization modes 0 and 1, each with an outer 60-second timeout and exclusive receipts. Do not rerun preparation after freeze. No normal-binary run, settings/provider load/configuration changes, installs, dependencies, service, credentials, network, PG, Git or timing. Build and execution require coordinator clearance after review.

## Limits

Finite semantic evidence cannot certify arbitrary nested mark counts, near-capacity queues, concurrent callers, actual allocation failures, failed ERR_set_mark, helper internal corruption or provider lifecycle changes. Strings/provider metadata retain the preceding diagnostic bounds. Mark getters/probes themselves modify or inspect supported state; no ERR_STATE/internal layouts/private symbols are used. The earlier unsupported loss assertion remains corrected; nothing here predetermines runtime outcomes.

Previously inspected primary references (no network used for this supplement):
- https://docs.openssl.org/3.5/man3/ERR_set_mark/
- https://docs.openssl.org/3.5/man3/ERR_get_error/
- https://raw.githubusercontent.com/openssl/openssl/openssl-3.5.7/crypto/err/err_mark.c
