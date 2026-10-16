# Current installation and artifact supplement

This supplement identifies the frozen doctor successor. It is not an install receipt, complete dependency bundle, or authorization to execute a new installation or database operation.

## Select by content, not version

All candidates retain package version `0.1.0`. Use only the current accepted artifacts from [the immutable package directory](https://github.com/debgh-workspace/cryptalis-research-lab/tree/220d35ce796b913c0cced2bd19b416cf287011c9/preview/artifacts/doctor-remedy-v2-20261015):

- `cryptalis-0.1.0-py3-none-any.whl`: **140953 bytes**, SHA-256 `053f06f9277cc5f15f38887f79a44d91dac98a5b94f2ef2fae5329d0f3086965`.
- `cryptalis-0.1.0.tar.gz`: **150427 bytes**, SHA-256 `2e2a3cfc266602b958e4f4b2206c4d7ccc9e8d1de154ef0412141f529446a330`.
- Source manifest: `40c9787c974d38e030ace0b985ffb8a78de76196b28afea071a511eb7bd132e7`, 221 files / 43 runtime modules.

Publication and independent inert restoration are accepted. Packaging review `20efb7f7e9b43ef78bd8fbb2adae668b1b7697017ecded51178942170a614404` accepts three identical wheels/two identical sdists on the same pinned host. Package-restoration review `7ce9bf7d67a55e1aa9b34462fd335abc97b6cd4fe5f9876d6d812204f9f5cc5a` accepts the exact six-file delivery. Neither result establishes clean-host dependency reproduction.

## Do not substitute historical hashes

The [immutable installation guide](https://github.com/debgh-workspace/cryptalis-research-lab/blob/d952c505a4666266019e32f27c77f93edd5151ca/preview/docs/source221-v4/INSTALL.md) names **original Integrated221**, not this successor:

- Original wheel: 144298 bytes, `dcff0ec62af960715627d0cb247a267b0068a4d61eae35aacbdd2e879da1bee6`.
- Original sdist: 154158 bytes, `1f447ac32bac75803826df6e2e66a1df5a8dd515448484c271175c279ef98b6c`.
- Original source manifest: `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`.

The intervening README-v2 documentation-only artifacts are also historical: wheel `ce4817376f25411c8685c676802cce25c1799c85a87277b1dcc099556a40229c`, sdist `7988fb28baa4dec5804d4779b8a1d626c7dae5e3d7d5e597a7a12a69e0d9a036`. Keep all predecessors and receipts intact. The current package retains the historical embedded README unchanged.

## Installation prerequisites and command template

The unchanged guide declares Python >=3.12 (recorded 3.12.14), SQLAlchemy >=2.0.51,<2.2 (admitted cells 2.0.51 and 2.1.3), psycopg[binary] 3.3.6, cryptography 50.0.2 and greenlet 3.5.6; recorded PostgreSQL is 16.15. These declarations do not qualify every version/platform. SQLModel is separate and optional.

A complete portable lock/wheelhouse, exact interpreter/platform inventory, SBOM and clean-host provenance remain incomplete. Exact historical locked dependency acquisition remains unresolved. Do not install a similarly named public-index package, relax hashes, or describe a copied environment as independent reproduction.

After the exact environment/artifact/dependency packet and action are approved, the existing guide's command shape is:

```sh
python -m pip install --no-index --find-links /APPROVED/WHEELHOUSE --require-hashes -r /APPROVED/COMPLETE-LOCK.txt
```

This is an **unexecuted template**. Both uppercase paths are mandatory approved inputs, not supplied files. The complete lock must select this current wheel hash and every dependency. Independently verify supplied artifact sizes/hashes, installed origin and payload before an approved synthetic test. Installation does not authorize fixture ACLs, role repair, plaintext exposure, provider access or publication. If prerequisites or authority are missing, stop and record the gap.
