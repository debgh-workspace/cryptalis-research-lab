# S22 source overlay

Restore the verified S21 210-file source (S20 remote base plus S21 overlay commit6e975d9e116b9422386aab1cff8eeaddabfd4a2f), then apply these three S22 source files. Verify all212 entries under source_sha256 in SOURCE_MANIFEST.json; reject missing, extra, or changed source files. Do not execute before checking approved environment and unchanged role preflights.

This snapshot adds NamedExpr and statement-target scanner corrections. Full SA21 source-overlay evidence is2623PASS/7FAIL/0SKIP plus56subtests; the seven legacy failures remain. SA20 full source run completed2577PASS/7FAIL/46SKIP plus56subtests; independent reconciliation is pending. Installed runtime validation remains pending. Packaging equality is bounded same-host evidence only. All seven qualification gates remain UNKNOWN.
