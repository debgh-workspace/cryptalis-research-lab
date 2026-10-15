"""UNEXECUTED standalone vectors. Root review is required before any run.

No product imports, database, network, filesystem, plugins or credentials.
Synthetic schema/guard placeholders test sizing only; they are not an admitted
physical schema, valid guard inventory, or authenticated transition artifact.
"""

import copy
import json
import unittest

from envelope_reference import (
    PreparationError, DOCUMENT_LIMIT, EXACT_ARTIFACT_COUNTER_MAX, check_expansion_reservation,
    check_next_progress, cursor, integer_width, maximum_state, object_from_pairs,
    sizes, string_width, validate_state, validate_within_envelope,
    validate_proposed_forward_summary, validate_proposed_reverse_summary,
)


TABLE = "00000000-0000-0000-0000-000000000001"
SOURCE = "00000000-0000-0000-0000-000000000002"


def synthetic_expanded(count, *, reverse=False):
    state = {"phase": "EXPANDED", "models": {TABLE: {
        "scope": {"count": count, "membership": "0" * 64},
        "cursor": None, "rows": 0, "chunks": 0,
        "schema": {"test_only": True, "text": "é 雪 😀 \" \\ \n"},
        "guard": ["A", "test-only; not an admitted native guard"],
    }}}
    if reverse:
        state.update(layout_version=101, source_operation_id=SOURCE,
                     source_plan_digest="1" * 64)
    return state


class ReferenceVectors(unittest.TestCase):
    def test_scalar_and_separator_vectors(self):
        vectors = [
            (None, 4, 0), (True, 4, 0), (False, 5, 0), (0, 1, 0),
            (-9223372036854775808, 20, 0), (9007199254740991, 16, 0),
            (10000000000000000, 17, 0), ("", 2, 0), ("é", 4, 0),
            ("雪", 5, 0), ("😀", 6, 0), ("\u0001", 8, 0),
            ("\n", 4, 0), ('"', 4, 0), ("\\", 4, 0),
            ([], 2, 0), ({}, 2, 0), ([0, 1], 5, 1),
            ({"a": 0}, 7, 1), ({"a": [0, 1], "b": True}, 20, 4),
        ]
        for value, compact, separators in vectors:
            with self.subTest(value_type=type(value).__name__, compact=compact):
                actual = sizes(value)
                self.assertEqual((actual.canonical_bytes, actual.separators), (compact, separators))
                wire = json.dumps(value, ensure_ascii=False, sort_keys=True,
                                  separators=(",", ":"), allow_nan=False).encode("utf-8")
                self.assertEqual(actual.canonical_bytes, len(wire))

    def test_invalid_json_inputs_stay_explicit(self):
        cycle = []
        cycle.append(cycle)
        cases = [float("nan"), float("inf"), 1.0, (1,), b"x", {1: "x"},
                 {"é": 1}, "\x00", "\ud800", "\udfff", cycle]
        for value in cases:
            with self.subTest(value_type=type(value).__name__):
                with self.assertRaises(PreparationError):
                    sizes(value)
        with self.assertRaises(PreparationError):
            json.loads('{"rows":1,"rows":2}', object_pairs_hook=object_from_pairs)

    def test_nesting_and_reused_subtrees(self):
        value = 0
        for _ in range(32):
            value = [value]
        self.assertEqual(sizes(value).canonical_bytes, 65)
        with self.assertRaises(PreparationError):
            sizes([value])
        shared = [0]
        self.assertEqual(sizes([shared, shared]).canonical_bytes, 9)

    def test_cursor_domains_and_exact_widths(self):
        self.assertEqual(string_width("ffffffff-ffff-ffff-ffff-ffffffffffff"), 38)
        self.assertEqual(string_width("-9223372036854775808"), 22)
        for value in (None, "-9223372036854775808", "9223372036854775807", "0", "-1"):
            cursor(value, "int64-be/v1")
        for value in ("+1", "01", "-0", " 1", "١", "9223372036854775808",
                      "-9223372036854775809", "1e0", True, 1):
            with self.assertRaises(PreparationError):
                cursor(value, "int64-be/v1")
        cursor("00000000-0000-0000-0000-000000000000", "uuid16/v1")
        for value in ("Ffffffff-ffff-ffff-ffff-ffffffffffff", "f" * 32,
                      "{ffffffff-ffff-ffff-ffff-ffffffffffff}"):
            with self.assertRaises(PreparationError):
                cursor(value, "uuid16/v1")

    def test_no_invented_sixteen_digit_journal_cap(self):
        codecs = {TABLE: "int64-be/v1"}
        for count in (0, 1, 9, 10, 9999, 10000, EXACT_ARTIFACT_COUNTER_MAX,
                      EXACT_ARTIFACT_COUNTER_MAX + 1, 10**16, 2**63):
            expanded = synthetic_expanded(count)
            maximum = maximum_state(expanded, codecs)
            self.assertEqual(maximum["models"][TABLE]["rows"], count)
            check_expansion_reservation(expanded, codecs)
        expanded = synthetic_expanded(EXACT_ARTIFACT_COUNTER_MAX + 1)
        with self.assertRaises(PreparationError):
            maximum_state(expanded, codecs, artifact_counter_profile=True)
        self.assertEqual(integer_width(10**5000), 5001)

    def test_forward_and_reverse_abort_never_grow_maximum(self):
        for reverse in (False, True):
            for codec in ("uuid16/v1", "int64-be/v1"):
                codecs = {TABLE: codec}
                expanded = synthetic_expanded(10, reverse=reverse)
                maximum = maximum_state(expanded, codecs, reverse=reverse)
                self.assertEqual("verification" in maximum, not reverse)
                for phase in ("EXPANDED", "BACKFILLED", "VERIFIED", "ABORTED"):
                    current = copy.deepcopy(maximum)
                    current["phase"] = phase
                    observed = validate_within_envelope(current, expanded, codecs, reverse=reverse)
                    self.assertLessEqual(observed.canonical_bytes, sizes(maximum).canonical_bytes)
                aborted = {**maximum, "phase": "ABORTED"}
                self.assertEqual(sizes(maximum).canonical_bytes - sizes(aborted).canonical_bytes, 3)

    def test_frozen_fields_unknown_fields_and_bool_aliases(self):
        codecs = {TABLE: "uuid16/v1"}
        expanded = synthetic_expanded(2)
        for field, value in (("rows", True), ("chunks", 1.0), ("rows", -1), ("rows", 3)):
            changed = copy.deepcopy(expanded)
            changed["models"][TABLE][field] = value
            with self.assertRaises(PreparationError):
                validate_state(changed, codecs)
        for field in ("active_schema", "unexpected"):
            changed = copy.deepcopy(expanded)
            changed["models"][TABLE][field] = {}
            with self.assertRaises(PreparationError):
                validate_state(changed, codecs)
        changed = copy.deepcopy(expanded)
        changed["models"][TABLE]["schema"]["test_only"] = 1
        with self.assertRaises(PreparationError):
            validate_within_envelope(changed, expanded, codecs)
        changed = copy.deepcopy(expanded)
        changed["models"][TABLE]["scope"]["membership"] = "2" * 64
        with self.assertRaises(PreparationError):
            validate_within_envelope(changed, expanded, codecs)

    def test_lineage_is_explicit_frozen_input_not_inferred_authority(self):
        codecs = {TABLE: "uuid16/v1"}
        # This key is illustrative only; no proposed product wire shape is selected.
        frozen = {"proof_only_lineage_placeholder": [{"operation_id": SOURCE, "digest": "a" * 64}]}
        expanded = {**synthetic_expanded(1), **copy.deepcopy(frozen)}
        maximum = maximum_state(expanded, codecs, frozen_root=frozen)
        validate_within_envelope(maximum, expanded, codecs, frozen_root=frozen)
        maximum["proof_only_lineage_placeholder"][0]["digest"] = "b" * 64
        with self.assertRaises(PreparationError):
            validate_state(maximum, codecs, frozen_root=frozen)

    def test_pre_sql_next_counter_guard(self):
        progress = synthetic_expanded(1)["models"][TABLE]
        self.assertEqual(check_next_progress(progress, 1), (1, 1))
        for count in (True, 0, -1, 2, 5001):
            with self.assertRaises(PreparationError):
                check_next_progress(progress, count)

    def test_proposed_summary_shapes_are_finite_and_exact(self):
        root = {"format": "cryptalis.transition/retained-native-comments-cluster-research-v2",
                "operation_id": SOURCE, "plan_digest": "a" * 64}
        summary = {"schema": "cryptalis.aborted-forward-lineage/research-v1", "root": root,
                   "predecessor": {"operation_id": SOURCE, "plan_digest": "a" * 64},
                   "count": 1, "digest": "b" * 64}
        validate_proposed_forward_summary(summary)
        expanded = {**synthetic_expanded(1), "aborted_forward": copy.deepcopy(summary)}
        frozen = {"aborted_forward": summary}
        check_expansion_reservation(expanded, {TABLE: "uuid16/v1"}, frozen_root=frozen)
        for count in (0, True, 1.0, EXACT_ARTIFACT_COUNTER_MAX + 1):
            with self.assertRaises(PreparationError):
                validate_proposed_forward_summary({**summary, "count": count})
        changed = copy.deepcopy(summary)
        changed["root"]["format"] += "-unknown"
        with self.assertRaises(PreparationError):
            validate_proposed_forward_summary(changed)
        validate_proposed_reverse_summary({"schema": "cryptalis.aborted-reverse-set/research-v1",
                                           "count": 0, "digest": "c" * 64})

    def test_exact_canonical_and_native_candidate_budget_edges(self):
        codecs = {TABLE: "uuid16/v1"}
        expanded = synthetic_expanded(1)
        expanded["models"][TABLE]["schema"]["fill"] = ""
        base = sizes(maximum_state(expanded, codecs))
        for margin in (-1, 0, 1):
            expanded["models"][TABLE]["schema"]["fill"] = "x" * (
                DOCUMENT_LIMIT - base.jsonb_text_candidate_bytes + margin)
            observed = sizes(maximum_state(expanded, codecs))
            self.assertEqual(observed.jsonb_text_candidate_bytes, DOCUMENT_LIMIT + margin)
            if margin <= 0:
                check_expansion_reservation(expanded, codecs)
            else:
                with self.assertRaises(PreparationError):
                    check_expansion_reservation(expanded, codecs)
        for margin in (-1, 0, 1):
            expanded["models"][TABLE]["schema"]["fill"] = "x" * (
                DOCUMENT_LIMIT - base.canonical_bytes + margin)
            self.assertEqual(sizes(maximum_state(expanded, codecs)).canonical_bytes,
                             DOCUMENT_LIMIT + margin)

    def test_omission_controls_expose_missing_reservations(self):
        codecs = {TABLE: "uuid16/v1"}
        expanded = synthetic_expanded(EXACT_ARTIFACT_COUNTER_MAX)
        correct = maximum_state(expanded, codecs)
        # Independent state construction: do not derive the deciding positive
        # state from the candidate maximum constructor whose omissions we test.
        actual_abort = copy.deepcopy(expanded)
        actual_abort["phase"] = "ABORTED"
        actual_abort["verification"] = {TABLE: "a" * 64}
        actual_abort["models"][TABLE].update(
            cursor="ffffffff-ffff-ffff-ffff-ffffffffffff",
            rows=EXACT_ARTIFACT_COUNTER_MAX, chunks=EXACT_ARTIFACT_COUNTER_MAX)
        self.assertLessEqual(sizes(actual_abort).canonical_bytes, sizes(correct).canonical_bytes)
        for omission in ("verification", "cursor", "counters"):
            wrong = copy.deepcopy(correct)
            if omission == "verification":
                del wrong["verification"]
            elif omission == "cursor":
                wrong["models"][TABLE]["cursor"] = None
            else:
                wrong["models"][TABLE]["rows"] = 0
                wrong["models"][TABLE]["chunks"] = 0
            self.assertGreater(sizes(actual_abort).canonical_bytes, sizes(wrong).canonical_bytes)
        changed = {**actual_abort, "unreserved_abort_receipt": "x"}
        with self.assertRaises(PreparationError):
            validate_within_envelope(changed, expanded, codecs)


# Intentionally no unittest.main() entry point. These vectors have NOT RUN.
