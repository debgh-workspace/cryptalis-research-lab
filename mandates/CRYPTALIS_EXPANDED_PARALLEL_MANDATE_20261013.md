# Cryptalis — Expand Parallel Agents and Accelerate the 72-Hour Sprint

The three existing agents are making progress. **Increase parallelism substantially to accelerate completion before 16 October, 6:06 PM IST.**

I authorize additional Dot-native background agents within the existing approved environment.

## 1. Increase agent count

You currently have three workers plus one coordinator.

**Target six worker agents initially, then expand toward eight if the platform and resource measurements permit.**

Do not assume six or eight agents are technically available. Inspect your actual agent-concurrency limits and spawn the maximum useful number supported.

Do not use external paid APIs, Codex cloud environments, additional separately billed services or unapproved computing infrastructure.

Current shared capacity:
- 9 CPU threads.
- Approximately 9.7 GiB RAM.
- Approximately 25 GiB available disk.
- One approved PostgreSQL cluster.

Agents are not required to run expensive tests simultaneously. Many can independently inspect code, research mechanisms, design corrections, write tests and prepare candidate patches while another runs PostgreSQL verification.

Avoid duplicated research, resource exhaustion and unnecessary database contention.

## 2. Expand the existing workstreams

Preserve the current agents:

- **A — ORM/backend compatibility:** Bulk operations, cascades, native SQL semantics, FastAPI integration and transaction correctness.
- **B — Reversible lifecycle:** Decrypt-back, legacy recovery, schema preservation, key rewrap and rotation.
- **C — Search/security performance:** Query optimization, stronger searchable encryption, leakage and benchmark analysis.

Add independent workers:

- **D — Online migration and parallel backfill:** Research and prototype safe concurrent-write capture, backfill, verification, fencing, short cutover and crash recovery.
- **E — Adversarial security and independent verification:** Inspect integrated candidates for security defects, design independent test oracles, find missed edge cases, and perform variant analysis. Do not approve your own code without separate verification.
- **F — Developer experience and framework integration:** Manifest-first setup, minimal-change real application adoption, SQLModel/Django/Flask compatibility, `cryptalis doctor`, installation and removal workflows.
- **G — Production key custody and release engineering:** AWS KMS integration research, key-provider faults, reproducible builds, supply-chain controls, packaging, operational runbooks and qualification evidence.

If fewer agents are supported, prioritize D, E and F, and reassign G's work according to the critical path.

## 3. Use the existing resources intelligently

- Give every worker an isolated source copy or worktree and separate branch.
- Do not let workers make conflicting changes to shared files.
- Keep PostgreSQL tests serialized unless you can prove another arrangement is safe within the existing authorization.
- Schedule expensive full-suite tests centrally.
- Allow lightweight research, code analysis, test design and documentation to continue concurrently.
- Monitor CPU, RAM, disk and agent queue time.
- Reduce concurrency if contention makes total throughput worse.
- Do not duplicate heavy dependency environments unnecessarily.

The target is **maximum verified progress per hour**, not maximum agent count.

## 4. Central integration authority

The coordinator remains responsible for the authoritative integrated candidate, build checklist, GitHub persistence and full regressions.

Workers submit independently tested changes. The coordinator must check interface compatibility, native semantics, security invariants and cross-workstream interactions before promotion.

Continue from the latest remotely verified checkpoint. Do not restart completed work or lose the existing isolated fixes.

Prioritize integration of the newly reproduced decrypt-back and ORDER BY corrections after their remaining tests pass.

## 5. Accelerate without reducing scope

All Cryptalis objectives remain mandatory: advanced searchable encryption, stronger confidentiality, native compatibility, complete lifecycle, online migration, high performance, minimal application changes, diagnostics, key management and seven independent production qualification gates.

Research aggressively, but convert verified research into integrated working software.

Use finite acceptance criteria. Stop unnecessary repetition. Do not merge unverified prototypes or weaken safeguards to meet the deadline.

Update `CRYPTALIS_BUILD_CHECKLIST.md` after every completed slice and preserve the evidence in the private GitHub research repository.

## 6. Report the expanded execution plan

Immediately report:

1. Maximum supported concurrent native agents.
2. Number of additional agents successfully launched.
3. Final worker assignments and their current tasks.
4. Estimated memory/CPU usage and expected bottlenecks.
5. Which critical-path activities can genuinely run concurrently.
6. Whether additional parallelism is improving completed work per hour.

Continue sending verified engineering checkpoints.

**Do not wait until the next 24-hour audit to expand the team. Scale up now, within verified platform and resource limits.**

Our objective remains the strongest possible complete, integrated and independently defensible Cryptalis product by the 72-hour deadline. Missing external audits or unfinished requirements must remain explicitly visible, never declared complete without evidence.
