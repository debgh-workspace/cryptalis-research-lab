# State cleanup V1 SA21 baseline: accepted intended RED

Decision: ACCEPTED_INTENDED_NO_DB_UNIT_RED, 2026-10-17. This supersedes the earlier pre-run observation for this cell only.

Packet: experiments/orm-flush-state-unit-packet-v1-20261016; PACKET.sha256 4125c88a620d2c628d0fb0ea0d204fc0356711800851b5a0966de8f79dde7b39. Command review a22da28547f01fa557fb28266b65fa67a10d5c5d6938445aba45b8277bbe8081. Actual run: packet/run/sa21-baseline. Root capture: persistence-recovery-20261013/flush-state-sa21-baseline-root-20261017 (workspace-root relative).

Exactly one selected CleanupStateFaults method, ten subtests: ordinary/close_fails False and True both PASS; setter, getter, stale_false and type_name each with close_fails False and True produce eight AssertionErrors. No errors/skips or ordinary zero-subcase method. Driver enforces zero skips before emitting RESULT. Stderr corroborates eight specific intended assertions and one method in 0.004s, not an import/setup/signature failure. Setter cases miss quarantine; getter cases replace primary with marker-read failure; stale_false cases expose marker hooks or skip later connection; type-name cases miss close/later connection. Exit1 is consistent with these exact failures.

Independently reconstructed all1334 pinned identities from sealed INPUTS plus driver/input hashes: exact equality to AFTER.expected_sha256 and metadata keys; RESULT.read_paths is exactly that set. All366 loaded-module paths/hashes equal admitted AFTER receipts and pins. Cryptalis15 is exactly the configured eager set under this baseline/source221, not installed/amended product. AFTER says unchanged with zero errors. Baseline/amended namespace-before and namespace-after equal sealed controls; preservation-before and after are byte-identical. Bytecode prefix absent. Child/root exit1; host-after and preservation-after exit0; root streams and child stdout empty. Reviewed current three regression file hashes match accepted inputs.

RESULT.json SHA256 d16c9be1f6a34d5f8fc23c692634518a5a4bbeddfa87c45d8266bca0deda6f36
AFTER.json SHA256 fe82454cce4dfd31d66c4d4e991887f1373049fd8dd3431b9b18b3a985caf298
LOADED_MODULES.json SHA256 d76c941a3cc4acd458e3da2f77678601ee98e5e8055a65d2cd22742f29e67c6b
stderr.txt SHA256 3b2449a55b983154d980045039c929794e3debef9ac3c8c891df30b0cd5b6264

Root invocation-transcript.json matches reviewed shell command and driver argv, but is explicitly a post-run transcription attributed to tool chunk48b5ab, not in-process telemetry; this reviewer did not independently observe that tool invocation. Selection and exits are separately retained. Closure acceptance is evidence-receipt review, not a fresh full host/dependency-body audit.

No reviewer product execution, retry, DB/status, installation, Git or source modification. Direct-helper tests use real admitted modules with doubles. Cooperative guards/native-library trust limits remain; no physical-release, native DB, installed/full-suite, promotion or qualification claim follows. SA20 remains separate.
