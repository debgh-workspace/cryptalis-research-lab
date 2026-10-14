# Additive packaging supervisor v3

SOURCE ONLY / NOT RUN. V1 and v2 files/freezes remain unchanged and v2 is NOT RUN. This version corrects the parent's receipt-size risk: two capped2MiB streams may expand beyond8MiB when escaped into JSON.

`outer_v3.py` saves the parent's original RLIMIT_FSIZE soft/hard pair. It lowers only the soft limit to at most8MiB, retaining the original hard limit. The trusted pinned bash/build/helper children inherit that soft limit. After the byte-identical supervisor's child cleanup returns, the outer finally path restores the original parent pair before integrity reporting or receipt writing. It never lowers the hard limit and therefore does not require privilege to restore the prior soft limit. Restoration errors mark the run failed and are retained.

This is an inherited soft file limit for the trusted pinned builder, not containment of adversarial software: child code could raise its soft limit within the retained hard limit. Wall-time, stream caps, before-reap group signaling, no signal after reap, exclusive paths, one invocation, first-failure stopping, and all integrity groups are otherwise unchanged.

Fresh exclusive receipt destination is `parent-results-v3/`. The unchanged V1 launcher still owns `run/` and refuses existing output. The exact outer environment uses `parent-results-v3/{home,tmp,cache}`; V1's explicit clean environment uses `run/{home,tmp,cache}`. No inherited environment dump is taken.

After independent review and execution approval, invoke the pinned Python with `-I -B` and this directory's absolute `outer_v3.py` path. Neither v2 nor v3 has been executed during source preparation. No builds, imports of product distributions, installs, DB or Git actions have run. All seven qualification gates remain UNKNOWN.
