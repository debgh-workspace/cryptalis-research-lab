# Frozen direction-only primitive experiment

Question: Does the standalone direction-specific system OpenSSL decrypt call reduce construction-plus-decrypt cost against a fresh public pyca AESGCMSIV object per item? This does not measure CF1, HKDF/HMAC, PostgreSQL, SQLAlchemy or product latency.

Use existing pinned Python3.12.14/cryptography50.0.2. Candidate source SHA5933299b46e349cd0e80032fd89beffd797e5ad04230cbfda1d985ef1eca0239, binary393cf26a573870a9e7e1d3b12a3196528f9301f840214dbc05d84e1cb37575ed. Backend difference (system3.5.7 vs pyca4.0.3) prevents attribution solely to context construction; report it as a limitation.

Fixed public deterministic fixtures:1000 distinct keys/nonces per size, sizes7,32,128 bytes as primaries and4096 bytes as control;31-byte AAD. Generate encrypted fixtures before timing using unchanged pyca. Seven blocks, alternate original/candidate order. Each variant executes100warmup calls then1000measured calls per size/block. Each timed interval contains the complete fresh-object-or-native-call list construction, then validate EVERY output outside timing. All block wall/process/thread clocks and resource counters retained, no filtering/rerun.

Mechanism acceptance requires at least20% lower median-of-seven block per-item wall times and6/7 strictly favorable blocks for each primary; control may regress no more than5%. This is only an experiment-selection rule, not promotion or fulfillment of the frozen C9/C10/product budgets. Any failure is preserved. No threshold/source change after measurement.

All76 component correctness checks must remain backed by the exact source/binary; full independently reviewed memory safety and CF1 binding remain unqualified. No product runtime import, key provider, database, network, install, or persistent key cache.
