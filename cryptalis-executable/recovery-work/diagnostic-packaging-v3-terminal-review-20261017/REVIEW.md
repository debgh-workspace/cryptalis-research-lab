# Diagnostic packaging V3 terminal audit

Disposition: FAIL PRESERVED; FIRST SDIST ACCEPTED AS AN INERT CONTINUATION INPUT. This is not five-output packaging acceptance. No build, parser/helper execution, installation or retry was performed by reviewer.

The selected V3 controller exited1. Its driver exited1 without timeout, cancellation, group signal or cleanup error; leader was reaped. stdout is empty; stderr is1309 bytes containing the exact namespace assertion traceback. The first uv sdist command recorded exit0 and its log says it completed. The driver then rejected the output directory because it contained an additional .gitignore. It did not reach the second sdist or any wheel. No extracted tree exists. The driver FAIL receipt correctly reports both source copies complete/equal and extracted incomplete. Root capture is persistence-recovery-20261013/diagnostic-packaging-v3-20261017-1437; root after-check exit is reported0, not a replacement for controller1.

All239 outer after entries report unchanged metadata and bytes. Independently rechecked all239 current declared metadata tuples against before and all current hashes against the233 static pins, copied actual review pins and selection/control bindings. Both complete221-file source copies independently match the proposed manifest:442 file hashes. Original patch remains bound by the same closure. Cold bytecode prefix is absent. descendants_verified_absent remains false; normal leader reap does not establish a global process-absence claim.

## Retained first artifact

run/sdist-1/cryptalis-0.1.0.tar.gz is150917 bytes, SHA256 f8520edb34bb20af9a348a2e68f4073346548057d8d7e52b1489d2d0608632d8. Independent bounded single-stream gzip decoding and exact header/type/namespace admission found49 regular payloads and6 directories. No extra member, link, PAX/sparse entry or trailing nonzero data was admitted. Header metadata equals the authenticated accepted predecessor. All43 runtime source payload hashes equal the proposed221 manifest. README/LICENSE/lock and original config match source; all remaining payloads equal predecessor. The only payload delta is cryptalis-0.1.0/src/cryptalis/migration.py. This supports reuse of this completed first sdist, not a claim of reproducibility before the second is built.

## Exact generated sidecar

After root explicitly admitted this one generated regular single-link one-byte file, a bounded O_NOFOLLOW read of run/sdist-1/.gitignore returned exactly the byte '*'. SHA256684888c0ebb17f374298b65ee2807526c066094c701bcc7ebbe1c1095f494fc1; mode0644; metadata was stable across descriptor/path checks. No other hidden/cache body was read.

Independently fetched official astral-sh/uv tag0.12.23 source through the GitHub connector: crates/uv/src/commands/build_frontend.rs, Git blob52fc0b40adfb19ef35277df0c64927196607b304, lines1362–1382. prepare_output_directory creates this exact output-side .gitignore exclusively and writes one asterisk when enabled. Source: https://github.com/astral-sh/uv/blob/0.12.23/crates/uv/src/commands/build_frontend.rs#L1362-L1382 . This explains documented source behavior and agrees with observed bytes. It does not prove source-to-binary provenance of the locally admitted uv binary. Initial web fetches returned cache misses; the connector read succeeded, with no access denial or workaround around a restriction.

## Smallest continuation

Prepare a separate sealed packet that pins this completed sdist, exact sidecar, V3 terminal/command receipts and review as preserved inputs. Leave V3 source/output/FAIL unchanged. Freshly admit all original source/tool/control inputs and quiescence; copy into new owned working trees if needed. Execute only the remaining four builds: second sdist, two direct wheels and one wheel from boundedly admitted first-sdist materialization. Retain the same payload/RECORD/negative-lock/reproducibility oracles and compare the new second sdist to this exact first artifact. Admit only the specifically source-proven one-byte sidecar in each relevant output namespace, not arbitrary dotfiles or cache bodies. Any new outcome still requires full original-input and retained-artifact before/after checks plus independent terminal audit.

The prospective continuation needs its own reviewed fixed commands, bounded outputs and explicit root selection; this report does not select it. No repeated first build is needed on the evidence currently established. No installer, runtime/DB test, search integration, production promotion or upload authority follows. Pending archive-upload hold remains unchanged.

Reviewer diagnostic: an initial data-reader assertion compared full stat tuples including atime and stopped after a read changed access time. It was corrected to the declared dev/ino/mode/nlink/size/mtime/ctime continuity tuple, then the independent data audit passed. No producer was rerun or modified. Exact checks and stable sidecar metadata are recorded in CHECKS.json.
