# Versioned corpus capture wrapper v2: SOURCE ONLY

Prepared 2026-10-14. Neither derivative nor fixture tests have been executed. Independent review is required before any use. Original toolchain/lab_session.py and scripts/test_postgres.py are unchanged. No credentials, environment dumps, tests.json or package-origin.json were read or copied.

## Scope

lab_session_corpus_v2.py is an isolated derivative of toolchain/lab_session.py. It imports the original toolchain/run_baseline.py from its unchanged location. Changes are restricted to filesystem artifact snapshot/capture/restoration and nested finally cleanup; PostgreSQL start/stop arguments, runner commands, both role preflight path, package-origin checks, environment configuration, lab lock and test timeout logic are copied unchanged. The original wrapper remains available and untouched.

Capture recognizes the original compatibility*corpus-v1-sa*.json pattern plus master-s4-compatibility*corpus-v1-sa*.json. Before PostgreSQL starts, under the original lock, matching originals are copied to the run's prior-corpus/ with a hash manifest. Changed/new outputs are copied exclusively into candidate-corpus/ before any restoration/removal. Deleted originals are restored and reported. Unchanged outputs are not described as newly emitted evidence.

Archive failures retain changed shared outputs rather than destroy uncaptured bytes. Other files still receive restoration attempts; saved original and archived output copies remain available for manual inspection. Restoration/enumeration/archive failures produce an explicit error and unsuccessful wrapper outcome. If the final isolation report itself cannot be written, its error propagates. Nested finally releases the lock and attempts corpus cleanup even if PostgreSQL stop/reporting raises. This does not claim crash/power-loss atomicity or change the inherited handling of a nonzero postgres-stop subprocess exit.

Snapshot failures occur before PostgreSQL starts; partial original backups may remain, but shared originals have not changed. Symlink artifacts are refused. Unrelated filenames are not touched. All operations assume cooperating writers honor the existing exclusive lab lock; this adds no protection against arbitrary external filesystem writers.

## Identified shared producers and preserved copies

The six currently present shared files are evidence/master-s4-compatibility-{core-flush,flush,implicit-flush}-corpus-v1-sa{2.0.51,2.1.3}.json. Their producers are respectively current candidate tests/test_sqlalchemy_core_autoflush_boundary.py, tests/test_sqlalchemy_flush_preparation_failure.py, and tests/test_sqlalchemy_provider_implicit_flush.py.

Restored external core harnesses also emit master-s4 compatibility corpus, lifecycle, relationship, state, truth, and method receipts when explicitly selected. Default tests discovery excludes those external harnesses. The original capture glob excludes every master-s4 prefix.

unattributed-observations/ preserves the six observed current shared files verbatim. unattributed-observations.json records their paths, SHA-256 and byte lengths, plus preserved S5 counterparts under persistence-recovery-20261013/restored-s5/current-core-corpus-receipts/. These mutable shared observations are not assigned to S20, S21, S22, or any completed run. The immutable preserved S5 corpus remains authoritative for its original revision only.

## Proposed non-DB verification

After independent review and authorization, run only test_corpus_artifacts_v2.py through the existing Python unittest runner from this derivative directory. It imports only the filesystem helper. Its twelve temporary-directory controls cover both patterns, success, a simulated operation failure, new output, deleted original, unchanged output, archive failure with independent restoration, restore failure retaining both versions, snapshot failure, unrelated files, symlink refusal, and parsed-finally-only stop/restore failure ordering. The finally tests inject all names and never import wrapper main or run_baseline.

Review source.diff and source-manifest.json before execution. No database campaign is authorized by this packet. Preserve all failure evidence; do not retry a failed fixture or database operation without the required diagnosis/authorization. All seven production gates remain UNKNOWN.
