# Installation and artifact selection

**Integrated221 package audit: ACCEPTED within its bounded same-host scope. Installed qualification and exact example smoke: PENDING.** This is a procedure template, not an installation receipt or authorization.

## Select an exact artifact

The intended source is Integrated221, with source-manifest SHA-256 `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`. Its build completed with entry 0, and the independent artifact review accepted bounded packaging at the coordinator's 14:15 UTC checkpoint.

| Artifact | Bytes | Audited SHA-256 |
|---|---:|---|
| `cryptalis-0.1.0-py3-none-any.whl` | 144,298 | `dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6` |
| `cryptalis-0.1.0.tar.gz` | 154,158 | `1f447ac32bac75803826df6e2e66a1df5a8dd515448484c271175c279ef98b6c` |

The direct, repeated and sdist-roundtrip wheels are byte-identical; both sdists are byte-identical. The audit checked all 43 runtime modules, exact archive payloads, RECORD hashes, metadata, license and source copies. These are same-host pinned-builder results. The supplied artifact must still match the accepted identity before installation.

[DELIVERY-BINDING.json](DELIVERY-BINDING.json) binds the independent review and actual-artifact record as well as these distribution identities. This documentation pass rehashed those two records, not the distributions. The source `uv.lock` hash is recorded separately from the still-pending complete portable installation lock/wheelhouse and SBOM binding. No missing hash is invented.

Before installation, the delivery owner must supply and independently verify:

1. Match the supplied wheel/sdist bytes to the audited identities and this source manifest.
2. Retain the accepted package-content, METADATA, RECORD, license and source-distribution audit.
3. Complete dependency lock, exact wheelhouse and hashes, interpreter/platform inventory, SBOM and build receipt.
4. Accepted installed-origin results for both SQLAlchemy cells and the separately pinned optional SQLModel cell.
5. The exact executed quickstart/smoke receipt, including failures and recovery checks.

The package version is `0.1.0` for multiple different candidates. A version string is not an artifact identity. Do not use a public-index package with the same name as a substitute. Transport218 is the highest audited installed baseline, but it still has seven historical failures per main cell and lacks source221's corrections. Its old receipts do not transfer to Integrated221.

## Dependency declaration and tested cells

| Component | Source declaration / evidence boundary |
|---|---|
| Python | Declared >=3.12; recorded main cells use 3.12.14 |
| SQLAlchemy | Declared >=2.0.51,<2.2; main source cells are 2.0.51 and 2.1.3 |
| psycopg | `psycopg[binary]==3.3.6` |
| cryptography | `cryptography==50.0.2` |
| greenlet | `greenlet==3.5.6` |
| PostgreSQL | Selected major 16; recorded cells use 16.15 |
| Build backend | `uv_build>=0.12.12,<0.13`; the release must bind an exact build environment |
| SQLModel | Optional, not a base dependency; use only the independently recorded dependency cell |

The declared ranges do not qualify every version, operating system or managed PostgreSQL service. No extension is required by the admitted storage/equality representation.

## Installation command shape

After the complete artifact and dependency packet is approved, use the approved environment's normal installer. The following ordinary pip command has **not been executed for this guide**:

```sh
python -m pip install --no-index --find-links /APPROVED/WHEELHOUSE --require-hashes -r /APPROVED/COMPLETE-LOCK.txt
```

Both uppercase paths are mandatory operator substitutions. The complete lock must select the reviewed Cryptalis wheel and every required dependency. This guide does not provide that wheelhouse or lock. Do not remove hash checking, skip dependencies, or copy an existing virtual environment and describe it as independent reproduction.

## Remaining provenance limits

Historical S20 environment metadata reports pycparser 3.11 / iniconfig 2.3.1 against lock versions 3.0 / 2.3.0. Static lock/SBOM equality is not installed-environment equality. Official metadata matches the 13 recorded dependency wheel hashes, but exact artifact acquisition timed out with zero bytes. Interpreter provenance, clean-host acquisition/build equivalence and fresh-host runtime/database recovery remain open.

After an approved install, verify installed origin and exact distribution contents before any database test. Use disposable synthetic data and separately reviewed runtime/maintenance roles. Installation alone does not authorize role changes, maintenance, provider access, plaintext recovery or publication.
