# Fixture hardening V1 source review: HOLD

Reviewed source only. Seal 8081e79460bb683a3deeea0ca4f42a53510f87d175bb3f1abb4b5c6fec2c74c2 and all four member hashes independently match. Original source remains pinned at 65223 bytes / 0d9de8f210d482db210b982e0aa2b027e989e0deb589114a753ee4dfbf869015. No imports, compilation, test collection/execution, DB, credentials or target mutations occurred.

## Correct narrow changes

_fixture_runtime_role performs the existing runtime connection/version/role checks before engine creation or fixture mutation, using explicit exceptions. _owned_fixture_schema performs CREATE and waits for its transaction context to return before entering the cleanup-protected body. A CREATE collision/failure or ambiguous commit therefore cannot reach DROP. This safely favors retaining an ambiguous fixture for separately authorized inspection over guessing ownership.

The source suffix from the first test definition onward is byte-identical to the accepted original; fixture ACL REVOKE/GRANT statements retain their original scope. Existing assertion behavior is not weakened. The new recording module declares nine parameter-expanded checks: three preflight refusals, one successful preflight ordering check, two unacquired failures and three owned-body outcomes. These are unexecuted source oracles, not test results. This review does not independently establish a native lifecycle count from parametrization.

## Blocking owned-handle paths

1. runtime.dispose() now lives inside the successfully entered _owned_fixture_schema body. A CREATE failure/collision or ambiguous commit bypasses that body and leaks the already created runtime engine. No DROP is correct, but no runtime disposal is not.
2. The tuple engine acquisition and mapping construction/setup occur before the outer try. If the second engine acquisition or subsequent setup raises, previously acquired owner/runtime/mapping handles do not receive guaranteed cleanup.
3. Outer cleanup calls owner.dispose() then mapping.dispose() sequentially. An owner disposal exception skips mapping disposal. The desired independently owned cleanup attempts are therefore not guaranteed.

The current helper-only recording owner cases cannot detect these search_application acquisition/disposal defects. The successful-preflight test intentionally stops at first engine acquisition and does not exercise cleanup.

## Required narrow successor

Preserve this V1 unchanged. Use acquisition-aware nested finally blocks or equivalent explicit owned-handle cleanup so every acquired resource gets a disposal attempt on all exits. Preserve runtime disposal before schema DROP after successful schema acquisition, and dispose runtime even when schema entry fails without issuing DROP. Ensure owner disposal failure cannot skip mapping disposal. Add recording-only full fixture-path oracles for second-engine failure, mapping/setup failure, CREATE collision/ambiguous commit, runtime disposal failure and owner disposal failure, with exact event ordering and zero guessed DROP. No DB execution is needed to prepare these tests.

External preflight for genuine credentials, role separation, exact cluster, exclusive fixture ownership and DROP CASCADE containment remains required. This helper does not establish those authorities. Cleanup exception aggregation/primary precedence must be stated accurately; no broader redesign is demanded. Source acceptance is HOLD pending the narrow immutable successor. Native DB authorization remains separate and unchanged.
