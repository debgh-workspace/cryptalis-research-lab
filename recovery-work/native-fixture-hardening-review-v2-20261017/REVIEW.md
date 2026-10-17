# Fixture hardening V2: conditional source acceptance

Decision: ACCEPTED_SOURCE_ONLY_FOR_SEPARATE_NO_DB_RUNNER_PREPARATION. The V1 handle-cleanup blockers are addressed by this immutable successor. This is not test execution acceptance or database authorization.

Packet recovery-work/native-fixture-hardening-v2-20261017 has SOURCE.sha256 1ef62cb531afcae5424a075fd81ca5fa1b96a5acda50fd5f5c4f9fc28e7ee346. All four member hashes independently match:

- INPUTS.json: 311 bytes, 55565521497daddb604b5954bb96d152671de09fac12e810869bf61545008100.
- PLAN.md: 2335 bytes, b3b76f744634dc121b3b4122fb1ca90391b69c3e4f3084c93350bb2336bf87c4.
- test_fixture_ownership_recording.py: 8506 bytes, f781b541d04954dee8eec7b6aff370f177b48d373113649b2d3136e66d552eb1.
- test_sqlalchemy_search.py: 66844 bytes, 113c40932fe7e84ccc309ce33362fa3fdcb8893b606e9938cc1676f8dfbd7c95.

Original source pin remains 65223 bytes / 0d9de8f210d482db210b982e0aa2b027e989e0deb589114a753ee4dfbf869015. V1 seal and all four bodies were rechecked unchanged; V1 retains its HOLD.

## Ownership and failure paths

Existing runtime connection/version/nonprivileged-role checks run before engine acquisition and all fixture mutations. Explicit exceptions retain checks even if assertions were optimized. Genuine credential, exact cluster, role separation and exclusive lab preflight remain external prerequisites.

CREATE and its transaction-context completion precede the cleanup-protected yield. Failed CREATE, collision, transaction entry or ambiguous commit cannot enter the DROP finally block. This deliberately retains ambiguity for separately authorized inspection rather than guessing ownership.

ExitStack now encloses owner acquisition, runtime acquisition, registry creation and subsequent setup. Each successfully returned resource registers its disposal. A second-engine failure disposes owner; registry failure disposes runtime and owner; mapping/setup or unacquired-schema failures dispose mapping, runtime and owner. No DROP occurs in those unacquired paths.

The runtime cleanup closure sets its attempted flag before invoking dispose. It is registered for early failures and explicitly invoked before DROP inside an acquired schema's body-finally. A raising runtime disposal therefore still reaches owned schema cleanup and remaining ExitStack callbacks, while the later registered callback does not silently retry it. Mapping cleanup and owner cleanup are independent callbacks; one raising does not skip the others. This establishes disposal attempts, not guaranteed successful disposal after a failure.

No exception suppression is introduced. An exception from cleanup can supersede the body exception under standard finally/ExitStack chaining. The design does not promise original-primary precedence, aggregate every failure or recovery from process termination. There is no custom throwing signal handler in this fixture change.

## Recording oracle review

Nine retained parameter-expanded helper/order cases plus ten full search_application cases give 19 declared cases. Their literal expected ledgers were inspected, not executed or collected:

- Three preflight refusals stop before engine access; successful preflight precedes owner acquisition.
- CREATE collision and ambiguous commit retain the selected exception identity and contain no DROP.
- Owned normal, ordinary-error and KeyboardInterrupt helper bodies reach exactly one DROP transaction.
- Full fixture cases cover first/second engine acquisition, registry acquisition, mapping setup, CREATE and commit failures, create_all failure and each runtime/mapping/owner disposal failure.

Full fixture mocks stop at create_all before compiler/provider work. Their event ledgers require correct acquisition/disposal order, and selected failure object identity. The runtime-disposal case's expected ledger contains only one disposal attempt before DROP. Disposal failures still reach remaining registered callbacks. These tests do not independently assert the complete exception __context__ chain or every possible combined cleanup failure; standard chaining is a source-semantic property here, not a tested claim.

The existing test suffix from the first test definition onward is byte-identical to the original; existing ACL statements and test assertions remain unchanged. This review does not independently certify the proposed 84 native fixture lifecycle count. Native case counts and mutation authority must be reconciled separately before any DB selection.

## Remaining gates

A separate reviewed no-DB runner must bind this exact isolated test module and recording module, avoid accidental frozen-module fallback or real credential/preflight access, admit required dependencies and bound execution. No such execution is selected by this review. Native pytest or DB operation remains independently gated, including exact generated fixture ownership, containment of DROP CASCADE, no unrelated dependencies, and survivor disposition after ambiguous commit. There are no new roles, credentials, global/default privileges or session-termination actions.

No target import, syntax compilation, test collection/run, native extension execution, database operation, Git or publication occurred during this review. Only separate reviewer output was written; the candidate, original source and held V1 remain untouched.
