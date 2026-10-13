

## 2026-10-12 native ORM deletion checkpoint

Candidate: `candidate-native-delete-20261012`, reconstructed from the verified 2031Z UUID parent, with an uncommitted operation-local native UOW deletion guard. This candidate does not contain the later missing private bulk permit or namespace/temporal candidates. Original 15-commit mailbox remains unchanged.

Evidence: ordinary public-row batched deletion, sync/async, commit/rollback/SAVEPOINT, opt-in on/off: 12 native differential tests PASS on 2.1.3 and 2.0.51. Versioned-row variant: 12 PASS on 2.1.3. Normal adapter selection: 20 PASS on 2.1.3, including four expired protected/native context cases. The separately run four expired-context cases overlap those 20; do not double-count.

Important baseline result: the recovered parent also passes all 12 ordinary deletion tests. Therefore these positive tests establish compatibility retention, NOT repair of the historical later-prototype deletion regression. The earlier checkpoint wording 'correction' must not be interpreted as a reproduced RED-to-GREEN claim. Historical source-specific failures remain open until tested against their exact source or an independent justified reconstruction.

Research evidence (accessed 2026-10-12): https://docs.sqlalchemy.org/en/20/orm/session_events.html explains that Session.delete marks state and DELETE occurs in flush. https://docs.sqlalchemy.org/en/21/orm/versioning.html specifies flush-time row version matching. Installed native persistence source supplies mapper-owned delete statement and PK/version bind collection; its private interfaces require version-pinned qualification. Real PostgreSQL tests are the independent operational oracle. None constitutes independent security review.

Alternatives: (1) authorize all DELETE during flush, rejected as overbroad; (2) snapshot Session.deleted before flush, insufficient for late native orphan discovery; (3) bind exact native UOW states and mapper statement plus one-use parameter packet, current bounded prototype. No new cryptographic contract. Public API unchanged. Inheritance, secondary association tables, protected orphan coverage and general bulk DML remain unqualified.

Next: cascade/orphan ordinary compatibility, stale-version native errors, cross-version repetition, lifecycle selection and installed artifacts. Add tests for defensive state invariants without constructing third-party exploit workflows. All seven production gates UNKNOWN.
