"""Finite offline advisory binding regressions; supplied source is never executed."""
import hashlib
import json
import textwrap

import pytest
from sqlalchemy import Column, Integer, MetaData, Table, Text
from sqlalchemy.orm import registry

from cryptalis.manifest.compatibility import inspect_plan_compatibility


@pytest.fixture
def inspect_source():
    mapping = registry(metadata=MetaData())

    class Customer:
        pass

    Customer.__module__ = "app.models"
    table = Table("customer", mapping.metadata, Column("id", Integer, primary_key=True),
                  Column("note", Text))
    mapper = mapping.map_imperatively(Customer, table)
    # This API validates report-input shape, not lock authenticity/admission.
    lock = json.dumps({"schema": "cryptalis.lock/v1", "models": [{
        "model": "Customer", "schema": "public", "table": "customer",
        "record": {"codec": "int64-be/v1"},
        "fields": [{"name": "note", "queries": []}],
    }]}).encode()

    def inspect(source):
        raw = source.encode()
        before = mapper.configured
        report = inspect_plan_compatibility(lock, mapping, sources={"app/jobs.py": raw})
        assert mapper.configured is before
        assert report["effects"] == "NONE"
        assert report["coverage"] == "PARTIAL"
        assert report["authority"] == "ADVISORY_NOT_AUTHENTICATED"
        assert report["staging_required"] is True
        assert report["sources"][0]["sha256"] == hashlib.sha256(raw).hexdigest()
        assert "PRIVATE_LITERAL" not in json.dumps(report)
        return report["findings"]

    yield inspect
    mapping.dispose()


FORMS = {
    "except": "try:\n    pass\nexcept Exception as NAME:\n    CALL\n",
    "as": "match subject:\n    case NAME if CALL:\n        pass\n",
    "star": "match subject:\n    case [*NAME] if CALL:\n        pass\n",
    "rest": "match subject:\n    case {**NAME} if CALL:\n        pass\n",
}
BINDINGS = [
    ("from sqlalchemy import delete", "delete", 'delete("PRIVATE_LITERAL")',
     "core_dml_refused_if_attached"),
    ("from sqlalchemy import text", "text", 'text("PRIVATE_LITERAL")',
     "raw_sql_refused_if_attached"),
    ("from app.models import Customer", "Customer", 'Customer.note == "PRIVATE_LITERAL"',
     "storage_only_comparison_refused_if_attached"),
]


@pytest.mark.parametrize("form", FORMS)
@pytest.mark.parametrize("scope", ["module", "class", "function", "async_function"])
@pytest.mark.parametrize("imported,name,call,refusal", BINDINGS)
def test_string_targets_are_unresolved_not_false_refusals(
        inspect_source, form, scope, imported, name, call, refusal):
    body = FORMS[form].replace("NAME", name).replace("CALL", call) + call + "\n"
    if scope in ("function", "async_function"):
        # Lexical shadowing applies before the first binding, too.
        body = call + "\n" + body
    if scope != "module":
        header = {"class": "class Work:", "function": "def work():",
                  "async_function": "async def work():"}[scope]
        body = header + "\n" + textwrap.indent(body, "    ")
    findings = inspect_source(imported + "\n" + body)
    assert refusal not in {f["code"] for f in findings}
    expected = "shadowed_query_binding" if "function" in scope else "rebound_query_binding"
    assert [(f["code"], f["certainty"]) for f in findings] == [(expected, "UNRESOLVED")]


@pytest.mark.parametrize("form", FORMS)
def test_inner_scope_does_not_erase_outer_import(inspect_source, form):
    body = FORMS[form].replace("NAME", "delete").replace("CALL", "delete(1)")
    source = "from sqlalchemy import delete\ndef work():\n" + textwrap.indent(body, "    ")
    source += "delete(None)\n"
    findings = inspect_source(source)
    assert [f["code"] for f in findings] == ["shadowed_query_binding", "core_dml_refused_if_attached"]
    assert findings[-1]["line"] == len(source.splitlines())


def test_match_subject_and_explicit_reimport_remain_visible(inspect_source):
    source = ('from sqlalchemy import delete\nmatch delete(None):\n'
              '    case delete:\n        pass\n'
              'from sqlalchemy import delete\ndelete(None)\n')
    findings = inspect_source(source)
    assert [(f["code"], f["line"]) for f in findings] == [
        ("core_dml_refused_if_attached", 2), ("rebound_query_binding", 3),
        ("core_dml_refused_if_attached", 6)]


def test_exception_target_cleanup_and_sibling_match_cases_are_conservative(inspect_source):
    source = ('from sqlalchemy import delete\ntry:\n    pass\n'
              'except Exception as delete:\n    from sqlalchemy import delete\n'
              '    delete(None)\ndelete(None)\n'
              'from sqlalchemy import delete\nmatch subject:\n'
              '    case [delete]:\n        from sqlalchemy import delete\n'
              '        delete(None)\n    case {"key": delete} if delete(1):\n'
              '        pass\ndelete(None)\n')
    findings = inspect_source(source)
    assert [(f["code"], f["line"]) for f in findings] == [
        ("rebound_query_binding", 4), ("core_dml_refused_if_attached", 6),
        ("rebound_query_binding", 10), ("core_dml_refused_if_attached", 12)]


def test_wildcards_unrelated_targets_and_outer_defaults_preserve_real_imports(inspect_source):
    source = ('from sqlalchemy import delete\n'
              'def work(value=delete(None)):\n'
              '    try:\n        pass\n    except Exception as unrelated:\n'
              '        delete(None)\n    match value:\n'
              '        case [*_]:\n            delete(None)\n'
              '        case _:\n            delete(None)\n'
              'delete(None)\n')
    findings = inspect_source(source)
    assert [(f["code"], f["line"]) for f in findings] == [
        ("core_dml_refused_if_attached", line) for line in (2, 6, 9, 11, 12)]


def test_nested_patterns_invalidate_every_capture(inspect_source):
    source = ('from sqlalchemy import delete, text\nfrom app.models import Customer\n'
              'match subject:\n'
              '    case {"key": [delete, *text], **Customer} if delete(1):\n'
              '        text("PRIVATE_LITERAL")\n'
              '        Customer.note == "PRIVATE_LITERAL"\n')
    findings = inspect_source(source)
    assert [(f["code"], f["line"], f["certainty"]) for f in findings] == [
        ("rebound_query_binding", 4, "UNRESOLVED")] * 3
