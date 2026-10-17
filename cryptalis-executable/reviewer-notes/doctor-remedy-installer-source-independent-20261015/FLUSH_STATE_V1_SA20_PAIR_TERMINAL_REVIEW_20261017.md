# State cleanup V1 SA20 pair: intended RED and bounded PASS accepted

Decision: ACCEPTED_INTENDED_NO_DB_UNIT_RED_AND_SUCCESSOR_PASS, 2026-10-17.

Packet experiments/orm-flush-state-unit-packet-v1-20261016, seal4125c88a620d2c628d0fb0ea0d204fc0356711800851b5a0966de8f79dde7b39. Rehashed root-entry40c8160727dc5d932a85e14446dd50eb06cecfaa990640dd2babf3156cb59116, driver289721421add5ec0518c80728428f9f8ebdc6a05351117765b9d3c74d7c38518 and INPUTS91efc7e7735cc65cae4e73af517523505ba63bd2055381d2a68a1351f1c7faa6 match accepted command review.

Actual packet/run/sa20-baseline: one method,10 arms,8 intended assertion failures and2 ordinary controls PASS, no errors/skips. Exact subcase/method/ordinary/test-hash ledgers equal accepted SA21 baseline. Stderr is byte-identical to SA21 baseline: same eight intended assertions, not setup/import/signature failures. Root/child exit1; host/preservation after0.

Actual packet/run/sa20-amended: six methods PASS,29 subtests PASS plus sole ordinary test_interrupted_loop_never_publishes_partial_false PASS; no failures/errors/skips. Exact ledgers equal accepted SA21 amended. Shared10 identities preserved; diagnostic15 method/parameter/outcome/exception-type tuples also exactly equal accepted V7 SA20 amended. UNKNOWN unpublished/missing/integer_zero/false_like arms all present and PASS. Driver explicitly excludes skips before RESULT. Stderr byte-identical to SA21 amended, six methods OK. Root/child/host-after/preservation-after exits0.

Independently reconstructed1329 pins per cell from both source maps, selected SA20 dependency map, host map,three tests and exact driver/input hashes. Both AFTER.expected_sha256 and metadata keysets exactly match; RESULT.read_paths exactly matches pinset. Baseline365/amended366 module receipts all match corresponding pins and AFTER path/hash/admitted values; module keysets equal. Cryptalis15 exactly matches configured eager source set under the selected view. Complete AFTER reports unchanged and errors[]. Both namespace-before/after sets equal sealed221-file controls; preservation-before/after byte-identical. Bytecode prefixes absent, child stdout/root streams empty.

Baseline evidence SHA256:
- RESULT.json 437ba603b84782b6dc32da3e31cbe9a38c733ebb7f47a45484a138a95b5350ca
- AFTER.json 08a03acae06b9b6ba0e361af86f198525b795cff68de85055a753aafb389451e
- LOADED_MODULES.json 26511d58a87afb69ada9486370b0e7436383accea394a47fa7935ec9a17ca529
- stderr.txt 3b2449a55b983154d980045039c929794e3debef9ac3c8c891df30b0cd5b6264

Amended evidence SHA256:
- RESULT.json 05abf704e0a656807678e19e5b94f7ebe96f225a1acd34d4d2bca0060b75284f
- AFTER.json 0e2cba982b95960c6c334fd0b7ad4a246dde071cbaa78cb8c9ef9e8dfaa61bbb
- LOADED_MODULES.json c46878c5294dcb944689f6c5ea3d96d4256812411c011c84613c0063fc5d0945
- stderr.txt ea3fa6bd21d21e2c6559cdd522fb9b802752869ad2efed95716efb763ec47e09

Root captures are workspace-root persistence-recovery-20261013/flush-state-sa20-{baseline,amended}-root-20261017. Invocation transcriptions cite chunks2a797c/046974 and match accepted command/actual driver argv; these are explicitly transcription, not in-process telemetry or independently witnessed root invocations. Receipt review is not a new live host/dependency-body audit.

No reviewer execution/retry,DB/status,installation,Git or product edit. This finite real-module/double matrix does not establish native physical release,public integration,installed/full-suite qualification,promotion or readiness; cooperative guards/native-library trust limits and wider approval/resource holds persist.
