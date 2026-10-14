# Manifest acceptance v2: complete connection observation

Status: SOURCE ONLY, NOT RUN. No product/runtime/helper change.

Independent review identified two gaps in v1's setup-only connection collector:
do_connect does not observe checkout of a pooled connection, and the unchanged
migration fixture supplies a custom creator that bypasses that dialect hook even
when it creates a new DBAPI connection. The SQL callback also cannot detect a
connection acquired and returned without a statement.

V2 observes the public engine_connect and pool checkout events, retaining
do_connect only as an additional signal. Before relying on a zero-event setup
observation, both sync and async cases acquire and release two connections using
their real public engine APIs. Both acquisitions must emit the two public events,
and their transient DBAPI identities must match to establish the pooled case.
Those identities are compared only in memory; no connection property or URL is
inspected or persisted. The setup invocation itself must emit no connection
event and no before_cursor_execute event.

The generated template body, query cases/native oracle, lifecycle helpers,
runtime-role use, driver-bind collector, and cleanup remain unchanged. The two
additional public acquisitions per mode occur only if the coordinator later
executes the reviewed test. No database activity occurred during preparation.

V1 test SHA256:
b6fe9c9cc44be86c0546d251925a6cc970a23b320db3a7205c04ddce56375c6e

V1 files are retained in versions/v1. PLAN.json and PACKET_SHA256.json bind the
current v2 bytes; V1_TO_V2.diff is an ordinary source diff. The reviewer must
recheck this delta before any execution. No earlier test failure or success is
reclassified because no version of this acceptance test has run.
