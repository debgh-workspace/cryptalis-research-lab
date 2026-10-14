# RELEASE-ENV-LOCK-01: offline environment feasibility

## Result

BLOCKED for an official-archive/hash-verified offline qualification environment with the inspected local inputs. There are zero named official locked dependency wheel/sdist archives under the executable workspace (walk completed without errors). Two UV caches retain unpacked directories for all 13 CPython 3.12/Linux-applicable runtime-plus-test distributions, including pycparser 3.0 and iniconfig 2.3.0. These directories are not original wheel ZIP files. Repacking them or trusting cache metadata cannot prove the original distribution SHA256 in uv.lock. No archive-byte hash proof is available for any of those 13 dependencies.

This is a bounded inventory, not a claim that no archive exists anywhere on the machine. The inspected archive filename suffixes are .whl, .tar.gz, .zip, .tar.bz2 and .tar.xz. Symlinks were inventoried but not traversed for archive searching. The two relevant cache roots are toolchain/uv-cache and apps/runtime/cache. Conventional /home/agent and /root pip/uv cache directories were absent. A shallow supplemental filename inventory of attachments, execution inputs, /workspace/shared and /tmp yielded no pycparser/iniconfig/wheel files. No opaque external bundles were extracted or treated as proof. UV .http/.msgpack files are small metadata files; no inference of original compressed archive bytes is made from them.

The exact locked pure-Python wheel targets are:
- pycparser-3.0-py3-none-any.whl: SHA256 b727414169a36b7d524c1c3e31839a521725078d7b2ff038656844266160a992.
- iniconfig-2.3.0-py3-none-any.whl: SHA256 f631c04d2c48c52b84d0d0549c99ff3859c98df65b3101406327ecc7d53fbf12.

Their toolchain unpacked directories are archive-v0/KLLZT-wWBNmWPOKW and archive-v0/oST9Fub7XnIigHfb respectively. The runtime cache equivalents are archive-v0/C2lMRu5z6sIoHZQf and archive-v0/h6n5-veHiQjAColc. This is path availability only, not executed-byte provenance or archive-hash verification.

## Scope distinctions

The S20 lock SHA256 is faae077d223037c4a7d9a54e1aafc4760cf217057eb18fbd93fc021908be343e. Its runtime union is cffi 2.1.1, cryptography 50.0.2, greenlet 3.5.6, psycopg 3.3.6, psycopg-binary 3.3.6, pycparser 3.0, sqlalchemy 2.1.3, typing-extensions 4.16.0, tzdata 2026.5. Its test-only union is colorama 0.4.6, iniconfig 2.3.0, packaging 26.3, pluggy 1.6.0, pygments 2.21.0, pytest 9.1.1.

For the CPython 3.12/Linux x86_64 planning target, tzdata and colorama are excluded by Windows markers. Their absence is not Linux environment drift. Keep typing-extensions for Python 3.12; psycopg's dependency edge is conditional below Python 3.13. Preserve implementation-specific cffi/pycparser and psycopg-binary edges rather than treating the union as a platform-neutral install list. ABI/platform wheel selection must still be explicitly verified against the chosen interpreter and glibc; listed manylinux candidates are not an execution-based compatibility determination.

Build backend uv_build >=0.12.12,<0.13 is a range, not a resolved locked runtime or test dependency. A uv-build 0.12.12 unpacked wheel cache exists, but no official uv_build archive/hash has been established here. Qualification of the existing product wheel need not build the product. Reproducible source-build qualification must separately pin and verify builder, interpreter and installer artifacts.

SQLAlchemy 2.0.51 remains an intentional second-cell override. It is absent from this S20 lock and therefore cannot claim this lock's hash attestation. Its unpacked caches exist; a separately approved exact official archive/hash manifest is required for that cell. Do not rewrite uv.lock to conceal the distinction.

## Evidence boundary

Read the root defect, S20 post-run reconciliation review, pyproject.toml, uv.lock, artifact report/build log and safe package-origin.log. The historical package-origin log points to Python 3.12 in the S20 wheel environment. Historical artifact report records Cryptalis wheel SHA256 a46e527484daaf4621831f395af8d8193716220a24106c5d6d0d983a16a9cbb7 and sdist SHA256 dd4b0f44c0b0114b56c5d57637ff79e159ce6c65e1c9e71fbdd2843aabb495c6, same-host repeated builds only. This inventory does not independently establish those historical execution claims. Existing static artifact/lock/SBOM ACCEPT does not attest dependency bytes or installed-environment identity. All seven product qualification gates remain UNKNOWN.

## Finite proposed next steps (not executed)

1. Approve a new isolated CPython 3.12/Linux x86_64 environment definition: exact interpreter, OS/glibc, installer, S20 lock and product wheel pins; separate SA21 locked cell and SA20 override cell. Leave existing environments and caches untouched.
2. Supply original wheel files for the 13 applicable locked packages listed in missing-wheel-candidates.tsv, selecting one compatible listed wheel per package. Acquire only through a separately authorized official-source download step, or accept user-supplied files and compare their bytes against the existing lock. No network step is authorized by this inventory task. Stop on absent files, wrong hashes, unsupported tags or unexpected dependencies. SA20 additionally needs an independently pinned official SQLAlchemy 2.0.51 artifact. Builder artifacts are needed only for a separately requested build boundary.
3. Before setup, create a reviewable immutable local file/hash manifest covering each selected wheel, interpreter, installer, product wheel and finite test/source snapshot. Require an independent review of platform markers and the SA20 delta. Do not use unpacked cache directories as substitutes for original archives.
4. Only after setup authorization, create two new uniquely named environments. Install exclusively from the verified local wheel set using no-index/no-network and required hashes; do not allow resolver upgrades or source builds. Verify installed name/version closure, distribution RECORD content integrity and allowed filesystem origins, and retain before/after manifests. This yields present-environment evidence only.
5. Stop after installation verification for a decision on the finite qualification run. Any tests, database roles/cluster, credentials or network have separate authorization requirements. An approved future run must capture contemporaneous interpreter/package/module identity, source/artifact pins, platform and test receipts; it cannot retroactively repair historical provenance or qualify unrelated gates.

No package imports, tests, installations, environment creations, credential reads, cluster actions or network use occurred. Python used only isolated stdlib parsing/hash/inventory operations. Only this new notes directory was written.
