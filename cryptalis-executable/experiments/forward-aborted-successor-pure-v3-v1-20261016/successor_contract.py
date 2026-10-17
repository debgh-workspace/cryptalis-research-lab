"""Unconnected v3 lineage-component prototype; source only, no authority.

Inputs are caller-owned, already decoded synthetic values. No JSON byte decoder,
compiler admission, native observation, mutation, planner or public dispatch is
implemented. See README.md before treating any check as evidence.
"""
import hashlib
import json
import math
from itertools import chain
from uuid import UUID


LEGACY_FORWARD = "cryptalis.transition/retained-native-research-v0"
COMMENTS_FORWARD = "cryptalis.transition/retained-native-comments-research-v1"
CLUSTER_FORWARD = "cryptalis.transition/retained-native-comments-cluster-research-v2"
FORWARD_V3 = "cryptalis.transition/retained-native-comments-cluster-aborted-successor-research-v3"
REVERSE_V3 = "cryptalis.reverse/retained-native-comments-cluster-aborted-successor-research-v3"
ROOT_FORMATS = (LEGACY_FORWARD, COMMENTS_FORWARD, CLUSTER_FORWARD)
LINEAGE_SCHEMA = "cryptalis.aborted-forward-lineage/research-v1"
MAX_BYTES = 16 * 1024 * 1024
MAX_COUNT = 2**53 - 1  # Artifact lineage count only, never journal progress N.
SCOPE_LOCK_KEYS = ("schema", "profile", "domain_id", "database", "declaration", "models", "required_readers")
LOCK_KEYS = frozenset(SCOPE_LOCK_KEYS + ("writer_inventory", "search_reviews", "ddl"))
RATE_PATHS = {("estimates", "backfill_rows_per_second"), ("estimates", "verify_rows_per_second")}


class ContractRefusal(ValueError):
    """Fixed diagnostic code only; retain no supplied artifact/state text."""
    effects = "NONE"

    def __init__(self, code):
        self.code = code
        super().__init__(code)


def _need(condition, code):
    if not condition:
        raise ContractRefusal(code)


def _members(value, names, code):
    _need(type(value) is dict and set(value) == set(names), code)


def _uuid(value):
    _need(type(value) is str, "invalid_uuid")
    try:
        parsed = UUID(value)
    except ValueError:
        raise ContractRefusal("invalid_uuid") from None
    _need(bool(parsed.int) and str(parsed) == value, "invalid_uuid")
    return value


def _digest(value):
    _need(type(value) is str and len(value) == 64
          and all(c in "0123456789abcdef" for c in value), "invalid_digest")
    return value


def canonical_bytes(value, *, artifact_rates=False):
    """C for decoded values only; no byte parsing or native transfer admission.

    Integers have no 2**53 journal-progress cutoff. A host encoder refusal is
    retained as a typed refusal; arbitrary huge-integer support is unqualified.
    """
    def inspect(item, path=(), depth=0):
        kind = type(item)
        if kind in (dict, list):
            _need(depth < 32, "canonical_depth_exceeded")
            if kind is dict:
                for key, member in item.items():
                    _need(type(key) is str, "invalid_json_key")
                    key.encode("utf-8")
                    inspect(member, path + (key,), depth + 1)
            else:
                for index, member in enumerate(item):
                    inspect(member, path + (index,), depth + 1)
        elif kind is str:
            item.encode("utf-8")
        elif kind is float:
            _need(artifact_rates and path in RATE_PATHS and math.isfinite(item)
                  and item > 0, "invalid_json_number")
        else:
            _need(item is None or kind in (bool, int), "invalid_json_value")

    try:
        inspect(value)
        raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (UnicodeError, ValueError, TypeError, RecursionError) as error:
        if isinstance(error, ContractRefusal):
            raise
        raise ContractRefusal("canonical_encoding_refused") from None
    _need(len(raw) <= MAX_BYTES, "successor_canonical_size_exceeded")
    return raw


def _hash(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _reference(value):
    _members(value, ("operation_id", "plan_digest"), "invalid_reference")
    return {"operation_id": _uuid(value["operation_id"]),
            "plan_digest": _digest(value["plan_digest"])}


def validate_summary(value):
    """Validate/detach only the closed fixed-size forward lineage component."""
    _members(value, ("schema", "root", "predecessor", "count", "digest"), "invalid_lineage")
    _need(type(value["schema"]) is str and value["schema"] == LINEAGE_SCHEMA, "invalid_lineage_schema")
    root = value["root"]
    _members(root, ("format", "operation_id", "plan_digest"), "invalid_root")
    _need(type(root["format"]) is str and root["format"] in ROOT_FORMATS, "unsupported_root_format")
    root = {"format": root["format"], "operation_id": _uuid(root["operation_id"]),
            "plan_digest": _digest(root["plan_digest"])}
    predecessor = _reference(value["predecessor"])
    count = value["count"]
    _need(type(count) is int and 1 <= count <= MAX_COUNT, "invalid_lineage_count")
    root_ref = {key: root[key] for key in ("operation_id", "plan_digest")}
    if count == 1:
        _need(predecessor == root_ref, "root_reference_mismatch")
    else:
        _need(predecessor["operation_id"] != root["operation_id"], "root_reused_as_head")
    return {"schema": LINEAGE_SCHEMA, "root": root, "predecessor": predecessor,
            "count": count, "digest": _digest(value["digest"])}


def scope_bytes(document):
    """Exact selected D1 projection; full compiler semantics remain external."""
    _need(type(document) is dict, "invalid_scope_document")
    for key in ("target_id", "target", "journal_schema", "runtime_role", "lock"):
        _need(key in document, "missing_scope_member")
    _uuid(document["target_id"])
    for key in ("journal_schema", "runtime_role"):
        _need(type(document[key]) is str and bool(document[key]), "invalid_scope_member")
    _need(type(document["target"]) is list and len(document["target"]) == 5, "invalid_target_tuple")
    lock = document["lock"]
    _members(lock, LOCK_KEYS, "invalid_lock_members")
    _need(type(lock["schema"]) is str and lock["schema"] == "cryptalis.lock/v1"
          and type(lock["profile"]) is str and lock["profile"] == "cf1", "invalid_lock_profile")
    _uuid(lock["domain_id"])
    _need(type(lock["models"]) is list and bool(lock["models"]), "invalid_models")
    projection = {key: lock[key] for key in SCOPE_LOCK_KEYS}
    return canonical_bytes(["cryptalis.aborted-forward/scope-v1", document["target_id"],
                            document["target"], document["journal_schema"],
                            document["runtime_role"], projection])


def require_same_scope(previous, current):
    previous_bytes, current_bytes = scope_bytes(previous), scope_bytes(current)
    _need(previous_bytes == current_bytes, "successor_scope_changed")
    for document in (previous, current):
        _need("key_policies" in document and type(document["key_policies"]) is dict,
              "invalid_key_policies")
        for tenant, fingerprint in document["key_policies"].items():
            _uuid(tenant)
            _digest(fingerprint)
    _need(canonical_bytes(previous["key_policies"]) == canonical_bytes(current["key_policies"]),
          "successor_tenant_policy_changed")
    return hashlib.sha256(previous_bytes).hexdigest()


def bind_predecessor(*, aborted_predecessor, predecessor_pin, decoded_predecessor=None):
    """Bind supplied bytes to a decoded view and PREPARED pin, not authenticate.

    Pin is this prototype's plain JSON view of the existing host pin. Its source
    and currency require separate host authentication. No public API is changed.
    """
    if aborted_predecessor is None and predecessor_pin is None:
        _need(decoded_predecessor is None, "unpaired_predecessor_view")
        return None
    _need(aborted_predecessor is not None and predecessor_pin is not None, "unpaired_predecessor_inputs")
    _need(type(aborted_predecessor) is bytes and type(decoded_predecessor) is dict,
          "invalid_predecessor_input")
    _need(len(aborted_predecessor) <= MAX_BYTES, "predecessor_artifact_size_exceeded")
    document = decoded_predecessor
    _need(document.get("format") in ROOT_FORMATS + (FORWARD_V3,)
          and document.get("kind") == "protect", "unsupported_predecessor_format")
    _need(canonical_bytes(document, artifact_rates=True) == aborted_predecessor,
          "predecessor_bytes_mismatch")
    _uuid(document.get("operation_id"))
    _uuid(document.get("target_id"))
    _members(predecessor_pin, ("target_id", "operation_id", "plan_digest", "phase"), "invalid_predecessor_pin")
    _uuid(predecessor_pin["target_id"])
    _uuid(predecessor_pin["operation_id"])
    _digest(predecessor_pin["plan_digest"])
    digest = hashlib.sha256(aborted_predecessor).hexdigest()
    _need(type(predecessor_pin["phase"]) is str and predecessor_pin["phase"] == "PREPARED"
          and predecessor_pin["target_id"] == document["target_id"]
          and predecessor_pin["operation_id"] == document["operation_id"]
          and predecessor_pin["plan_digest"] == digest, "predecessor_pin_mismatch")
    if document["format"] == FORWARD_V3:
        _need("aborted_forward" in document, "missing_predecessor_lineage")
        validate_summary(document["aborted_forward"])
    else:
        _need("aborted_forward" not in document, "historical_lineage_field_forbidden")
    return {"operation_id": document["operation_id"], "plan_digest": digest}


def _terminal_row(row, reference, *, has_prefix):
    """Minimal forward shape plus full-state hash; not a journal-state decoder."""
    _members(row, ("operation_id", "plan_digest", "state"), "invalid_row_members")
    actual = _reference({key: row[key] for key in ("operation_id", "plan_digest")})
    _need(actual == reference, "journal_reference_mismatch")
    state = row["state"]
    _need(type(state) is dict, "invalid_terminal_state")
    required = {"phase", "models"} | ({"aborted_forward"} if has_prefix else set())
    _need(set(state) in (required, required | {"verification"}), "invalid_forward_state_members")
    _need(state["phase"] == "ABORTED" and type(state["models"]) is dict
          and bool(state["models"]), "not_forward_terminal")
    # Complete nested model/schema/guard grammar and exact-N progress admission
    # are intentionally not implemented here. C binds every supplied member.
    return _hash(state)


def _seed(scope_digest, root):
    return _hash(["cryptalis.aborted-forward/seed-v1", _digest(scope_digest), root])


def _fold(scope_digest, count, prior_digest, reference, terminal_digest):
    return _hash(["cryptalis.aborted-forward/row-v1", scope_digest, count, prior_digest,
                  reference["operation_id"], reference["plan_digest"], terminal_digest])


def verify_lineage(summary, scope_digest, rows_newest_first, *, new_operation_id):
    """Check the commitment chain over a fixed, unique-key snapshot premise.

    Consumes one supplied row at a time, never allocates a history-wide set/list.
    A stable unique-key source is a prerequisite, not proved by this function.
    Does not establish physical membership, row provenance or execution authority.
    """
    expected = validate_summary(summary)
    _digest(scope_digest)
    _uuid(new_operation_id)
    root = expected["root"]
    row_iterator = iter(rows_newest_first)
    remaining = expected["count"]
    wanted_digest, reference = expected["digest"], expected["predecessor"]
    missing = object()
    while remaining:
        row = next(row_iterator, missing)
        _need(row is not missing, "missing_ancestor")
        _need(reference["operation_id"] != new_operation_id, "successor_identity_reused")
        terminal_digest = _terminal_row(row, reference, has_prefix=remaining > 1)
        if remaining == 1:
            _need(reference == {key: root[key] for key in ("operation_id", "plan_digest")},
                  "root_reference_mismatch")
            prior_digest = _seed(scope_digest, root)
            next_reference = None
        else:
            prefix = validate_summary(row["state"]["aborted_forward"])
            _need(prefix["count"] == remaining - 1 and canonical_bytes(prefix["root"]) == canonical_bytes(root),
                  "lineage_prefix_mismatch")
            prior_digest, next_reference = prefix["digest"], prefix["predecessor"]
        _need(_fold(scope_digest, remaining, prior_digest, reference, terminal_digest) == wanted_digest,
              "lineage_commitment_mismatch")
        remaining -= 1
        wanted_digest, reference = prior_digest, next_reference
    _need(next(row_iterator, missing) is missing, "extra_ancestor")
    return expected  # Detached component, never an admission/authority token.


def construct_lineage(*, aborted_predecessor, predecessor_pin, decoded_predecessor,
                      current_proposal, rows_newest_first, journal_row_count):
    """Construct only aborted_forward for a fresh proposal; no artifact writes.

    Rows/count are synthetic caller inputs, not self-authenticating DB evidence.
    A future adapter must prove their common snapshot, PK and complete rowset.
    """
    predecessor = bind_predecessor(aborted_predecessor=aborted_predecessor,
                                  predecessor_pin=predecessor_pin,
                                  decoded_predecessor=decoded_predecessor)
    _need(predecessor is not None, "explicit_predecessor_required")
    _need(type(current_proposal) is dict, "invalid_current_proposal")
    new_id = _uuid(current_proposal.get("operation_id"))
    _need(new_id != predecessor["operation_id"], "successor_identity_reused")
    scope_digest = require_same_scope(decoded_predecessor, current_proposal)
    iterator = iter(rows_newest_first)
    missing = object()
    head = next(iterator, missing)
    _need(head is not missing, "missing_predecessor_row")
    later = decoded_predecessor["format"] == FORWARD_V3
    terminal_digest = _terminal_row(head, predecessor, has_prefix=later)
    if later:
        prefix = validate_summary(decoded_predecessor["aborted_forward"])
        _need(canonical_bytes(head["state"]["aborted_forward"]) == canonical_bytes(prefix),
              "predecessor_artifact_prefix_mismatch")
        _need(prefix["count"] < MAX_COUNT, "lineage_count_exhausted")
        root, count, prior_digest = prefix["root"], prefix["count"] + 1, prefix["digest"]
    else:
        root = {"format": decoded_predecessor["format"], **predecessor}
        count, prior_digest = 1, _seed(scope_digest, root)
    _need(type(journal_row_count) is int and journal_row_count == count,
          "journal_count_mismatch")
    summary = {"schema": LINEAGE_SCHEMA, "root": root, "predecessor": predecessor,
               "count": count, "digest": _fold(scope_digest, count, prior_digest, predecessor, terminal_digest)}
    return verify_lineage(summary, scope_digest, chain((head,), iterator), new_operation_id=new_id)
