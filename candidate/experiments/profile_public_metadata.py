"""Pure CF1 public-metadata experiment; no database, network or real-data use.

Run with the pinned lab interpreter and PYTHONPATH=src. The old bodies below are
the unchanged S14 derivation/term baseline, including the S10 tuple encoder.
Only these two functions vary in process; all key and frame checks stay active.
"""
import argparse
import hashlib
import json
import os
import platform
import statistics
import time
from pathlib import Path
from uuid import UUID

import cryptography
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from cryptalis.crypto import cf1
from cryptalis.crypto.keys import (
    CryptoBackendUnavailable, DevelopmentKeyProvider, KeyContext, KeyPolicy,
    Keyring, tuple_bytes,
)


def baseline_derive(material, info):
    c = material.context
    salt = hashlib.sha256(tuple_bytes(b"CF1/root", c.domain_id.bytes, c.tenant_id.bytes,
                                     c.root_id.bytes, c.generation.to_bytes(4, "big"))).digest()
    try:
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=info).derive(material.root)
    except Exception:
        raise CryptoBackendUnavailable() from None


def baseline_term(encoded, field, material):
    key = cf1._derive(material, tuple_bytes(b"CF1/search-key", field.field_id.bytes,
                                          b"utf8-exact/v1", b"identity/v1", b"equality"))
    try:
        mac = hmac.HMAC(key, hashes.SHA256())
        mac.update(tuple_bytes(b"equality", encoded))
        return mac.finalize()
    except Exception:
        raise CryptoBackendUnavailable() from None


def prototype_derive(material, info):
    c = material.context
    salt = c.__dict__.get("_cf1_root_salt")
    if salt is None:
        salt = hashlib.sha256(tuple_bytes(b"CF1/root", c.domain_id.bytes, c.tenant_id.bytes,
                                         c.root_id.bytes, c.generation.to_bytes(4, "big"))).digest()
        object.__setattr__(c, "_cf1_root_salt", salt)
    try:
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=info).derive(material.root)
    except Exception:
        raise CryptoBackendUnavailable() from None


def prototype_term(encoded, field, material):
    info = field.__dict__.get("_cf1_search_info")
    if info is None:
        info = tuple_bytes(b"CF1/search-key", field.field_id.bytes,
                           b"utf8-exact/v1", b"identity/v1", b"equality")
        object.__setattr__(field, "_cf1_search_info", info)
    key = cf1._derive(material, info)
    try:
        mac = hmac.HMAC(key, hashes.SHA256())
        mac.update(tuple_bytes(b"equality", encoded))
        return mac.finalize()
    except Exception:
        raise CryptoBackendUnavailable() from None


def fixture(vector):
    field = cf1.FieldDescriptor.from_compiled(vector["descriptor"], vector["descriptor_digest"])
    tenant = UUID(vector["tenant_id"])
    record = UUID(vector["record_id"]) if field.record_codec == "uuid16/v1" else vector["record_id"]
    provider = DevelopmentKeyProvider()
    wrappers = tuple(provider.wrap(bytes.fromhex(vector[purpose + "_root"]),
                     KeyContext(field.domain_id, tenant, purpose, UUID(vector[purpose + "_root_id"]),
                                vector[purpose + "_generation"]))
                     for purpose in (("payload", "search") if field.equality else ("payload",)))
    keys = Keyring(KeyPolicy(field.domain_id, tenant, wrappers, vector["payload_generation"],
                            vector["search_generation"] or None),
                   {provider.provider_id: provider}, max_age=300).prepare()
    return field, tenant, record, keys


def run(output, *, implemented=False, iterations=4000):
    vectors = json.loads((Path(__file__).resolve().parents[1] / "tests/fixtures/cf1_vectors.json").read_text())["vectors"]
    saved = cf1._derive, cf1._term
    candidate = saved if implemented else (prototype_derive, prototype_term)
    variants = [("baseline", (baseline_derive, baseline_term)), ("public_metadata", candidate)]
    records = []
    try:
        cases = []
        for vector in vectors[:2]:
            field, tenant, record, keys = fixture(vector)
            frame = bytes.fromhex(vector["frame"])
            label = "equality" if field.equality else "storage"
            cases.append(("open_" + label, lambda f=field,t=tenant,r=record,k=keys,b=frame:
                          cf1.open_text(b,f,t,r,k), vector["text"]))
            if field.equality:
                cases.append(("query_term", lambda f=field,t=tenant,k=keys,v=vector["text"]:
                              cf1.equality_term(v,f,t,k), frame[14:46]))
        for block in range(9):
            for variant, functions in (variants if block % 2 == 0 else list(reversed(variants))):
                cf1._derive, cf1._term = functions
                for name, operation, expected in cases:
                    for _ in range(100):
                        assert operation() == expected
                    wall = time.perf_counter_ns()
                    raw = time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)
                    cpu = time.process_time_ns()
                    for _ in range(iterations):
                        actual = operation()
                        assert actual == expected
                    elapsed_cpu = time.process_time_ns() - cpu
                    elapsed_raw = time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW) - raw
                    elapsed_wall = time.perf_counter_ns() - wall
                    records.append(dict(block=block, variant=variant, family=name,
                                        iterations=iterations, ns_each=elapsed_wall / iterations,
                                        raw_ns_each=elapsed_raw / iterations,
                                        cpu_ns_each=elapsed_cpu / iterations))
    finally:
        cf1._derive, cf1._term = saved
    aggregate = []
    for name, _, _ in cases:
        medians = {variant:[r["ns_each"] for r in records if r["variant"] == variant and r["family"] == name]
                   for variant, _ in variants}
        before, after = (statistics.median(medians[v]) for v, _ in variants)
        favorable = sum(a > b for a,b in zip(medians["baseline"], medians["public_metadata"]))
        aggregate.append(dict(family=name, baseline_ns=before, candidate_ns=after,
                              reduction_percent=100*(before-after)/before, favorable_pairs=favorable))
    gate = all(r["reduction_percent"] >= 10 and r["favorable_pairs"] >= 7
               for r in aggregate if r["family"] in ("open_equality", "query_term"))
    gate = gate and all(r["reduction_percent"] >= -5 for r in aggregate)
    report = dict(scope="Pure warm CF1 metadata-only prototype, synthetic frozen vectors, same process alternating pairs. No SQL/native result, production or independent security qualification.",
                  gate_passed=gate, implemented=implemented, python=platform.python_version(),
                  cryptography=cryptography.__version__, pid=os.getpid(),
                  source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(cf1.__file__), Path(__file__))},
                  aggregate=aggregate, records=records)
    Path(output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"gate_passed":gate, "aggregate":aggregate}, indent=2))
    return gate


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--implemented", action="store_true")
    args = parser.parse_args()
    raise SystemExit(0 if run(args.output, implemented=args.implemented) else 1)
