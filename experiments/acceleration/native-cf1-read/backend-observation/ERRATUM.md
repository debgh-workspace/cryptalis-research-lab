# Preexisting mark claim correction

Earlier static/reconciliation reports included an unqualified claim that the helper loses a preexisting top-entry mark. Preserve those historical reports, but do not repeat that claim as established for the pinned OpenSSL 3.5.7 implementation.

Tagged primary source crypto/err/err_mark.c increments the top entry mark count in ERR_set_mark and decrements that count in ERR_pop_to_mark. Thus a successful balanced helper set/pop does not by itself establish loss of a preexisting mark in this implementation. Public documentation describes removal of a mark but does not detail this counter behavior. This is a source-backed correction, not a new runtime mark-preservation result.

This slice installs no preexisting marks. Its result covers only the declared ordinary unmarked public sentinel entries. Preexisting marks remain UNTESTED here; arbitrary queue/exhaustion/failure behavior remains unqualified. Full error-queue preservation must not be claimed.

Primary sources inspected:
- https://raw.githubusercontent.com/openssl/openssl/openssl-3.5.7/crypto/err/err_mark.c
- https://docs.openssl.org/3.5/man3/ERR_set_mark/
- https://docs.openssl.org/3.5/man3/ERR_get_error/

Observation API references:
- https://docs.openssl.org/3.5/man3/EVP_EncryptInit/
- https://docs.openssl.org/3.5/man3/EVP_KDF/
- https://docs.openssl.org/3.5/man3/EVP_MAC/
- https://docs.openssl.org/3.5/man3/OSSL_PROVIDER/
