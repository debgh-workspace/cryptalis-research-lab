# Source-only preparation incident

The first preparation pass compared entire JUnit diagnostic bodies between accepted S25 source and installed main runs. It stopped at an assertion because source/installed traceback text carries different source paths. It performed no target import, collection, test, database or candidate mutation. Already written new packet files were retained.

The corrected data-only comparison requires exact ordinary ID/outcome maps and exact failure/skip messages, consistent with the accepted independent S25 audit boundary. Original source diagnostic bodies are retained in S25_*_DIAGNOSTICS.json for review. Existing partial packet files were required to be byte-identical before reuse; no old packet or candidate was replaced. No result is relabeled and no traceback semantic mismatch is waived by this correction.
