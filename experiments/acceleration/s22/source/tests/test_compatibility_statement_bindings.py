"""Finite statement-target diagnostics, never execution of supplied sources."""
import textwrap

import pytest

from test_compatibility_string_bindings import inspect_source, BINDINGS


FORMS = {
    "for": "for NAME in values:\n    CALL\n",
    "with": "with manager as NAME:\n    CALL\n",
    "augassign": "NAME += replacement\nCALL\n",
    "delete": "del NAME\nCALL\n",
    "async_for": "async for NAME in values:\n    CALL\n",
    "async_with": "async with manager as NAME:\n    CALL\n",
}
SCOPES = [(form, scope) for form in ("for", "with", "augassign", "delete")
          for scope in ("module", "class", "function", "async_function")]
SCOPES += [(form, "async_function") for form in ("async_for", "async_with")]


@pytest.mark.parametrize("form,scope", SCOPES)
@pytest.mark.parametrize("imported,name,call,refusal", BINDINGS)
def test_statement_target_invalidates_local_import(inspect_source, form, scope,
                                                  imported, name, call, refusal):
    body = imported + "\n" + FORMS[form].replace("NAME", name).replace("CALL", call)
    body += call + "\n"
    if scope != "module":
        header = {"class": "class Work:", "function": "def work():",
                  "async_function": "async def work():"}[scope]
        body = header + "\n" + textwrap.indent(body, "    ")
    findings = inspect_source(body)
    assert [(f["code"], f["certainty"]) for f in findings] == [
        ("rebound_query_binding", "UNRESOLVED")]


@pytest.mark.parametrize("statement", [
    "for delete in delete(None):\n    delete(1)\n",
    "with delete(None) as delete:\n    delete(1)\n",
    "delete += delete(None)\ndelete(1)\n",
])
def test_input_expression_is_inspected_before_name_rebinding(inspect_source, statement):
    source = 'from sqlalchemy import delete\n' + statement
    source += 'from sqlalchemy import delete\ndelete(None)\n'
    findings = inspect_source(source)
    assert [(f["code"], f["line"]) for f in findings] == [
        ("core_dml_refused_if_attached", 2), ("rebound_query_binding", 2),
        ("core_dml_refused_if_attached", len(source.splitlines()))]


@pytest.mark.parametrize("statement,count", [
    ("for bucket[delete(1)] in delete(2):\n    pass\n", 2),
    ("with delete(1) as bucket[delete(2)], delete(3) as other:\n    pass\n", 3),
    ("bucket[delete(1)] += delete(2)\n", 2),
    ("del bucket[delete(1)]\n", 1),
])
def test_target_expressions_are_inspected_once_without_rebinding_load_names(
        inspect_source, statement, count):
    source = 'from sqlalchemy import delete\n' + statement + 'delete(None)\n'
    findings = inspect_source(source)
    assert [(f["code"], f["line"]) for f in findings] == [
        ("core_dml_refused_if_attached", 2)] * count + [
        ("core_dml_refused_if_attached", len(source.splitlines()))]


@pytest.mark.parametrize("statement", [
    "for delete.attribute in values:\n    pass\n",
    "with manager as delete.attribute:\n    pass\n",
    "delete.attribute += replacement\n",
    "del delete.attribute\n",
    "for delete[index] in values:\n    pass\n",
    "with manager as delete[index]:\n    pass\n",
    "delete[index] += replacement\n",
    "del delete[index]\n",
])
def test_attribute_and_subscript_bases_are_not_local_bindings(inspect_source, statement):
    source = 'from sqlalchemy import delete\n' + statement + 'delete(None)\n'
    assert [(f["code"], f["line"]) for f in inspect_source(source)] == [
        ("core_dml_refused_if_attached", len(source.splitlines()))]


@pytest.mark.parametrize("statement", [
    "for (delete, [text, *Customer]) in values:\n    pass\n",
    "with manager as (delete, [text, *Customer]):\n    pass\n",
    "del (delete, [text, Customer])\n",
])
def test_nested_actual_target_names_are_all_invalidated(inspect_source, statement):
    source = ('from sqlalchemy import delete, text\nfrom app.models import Customer\n'
              + statement + 'delete(1)\ntext("PRIVATE_LITERAL")\n'
              'Customer.note == "PRIVATE_LITERAL"\n')
    assert [(f["code"], f["line"], f["certainty"]) for f in inspect_source(source)] == [
        ("rebound_query_binding", 3, "UNRESOLVED")] * 3


def test_with_items_bind_left_to_right(inspect_source):
    source = ('from sqlalchemy import delete\n'
              'with delete(None) as delete, delete(1) as other:\n    delete(2)\n')
    assert [(f["code"], f["line"]) for f in inspect_source(source)] == [
        ("core_dml_refused_if_attached", 2), ("rebound_query_binding", 2)]


def test_target_unpacking_binds_left_to_right(inspect_source):
    source = ('from sqlalchemy import delete\n'
              'for delete, bucket[delete(1)] in values:\n    delete(2)\n')
    assert [(f["code"], f["line"]) for f in inspect_source(source)] == [
        ("rebound_query_binding", 2)]


def test_augmented_target_evaluation_precedes_rhs_without_repeating_target(inspect_source):
    source = ('from sqlalchemy import delete\n'
              'bucket[(delete := replacement)] += delete(1)\ndelete(2)\n')
    assert [(f["code"], f["line"]) for f in inspect_source(source)] == [
        ("rebound_query_binding", 2)]


def test_delete_sequence_and_explicit_reimport(inspect_source):
    source = ('from sqlalchemy import delete\ndel bucket[delete(1)], delete\n'
              'delete(2)\nfrom sqlalchemy import delete\ndelete(None)\n')
    assert [(f["code"], f["line"]) for f in inspect_source(source)] == [
        ("core_dml_refused_if_attached", 2), ("rebound_query_binding", 2),
        ("core_dml_refused_if_attached", 5)]


def test_del_is_function_lexical_binding_even_before_statement(inspect_source):
    source = ('from sqlalchemy import delete\ndef work():\n    delete(1)\n'
              '    del delete\n    delete(2)\ndelete(None)\n')
    assert [(f["code"], f["line"]) for f in inspect_source(source)] == [
        ("shadowed_query_binding", 2), ("core_dml_refused_if_attached", 6)]


def test_delete_attribute_does_not_make_base_a_function_local(inspect_source):
    source = ('from sqlalchemy import delete\ndef work():\n    delete(1)\n'
              '    del delete.attribute\n    delete(2)\n')
    assert [(f["code"], f["line"]) for f in inspect_source(source)] == [
        ("core_dml_refused_if_attached", 3), ("core_dml_refused_if_attached", 5)]
