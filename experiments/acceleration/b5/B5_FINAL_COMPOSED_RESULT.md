# B5 final composed test evidence

The retained-profile qualification map and stronger observers are complete for
the selected synthetic cell. Runtime and every original S17 test are unchanged.
The full S17 runs still have all seven historical legacy-profile failures.

- Original observer: 35 PASS per cell; original observer caveats remain attached.
- Stronger native-buffer/provenance observer: 37 PASS per cell, 10.93/10.19 s.
- Final first-backfill-attempt correction: one affected case PASS per cell,
  0.62/0.71 s. Other test branches are unchanged.

This is composed evidence, not a new full 37-case run of final bytes. The safe
combined receipt file preserves exact source hashes, six original runner receipts
and logs, stable source status, and stopped-server confirmation.

The final test SHA256 is
493ea7a52ad331f838845cf2b1cc57df75333285db0ec2479306fac5a3308da2.
The prior 37-case and original 35-case test bytes are retained separately.

Restore the complete 195-file S17 base using PROFILE_ORACLE_PROVENANCE.json
before adding this test-only derivative. No runtime module is replaced. The
publication subset alone is not a recovered runnable package.

No main promotion, contract change, old-worker read relaxation or production
qualification is implied. All seven production gates remain UNKNOWN.
