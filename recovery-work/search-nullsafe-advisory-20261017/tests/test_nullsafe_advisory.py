"""Unexecuted finite scanner oracles; no database or application-source execution."""
import ast
import json
import unittest

from cryptalis.manifest.compatibility import _Scan


CODE = "encrypted_nullsafe_comparison_refused_if_attached"
REASON = "This encrypted NULL-safe comparison is not admitted through the attached factory."
ALTERNATIVE = ("Review exact NULL-aware alternatives in staging; ordinary equality or inequality is not a general replacement. "
               "Never bypass the attached factory or use a plaintext fallback.")


def scan(source, queries=("eq",)):
    # Deliberately bypass plan/mapping validation to isolate deterministic AST
    # diagnostics. These declared-model facts are synthetic, not DB evidence.
    models = {"app.models.Customer": {"fields": {"secret": {"queries": list(queries)}}}}
    scanner = _Scan("app/queries.py", models)
    scanner.visit(ast.parse(source, filename="app/queries.py"))
    return scanner.findings


class NullSafeAdvisoryTests(unittest.TestCase):
    def test_both_methods_have_literal_line_and_remedy(self):
        for method in ("is_distinct_from", "is_not_distinct_from"):
            for queries in (("eq",), ()):
                for argument in ("None", "'PRIVATE_VALUE'", "runtime_operand"):
                    with self.subTest(method=method, queries=queries, argument=argument):
                        findings = scan("from app.models import Customer\nq = Customer.secret." + method + "(" + argument + ")\n", queries)
                        self.assertEqual(findings, [{
                            "code": CODE, "path": "app/queries.py", "line": 2,
                            "reason": REASON, "alternative": ALTERNATIVE,
                            "certainty": "CONDITIONAL_REFUSAL", "status": "SOURCE-INSPECTED",
                        }])

    def test_import_alias_and_multiple_occurrences_are_retained(self):
        findings = scan("from app.models import Customer as C\na = C.secret.is_distinct_from(None)\nb = C.secret.is_not_distinct_from(None)\n")
        self.assertEqual([(f["code"], f["line"]) for f in findings], [(CODE, 2), (CODE, 3)])

    def test_plain_or_unknown_fields_are_not_declared_refused(self):
        for expression in ("Customer.public", "Unknown.secret"):
            for method in ("is_distinct_from", "is_not_distinct_from"):
                self.assertEqual(scan("from app.models import Customer\nq = " + expression + "." + method + "(None)\n"), [])

    def test_shadowed_model_remains_unresolved_not_definite_refusal(self):
        source = "from app.models import Customer\ndef build(Customer):\n    return Customer.secret.is_distinct_from(None)\n"
        findings = scan(source)
        self.assertNotIn(CODE, [f["code"] for f in findings])
        self.assertTrue(any(f["code"] == "shadowed_query_binding" and f["certainty"] == "UNRESOLVED" for f in findings))

    def test_supported_presence_and_declared_equality_are_unchanged(self):
        source = "from app.models import Customer\na = Customer.secret.is_(None)\nb = Customer.secret.is_not(None)\nc = Customer.secret == 'ordinary'\nd = Customer.secret.in_(['ordinary'])\n"
        self.assertEqual(scan(source), [])
        self.assertEqual(scan("from app.models import Customer\na = Customer.secret.is_(None)\nb = Customer.secret.is_not(None)\n", ()), [])

    def test_source_literals_are_not_echoed_or_executed(self):
        findings = scan("from app.models import Customer\nq = Customer.secret.is_not_distinct_from('PRIVATE_SENTINEL')\nraise RuntimeError('MUST_NOT_EXECUTE')\n")
        rendered = json.dumps(findings)
        self.assertNotIn("PRIVATE_SENTINEL", rendered)
        self.assertNotIn("MUST_NOT_EXECUTE", rendered)
        self.assertEqual(len(findings), 1)
        # Positive control: the same collector can see an injected exposure.
        self.assertIn("PRIVATE_SENTINEL", json.dumps({"exposed": "PRIVATE_SENTINEL"}))


if __name__ == "__main__":
    unittest.main()
