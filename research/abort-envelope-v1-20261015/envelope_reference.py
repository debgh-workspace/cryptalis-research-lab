"""SOURCE-ONLY, UNEXECUTED proof scaffolding, not product or accepted algorithm.

No product imports, SQL, I/O, entry point, or test execution. See SPEC.md.
Only exact plain JSON types are admitted. The model is deliberately narrower
than PostgreSQL jsonb. A refusal here is a preparation result, never authority
to disable the existing abort path or reinterpret historical journal bytes.
"""

from copy import deepcopy
from dataclasses import dataclass
from uuid import UUID


DOCUMENT_LIMIT = 16 * 1024 * 1024  # Existing artifact limit, not a larger limit.
EXACT_ARTIFACT_COUNTER_MAX = 2**53 - 1
MAX_DEPTH = 32
PRE_SWITCH_PHASES = frozenset(("EXPANDED", "BACKFILLED", "VERIFIED", "ABORTED"))


class PreparationError(ValueError):
    """Static code only; do not retain input values in diagnostics."""


def require(condition, code):
    if not condition:
        raise PreparationError(code)


def integer_width(value):
    """Decimal width without str(int)'s interpreter-specific digit ceiling."""
    require(type(value) is int, "integer_type")
    sign = int(value < 0)
    value = abs(value)
    width = 1
    while value >= 10:
        value //= 10
        width += 1
    return sign + width


def string_width(value):
    """Exact ensure_ascii=False UTF-8 JSON-string width, including quotes.

    PostgreSQL jsonb cannot store U+0000. Lone surrogates are not UTF-8.
    Refusing them here makes the later native comparison domain explicit.
    """
    require(type(value) is str, "string_type")
    width = 2
    for char in value:
        scalar = ord(char)
        require(scalar != 0, "jsonb_nul_unrepresentable")
        require(not 0xD800 <= scalar <= 0xDFFF, "unicode_surrogate")
        if char in ('"', "\\", "\b", "\f", "\n", "\r", "\t"):
            width += 2
        elif scalar < 0x20:
            width += 6
        else:
            width += len(char.encode("utf-8"))
    return width


@dataclass(frozen=True)
class Sizes:
    canonical_bytes: int
    separators: int

    @property
    def jsonb_text_candidate_bytes(self):
        """Candidate equality, NOT native evidence; see NATIVE_PROTOCOL.md."""
        return self.canonical_bytes + self.separators


def sizes(value):
    """Exact compact canonical count for the admitted plain JSON domain.

    Object ordering cannot change byte length. Cycle detection is path-local:
    repeated acyclic subtrees are counted at each occurrence, never deduped.
    A float, Decimal, UUID instance, tuple, custom subclass, non-ASCII property
    name, cycle, NUL or surrogate is an explicit unsupported preparation case.
    """
    ancestors = set()

    def visit(item, depth):
        kind = type(item)
        if item is None:
            return Sizes(4, 0)
        if kind is bool:
            return Sizes(4 if item else 5, 0)
        if kind is int:
            return Sizes(integer_width(item), 0)
        if kind is str:
            return Sizes(string_width(item), 0)
        require(kind in (dict, list), "unsupported_json_type")
        require(depth <= MAX_DEPTH, "nesting_depth")
        require(id(item) not in ancestors, "cyclic_value")
        ancestors.add(id(item))
        total, separators = 2, max(len(item) - 1, 0)
        if kind is dict:
            total += separators + len(item)  # Commas and colons.
            separators += len(item)
            for key, member in item.items():
                require(type(key) is str and key.isascii(), "object_key_type")
                total += string_width(key)
                child = visit(member, depth + 1)
                total += child.canonical_bytes
                separators += child.separators
        else:
            total += separators
            for member in item:
                child = visit(member, depth + 1)
                total += child.canonical_bytes
                separators += child.separators
        ancestors.remove(id(item))
        return Sizes(total, separators)

    return visit(value, 1)


def object_from_pairs(pairs):
    """JSON decoder hook; do not first collapse duplicate keys into a dict."""
    result = {}
    for key, value in pairs:
        require(type(key) is str and key.isascii(), "object_key_type")
        require(key not in result, "duplicate_object_key")
        result[key] = value
    return result


def canonical_uuid(value, *, nonzero=True):
    require(type(value) is str, "uuid_type")
    try:
        parsed = UUID(value)
    except (ValueError, AttributeError):
        raise PreparationError("uuid_syntax") from None
    require(str(parsed) == value, "uuid_noncanonical")
    require(not nonzero or parsed.int != 0, "uuid_zero")


def digest(value):
    require(type(value) is str and len(value) == 64
            and all(char in "0123456789abcdef" for char in value), "digest_syntax")


def counter(value, *, artifact_profile=False):
    require(type(value) is int and value >= 0, "counter_type_or_range")
    if artifact_profile:
        require(value <= EXACT_ARTIFACT_COUNTER_MAX, "proposed_artifact_counter_cap")


def validate_proposed_forward_summary(value):
    """Reviewer's proposed shape only; NOT an authenticated ancestry proof."""
    require(type(value) is dict and value.keys()
            == {"schema", "root", "predecessor", "count", "digest"}, "summary_shape")
    require(value["schema"] == "cryptalis.aborted-forward-lineage/research-v1", "summary_schema")
    counter(value["count"], artifact_profile=True)
    require(value["count"] > 0, "summary_empty")
    digest(value["digest"])
    root, predecessor = value["root"], value["predecessor"]
    require(type(root) is dict and root.keys() == {"format", "operation_id", "plan_digest"},
            "summary_root_shape")
    require(type(predecessor) is dict and predecessor.keys() == {"operation_id", "plan_digest"},
            "summary_predecessor_shape")
    require(root["format"] in (
        "cryptalis.transition/retained-native-research-v0",
        "cryptalis.transition/retained-native-comments-research-v1",
        "cryptalis.transition/retained-native-comments-cluster-research-v2"), "summary_root_format")
    for ref in (root, predecessor):
        canonical_uuid(ref["operation_id"])
        digest(ref["plan_digest"])
    if value["count"] == 1:
        require(all(root[key] == predecessor[key] for key in predecessor), "summary_single_root")
    else:
        require(root["operation_id"] != predecessor["operation_id"], "summary_root_repeated")
    sizes(value)


def validate_proposed_reverse_summary(value):
    """Proposed reverse ARTIFACT summary, not a current journal-state field."""
    require(type(value) is dict and value.keys() == {"schema", "count", "digest"}, "summary_shape")
    require(value["schema"] == "cryptalis.aborted-reverse-set/research-v1", "summary_schema")
    counter(value["count"], artifact_profile=True)
    digest(value["digest"])
    sizes(value)


def cursor(value, codec):
    require(codec in ("uuid16/v1", "int64-be/v1"), "record_codec")
    if value is None:
        return
    require(type(value) is str, "cursor_type")
    if codec == "uuid16/v1":
        # Record values need not follow the nonzero table/operation-ID rule.
        canonical_uuid(value, nonzero=False)
    else:
        # Match str(native signed int64), without int(str) digit-limit hazards.
        require(1 <= len(value) <= 20, "int64_cursor_width")
        digits = value[1:] if value.startswith("-") else value
        require(bool(digits) and all(char in "0123456789" for char in digits),
                "int64_cursor_syntax")
        number = int(value)
        require(-(2**63) <= number <= 2**63 - 1 and str(number) == value,
                "int64_cursor_range_or_canonical")


def _same_json(left, right):
    """Type-sensitive frozen-subtree comparison; bool is not integer 1."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return (left.keys() == right.keys()
                and all(_same_json(left[key], right[key]) for key in left))
    if type(left) is list:
        return len(left) == len(right) and all(_same_json(a, b) for a, b in zip(left, right))
    return left == right


def validate_state(state, codecs, *, reverse=False, frozen_root=None,
                   artifact_counter_profile=False):
    """Validate the proposed pre-switch envelope shape, not its authority.

    frozen_root is an EXACT, caller-supplied mapping of proposed immutable
    top-level fields, e.g. an eventually approved lineage field. No lineage
    wire format, ancestry authenticity, or relation safety is inferred here.
    """
    frozen_root = {} if frozen_root is None else frozen_root
    require(type(state) is dict and type(codecs) is dict and bool(codecs), "root_type")
    require(type(frozen_root) is dict, "frozen_root_type")
    reserved = {"phase", "models", "verification", "layout_version",
                "source_operation_id", "source_plan_digest"}
    require(not reserved.intersection(frozen_root), "frozen_root_collision")
    if "aborted_forward" in frozen_root:
        require(not reverse, "unexpected_forward_summary")
        validate_proposed_forward_summary(frozen_root["aborted_forward"])
    sizes(state)  # Validate plain JSON, Unicode and nesting before comparisons.
    sizes(frozen_root)
    for key, value in frozen_root.items():
        require(key in state and _same_json(state[key], value), "frozen_root_changed")
    expected = {"phase", "models"} | frozen_root.keys()
    if reverse:
        expected |= {"layout_version", "source_operation_id", "source_plan_digest"}
        require(type(state.get("layout_version")) is int and state["layout_version"] == 101,
                "reverse_layout")
        canonical_uuid(state.get("source_operation_id"))
        digest(state.get("source_plan_digest"))
    elif "verification" in state:
        expected.add("verification")
    require(state.keys() == expected and type(state["phase"]) is str
            and state["phase"] in PRE_SWITCH_PHASES, "root_shape_or_phase")
    models = state["models"]
    require(type(models) is dict and models.keys() == codecs.keys(), "model_set")
    for table_id, progress in models.items():
        canonical_uuid(table_id)
        require(type(progress) is dict and progress.keys()
                == {"scope", "cursor", "rows", "chunks", "schema", "guard"}, "model_shape")
        scope = progress["scope"]
        require(type(scope) is dict and scope.keys() == {"count", "membership"}, "scope_shape")
        counter(scope["count"], artifact_profile=artifact_counter_profile)
        digest(scope["membership"])
        for key in ("rows", "chunks"):
            counter(progress[key], artifact_profile=artifact_counter_profile)
        require(progress["chunks"] <= progress["rows"] <= scope["count"], "progress_order")
        require((progress["rows"] == 0) == (progress["chunks"] == 0), "empty_progress")
        require((progress["rows"] == 0) == (progress["cursor"] is None), "cursor_progress")
        cursor(progress["cursor"], codecs[table_id])
        require(type(progress["schema"]) is dict and type(progress["guard"]) is list
                and bool(progress["guard"]), "frozen_subtree_shape")
    if not reverse and "verification" in state:
        verification = state["verification"]
        require(type(verification) is dict and verification.keys() == models.keys(), "verification_set")
        for value in verification.values():
            digest(value)
    # Full schema/guard semantic validators and phase/verification reachability
    # are separate obligations. Being smaller than this envelope is not validity.


def maximum_state(expanded, codecs, *, reverse=False, frozen_root=None,
                  artifact_counter_profile=False):
    """Fresh maximum-width representative; never a state to write to a journal.

    Exact scope N, schema, guard and frozen_root are retained. The returned
    structure is a deep copy so callers cannot mutate the input through it.
    Every field added at a later boundary needs its own reviewed reservation.
    """
    validate_state(expanded, codecs, reverse=reverse, frozen_root=frozen_root,
                   artifact_counter_profile=artifact_counter_profile)
    require(expanded["phase"] == "EXPANDED" and "verification" not in expanded, "expansion_phase")
    result = {**deepcopy(expanded), "phase": "BACKFILLED", "models": {}}
    for table_id, progress in expanded["models"].items():
        require(progress["rows"] == 0 and progress["chunks"] == 0
                and progress["cursor"] is None, "initial_progress")
        count = progress["scope"]["count"]
        maximum_cursor = None if count == 0 else (
            "ffffffff-ffff-ffff-ffff-ffffffffffff" if codecs[table_id] == "uuid16/v1"
            else "-9223372036854775808")
        result["models"][table_id] = {
            **deepcopy(progress), "cursor": maximum_cursor, "rows": count, "chunks": count}
    if not reverse:
        result["verification"] = {table_id: "f" * 64 for table_id in codecs}
    # The representative deliberately combines longest phase with verification;
    # it need not be an actually reachable state. Do not execute it as progress.
    sizes(result)
    return result


def check_expansion_reservation(expanded, codecs, *, reverse=False, frozen_root=None,
                                artifact_counter_profile=False):
    """Canonical candidate only. Native comparison is a separate admission gate."""
    maximum = maximum_state(expanded, codecs, reverse=reverse, frozen_root=frozen_root,
                            artifact_counter_profile=artifact_counter_profile)
    measured = sizes(maximum)
    require(measured.canonical_bytes <= DOCUMENT_LIMIT, "canonical_envelope_exceeded")
    # This is conservative against the specified native spacing model, pending
    # actual SELECT-only native conformance. It is not a new artifact limit.
    require(measured.jsonb_text_candidate_bytes <= DOCUMENT_LIMIT, "native_candidate_envelope_exceeded")
    return measured


def validate_within_envelope(current, expanded, codecs, *, reverse=False,
                             frozen_root=None, artifact_counter_profile=False):
    """Preparation comparison; NEVER add as a retrofit gate on legacy abort."""
    validate_state(current, codecs, reverse=reverse, frozen_root=frozen_root,
                   artifact_counter_profile=artifact_counter_profile)
    maximum = maximum_state(expanded, codecs, reverse=reverse, frozen_root=frozen_root,
                            artifact_counter_profile=artifact_counter_profile)
    for table_id, initial in expanded["models"].items():
        for key in ("scope", "schema", "guard"):
            require(_same_json(current["models"][table_id][key], initial[key]),
                    "frozen_model_field_changed")
    if reverse:
        for key in ("layout_version", "source_operation_id", "source_plan_digest"):
            require(_same_json(current[key], expanded[key]), "frozen_reverse_field_changed")
    observed, reserved = sizes(current), sizes(maximum)
    require(observed.canonical_bytes <= reserved.canonical_bytes, "canonical_reservation_broken")
    require(observed.jsonb_text_candidate_bytes <= reserved.jsonb_text_candidate_bytes,
            "native_candidate_reservation_broken")
    return observed


def check_next_progress(progress, returned_rows):
    """Proposed v3-only pre-SQL guard; a refusal leaves prior commit untouched.

    This does not authenticate fetched identities or guarantee rowcount,
    transaction pairing, writer exclusion, or monotone cursor correctness.
    """
    require(type(progress) is dict and type(progress.get("scope")) is dict, "progress_type")
    counter(returned_rows)
    require(1 <= returned_rows <= 5000, "chunk_count")
    for value in (progress.get("rows"), progress.get("chunks"), progress["scope"].get("count")):
        counter(value)
    require(progress["chunks"] <= progress["rows"] <= progress["scope"]["count"], "progress_order")
    require(progress["rows"] + returned_rows <= progress["scope"]["count"], "next_rows_exceed_scope")
    require(progress["chunks"] + 1 <= progress["rows"] + returned_rows, "next_chunks_exceed_rows")
    return progress["rows"] + returned_rows, progress["chunks"] + 1
