"""Pure S17 admission counterfactual; no engine, key preparation or DB calls."""
import argparse
import asyncio
import concurrent.futures
import cProfile
import hashlib
import inspect
import json
import pstats
import statistics
import textwrap
import time
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID

import sqlalchemy
from sqlalchemy import Column, Integer, Text, Uuid, asc, desc, func, nulls_last, select, type_coerce
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import aliased, declarative_base
from sqlalchemy.sql.functions import FunctionElement
import cryptalis.sqlalchemy as adapter

BASELINE_SHA = 'fc2f7a7c983370f7c81874b56ec8e511532d226fc962bc0c8939b38d4daadfbe'


def candidate_method():
    assert hashlib.sha256(Path(adapter.__file__).read_bytes()).hexdigest() == BASELINE_SHA
    original = textwrap.dedent(inspect.getsource(adapter._Attachment.admit))
    needle = 'safe_count_stars = set()\n    for node in visitors.iterate(statement):\n'
    replacement = ('safe_count_stars = set()\n    has_textual_references = False\n'
                   '    for node in visitors.iterate(statement):\n'
                   '        if getattr(node, "__visit_name__", None) == "textual_label_reference":\n'
                   '            has_textual_references = True\n')
    assert original.count(needle) == 1
    source = original.replace(needle, replacement)
    needle = '            self._admit_textual_references(node)'
    replacement = ('            if has_textual_references:\n'
                   '                self._admit_textual_references(node)\n'
                   '            else:\n'
                   '                for root in node._order_by_clauses + node._group_by_clauses:\n'
                   '                    if self.protected(root):\n'
                   '                        raise UnsupportedProtectedOperation()')
    assert source.count(needle) == 1
    source = source.replace(needle, replacement)
    namespace = dict(vars(adapter))
    exec(compile(source, '<C5-counterfactual>', 'exec'), namespace)
    return namespace['admit'], hashlib.sha256(source.encode()).hexdigest()


Base = declarative_base()
class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Uuid, primary_key=True)
    tenant_id = Column(Uuid)
    name = Column(Text)
    rank = Column(Integer)

class Public(Base):
    __tablename__ = 'public_subject'
    id = Column(Uuid, primary_key=True)
    name = Column(Text)
    rank = Column(Integer)


def owners():
    method, digest = candidate_method()
    class Candidate(adapter._Attachment):
        admit = method
    result = {}
    for name, cls in [('baseline', adapter._Attachment), ('candidate', Candidate)]:
        owner = cls(Base.registry, SimpleNamespace(dialect=postgresql.dialect()), {}, None)
        owner.bindings = [SimpleNamespace(column=Subject.__table__.c.name,
                                         descriptor=SimpleNamespace(equality=True))]
        result[name] = owner
    return result, digest


def outcome(owner, query):
    try:
        owner.admit(query)
    except adapter.UnsupportedProtectedOperation:
        return 'refused'
    return 'admitted'


def controls(pair):
    from test_textual_clause_boundary import CLAUSES, _queries
    app = SimpleNamespace(Customer=Subject, tenant=UUID(int=77))
    cases = []
    for clause in CLAUSES:
        if clause == 'distinct_extension' and not hasattr(postgresql, 'distinct_on'):
            continue
        if clause == 'aggregate_order' and not hasattr(FunctionElement, 'aggregate_order_by'):
            continue
        for alias in (False, True):
            for public in (False, True):
                q, _, _ = _queries(app, clause, alias, public)
                cases.append((q, 'admitted' if public else 'refused'))
            if clause.startswith('distinct'):
                q, _, _ = _queries(app, clause, alias, True, shadow=True)
                cases.append((q, 'admitted'))
    for model in (Subject, aliased(Subject, name='a')):
        for wrapper in (lambda x:x, asc, lambda x:nulls_last(desc(x)),
                        lambda x:type_coerce(asc(x), Text())):
            cases.extend(((select(model.id).order_by(wrapper('name')), 'refused'),
                          (select(model.id, model.rank.label('name')).order_by(wrapper('name')), 'admitted'),
                          (select(model.id).order_by(wrapper(model.name)), 'refused')))
        cases.append((select(func.count().label('name')).select_from(model).group_by('name'), 'refused'))
        cases.append((select(model.id, model.name.label('rank')).group_by(model.id, 'rank'), 'admitted'))
        inner = select(Public.rank).order_by('name').limit(1).scalar_subquery()
        cases.append((select(model.id, inner), 'admitted'))
        inner = select(model.rank).order_by('name').limit(1).scalar_subquery()
        cases.append((select(Public.id, inner), 'refused'))
    for query, expected in cases:
        assert {outcome(o, query) for o in pair.values()} == {expected}
    return cases


def profile_calls(owner, query):
    profile = cProfile.Profile()
    for _ in range(100):
        profile.runcall(owner.admit, query)
    stats = pstats.Stats(profile)
    names = {'admit', '_admit_textual_references', 'references', 'protected',
             'iterate', 'search_shape', 'shares_lineage'}
    result = {}
    for (_, _, name), values in stats.stats.items():
        if name in names:
            result[name] = result.get(name, 0) + values[1]
    return result


def main(output):
    pair, digest = owners()
    cases = controls(pair)
    fixed = {
        'point': select(Subject.id, Subject.name).where(Subject.id == UUID(int=600)).order_by(Subject.id),
        'equality': select(Subject.id, Subject.name).where(Subject.name == 'exact').order_by(Subject.id),
        'in2': select(Subject.id, Subject.name).where(Subject.name.in_(['exact', '雪😀'])).order_by(Subject.id),
        'public_label': select(Subject.id, Subject.name, Subject.rank.label('chosen')).order_by('chosen'),
    }
    calls = {family:{variant:profile_calls(owner, query) for variant,owner in pair.items()}
             for family,query in fixed.items()}
    mechanism = all(calls[f]['baseline']['_admit_textual_references'] == 100 and
                    calls[f]['candidate'].get('_admit_textual_references', 0) == 0 and
                    calls[f]['baseline']['admit'] == calls[f]['candidate']['admit'] == 100
                    for f in ('point', 'equality', 'in2'))
    mechanism = mechanism and calls['public_label']['candidate']['_admit_textual_references'] == 100
    def threaded(number):
        local, _ = owners()
        for i in range(128):
            query, expected = cases[(number + i) % len(cases)]
            assert outcome(local['candidate'], query) == expected
        return 128
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        thread_checks = sum(executor.map(threaded, range(8)))
    async def cancellation():
        async def worker(number):
            local, _ = owners()
            before = dict(local['candidate'].__dict__)
            await asyncio.sleep(0)
            for query, expected in cases:
                assert outcome(local['candidate'], query) == expected
            assert local['candidate'].__dict__ == before
            await asyncio.sleep(0)
            return True
        tasks = [asyncio.create_task(worker(i)) for i in range(8)]
        tasks[0].cancel()
        await asyncio.sleep(0)
        tasks[1].cancel()
        result = await asyncio.gather(*tasks, return_exceptions=True)
        assert sum(isinstance(x, asyncio.CancelledError) for x in result) == 2
        assert sum(x is True for x in result) == 6
        return {'cancelled':2,'completed':6,'owner_state_unchanged':True}
    cancellation_result = asyncio.run(cancellation())
    records = []
    for block in range(9):
        for family, query in fixed.items():
            for variant in (['baseline', 'candidate'] if block % 2 == 0 else ['candidate', 'baseline']):
                owner = pair[variant]
                for _ in range(30):owner.admit(query)
                started = time.perf_counter_ns()
                for _ in range(500):owner.admit(query)
                elapsed = (time.perf_counter_ns() - started) / 500 / 1000
                records.append({'block':block,'family':family,'variant':variant,'us_per_admission':elapsed})
    aggregate = []
    for family in fixed:
        values = {v:[r['us_per_admission'] for r in records if r['family']==family and r['variant']==v]
                  for v in pair}
        before, after = (statistics.median(values[v]) for v in pair)
        aggregate.append({'family':family,'before_us':before,'after_us':after,
                          'reduction_percent':100*(before-after)/before,
                          'favorable_pairs':sum(a>b for a,b in zip(values['baseline'], values['candidate']))})
    speed = all(r['reduction_percent'] >= 10 and r['favorable_pairs'] >= 8
                for r in aggregate if r['family'] != 'public_label')
    speed = speed and next(r['reduction_percent'] for r in aggregate if r['family']=='public_label') >= -5
    report = {'scope':'Pure admission only; not end-to-end latency or native DB verification',
              'sqlalchemy':sqlalchemy.__version__,'baseline_sha256':BASELINE_SHA,
              'counterfactual_sha256':digest,'outcome_controls':len(cases),'thread_checks':thread_checks,
              'cancellation':cancellation_result,'call_counts_per_100':calls,'mechanism_gate':mechanism,
              'pure_speed_gate':speed,'aggregate':aggregate,'records':records}
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('sqlalchemy','outcome_controls','thread_checks','mechanism_gate','pure_speed_gate','aggregate')}, indent=2))

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output', type=Path, required=True)
    main(parser.parse_args().output)
