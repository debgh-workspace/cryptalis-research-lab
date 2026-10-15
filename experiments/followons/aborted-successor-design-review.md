# Aborted-forward successor: independent source-design review

## Verdict and boundary

ACCEPT THE DIRECTION FOR AN ISOLATED PROTOTYPE, subject to the exact constraints below. This is a source/design judgment, not implementation admission, launch permission, a test result, or full recovery qualification. Do not modify the selected Integrated221 preview or its v0/v1/v2 wire contracts.

Prefer a fixed-size authenticated lineage summary with bounded-memory traversal over an embedded bounded list of ancestors. A fixed list eventually makes another safe forward abort unrecoverable through this route. No history pruning, journal rewrite, automatic fallback, or forced finalization is an acceptable response to that limit.

The recommended design introduces one forward/reverse format pair. It changes no journal SQL columns, role, ACL, credential, cluster, or automatic retry behavior. It does require explicit new journal-state metadata on newly created operations. Never add that metadata to historical rows.

Source checks confirm the initial finding: ordinary plan rejects an existing journal (migration.py:360-362); expansion unconditionally creates it (626-672); abort retains the operation and changes phase to ABORTED (881-900); reverse planning/removal recognizes only aborted reverse attempts (deprotection.py:163-169, 558-567). Both comments and designation dispatch are exact-format checks. The source is a research prototype; all broad qualification claims remain outside this review.

## 1. API and scope admission

Proposed API: add the explicit optional keyword pair aborted_predecessor and predecessor_pin to the existing forward planning family. Supplying either requires both. Ordinary plan retains its existing-journal refusal. A standalone convenience entry point is acceptable if it delegates to the same compiler and admission path; no second transition engine is needed.

- aborted_predecessor is the exact host-authenticated MigrationPlan bytes. Parsing or possession of a plan does not authenticate it. predecessor_pin is the host's current authenticated pin for that exact artifact/target, supplied outside the database. Require PREPARED for this route, matching existing repeat-abort admission. Do not introduce ABORTED as a new automatically accepted publication phase.
- Prove a durable row exists. A no-journal/unstarted plan uses the existing fresh replacement route. A missing predecessor row is not an aborted operation.
- Require exact target_id, native target tuple including database and maintenance owner, journal_schema, runtime_role, and the same ordered compiler declaration/model scope. Keep domain, table/field identities, mapped columns, context codecs, tenancy declaration, original ordinary schema, reader set, representation, queries and leakage intent unchanged. Compare canonical values; Python bool/int aliasing must not admit a different representation.
- Recompile from the present native schema and current rows. Revalidate writer inventory, domain reviews, mapping, routine admission, runtime privileges and costs. Allow fresh host observations and estimates without changing declared protection scope. Do not use this route to rotate existing tenant policy/provider fingerprints; compare retained tenant fingerprints. The first prototype may keep the existing tenant universe and must label broader tenant-set changes unverified.
- Current comments and designation may legitimately differ from the old artifact after abort. Inventory them afresh while original native objects still exist. Do not compare old NOT_INVENTORIED status to a guessed false flag. Changes after this new proposal must refuse before effects.
- Reject PENDING/ACTIVE/DEPROTECTING, reverse-abort substitution, residual predecessor staging/guards/dependencies, owner/ACL changes, wrong target, missing or extra journal rows, malformed state, and unsupported historical format. No old cursor, scope, verification result or discarded ciphertext is resumed.
- Produce a fresh operation ID and exact v3 digest. Execution requires a separately published fresh PREPARED pin. Plan construction never advances external policy and never treats a database digest as approval.

The existing advisory identity hashes the ordered table list, not a newly sorted set. Keep the exact admitted ordering for this slice or separately reconcile lock identity across old and new executors. Changing lock derivation silently is unsafe.

## 2. Exact proposed wire/state schema

Proposed exact format names:

- cryptalis.transition/retained-native-comments-cluster-aborted-successor-research-v3
- cryptalis.reverse/retained-native-comments-cluster-aborted-successor-research-v3

Forward v3 has exactly the existing v2 top-level fields plus aborted_forward. No historical artifact is relabeled. v3 is used only by the explicit successor route; an ordinary fresh plan can remain v2.

aborted_forward has exactly these fields:

    schema: "cryptalis.aborted-forward-lineage/research-v1"
    root: {format: <exact admitted v0/v1/v2 forward format>,
           operation_id: <canonical nonzero UUID>, plan_digest: <lowercase SHA-256>}
    predecessor: {operation_id: <canonical nonzero UUID>, plan_digest: <lowercase SHA-256>}
    count: <positive exact integer>
    digest: <lowercase SHA-256>

count is the number of durable forward-ABORTED ancestors, including the root and immediate predecessor, excluding the new operation. It is not an execution permission or a database-selected generation. Existing integer grammar remains 0..2**53-1. Use no small hard-count limit. This is finite machine representability, not mathematical infinity; disclose exhaustion rather than wrapping or pruning.

The newly inserted forward journal state contains its normal phase/models plus aborted_forward, byte-equivalent under canonical serialization to its approved artifact. Retain that member through all phases and safe abort. The historical root row receives no additions. The current operation ID must differ from every ancestor. The SQL table remains (operation_id uuid PRIMARY KEY, plan_digest text NOT NULL, state jsonb NOT NULL).

Forward/reverse dispatch changes must be explicit in MigrationPlan, DeprotectionPlan, comments.enabled/status/reverse_format/validate_forward/validate_reverse, designation.enabled, any legacy classification that dispatches by format, and exact-format test helpers. v3 inherits the existing comments/designation inventories, validation and late checks. Unknown formats remain refusals; no startswith or generic latest-format fallback.

Reverse v3 retains the source_plan/source_pin and normal reverse layout/version 101 behavior. For this format only, replace the list-valued retirable_aborted member with a distinctly named retirable_aborted_reverse summary:

    schema: "cryptalis.aborted-reverse-set/research-v1"
    count: <nonnegative exact integer>
    digest: <lowercase SHA-256>

All old reverse formats keep their exact retirable_aborted list and old parser semantics. Do not silently reinterpret that name as forward ancestry. The embedded authenticated source_plan already binds the forward history. Do not duplicate an ancestor list or recursively embed predecessor plans.

Changing the v3 reverse field requires a new exact-key schema and an updated reverse-envelope proof. Removing the old 1 MiB history-list reservation for v3 is justified only by accounting for the exact fixed-size replacement and all existing active-schema/readiness/role/rate reservations. MAX_DOCUMENT_BYTES stays 16 MiB. The source artifact is embedded once, including its fixed history summary.

## 3. Canonical commitment and bounded verification

Let C be the existing canonical UTF-8 JSON encoding: ensure_ascii=False, sorted object keys, compact separators, no NaN. All UUID strings are lowercase canonical UUIDs, all SHA-256 strings lowercase 64 hex characters, all object member sets exact. A digest input is an unambiguous canonical JSON array with a versioned domain string. No delimiter-concatenated free text.

Derive a scope digest S from canonical target_id, target, journal_schema, runtime_role and the unchanged protection declaration/models/readers/database/profile. This is derived from the authenticated artifact, not a new database authority. It deliberately excludes refreshed comments, designation, current row scopes, estimates, and host evidence text.

For forward history, define:

    H0 = SHA256(C(["cryptalis.aborted-forward/seed-v1", S, root]))
    T(row) = SHA256(C(row.state))
    Hi = SHA256(C(["cryptalis.aborted-forward/row-v1", S, i, H(i-1),
                    row.operation_id, row.plan_digest, T(row)]))

The canonical order is root first, then each unique immediate successor, oldest to newest. Every committed row in this history is phase ABORTED. The summary for a new plan with n ancestors stores count=n, digest=Hn, predecessor=the nth row. T binds the entire terminal state, including the exact predecessor metadata and old progress fields. It does not authenticate that state by itself.

The first predecessor uses the supplied exact historical forward artifact. Validate its compiler lock and exact target/scope; require the complete journal to be its single matching durable ABORTED row and require the ordinary source/absence of staging. Reject reverse source/link/layout members in this historical forward root. Compute H1 from that observed terminal row. No claim is made that a JSON phase alone proves genuine execution: host trust and the independent producer campaign supply the separate provenance boundary.

For a later predecessor, first validate its old approved aborted_forward summary against the journal. Verify its own terminal row carries exactly that summary, then append its complete terminal row into the new Hn. Its predecessor artifact authenticates the old prefix; the newly approved artifact authenticates the extension. Old artifacts need not be embedded or loaded recursively.

Bounded-memory validation can walk newest-to-oldest using the primary key:

1. Begin with the authenticated expected count, digest, root and predecessor reference.
2. Read exactly that referenced row. Check digest, strict state shape, phase ABORTED, and the expected prefix count/root. Canonicalize/hash the full bounded state.
3. For a nonroot row, its approved-prefix summary is inside T(row). Compute the expected Hi from that prefix and compare to the currently trusted Hi before following the link. Require the prefix count to be exactly i-1. Then follow its immediate predecessor.
4. At i=1 require the exact root reference and H0. No ancestry metadata is synthesized for that old row. Each counter strictly decreases; a repeated node, cycle, reordered link, gap, or fabricated prefix cannot pass. No visited-set accumulation is needed.
5. Count the full journal under the same snapshot/lock and compare the exact expected total, including the explicitly admitted current/reverse rows. Primary-key uniqueness plus the complete authenticated chain establishes exact membership, not merely a subset. A foreign or competing sibling row makes the count/partition fail.

Do not execute SELECT ... .all()/fetchall() over history or allocate an ID/digest set proportional to all attempts. The point-read walk uses O(maximum admitted row state) client memory, O(n) queries/work, and retained O(n) database history. Database time, storage and round trips are not constant and must appear in costs. An iterator over a normal fully buffering driver result does not prove streaming.

Before fetching a whole state, inspect its serialized octet length and type. For the isolated prototype, a 16 MiB raw-state transfer ceiling and the existing canonical/depth grammar provide a finite per-row bound, separate from the unchanged 16 MiB artifact limit. Oversized historical state is an explicit no-effects scope refusal, not permission to truncate. For new rows, prove a worst-case state envelope at expansion, including later counter widths/verification/lineage, so a newly introduced budget cannot strand an otherwise safe abort. If that envelope cannot be proved, stop implementation selection at this blocker. Do not retroactively impose a failure during abort after admitting an expansion that can exceed it.

A more general chunked state canonicalizer can replace this per-row restriction later, after review. Do not invent PostgreSQL extensions or make server-supplied hashes authoritative to avoid the memory problem.

Aborted reverse history has a separate domain and order. Seed its hash with S and the authenticated active forward operation ID/digest. Stream only its validated aborted reverse rows in ascending native UUID order (equivalent to canonical UUID-byte order), and fold [domain, index, prior_hash, operation_id, plan_digest, T(row)] with a distinct reverse row domain string. Bind the exact final count and digest in the reverse artifact. Every row must still have phase ABORTED and source_operation_id/source_plan_digest exactly equal to the active forward source. Fixed-format summary cannot replace these semantic checks.

This avoids growth in both v3 artifact history fields. A bounded old reverse list would otherwise leave a separate repeat-abort/removal exhaustion point. No old-format reader is required to accept v3.

## 4. Atomicity, locks and exact membership

Validate the journal relation itself before relying on row count or the primary key: exact ordinary relation/columns/types/NOT NULL/PK, expected owner, compatible existing privileges, and absence of unexpected rules, triggers, RLS or dependencies that could change reads/writes. Refuse altered structure; do not repair it or broaden ACLs. The old owner/privilege helper alone is not a complete physical-journal validator.

Planning remains no-effects. Use a consistent read-only snapshot for ancestry and rowset observations; recheck compiled native facts in that observation. A schema change or racing operation may cause a typed refusal. A coherent plan still requires execution-time revalidation.

For mutating entry points, acquire the existing same-scope advisory lock, then sorted transition table locks, then the journal table lock in one documented order. SHARE ROW EXCLUSIVE on the journal is a sufficient candidate to exclude concurrent row writers and structural DDL while retaining readers; inspect interactions before implementation. Row-level FOR UPDATE alone does not exclude an inserted sibling. Do not silently reverse lock order relative to existing transition code.

Inside the same transaction, after all locks and before effects:

- recheck target, owner/runtime/journal permissions, exact relation structure, current native metadata, expected history and rowset;
- for unstarted forward v3, require new PREPARED pin, own row absent, exactly the bound ABORTED forward ancestry present;
- reuse the journal relation without DROP/CREATE/RENAME/GRANT/REVOKE, insert only the new row, and create only the new operation's staging/guards;
- preserve every predecessor operation ID, digest and full terminal JSON state; transaction failure restores the prior ordinary schema and exact predecessor rows;
- any already inserted sibling, even one that later ABORTED, invalidates the stale proposal. The host must inspect and propose a successor of the actual terminal head; never auto-select a new head.

Do not weaken generic missing-own-row behavior. Only v3 with authenticated exact lineage and PREPARED pin may be unstarted in an existing journal. Missing own row at a later pin remains restore/missing-transition refusal. Old ABORTED apply remains operation_aborted, old repeated abort stays idempotent under its old contract, and no call writes an old row merely to add lineage.

On forward resume, verify its own stored prefix equals its artifact and validate immutable forward history before effects. Old completed abort calls should remain harmless after later successors; do not require their historical prefix to equal the entire newer journal just to return ABORTED.

On reverse planning/expansion/resume/removal, partition the whole journal into exactly:

1. authenticated ABORTED forward ancestry of the active source;
2. that one active source row, with the existing phase expected at that stage;
3. the exact separately committed aborted reverse set linked to that source;
4. the current reverse row, when it exists.

No category may overlap. Sum and validate exact membership, not only known IDs. At reverse expansion the source is ACTIVE; the existing atomic insertion/source-to-DEPROTECTING pairing remains. At removal require the existing source DEPROTECTING/current PLAINTEXT_ACTIVE linkage, native ordinary schema/readiness and explicit removal proof. The final DROP TABLE occurs only at the existing approved removal stage, with no CASCADE. Forward ancestors are retired there, never as a planning prerequisite.

Keep completed aborted reverse idempotence when a newer reverse owns the source. A v3 history check must not accidentally restore the old bug covered by test_reverse_predecessor_consistency.py.

A lost reply is UNKNOWN until original transaction terminal state and the exact intended-primary marker/native state are inspected. This design creates no retry permission, journal repair, or cross-service atomic publication claim.

## 5. Minimum new deciding evidence

These are proposals only; none ran in this review.

1. Genuine historical root: separate frozen v0/213 and v1/218 producer processes reach real EXPANDED, BACKFILLED or VERIFIED, commit abort, and hand off exact artifact/digest/journal after disposing pools and proving old backend absence. Selected v2 is an additional root case. No rewritten fixture format counts as historical production.
2. RED: selected public fresh plan after genuine durable abort refuses existing_transition_requires_inspection and preserves a complete independent native snapshot. No-journal/unstarted replacement remains a distinct read-only positive control.
3. Current-data/metadata positive: committed native insert/update/delete after abort; Unicode, NULL, tenant/scoped uniqueness; standalone, constraint-backed and unaffected indexes. Independent expected rows and catalog observations must not call product _facts, comment or lineage helpers. Inventory a native comment/designation edit before planning; refuse a late edit after planning. Continue protect, attached current edits, decrypt-back, package-free native workload and approved removal.
4. Repeatability: at least root -> successor abort -> successor abort -> active successor, then reverse abort -> new reverse -> final removal. Reconstruct plans in independent consumer processes. Old rows remain byte/semantic-identical throughout; current IDs differ. Establish history memory does not grow with attempt count using controlled synthetic metadata plus at least one real multi-abort path, not a single short happy path.
5. Atomicity and sibling race: real native DDL failure after first-table expansion rolls back all new rows/staging while native writes still work. Two independently proposed successors of one head cannot both start. A late sibling, missing/interposed ancestor, wrong digest/terminal state/prefix/count, branch/cycle, wrong root/target/pin/scope, reverse substituted as root, malformed journal, or ACL/dependency drift refuses without further effects.
6. Bounded proof: exact 16 MiB artifact/reverse-envelope edges, per-state transfer/depth limits, state-envelope guarantee for later abort, no history .all()/set accumulation, exact integer/UUID/digest/unknown-key rejection, and no logging of artifact-native free text.
7. Reverse regressions: existing source-link corruption cases for every staged reverse phase, completed old reverse abort while a newer reverse owns the source, reverse policy drift with committed prefix retained, and unreviewed-row removal refusal. Add the same cases with forward ancestry present and mutate a terminal forward ancestor after the reverse proposal.
8. Sensitivity: omit predecessor artifact binding; omit terminal state digest/prefix validation; omit exact total/partition; omit journal insert exclusion; omit late metadata recheck; omit forward-ancestry removal membership. Each mutation must be killed by its corresponding independent observation, not merely by parser failure or generic exception matching. No unrelated completed campaign needs rerunning just to relabel it.

Qualify each established SQLAlchemy cell and the exact installed successor later, under separately selected runtime/corpus/freeze/stop conditions. A source design cannot establish concurrent lock behavior, true driver streaming, native identity retention, or package-free removal.

## 6. Existing evidence and helper authority

Precisely retained old-test meaning:

- test_safe_default_legacy.py:135-145 is unstarted replacement before a journal, not durable-abort recovery. :150-167 is pre-switch refusal plus abort; no fresh plan follows the durable abort. PREPARED can have no durable row.
- test_migration.py:573-584 checks native values/write and repeated abort, not replan/reprotect.
- test_deprotection.py:411-425 checks aborted reverse retry/removal, not forward ancestor adoption.
- test_reverse_predecessor_consistency.py checks source row/link refusal and the completed-old-abort/new-reverse exception. Its snapshot helper uses product inspectors, so the new independent native oracle must not inherit that dependency.

The existing test_deprotection.retire_old_role helper is a privileged operator action, not product behavior. Source shows create_role=False but grants on fixture schema/tables, revokes old/PUBLIC write paths, possible reviewed membership/default/routine remediation, and session termination. It accesses existing lab credentials and runs on the established localhost:55432 lab. Reading its source did not read credentials or execute it.

The accepted integration review explicitly requires current authorization for the bounded helper calls, including earlier removal cases, not only a last activation case. That review and a helper function name are not authorization for new fixtures. Root must verify that actual prior user approval covers the new fixture objects, existing role pair, exact generated statement effects and invocation set. Otherwise hold plaintext activation/removal and ask for that precise missing scope. Design and nonprivileged independent preparation can continue. No new grants, roles, credentials, cluster or helper broadening are proposed here.

## 7. Open limits and implementation stopping points

- The fixed commitments remove an ordinary ancestor-count/artifact-growth dead end. They do not provide unlimited database space, unbounded counters, arbitrary state sizes, or constant recovery time. There is no new short timer, history pruning, forced finalization or silent retirement.
- Keep blocked historical active/post-retirement cases, legacy metadata importer work, arbitrary scope changes, new tenant-universe admission, final backup recovery and full lifecycle/release qualification explicitly open.
- Before selecting code implementation, root must accept the new exact format pair and summary schemas, per-row state-envelope condition, physical journal validator, lock order and v3 reverse-summary dispatch. If any is omitted, select a narrower prototype with the resulting limitation named; do not call it complete recovery.
- No source/test import, test collection/run, database, live runtime/corpus/cache/environment/credential/raw-phase inspection, build, install, Git or network action was performed. Only this reviewer directory was written. INPUTS.json pins finite consumed source/contracts/tests/reviews; it does not claim a full selected-tree verification.
