# Forward supervisor ownership correction — 2026-10-14

Root source review found that several historical experiment supervisors call killpg using a numeric process-group ID after wait/poll has already reaped the owned leader. Numeric IDs can later be reused; future launchers must not signal after known reaping. This is a source-level cleanup risk, not evidence that a wrong-target signal or corrupted result occurred. Existing receipts and exact candidate results remain preserved with their bounded containment limitations.

Forward correction: signal only while the owned child remains unreaped; where used, non-reaping waitid observation can retain ownership until group cleanup precedes final wait. Catch individual cleanup failures so later descriptor closure, integrity checks and failure receipts are still attempted. Do not claim every descendant absent. Preserve prior versions and freeze corrected source before new execution.

The local recovery smoke v2 was reviewed and executed with an unreaped-child guard and separate cleanup catches. S fork and paired-normal-F future launchers are being corrected before their runs. New sanitizer adapters were instructed to use this ownership boundary. No system security settings, process outside the authorized lab, production resource or original repository was changed.
