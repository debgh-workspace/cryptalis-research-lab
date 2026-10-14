# Additive packaging supervisor v2

SOURCE ONLY / NOT RUN. V1 launcher, build plan, verifier, source inventories and frozen-input manifest are untouched. This supplement corrects the environment description to include actual TMPDIR: V1 uses `run/tmp`; outer supervision uses `parent-results-v2/tmp` before V1 replaces it. The exact existing v1 launcher is authoritative for inner environment.

`supervisor_v2.py` is a byte-for-byte copy of the existing reviewed sanitizer supervisor. Its source origin is `candidate-native-controls-sanitizer-20261014/supervisor_v2.py`; both copies are in the outer freeze. It observes child termination with WNOWAIT, issues any timeout/output-limit group signal before reaping, and makes no group signal after reaping. No supervisor algorithm is changed. Descendant absence is not independently established; its receipt says so.

`outer_v2.py` creates fresh exclusive `parent-results-v2/`, checks the outer freeze and all v1/original/derivative pins, refuses existing `run/`, and invokes the frozen v1 launcher once. The child receives a clean explicit environment. Capture caps are2MiB per stdout/stderr and wall time120seconds, with the existing supervisor's up-to10second reap allowance. An inherited regular-file-size limit8MiB also bounds each redirected log/artifact, which pipe caps alone cannot bound. It is a per-file limit, not an aggregate filesystem quota.

Whether the child succeeds, fails under `set -e`, reaches a timeout/output cap, or a Python exception occurs, the outer finally path attempts all four integrity groups and writes an exclusive parent receipt. Integrity failure overrides a success verdict. Unexpected failures stop; no retries/backend substitution occur. Absolute OS termination or storage failure can still prevent receipt persistence and must not be represented as a guarantee otherwise.

After independent review and execution approval, exact entry command from any directory is the pinned Python executable with `-I -B` and the absolute `outer_v2.py` path. It loads only the byte-pinned supervisor source via compile/exec, not product packages. Source-only preparation has not invoked it, the v1 launcher, backend, extraction or artifact verifier.

All v1 acceptance criteria and seven UNKNOWN gates are retained. The bounded launcher does not authorize a broader experiment.
