# Erratum: preexisting OpenSSL error marks

2026-10-14. Earlier research discussion treated loss of a preexisting top-entry error mark as established. That assertion was unsupported for the pinned OpenSSL3.5.7 source.

Primary source: https://raw.githubusercontent.com/openssl/openssl/openssl-3.5.7/crypto/err/err_mark.c

The tagged implementation increments a per-entry mark count when setting a mark and decrements it when popping to one. Therefore a nested helper set/pop pair does not, from this source alone, establish the alleged loss. Root and the backend-observation worker independently inspected this source.

Correction: mark preservation is UNTESTED in the current finite runtime evidence, not a demonstrated loss. This does not certify installed source/binary correspondence, arbitrary queue preservation, full queue capacity behavior or all mark/error combinations. Original reports remain preserved; this note supersedes only their unverified categorical loss claim. The planned new benign queue slice covers unmarked sentinel entries only and will retain that scope.
