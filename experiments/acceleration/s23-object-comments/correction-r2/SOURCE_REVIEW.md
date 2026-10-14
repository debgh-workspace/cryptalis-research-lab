# Independent r2 identity correction review

2026-10-14. Static source review only. No project import, test execution, database access, Git operation, product edit, or credential read. Only this new versioned review note was written.

## Verdict

**CLEARANCE: prior implementation blocker C1 is closed for the exact r2 source below.** This is source-review clearance, not permission to execute, a runtime result, packet clearance, integration approval, or promotion. All runtime qualification gates and historical RED evidence remain unchanged.

- Frozen v1 source manifest: `8e6dde20f735278e5b5e103dd31dcc05a3f9e98ff12968150ea7270754252a29`.
- R2 source manifest: `f60c533cd016eee96c2045ddd3efe95633aaf07b2df5761bc2b6bcd695c32741`.
- R2 helper, `src/cryptalis/_object_comments.py`: `00c6bc68768fffc813bdfa4ee5302e93d4f76a9754b7b704955cf186c978192c`.
- V1 helper: `3a3d85f4b76350beda0dade378e83d60a3c60a82d31e3561e5d04221836fa5ad`.

A fresh recursive byte comparison of the two candidate trees found only the helper changed. Both manifest hashes and the helper hashes were independently recalculated. The existing SOURCE_AUDIT_r2.json reports 214 files, 210 unchanged from S23, three changed baseline files and one added helper; this review did not rerun its full manifest/AST audit.

## C1 closure

1. Helper lines 152-153 compare canonical serialized bytes for duplicated `lock`, `target`, `runtime_role` and `journal_schema`. Canonicalization recursively preserves JSON boolean versus integer distinctions, including nested structures. Python equality in the unchanged outer reverse constructor is now only an earlier check; it cannot replace or bypass this stricter new-format validation.
2. Helper lines 162-164 require a reverse policy-map key subset and canonical byte equality for every included source value. Empty, proper and complete exact subsets remain admissible at this check.
3. Helper lines 137-141 constrain the new forward policy map to canonical nonzero UUID tenant strings and exactly 64 lowercase hexadecimal string fingerprints. This matches planner-produced UUID keys and SHA-256 policy fingerprints. New source numeric/boolean policy aliases are rejected independently of reverse correspondence.
4. DeprotectionPlan constructs and validates its embedded MigrationPlan first, binds the source pin through `_admit`, verifies source ACTIVE state and target identity, and then invokes the stricter helper before constructor success. Canonical new-format target/operation/source-pin UUID spelling plus existing pin matching establishes exact duplicated identity spelling. The digest remains bound to the exact source artifact.
5. The unchanged canonicalizer uses sorted keys, compact JSON separators, UTF-8, and disallows NaN. The unchanged transition decoder rejects duplicate members and non-rate floats. Equality is therefore between the same canonical byte representation used for envelope accounting.

## Legacy boundary

MigrationPlan invokes forward helper validation only when the exact new forward format is enabled. DeprotectionPlan invokes reverse helper validation only for the exact new reverse format. No new unconditional checks were inserted by r2. Thus the r2 delta does not alter v0 policy grammar, UUID acceptance, duplicate-field equality semantics, execution, or lifecycle behavior. It does not upgrade legacy metadata guarantees. Prior v1 lifecycle and inventory review remains applicable because all other candidate files are byte-identical.

Unchanged v1/r2 runtime-file hashes independently recalculated:

- deprotection.py: `e8498a94410ed5ff28ec21acd585418b6f849b89daf666a7ce0f8b0c78826f0b`
- migration.py: `c039af611f5be18e5a43dd6492335d6c0860aa07a07d966adfd11678396751d6`
- sqlalchemy.py: `9af0b4d5293a167fffd7fc6ec2ae0e303a776b724d400d6fffb152aedfa20f16`

## Prepared evidence and remaining boundary

Static inspection of `experiments/s23-comments-envelope-independent-20261014/test_comment_envelope_product_r2.py`, SHA-256 `3688e51057ec0e7f11eef8323335b5ae9be9740dd347b584842a00af9113449f`, found prepared nested lock and target type-identity checks, strict forward fingerprint/key checks, an isolated reverse-policy canonical comparison check, valid empty/proper/full policy-subset acceptance, and separate legacy/new pairing coverage. These controls were not run by this reviewer. Their presence is not a PASS result or a complete independent oracle/command review.

The r2 GREEN packet SOURCE_PREPARATION.json was still a copied v1/7-test description when read. Its owner confirmed reconciliation is underway. This is a packet-freeze issue outside this source clearance; root must use the final reviewed packet and commands, not that stale description.

Reviewed design inputs retain their frozen hashes:

- SCHEMA_STRATEGY_v2.md: `86d19bb33dec99f1bdbebfb54ccdb2f70c6df8ac56a9150ba9377d3f6c7f4ba8`
- V2_IDENTITY_ADDENDUM.md: `95b859495e9d17c0e05dfaf99660475b1630ca2e612a6c5d73a1d4660bd734d9`
- PROTOTYPE_GATE_ADDENDUM.md: `3579e5d1b801b918277960e4f87e48b27a98da0e10df4f77fbe6e4ee1e997034`

The original REVIEW_v1.md remains unchanged at `233df7607351274cc429d8f78add7648ffd45492a580d43ec0feca2cb7ed80d0`.
