"""Offline deciding checks; public synthetic roots only, no database/provider.

Uses the existing reference generator unchanged. It reproduces frozen CF1 and
published RFC primitive vectors before extending bigint decoding evidence.
"""
import argparse
from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
from uuid import UUID

import cryptography

import independent_cf1_decode as oracle


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "tests" / "reference_cf1_vectors.py"
FIXTURE = ROOT / "tests" / "fixtures" / "cf1_vectors.json"


def reference_module():
    spec = importlib.util.spec_from_file_location("_unchanged_public_cf1_reference", REFERENCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parameters(vector):
    descriptor = dict(vector["descriptor"])
    return {
        "descriptor": descriptor,
        "descriptor_digest": vector["descriptor_digest"],
        "tenant": UUID(vector["tenant_id"]),
        "record": vector["record_id"] if descriptor["record_codec"] == "int64-be/v1" else UUID(vector["record_id"]),
        "payload": oracle.PublicFixtureRoot(UUID(vector["payload_root_id"]), vector["payload_generation"], bytes.fromhex(vector["payload_root"])),
        "search": oracle.PublicFixtureRoot(UUID(vector["search_root_id"]), vector["search_generation"], bytes.fromhex(vector["search_root"])) if vector["search_generation"] else None,
    }


def changed_descriptor(params, key, value):
    descriptor = dict(params["descriptor"], **{key: value})
    encoded = json.dumps(descriptor, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("utf8")
    return dict(params, descriptor=descriptor, descriptor_digest=hashlib.sha256(encoded).hexdigest())


def run_checks():
    started = time.monotonic()
    before = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in (REFERENCE, FIXTURE, Path(oracle.__file__), Path(__file__))}
    reference = reference_module()
    frozen = json.loads(FIXTURE.read_text())
    results = []

    def equal(name, actual, expected):
        if actual != expected:
            raise AssertionError(name + ": independent value mismatch")
        results.append({"case": name, "result": "PASS"})

    def refused(name, body, params, expected_code=None):
        try:
            oracle.decode_cf1(body, **params)
        except oracle.OracleRefused as exc:
            if expected_code is not None and str(exc) != expected_code:
                raise AssertionError(name + ": unexpected refusal boundary") from exc
        else:
            raise AssertionError(name + ": invalid frame/context was released")
        results.append({"case": name, "result": "PASS"})

    # This runs the unchanged RFC8452/OpenSSL reference and stdlib HKDF/HMAC
    # checks; exact equality includes every intermediate frozen CF1 byte.
    equal("published_primitives_and_frozen_fixture_reproduction", reference.generate(), frozen)

    for vector in frozen["vectors"]:
        name, params = vector["name"], parameters(vector)
        body = bytes.fromhex(vector["frame"])
        equal(name + ":decode", oracle.decode_cf1(body, **params), vector["text"])
        equal(name + ":identity_bytes", oracle.record_bytes(params["descriptor"]["record_codec"], params["record"]).hex(), vector["typed_record_id"])
        equal(name + ":sql_null", oracle.decode_cf1(None, **params), None)
        other_record = UUID(int=123) if type(params["record"]) is UUID else params["record"] + 1
        refused(name + ":wrong_record", body, dict(params, record=other_record), "authentication")
        refused(name + ":wrong_tenant", body, dict(params, tenant=UUID(int=123)),
                "tenant_context" if params["descriptor"]["tenant_codec"] == "single-tenant-uuid/v1" else "authentication")
        for field in ("field_id", "domain_id", "table_id"):
            changed = changed_descriptor(params, field, str(UUID(int=123)))
            refused(name + ":wrong_" + field, body, changed,
                    "tenant_context" if field == "table_id" and params["descriptor"]["tenant_codec"] == "single-tenant-uuid/v1" else "authentication")
        refused(name + ":wrong_descriptor_digest", body, dict(params, descriptor_digest="0" * 64), "descriptor_digest")
        for field, value in (("root_id", UUID(int=123)), ("root", b"x" * 32)):
            refused(name + ":wrong_payload_" + field, body,
                    dict(params, payload=replace(params["payload"], **{field: value})), "authentication")
        refused(name + ":payload_generation_pin", body,
                dict(params, payload=replace(params["payload"], generation=params["payload"].generation + 1)), "generation_pin")
        if params["search"] is not None:
            for field, value in (("root_id", UUID(int=123)), ("root", b"x" * 32)):
                refused(name + ":wrong_search_" + field, body,
                        dict(params, search=replace(params["search"], **{field: value})), "equality_term")
            refused(name + ":search_generation_pin", body,
                    dict(params, search=replace(params["search"], generation=params["search"].generation + 1)), "generation_pin")
        refused(name + ":tag_tamper", body[:-1] + bytes([body[-1] ^ 1]), params, "authentication")
        refused(name + ":unknown_flag", body[:5] + b"\x04" + body[6:], params, "frame_profile")
        refused(name + ":truncated", body[:20], params, "frame_size")
        refused(name + ":trailing", body + b"\x00", params, "authentication")

    # Existing frozen inputs already include INT64_MIN and -42. Extend only the
    # nearby lower bound, -1, zero, +1 and upper bound across both existing forms.
    extension_values = (-(1 << 63) + 1, -1, 0, 1, (1 << 63) - 1)
    generated = []
    index = 0
    for single_tenant in (False, True):
        for equality in (False, True):
            for record in extension_values:
                index += 1
                name = f"int64-{record}-equality-{equality}-single-{single_tenant}"
                vector = reference.make_vector(name, equality, record, "雪😀 e\u0301 é trailing ",
                                               index.to_bytes(12, "big"), single_tenant=single_tenant)
                generated.append(vector)
                params = parameters(vector)
                equal(name + ":decode", oracle.decode_cf1(bytes.fromhex(vector["frame"]), **params), vector["text"])
                equal(name + ":identity_bytes", oracle.record_bytes("int64-be/v1", record).hex(), vector["typed_record_id"])

    vector = next(v for v in frozen["vectors"] if v["name"] == "int64-equality-unicode")
    params, body = parameters(vector), bytes.fromhex(vector["frame"])
    for index, invalid in enumerate((-(1 << 63) - 1, 1 << 63, True, False, "-42", -42.0, None, UUID(int=42))):
        refused(f"int64_invalid_record_{index}", body, dict(params, record=invalid), "record_context")
    uuid_vector = next(v for v in frozen["vectors"] if v["name"] == "uuid-storage-unicode")
    uuid_params, uuid_body = parameters(uuid_vector), bytes.fromhex(uuid_vector["frame"])
    for index, invalid in enumerate((uuid_vector["record_id"], 0, b"\x00" * 16)):
        refused(f"uuid_invalid_record_{index}", uuid_body, dict(uuid_params, record=invalid), "record_context")

    # Distinct typed identity universes must remain distinct, including zero.
    equal("typed_zero_not_uuid_zero", oracle.record_bytes("int64-be/v1", 0) != oracle.record_bytes("uuid16/v1", UUID(int=0)), True)

    # The deciding negative control actually detects an omitted record binding.
    # This change exists only in memory and is restored before returning.
    saved_record_bytes = oracle.record_bytes
    expected = saved_record_bytes("int64-be/v1", params["record"])
    try:
        oracle.record_bytes = lambda codec, requested: expected
        try:
            refused("omitted_expected_record_binding", body, dict(params, record=params["record"] + 1), "authentication")
        except AssertionError as exc:
            if "invalid frame/context was released" not in str(exc):
                raise
            results.append({"case": "omitted_expected_record_binding_mutant", "result": "EXPECTED_FAIL_DETECTED"})
        else:
            raise AssertionError("Record-binding omission was not detected")
    finally:
        oracle.record_bytes = saved_record_bytes
    refused("record_binding_restored", body, dict(params, record=params["record"] + 1), "authentication")

    after = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in before}
    equal("source_and_frozen_fixtures_unchanged", after, before)
    equal("no_product_or_database_modules_imported",
          any(name == "cryptalis" or name.startswith("cryptalis.") or name == "psycopg" for name in sys.modules), False)
    return {
        "scope": "Finite independent CF1 decode oracle; PUBLIC fixture roots; no database, provider profile, product integration or online qualification",
        "python": platform.python_version(), "cryptography": cryptography.__version__,
        "openssl": subprocess.run(["openssl", "version"], capture_output=True, text=True, check=True).stdout.strip(),
        "source_sha256": before,
        "frozen_cf1_vectors": len(frozen["vectors"]), "new_bigint_vectors": len(generated),
        "extended_vectors_sha256": hashlib.sha256(json.dumps(generated, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "checks_passed": sum(row["result"] == "PASS" for row in results),
        "expected_mutant_failures_detected": sum(row["result"] == "EXPECTED_FAIL_DETECTED" for row in results),
        "elapsed_seconds": time.monotonic() - started, "results": results,
        "limits": ["Same AES-GCM-SIV library primitive is shared with the product", "No independent human cryptographic review", "SQL NULL presence, replay freshness and row-set completeness remain outside frame authentication", "No D1 capture/CF1 hook or product phase/capture admission", "No key custody, lease, provider or crash-recovery qualification"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    receipt = run_checks()
    with args.receipt.open("x") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    print(json.dumps({key: receipt[key] for key in ("checks_passed", "expected_mutant_failures_detected", "frozen_cf1_vectors", "new_bigint_vectors", "elapsed_seconds")}))
