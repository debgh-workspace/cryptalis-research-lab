# V2 regression-oracle correction

Preserve V1 seal `987025a827c5b2b1b8ebbbddcee17b752c3c291190da593f8d549cba19fdf5a2`.
No V1 byte is changed. Both amended product files and their diff are identical
to V1. This remains the note-only slice; marker/name hazards stay unresolved.

The cleanup stub now records `sys.exception()` and the test asserts identity
after the helper returns, separately in all nine arms. A product catch block
cannot swallow this assertion. The transaction double likewise records the
native capture flag and asserts its exact True identity after helper completion.
No assertion inside a callback caught by the product is relied on.

The same three unittest methods and 15 subcases remain. Expected baseline RED
is still ten failed subcases and five passing controls; expected amended GREEN
is all 15. Neither expectation has been executed. A separately reviewed root
runner must record each addSubTest event to establish the observed arm ledger;
the ordinary unittest method count alone is three, not fifteen.

V1 source-only review remains its own historical verdict. V2 tests require a
new source review and root startup/import/command admission before execution.
