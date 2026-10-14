# S25 main and optional post-install independent payload audit

Verdict: PASS_INDEPENDENT_INSTALLED_PAYLOAD_AUDIT for main sa20/sa21 and optional sqlmodel cells. Data-only audit performed; no imports or runtime tests. Runtime commands still require separate review and coordinator authorization.

All frozen installer manifests rechecked against actual bytes. Original main inventories remain1658 entries each, equal the historical snapshots; optional remains5900 complete entries. Clean216-file source remains exact. Each main new cell preserves1582 nonproduct entries; optional preserves5845. All original interpreter/lib symlink targets remain exact in copied cells. Every installed41-module source payload equals actual audited wheel42150bab589fcb80083dafb8bd34186c5040776950fa1f5b04b11a43c1e3b36c and clean source. All45 non-RECORD wheel payloads match installed bytes. Each installed RECORD has51 unique rows, complete wheel coverage and exactly five permitted installer/CLI additions; every hashed installed entry validates size/digest and resolves within its cell. Direct URL equals actual local wheel URI, INSTALLER is uv, and exact first CLI shebang names the new cell/bin/python. These are on-disk origin checks, not observed import origins.

Installed RECORD hashes:
- sa20:8961a7bf0fee300290f8ab0268c99208a5d2c4f092dd23b0b855b2cafddbb0f3
- sa21:4d5c1faf7ea90a930e9a0c515de247db577f8ea3135793034c2148f38c470631
- sqlmodel:cc904cc6f6b801bfadafefaeed3189d0321a1bf46ce6621f5717aa61135d59d5

Copy inode receipts cover every original regular path; all recorded original/copy pairs are distinct. Current original inode identities reconcile to both receipt types, and surviving installed inode identities reconcile to actual paths. Complete current regular inode sets reject overlap with originals, earlier new cells and clean source. Main cells have1629 regular inodes each; optional has5892. Historical intermediate copy identities are receipt evidence, while final disjointness was independently measured. No claim that old dependency console script shebangs were rewritten: use only new bin/python.

Both terminal parent receipts pass bounded installation, child exit0, leader reaped, no reason/errors/cleanup errors, all before/after integrity groups pass.120s configured deadline,2MiB captured streams,64MiB regular-file limit and restored original limits verified. Captured stream bytes/hashes reconcile and actual output files remain below limit. Descendant absence remains explicitly false/unproven. These bounds are not aggregate quotas or hostile-code containment.

Independent executable audit source: audit_installed_payload.py, standard-library data reads only. Results: MAIN_INSTALLED_AUDIT.json and OPTIONAL_INSTALLED_AUDIT.json. Optional POSTINSTALL_CLEARANCE.sha256 is additive and binds this review, optional audit JSON, installer terminal verification, safe installation parent receipt, copy/installed inode receipts and installed RECORD. No raw runtime phase JSON was read or included.

No broader runtime acceptance, full installed suite, natural fault equivalence, dependency archive provenance or production qualification follows. All seven broader gates remain UNKNOWN.
