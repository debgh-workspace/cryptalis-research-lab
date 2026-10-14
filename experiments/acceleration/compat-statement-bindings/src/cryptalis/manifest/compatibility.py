"""Advisory source inspection. Never import sources or authorize an operation."""
import ast
import hashlib
from pathlib import PurePosixPath

from sqlalchemy.orm import registry as Registry

from .parser import ManifestInvalid, decode_manifest_json

MAX_SOURCE_FILES = 256
MAX_SOURCE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 16 * 1024 * 1024
MAX_AST_NODES = 50000
MAX_FINDINGS = 2048


class CompatibilityInspectionUnavailable(RuntimeError):
    effects = "NONE"
    stage = "compatibility_source_inspection"
    remedy = "Supply a bounded source snapshot and run the application suite in staging."

    def __init__(self, code):
        self.code = code
        super().__init__(f"Compatibility inspection unavailable: {code}. {self.remedy}")


def _finding(code, path, line, reason, alternative, certainty="CONDITIONAL_REFUSAL"):
    return dict(code=code, path=path, line=line, reason=reason,
                alternative=alternative, certainty=certainty, status="SOURCE-INSPECTED")


def _module(path):
    parts = list(PurePosixPath(path).parts)
    parts[-1] = parts[-1][:-3]
    package = parts[-1] == "__init__"
    if package:
        parts.pop()
    if not parts or not all(part.isidentifier() for part in parts):
        return None, package
    return ".".join(parts), package


def _string_binding(node):
    """Binding targets represented as strings rather than Name(Store) nodes."""
    if isinstance(node, (ast.ExceptHandler, ast.MatchAs, ast.MatchStar)):
        return node.name
    if isinstance(node, ast.MatchMapping):
        return node.rest
    return None


def _locals(node):
    """Python locals shadow outer names even before their first assignment."""
    names = set()
    args = node.args
    for arg in (*args.posonlyargs, *args.args, *args.kwonlyargs):
        names.add(arg.arg)
    for arg in (args.vararg, args.kwarg):
        if arg is not None:
            names.add(arg.arg)
    pending = list(node.body) if isinstance(node.body, list) else [node.body]
    while pending:
        child = pending.pop()
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(child.name)
            continue
        if isinstance(child, (ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            for expression in ast.walk(child):
                if isinstance(expression, ast.NamedExpr) and isinstance(expression.target, ast.Name):
                    names.add(expression.target.id)
            continue
        if isinstance(child, ast.Name) and isinstance(child.ctx, (ast.Store, ast.Del)):
            names.add(child.id)
        elif isinstance(child, (ast.Import, ast.ImportFrom)):
            names.update(alias.asname or alias.name.split(".")[0] for alias in child.names)
        name = _string_binding(child)
        if name is not None:
            names.add(name)
        pending.extend(ast.iter_child_nodes(child))
    return names


class _Scan(ast.NodeVisitor):
    def __init__(self, path, models):
        self.path = path
        self.module, self.package = _module(path)
        self.models = models
        self.bindings = {name: "builtins." + name for name in ("exec", "eval", "__import__")}
        self.findings = []

    def add(self, code, node, reason, alternative, certainty="CONDITIONAL_REFUSAL"):
        if len(self.findings) >= MAX_FINDINGS:
            raise CompatibilityInspectionUnavailable("finding_budget_exceeded")
        self.findings.append(_finding(code, self.path, getattr(node, "lineno", None),
                                      reason, alternative, certainty))

    def qualified(self, node):
        if isinstance(node, ast.Name):
            return self.bindings.get(node.id)
        if isinstance(node, ast.Attribute):
            base = self.qualified(node.value)
            return base + "." + node.attr if base else None
        return None

    def field(self, node):
        if isinstance(node, ast.Attribute):
            model = self.models.get(self.qualified(node.value))
            if model is not None:
                return model["fields"].get(node.attr)
        return None

    def visit_Import(self, node):
        for alias in node.names:
            self.bindings[alias.asname or alias.name.split(".")[0]] = (
                alias.name if alias.asname else alias.name.split(".")[0])

    def visit_ImportFrom(self, node):
        base = node.module or ""
        if node.level:
            package = self.module if self.package else (self.module or "").rpartition(".")[0]
            parts = package.split(".") if package else []
            if not parts or node.level > len(parts):
                self.add("relative_import_unresolved", node,
                         "This relative import cannot be resolved from the supplied source label.",
                         "Use repository-relative module paths and verify the call sites in staging.", "UNRESOLVED")
                return
            base = ".".join(parts[:len(parts) - node.level + 1] + ([base] if base else []))
        for alias in node.names:
            if alias.name == "*":
                self.add("wildcard_import_unresolved", node,
                         "Wildcard imports hide query and model bindings from this analysis.",
                         "Inspect these bindings and exercise the application paths in staging.", "UNRESOLVED")
            else:
                self.bindings[alias.asname or alias.name] = base + "." + alias.name

    def _function(self, node):
        for expression in (*node.decorator_list, *node.args.defaults, *node.args.kw_defaults):
            if expression is not None:
                self.visit(expression)
        self._rebind(node.name, node)
        previous = self.bindings
        locals_ = _locals(node)
        relevant = {name for name in locals_ if name in previous and (
            previous[name].startswith(("sqlalchemy.", "sqlmodel.", "builtins."))
            or previous[name] in self.models)}
        if relevant:
            self.add("shadowed_query_binding", node,
                     "A local name shadows an imported query or model binding.",
                     "Confirm the actual callable or model in staging; do not treat this source scan as admission.",
                     "UNRESOLVED")
        self.bindings = {name: value for name, value in previous.items() if name not in locals_}
        try:
            for statement in node.body:
                self.visit(statement)
        finally:
            self.bindings = previous

    visit_FunctionDef = _function
    visit_AsyncFunctionDef = _function

    def visit_Lambda(self, node):
        previous = self.bindings
        self.bindings = {name: value for name, value in previous.items() if name not in _locals(node)}
        try:
            self.visit(node.body)
        finally:
            self.bindings = previous

    def visit_ClassDef(self, node):
        previous = self.bindings
        qualified = f"{self.module}.{node.name}" if self.module else None
        if qualified in self.models:
            self.bindings[node.name] = qualified
        else:
            self._rebind(node.name, node)
        nested = dict(self.bindings)
        self.bindings = nested
        try:
            for statement in node.body:
                self.visit(statement)
        finally:
            self.bindings = previous

    def _rebind(self, name, node):
        bound = self.bindings.get(name, "")
        if bound.startswith(("sqlalchemy.", "sqlmodel.", "builtins.")) or bound in self.models:
            self.add("rebound_query_binding", node,
                     "A query/model binding is reassigned or shadowed in this source.",
                     "Confirm the actual callable or model in staging; static binding resolution is incomplete.",
                     "UNRESOLVED")
        self.bindings.pop(name, None)

    def _comprehension(self, node):
        previous = self.bindings
        self.bindings = dict(previous)
        try:
            for generator in node.generators:
                self.visit(generator.iter)
                for target in ast.walk(generator.target):
                    if isinstance(target, ast.Name):
                        self._rebind(target.id, target)
                for condition in generator.ifs:
                    self.visit(condition)
            if isinstance(node, ast.DictComp):
                self.visit(node.key)
                self.visit(node.value)
            else:
                self.visit(node.elt)
        finally:
            self.bindings = previous
        for expression in ast.walk(node):
            if isinstance(expression, ast.NamedExpr) and isinstance(expression.target, ast.Name):
                self._rebind(expression.target.id, expression)

    visit_ListComp = _comprehension
    visit_SetComp = _comprehension
    visit_DictComp = _comprehension
    visit_GeneratorExp = _comprehension

    def visit_Assign(self, node):
        self.visit(node.value)
        for target in node.targets:
            for name in ast.walk(target):
                if isinstance(name, ast.Name):
                    self._rebind(name.id, node)

    def visit_AnnAssign(self, node):
        if node.value is not None:
            self.visit(node.value)
        if isinstance(node.target, ast.Name):
            self._rebind(node.target.id, node)

    def visit_NamedExpr(self, node):
        self.visit(node.value)
        self._rebind(node.target.id, node)

    def _statement_target(self, target):
        """Visit target evaluation and invalidate only actual local names."""
        if isinstance(target, ast.Name):
            self._rebind(target.id, target)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for item in target.elts:
                self._statement_target(item)
        elif isinstance(target, ast.Starred):
            self._statement_target(target.value)
        else:
            # Attribute/subscript bases and indices are loads, not bindings.
            self.visit(target)

    def visit_For(self, node):
        self.visit(node.iter)
        self._statement_target(node.target)
        for statement in (*node.body, *node.orelse):
            self.visit(statement)

    visit_AsyncFor = visit_For

    def visit_With(self, node):
        for item in node.items:
            self.visit(item.context_expr)
            if item.optional_vars is not None:
                self._statement_target(item.optional_vars)
        for statement in node.body:
            self.visit(statement)

    visit_AsyncWith = visit_With

    def visit_AugAssign(self, node):
        # Augmented assignment evaluates its target once, before the RHS.
        self.visit(node.target)
        self.visit(node.value)
        if isinstance(node.target, ast.Name):
            self._statement_target(node.target)

    def visit_Delete(self, node):
        for target in node.targets:
            self._statement_target(target)

    def visit_ExceptHandler(self, node):
        if node.type is not None:
            self.visit(node.type)
        if node.name is not None:
            self._rebind(node.name, node)
        for statement in node.body:
            self.visit(statement)
        # Python deletes the exception target at handler exit. Do not restore
        # an outer import or retain an import assigned inside this handler.
        if node.name is not None:
            self.bindings.pop(node.name, None)

    def visit_Match(self, node):
        self.visit(node.subject)
        captures = {}
        for case in node.cases:
            for pattern in ast.walk(case.pattern):
                name = _string_binding(pattern)
                if name is not None:
                    captures.setdefault(name, pattern)
        # This is not branch analysis. Any case can bind a captured name, so
        # remove its imported identity before guards/bodies and after the match.
        for name, pattern in captures.items():
            self._rebind(name, pattern)
        for case in node.cases:
            for name in captures:
                self.bindings.pop(name, None)
            self.visit(case.pattern)
            if case.guard is not None:
                self.visit(case.guard)
            for statement in case.body:
                self.visit(statement)
        for name in captures:
            self.bindings.pop(name, None)

    def visit_Compare(self, node):
        values = [node.left, *node.comparators]
        for left, operation, right in zip(values, node.ops, values[1:]):
            field = self.field(left) or self.field(right)
            if field is None:
                continue
            null_check = (isinstance(operation, (ast.Eq, ast.NotEq)) and
                          any(isinstance(v, ast.Constant) and v.value is None for v in (left, right)))
            if null_check:
                continue
            if isinstance(operation, (ast.Eq, ast.NotEq)) and not field["queries"]:
                self.add("storage_only_comparison_refused_if_attached", node,
                         "Non-NULL equality or inequality on this storage-only field is not admitted.",
                         "Use NULL checks, or explicitly declare and qualify searchable equality in the manifest.")
            elif isinstance(operation, (ast.Lt, ast.LtE, ast.Gt, ast.GtE)):
                self.add("encrypted_range_refused_if_attached", node,
                         "Native range comparison is not admitted on this encrypted field.",
                         "Use an approved searchable capability when available; do not present filtered approximations as exact.")
        self.generic_visit(node)

    def visit_Call(self, node):
        qualified = self.qualified(node.func) or ""
        leaf = qualified.rsplit(".", 1)[-1]
        sql_binding = qualified.startswith(("sqlalchemy.", "sqlmodel."))
        if sql_binding and leaf in ("delete", "update", "insert", "Delete", "Update", "Insert"):
            self.add("core_dml_refused_if_attached", node,
                     "The default attached profile refuses non-flush Core DML, including DML on unprotected tables.",
                     "Use ordinary ORM instance writes/deletes. Private bounded DELETE opt-ins require exact target, effect-inventory and staging verification; this scan cannot establish them.")
        if sql_binding and leaf in ("text", "TextClause"):
            self.add("raw_sql_refused_if_attached", node,
                     "Textual SQL is not admitted through the attached application factory.",
                     "Use supported ORM/Core SELECT expressions; review maintenance SQL separately without a plaintext fallback.")
        if qualified in ("builtins.exec", "builtins.eval", "builtins.__import__", "importlib.import_module"):
            self.add("dynamic_code_requires_staging", node,
                     "Dynamic code or imports cannot be covered by this static snapshot.",
                     "Exercise the generated application paths in staging and retain their runtime evidence.", "UNRESOLVED")
        if isinstance(node.func, ast.Attribute):
            method = node.func.attr
            field = self.field(node.func.value)
            if field is not None and method in ("like", "ilike", "startswith", "endswith", "contains", "match", "asc", "desc"):
                self.add("encrypted_operation_refused_if_attached", node,
                         "This encrypted pattern, text-search or ordering operation is not admitted.",
                         "Use declared equality/IN or an explicitly reviewed alternative; never use a plaintext fallback.")
            if field is not None and method in ("in_", "not_in", "notin_") and not field["queries"]:
                self.add("storage_only_comparison_refused_if_attached", node,
                         "Set-membership search is not declared for this storage-only field.",
                         "Explicitly declare and qualify equality search, or retain the field as storage-only.")
            if method in ("get", "get_one"):
                keywords = {item.arg: item.value for item in node.keywords if item.arg}
                entity = node.args[0] if node.args else keywords.get("entity")
                identity = node.args[1] if len(node.args) > 1 else keywords.get("ident")
                model = self.models.get(self.qualified(entity))
                if model is not None and model["record"]["codec"] == "uuid16/v1":
                    invalid_text = False
                    if isinstance(identity, ast.Constant) and type(identity.value) is str:
                        # Share the existing runtime grammar; never issue SQL or echo the literal.
                        from cryptalis.sqlalchemy import _uuid_record_context, UnsupportedUUIDRecordBind
                        try:
                            _uuid_record_context(identity.value)
                        except UnsupportedUUIDRecordBind:
                            invalid_text = True
                    if invalid_text:
                        self.add("uuid_text_record_bind_refused_if_attached", node,
                                 "This literal does not satisfy the admitted PostgreSQL 16 UUID text grammar.",
                                 "Supply a UUID object or an admitted UUID text spelling with ordinary typed record binds; verify routing in staging.")
                    elif identity is not None:
                        self.add("record_bind_requires_staging", node,
                                 "This record-key input type is not proven by the source snapshot.",
                                 "Verify UUID/int record inputs through the attached factory in staging; inspect JWT string paths.",
                                 "UNRESOLVED")
        self.generic_visit(node)


def inspect_plan_compatibility(lock_bytes, mapping, *, sources=None):
    """Inspect supplied source text only. This report is not an admission token."""
    if not isinstance(mapping, Registry):
        raise CompatibilityInspectionUnavailable("invalid_mapping")
    if sources is None:
        sources = {}
    if type(sources) is not dict or len(sources) > MAX_SOURCE_FILES:
        raise CompatibilityInspectionUnavailable("source_inventory_budget_or_type")
    prepared = []
    total = 0
    for path, value in sources.items():
        if (type(path) is not str or not path or len(path) > 512 or "\\" in path or
                path.startswith("/") or any(part in ("", ".", "..") for part in path.split("/")) or
                not path.endswith(".py") or any(ord(char) < 32 for char in path)):
            raise CompatibilityInspectionUnavailable("invalid_source_label")
        original = value
        if type(value) is str:
            try:
                value = value.encode("utf-8", "strict")
            except UnicodeError:
                raise CompatibilityInspectionUnavailable("invalid_source_encoding") from None
        if type(value) is not bytes or len(value) > MAX_SOURCE_BYTES:
            raise CompatibilityInspectionUnavailable("source_byte_budget_or_type")
        total += len(value)
        if total > MAX_TOTAL_BYTES:
            raise CompatibilityInspectionUnavailable("total_source_budget_exceeded")
        prepared.append((path, value, original))
    # Validate the report's input shape, not the cryptographic admission contract.
    try:
        document = decode_manifest_json(lock_bytes)
        if document.get("schema") != "cryptalis.lock/v1" or type(document.get("models")) is not list:
            raise ManifestInvalid("invalid report input")
        for model in document["models"]:
            if (type(model) is not dict or
                    any(type(model.get(key)) is not str or not model[key] for key in ("model", "schema", "table")) or
                    type(model.get("record")) is not dict or
                    model["record"].get("codec") not in ("uuid16/v1", "int64-be/v1") or
                    type(model.get("fields")) is not list):
                raise ManifestInvalid("invalid report input")
            for field in model["fields"]:
                if (type(field) is not dict or type(field.get("name")) is not str or not field["name"] or
                        type(field.get("queries")) is not list or
                        any(type(query) is not str for query in field["queries"])):
                    raise ManifestInvalid("invalid report input")
    except ManifestInvalid:
        raise CompatibilityInspectionUnavailable("invalid_compiled_lock") from None
    models = {}
    findings = []
    summaries = []
    by_name = {}
    for mapper in mapping.mappers:
        by_name.setdefault(mapper.class_.__name__, []).append(mapper)
    for model in document["models"]:
        matches = by_name.get(model["model"], [])
        summaries.append(dict(model=model["model"], schema=model["schema"], table=model["table"],
                              record_codec=model["record"]["codec"],
                              fields=[dict(name=f["name"], queries=list(f["queries"])) for f in model["fields"]]))
        if len(matches) != 1:
            findings.append(_finding("mapping_not_identified", None, None,
                                     "A declared model is missing or ambiguous in the supplied registry.",
                                     "Use the exact registry supplied to planning and attachment.", "UNRESOLVED"))
            continue
        table = matches[0].local_table
        if (table.name != model["table"] or
                (table.schema is not None and table.schema != model["schema"])):
            findings.append(_finding("mapping_identity_mismatch", None, None,
                                     "The supplied model does not match the declared table/schema identity.",
                                     "Use the exact registry supplied to planning and attachment.", "UNRESOLVED"))
            continue
        cls = matches[0].class_
        models[f"{cls.__module__}.{cls.__name__}"] = {"record": model["record"],
            "fields": {field["name"]: field for field in model["fields"]}}
    snapshots = []
    for path, raw, original in sorted(prepared):
        snapshots.append(dict(path=path, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                              input_kind="bytes" if type(original) is bytes else "utf8_encoded_text"))
        try:
            tree = ast.parse(original, filename="<compatibility-source>")
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            findings.append(_finding("query_source_unparseable", path, None,
                                     "This source cannot be parsed by the current Python grammar/encoding.",
                                     "Use the application's Python version and cover this source in staging.", "UNRESOLVED"))
            continue
        if sum(1 for _ in ast.walk(tree)) > MAX_AST_NODES:
            raise CompatibilityInspectionUnavailable("ast_budget_exceeded")
        visitor = _Scan(path, models)
        try:
            visitor.visit(tree)
        except RecursionError:
            raise CompatibilityInspectionUnavailable("analysis_depth_exceeded") from None
        findings.extend(visitor.findings)
        if len(findings) > MAX_FINDINGS:
            raise CompatibilityInspectionUnavailable("finding_budget_exceeded")
    if not prepared:
        findings.append(_finding("query_sources_not_inspected", None, None,
                                 "No application query source snapshots were supplied.",
                                 "Supply a source inventory and run the unchanged application suite in staging.", "UNRESOLVED"))
    if len(findings) > MAX_FINDINGS:
        raise CompatibilityInspectionUnavailable("finding_budget_exceeded")
    return dict(format="cryptalis.compatibility-report/v1", effects="NONE",
                authority="ADVISORY_NOT_AUTHENTICATED", lock_digest=hashlib.sha256(lock_bytes).hexdigest(),
                coverage="PARTIAL" if prepared else "NOT_INSPECTED", staging_required=True,
                models=summaries, sources=snapshots,
                findings=sorted(findings, key=lambda f: (f["path"] or "", f["line"] or 0, f["code"])),
                limits=["Only supplied source snapshots are inspected; no files are discovered or imported.",
                        "Findings are conditional on execution through the attached factory, not proof of runtime routing.",
                        "Dynamic queries, aliases, custom callables and actual parameter types require staging.",
                        "This advisory report is not authenticated by the plan and does not authorize deployment."])
