# C6 identical-code A/A diagnostic

## Result

The predeclared material-variance condition was met: **9 of 36 identical-code
pairs differed by at least 10%**. The one SQLAlchemy 2.0.51 sweep completed all
72 cells and 36,000 timed admissions. No run failure, incomplete cell, owner
state change or GC-setting change was reported. No observation was excluded.

This result does not change C5's failed consistency gate. C5 remains held at
checkpoint `94adea55905b1c69838df0f0fc725d1924eaf0b8`. No candidate admission
method was imported or created during this diagnostic, and no database was used.

| Family | A median, us/admission | B median, us/admission | B faster pairs | Pairs differing by >=10% |
| --- | ---: | ---: | ---: | ---: |
| Point | 97.562910 | 96.313174 | 5/9 | 3/9 |
| Equality | 94.627402 | 99.813154 | 5/9 | 2/9 |
| IN2 | 104.837810 | 100.309502 | 5/9 | 3/9 |
| Public textual label | 142.049398 | 148.533940 | 3/9 | 1/9 |

These are arbitrary A/B labels for the same method, owner and statement. The
table's marginal medians are not the median of paired differences. For example,
equality's B marginal median is 5.48% higher while its median paired difference
is -5.39%; neither is an optimization effect.

## What the telemetry supports

- Thread-CPU duration closely tracked wall duration. No pair met the predeclared
  wall-dominant rule. The maximum absolute wall/thread difference in a cell was
  0.044452 ms. This does not support a wall-only lost-CPU explanation in this
  particular sweep, but it does not identify an alternative cause or prove equal
  instruction counts.
- No cell crossed the predeclared perf-counter/raw-clock disagreement rule. The
  largest absolute difference was 0.001665 ms. This supplies no evidence of a
  material disagreement between those two clocks here.
- The observer recorded 147 GC spans: 134 generation-0, 12 generation-1 and one
  generation-2 collection. The generation-2 span lasted 23.192220 ms during
  point block 0, slot B. That pair's B-minus-A gap was 25.369025 ms, with total
  observed GC overlap of 24.273035 ms in B and 0.119294 ms in A. This is direct
  temporal overlap, not a subtraction-based corrected result or a claim that
  the whole gap was caused by GC.
- The other eight material pairs had absolute wall gaps from 6.968531 to
  20.711292 ms. Their A/B GC-overlap differences were all below 0.136 ms. Thus
  the single long GC event cannot explain all material variation observed here.
- Separate untimed call counts match the unchanged baseline mechanism: 100
  `admit` and 100 `_admit_textual_references` calls per 100 admissions for every
  family. The actual A/B timed cells use that same baseline code. Equality and
  IN2 retain 200 `search_shape` calls per 100 admissions.

## Limits and stopping decision

Telemetry and retained observation objects add allocations and can change GC
behavior. These times are diagnostic, not native-query or product latency.
CPU duration, clock data and GC spans were contemporaneous; system load,
hardware frequency and instruction counts were not collected. A coordinator's
later resource sample is outside this timed interval and is not used here.

This separately authorized negative control establishes that variance material
relative to the 10% threshold occurred under its instrumented harness. It cannot
identify the cause of the earlier C5 IN2 failures. It neither rescues C5 nor
justifies removing observations, lowering its threshold or rerunning its gate.
The finite diagnostic is complete; no further timing run is requested.

## Reproducible receipt

The plan and runner were written before the single sweep. All pair, cell,
sub-batch and GC-event observations are retained in `evidence/admission-aa-sa20.json`.
`analyze_aa.py` consumes this existing JSON and makes no admission calls.

- Baseline: S17 `cryptalis/sqlalchemy.py`, SHA-256
  `fc2f7a7c983370f7c81874b56ec8e511532d226fc962bc0c8939b38d4daadfbe`
- S17 manifest: 195 files, SHA-256
  `70a5293e76486f243305968c7a58b8fa8c6be97d5bec5508593529b9eacc49e7`;
  all 195 source files rechecked unchanged after the diagnostic
- Plan SHA-256:
  `d3ccf9a5c147b22efeb95bdf05025ed56c51f8d0ab7bdece33433c2ba14c76be`
- Runner SHA-256:
  `caa4f15fb381445b73e2b19827663a6e30760b9cbc82266004ede0e2d2a9c5b7`
- Raw receipt SHA-256:
  `7d6be793a168d635bac4e53416d27a788324e66cadfeacb944304ba4b2b113ef`
- Analyzer SHA-256:
  `296c5da6af89ae7be35b6abd70b45249fc0704ff4ecbade9ea814dd4a4868a18`
- Analysis JSON SHA-256:
  `34704911d4ad8325abd440dc49036d8d8b5135f2663aeac6cb3177c2893bec6d`

The failed C5 publication's ten files and publication plan were not changed.
