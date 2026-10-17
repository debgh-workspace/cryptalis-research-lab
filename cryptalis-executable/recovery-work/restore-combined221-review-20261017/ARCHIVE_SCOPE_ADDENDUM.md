# Exact focused archive read-scope reconciliation

This addendum clarifies inherited archive admission, without changing any parser, map or sealed review.

ARCHIVE_REVIEW.md SHA256 63fc609c7977f621c9db95751249f900869f01992d45bf4489c9fb3b06e4e05b explicitly records 664 ordinary members (656 content-addressed objects and eight generated controls), full UTF-8 member-body content review, 703 nonexcluded historical V2 safe-source entries, 255 V3 map entries and 1,014 excluded dependency-source bodies. Its scope states no raw phase JSON, environment dump, credential/home content, dependency/interpreter/cache/bytecode body, live corpus or runtime referent was opened. This is accepted bounded prior review evidence, not exhaustive secrets proof.

The new parser admits only the identical compressed archive SHA256 1f76f9bf50e7e757430edfe45b5ecb81afee67283675f2465c0d0b102f05822b AND identical raw tar SHA256 8e6c5233a98295872d30cd45bb5c79c27dda6e233ba20eb87497436c8caac50d before member hashing. Therefore the reviewed exact body set, not arbitrary paths in an untrusted archive, supplies the inherited source-data read scope. It does not authorize the excluded live files or any changed archive. Generic safe header admission alone would be insufficient without these exact pins and accepted review.

A filename denylist would not establish logical exclusion for content-addressed objects. The old external per-header/logical inventory was not separately recovered, so this reviewer does not claim independent reconstruction of every logical excluded path. Reliance on the accepted exact focused capsule must remain explicit. Root identified that capsule as the safe independent replacement; no new exclusion defect was established. The initial concern about absence of a newly reconstructed exclusion map should not be read as invalidating the accepted exact-archive scope.

Only the 221 source bodies are restored; archive evidence is hashed as already admitted inert data, never followed to runtime referents or restored as an environment. tests/conftest.py is inert hash/copy only, never import or execution. No decoder/parser was executed by this reviewer.
