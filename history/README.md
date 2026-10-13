# Original history recovery

The seven binary parts preserve the original complete Git bundle. They are not rewritten commits. The original source repository remains unchanged.

Concatenate original-history.bundle.part000 through part006, in numeric order, into a new original-history.bundle outside the checkout. Compare its byte count and SHA256 against manifest.json before using it. Run `git clone --no-checkout /absolute/path/original-history.bundle /new/empty/history-check` to restore the historical objects without executing checked-out code. The manifest records the original source HEAD and locally verified bundle provenance. Remote byte comparison is recorded per batch; do not equate this history recovery with new product qualification.

Never copy runtime credentials or private SSH keys into this repository. Original 15-message mailbox is separately preserved inside the S5 archive.
