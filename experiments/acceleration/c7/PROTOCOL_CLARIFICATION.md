# C7 protocol clarification: existing leased key cache

Independent internal review identified an overstatement in the frozen protocol
SHA-256 `8db8d0b85dcbc277e39376a8ee2291829d96b9e48b3a0384cb622fb19028184d`:
“No keys or plaintext are cached across scans.”

The precise claim is:

**There is no new cross-scan plaintext/result cache. The existing bounded keyring
cache and per-use lease checks remain in force.**

The harness retains `app.rings`, and the unchanged `Keyring` may reuse root
material until its original deadline. Access does not renew that deadline. The
short-lived negative-test ring narrows its test lease and is replaced with the
ordinary fixture ring before the separate recovery check. No cache optimization,
new provider or extended key lifetime was added.

This is a documentation correction, not a runtime defect or a changed experiment.
The frozen protocol and harness bytes are retained for source-to-run provenance.
Interpret the protocol's earlier cache sentence using this clarification.
