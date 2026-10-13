"""One retained-layout, same-session before/after question with native control.

Coordinator only: execute through unchanged lab_session/test_postgres preflights.
No statement cache, key lifetime, result processing or query semantics changes.
"""
import contextlib
import json
import os
import platform
import statistics
import sys
import time
from pathlib import Path
from uuid import UUID

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(os.environ["GIT_WORK_TREE"]) / "tests"))
from single_tenant_public_cascade_fixture import single_tenant_public_cascade_application
from test_migration import run, publish, keys, TABLE_ID
from cryptalis.sqlalchemy import attach
from cryptalis.crypto import cf1
from profile_public_metadata import baseline_derive, baseline_term


def test_same_session_public_metadata_with_native_results():
    saved = cf1._derive, cf1._term
    records = []
    families = ["point", "equality", "in2"]
    variants = ["native", "baseline", "public_metadata"]
    with contextlib.ExitStack() as stack:
        native = stack.enter_context(single_tenant_public_cascade_application(rows=1000, unique=False))
        protected = stack.enter_context(single_tenant_public_cascade_application(rows=1000, unique=False))
        run(protected, chunk_size=256)
        publish(protected)
        factory = attach(protected.mapping, protected.runtime, lock=protected.plan.lock_bytes,
                         keys=keys, deployment=(protected.plan, protected.pin))
        plain_session = stack.enter_context(sessionmaker(native.runtime)())
        protected_session = stack.enter_context(factory(tenant_id=TABLE_ID))

        def statement(app, family):
            c = app.Customer
            predicate = {"point":c.id == UUID(int=600), "equality":c.name == "exact",
                         "in2":c.name.in_(["exact", "雪😀"])}[family]
            return select(c.id, c.name).where(predicate).order_by(c.id)

        plain = {family:statement(native, family) for family in families}
        queries = {family:statement(protected, family) for family in families}
        expected = {family:list(plain_session.execute(query)) for family,query in plain.items()}
        try:
            for block in range(7):
                for variant in (variants if block % 2 == 0 else list(reversed(variants))):
                    cf1._derive, cf1._term = ((baseline_derive, baseline_term) if variant == "baseline" else saved)
                    for family in families:
                        samples, raw_samples, cpu_samples = [], [], []
                        for iteration in range(50):
                            session, query = ((plain_session, plain[family]) if variant == "native"
                                              else (protected_session, queries[family]))
                            start = time.perf_counter_ns()
                            raw = time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)
                            cpu = time.process_time_ns()
                            actual = list(session.execute(query))
                            elapsed_cpu = (time.process_time_ns()-cpu) / 1e6
                            elapsed_raw = (time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)-raw) / 1e6
                            elapsed = (time.perf_counter_ns()-start) / 1e6
                            assert actual == expected[family]
                            if iteration >= 10:
                                samples.append(elapsed)
                                raw_samples.append(elapsed_raw)
                                cpu_samples.append(elapsed_cpu)
                        records.append(dict(block=block, variant=variant, family=family,
                                            rows=len(expected[family]), samples_ms=samples,
                                            raw_samples_ms=raw_samples, cpu_samples_ms=cpu_samples,
                                            median_ms=statistics.median(samples)))
        finally:
            cf1._derive, cf1._term = saved
    aggregate = []
    for family in families:
        medians = {variant:[r["median_ms"] for r in records if r["family"] == family and r["variant"] == variant]
                   for variant in variants}
        before, after = statistics.median(medians["baseline"]), statistics.median(medians["public_metadata"])
        aggregate.append(dict(family=family, rows=len(expected[family]),
                              median_ms={v:statistics.median(values) for v,values in medians.items()},
                              reduction_percent=100*(before-after)/before,
                              favorable_pairs=sum(a>b for a,b in zip(medians["baseline"],medians["public_metadata"])) ))
    gate = all(r["reduction_percent"] >= 5 and r["favorable_pairs"] >= 6
               for r in aggregate if r["family"] in ("equality", "in2"))
    gate = gate and next(r["reduction_percent"] for r in aggregate if r["family"] == "point") >= -10
    report = dict(scope="1000 synthetic rows; same protected session/query objects; seven alternating blocks, forty measured queries per cell; only public-metadata derivation/term functions vary. Exact native results checked each time. No production performance or independent security qualification.",
                  question="Does immutable public CF1 metadata reuse reduce equality/IN end-to-end work with native results unchanged?",
                  gate="At least 5% reduction and 6/7 favorable pairs for equality and IN; point no worse than 10%.",
                  gate_passed=gate, python=platform.python_version(), sqlalchemy=sqlalchemy.__version__,
                  exact_native_results=True, aggregate=aggregate, records=records)
    output = Path(os.environ["CRYPTALIS_LAB_PROGRESS"]).parent / "public-metadata-paired.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    # Preserve measurements even if this finite speed gate fails.
    assert gate, "Public-metadata native paired performance gate was not met; inspect retained receipt."
