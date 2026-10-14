"""Offline assignment-expression binding oracle; never execute supplied sources."""
import textwrap

import pytest

# Shared public-report fixture checks PARTIAL/advisory status, source hashes,
# unchanged mapper configuration and absence of supplied literal text.
from test_compatibility_string_bindings import inspect_source, BINDINGS


@pytest.mark.parametrize("scope", ["module", "class", "function", "async_function"])
@pytest.mark.parametrize("imported,name,call,refusal", BINDINGS)
def test_named_expression_rebinds_an_existing_local_import(
        inspect_source, scope, imported, name, call, refusal):
    body = imported + "\n(" + name + " := replacement)\n" + call + "\n"
    if scope != "module":
        header = {"class": "class Work:", "function": "def work():",
                  "async_function": "async def work():"}[scope]
        body = header + "\n" + textwrap.indent(body, "    ")
    findings = inspect_source(body)
    assert [(f["code"], f["certainty"]) for f in findings] == [
        ("rebound_query_binding", "UNRESOLVED")]


def test_named_expression_visits_rhs_before_rebinding_and_preserves_reimport(inspect_source):
    source = ('from sqlalchemy import delete\n'
              '(delete := delete("PRIVATE_LITERAL"))\ndelete(None)\n'
              'from sqlalchemy import delete\ndelete(None)\n')
    findings = inspect_source(source)
    assert [(f["code"], f["line"]) for f in findings] == [
        ("core_dml_refused_if_attached", 2), ("rebound_query_binding", 2),
        ("core_dml_refused_if_attached", 5)]


def test_unrelated_assignment_expression_keeps_the_query_import(inspect_source):
    source = ('from sqlalchemy import text\n'
              '(value := text("PRIVATE_LITERAL"))\ntext("PRIVATE_LITERAL")\n')
    findings = inspect_source(source)
    assert [(f["code"], f["line"]) for f in findings] == [
        ("raw_sql_refused_if_attached", 2), ("raw_sql_refused_if_attached", 3)]


@pytest.mark.parametrize("expression", [
    '[(delete := replacement, delete(1)) for item in values]',
    '{(delete := replacement, delete(1)) for item in values}',
    '{item: (delete := replacement, delete(1)) for item in values}',
    '((delete := replacement, delete(1)) for item in values)',
])
def test_comprehension_walrus_invalidates_inner_and_enclosing_import(inspect_source, expression):
    source = 'from sqlalchemy import delete\n' + expression + '\ndelete(None)\n'
    findings = inspect_source(source)
    # Existing conservative outer invalidation remains. The new visitor also
    # invalidates the name before the later call in the element expression.
    assert [(f["code"], f["line"], f["certainty"]) for f in findings] == [
        ("rebound_query_binding", 2, "UNRESOLVED")] * 2


def test_comprehension_loop_target_remains_local_and_outer_call_is_visible(inspect_source):
    source = ('from sqlalchemy import delete\n'
              '[(value := delete(1)) for delete in callbacks]\ndelete(None)\n')
    findings = inspect_source(source)
    assert [(f["code"], f["line"]) for f in findings] == [
        ("rebound_query_binding", 2), ("core_dml_refused_if_attached", 3)]


def test_function_lexical_walrus_shadowing_and_outer_scope_are_preserved(inspect_source):
    source = ('from sqlalchemy import delete\ndef work():\n    delete(1)\n'
              '    [(delete := replacement) for item in values]\n'
              '    delete(1)\ndelete(None)\n')
    findings = inspect_source(source)
    assert [(f["code"], f["line"]) for f in findings] == [
        ("shadowed_query_binding", 2), ("core_dml_refused_if_attached", 6)]
