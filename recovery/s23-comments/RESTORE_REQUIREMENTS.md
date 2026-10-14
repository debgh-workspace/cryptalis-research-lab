# Bounded source/evidence recovery requirements

This addon requires the separately published S23 source/evidence capsule:
SHA-256 41c756d905f84f4754208ba4d27bda87621ab88d0bac58fcf421c7bbcbf50870,
1750488 bytes, canonical source checkpoint d6334eb2fc003d5609d3323135d50e3059ce1366,
metadata publication 1cdc5c795c62b7caa9f229e5d00f4aec84c686ca.

To reconstruct each isolated original/r2/r3 candidate, take the 213 canonical
source files, overlay only that candidate's four delta files, and require exact
equality with its 214-entry CANDIDATE_SOURCE_MANIFEST.json. Three existing files
change; one helper is added; 210 files retain canonical hashes. Each variant's
separate directory and manifest must remain separate. Do not overlay r3 onto r2
and continue to label r2 observations as r3 evidence.

The archive preserves selected experiment source, frozen pins, safe observations,
source snapshots and independent reviews at their recorded relative paths.
Absolute historical paths inside receipts describe the original run; relocation
does not establish reproducibility of execution. Source hash reconstruction is
performed as data and never imports or runs restored code.

R2's 120-second timeout and exit 124 are preserved independently from r3's
17-method PASS/8.470-second/exit-0 result. Neither is a timing benchmark. R2 native
8 PASS per cell remains separately bound to r2. R3 native and lifecycle evidence
must be terminal and independently reviewed before a final completion claim.

The separately published acceptance/comment-RED addon, SHA-256
7fd2bc7e4df3dfae16747f737dd1b410862e4dd80ce14a5c2a629fbe0b3799cd,
retains earlier native RED evidence; it is referenced rather than silently
rewritten here. Complete historical reconstruction requires that addon too.

This packet excludes credentials, raw environment-bearing run JSON, dependency
installations, interpreter binaries, caches and database state. Operational
execution would require separately authorized existing dependencies, PostgreSQL
and role setup, environment provisioning, reviewed runtime commands, and the
coordinator's lock/preflight/capture workflow. Those requirements are not fulfilled
by byte restoration. No runtime, new platform, product integration, production
qualification or gate closure follows. S23 planning remains highest integrated
bounded checkpoint and all seven full qualification gates remain UNKNOWN.

During preparation, append versioned inventory snapshots rather than overwriting
old ones. Freeze only after coordinator confirmation and after terminal evidence
and reviews are identified. Recheck every inventoried byte immediately before
archiving; fail if a concurrent writer changed an input.
