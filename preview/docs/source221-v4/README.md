# Cryptalis Research Preview / Internal Evaluation Candidate

Documentation v3, 15 October 2026. **Synthetic, disposable evaluation only. No production release or security qualification is claimed.**

Cryptalis protects admitted text values in the application before PostgreSQL receives them. Its current Python APIs compile a JSON declaration, plan a maintenance transition, attach supported SQLAlchemy operations, and decrypt current values back before removal. Unsupported operations fail explicitly.

## Current delivery boundary

| Item | Verified status at this documentation snapshot |
|---|---|
| Highest engineering source | Integrated221: `candidate-cluster-retained-integrated-v2-20261015` |
| 221-file source-manifest SHA-256 | `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520` |
| Independent source SQLAlchemy 2.1.3 | 2,684 PASS / 0 FAIL / 0 SKIP, plus 56 passing subtests |
| Independent source SQLAlchemy 2.0.51 | 2,638 PASS / 0 FAIL / 46 expected native-version skips, plus 56 passing subtests |
| Independent source optional SQLModel | 38 PASS / 114 passing phases |
| Integrated221 distributions | Build entry 0; independent bounded artifact audit accepted. Exact wheel/sdist identities are in [INSTALL.md](INSTALL.md) |
| Integrated221 installed suites and public example smoke | **PENDING** |
| Highest audited installed baseline | Transport218; its two main cells retain seven historical failures each |
| Production gates | **All seven UNKNOWN** |

The seven historical suffix-layout failures are resolved in source221 through independently checked retained-native contracts, native controls and mutation evidence. Source221 also integrates the bounded remembered-CLUSTER-designation correction and conditional legacy recovery/refusal. These source results do not establish installed221 acceptance, generic legacy repair or complete PostgreSQL metadata preservation.

## Use this guide

1. Review [actual capabilities and refusals](CAPABILITIES.md) and [known limitations](KNOWN-LIMITATIONS.md).
2. Check the [artifact identities and pending installed qualification](INSTALL.md). Do not install an unidentified `cryptalis==0.1.0` artifact.
3. Read the [manifest reference](MANIFEST.md), [host inputs](HOST-INPUTS.md), and [small quickstart](QUICKSTART.md).
4. Keep the [maintenance, recovery and removal handoff](RECOVERY.md) with the operator procedure.
5. Check [evidence](EVIDENCE.md), [the unexecuted smoke boundary](SMOKE-TEST.md), [source references](SOURCE-MAP.md), and [all 34 continuing objectives](OBJECTIVES.md).

All examples are source-checked templates, **not an executed standalone quickstart**. They require real host objects, reviewed authority and approved infrastructure. No import, installation, test, key creation, database connection or external action occurred during this documentation pass.

All 34 objectives remain active. A research preview is the first delivery milestone; it does not complete the product. The packaged source retains historical documentation statements. Use the dated evidence boundaries here to interpret them; the immutable source and earlier documentation were not edited.
