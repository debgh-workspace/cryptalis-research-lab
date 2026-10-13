"""C8 coordinator-only unchanged-runtime attribution; not an optimization gate."""
from contextlib import ExitStack
import cProfile
import gc
import hashlib
import json
import os
from pathlib import Path
import platform
import pstats
import resource
import time
from uuid import UUID

import psycopg
from psycopg import sql
import sqlalchemy
from sqlalchemy import Text, bindparam, event, select
from sqlalchemy.orm import sessionmaker

import cryptalis.sqlalchemy as adapter
from cryptalis.crypto import cf1
from cryptalis.crypto.keys import PreparedKeys, tuple_bytes
from cryptalis._sqlalchemy_search import _SearchValue, rewrite_search
from single_tenant_public_cascade_fixture import single_tenant_public_cascade_application
from test_migration import TABLE_ID, keys, publish, run

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / 'experiments/INDEXED_PROFILE_PROTOCOL.md'
MANIFEST = ROOT / 'experiments/INDEXED_PROFILE_SOURCE_MANIFEST.json'
EXPECTED_MANIFEST = 'aba658622e884084762e09be61aed54c7a1023af37d332af9f5143aa5e358688'
FAMILIES = (
    ('point', UUID(int=600), 0, 1),
    ('eq_miss', 'C8-missing', 1, 0),
    ('eq_hot', 'exact', 1, 143),
    ('in2_miss', ['C8-missing-0', 'C8-missing-1'], 2, 0),
    ('in2_hot', ['exact', '雪😀'], 2, 286),
    ('in20_miss', [f'C8-missing-{i}' for i in range(20)], 20, 0),
    ('in20_hot', ['exact', '雪😀'] + [f'C8-missing-{i}' for i in range(18)], 20, 286),
    ('in20_duplicate', ['exact', '雪😀'] * 10, 20, 286),
)
TARGETS = {
    'derive': cf1._derive, 'term': cf1._term, 'open_text': cf1.open_text,
    'equality_term': cf1.equality_term, 'resolve': PreparedKeys._resolve,
    'tuple_bytes': tuple_bytes, 'admit': adapter._Attachment.admit,
    'read_result': adapter._ReadText.process_result_value,
    'search_bind': _SearchValue.process_bind_param, 'rewrite': rewrite_search,
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_source():
    assert digest(MANIFEST) == EXPECTED_MANIFEST
    entries = json.loads(MANIFEST.read_text())
    assert len(entries) == 201
    assert all(digest(ROOT / name) == expected for name, expected in entries.items())
    assert Path(adapter.__file__).resolve() == ROOT / 'src/cryptalis/sqlalchemy.py'
    return {'files': len(entries), 'manifest_sha256': digest(MANIFEST),
            'harness_sha256': digest(Path(__file__)), 'protocol_sha256': digest(PROTOCOL)}


def clocks():
    return {'wall_ns': time.perf_counter_ns(),
            'raw_ns': time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW),
            'process_ns': time.process_time_ns(), 'thread_ns': time.thread_time_ns()}


def elapsed(start, end):
    return {name: (end[name] - start[name]) / 1e6 for name in start}


def usage():
    value = resource.getrusage(resource.RUSAGE_SELF)
    return {'clocks': clocks(), 'load_1_5_15': list(os.getloadavg()),
            'maxrss_kib_process_highwater': value.ru_maxrss,
            'minor_faults': value.ru_minflt, 'major_faults': value.ru_majflt,
            'voluntary_switches': value.ru_nvcsw, 'involuntary_switches': value.ru_nivcsw}


def safe_name(key):
    filename, line, name = key
    if filename.startswith(str(ROOT) + '/'):
        filename = 'candidate/' + str(Path(filename).relative_to(ROOT))
    elif '/site-packages/' in filename:
        filename = 'dependency/' + filename.split('/site-packages/', 1)[1]
    elif filename != '~':
        filename = 'python/' + Path(filename).name
    return [filename, line, name]


def stats_document(profile):
    stats = pstats.Stats(profile)
    named = {}
    for name, function in TARGETS.items():
        code = function.__code__
        value = stats.stats.get((code.co_filename, code.co_firstlineno, code.co_name))
        named[name] = {'calls': value[1], 'self_cpu_s': value[2], 'inclusive_cpu_s': value[3]} if value else {
            'calls': 0, 'self_cpu_s': 0, 'inclusive_cpu_s': 0}
    functions = []
    for key, (primitive, calls, own, cumulative, callers) in sorted(stats.stats.items()):
        functions.append({'function': safe_name(key), 'primitive_calls': primitive, 'calls': calls,
                          'self_cpu_s': own, 'inclusive_cpu_s': cumulative,
                          'callers': [{'function': safe_name(caller), 'stats': list(data) if isinstance(data, tuple) else data}
                                      for caller, data in sorted(callers.items())]})
    return {'timer': 'time.thread_time; instrumentation overhead included',
            'total_cpu_s': stats.total_tt, 'named': named, 'functions': functions}


def measured(call, profiled):
    profile = cProfile.Profile(timer=time.thread_time) if profiled else None
    start = clocks()
    try:
        if profile is None:
            value = call()
        else:
            value = profile.runcall(call)
    finally:
        end = clocks()
    return value, {'start': start, 'end': end, 'elapsed_ms': elapsed(start, end),
                   'profile': stats_document(profile) if profile is not None else None}


def statement(app, family, value, projection):
    c = app.Customer
    if family == 'point':
        predicate = c.id == value
    elif family.startswith('eq'):
        predicate = c.name == bindparam('needle', value=value, type_=Text())
    else:
        predicate = c.name.in_(bindparam('needles', value=value, expanding=True, type_=Text()))
    columns = (c.id,) if projection == 'ids' else (c.id, c.name)
    return select(*columns).where(predicate).order_by(c.id)


def independent(driver, app, family, value, projection):
    columns = sql.SQL('id') if projection == 'ids' else sql.SQL('id, name')
    predicate = (sql.SQL('id = %s') if family == 'point' else
                 sql.SQL('name = %s::text') if family.startswith('eq') else
                 sql.SQL('name = ANY(%s::text[])'))
    query = sql.SQL('SELECT {} FROM {}.customer WHERE {} ORDER BY id').format(
        columns, sql.Identifier(app.schema), predicate)
    return driver.execute(query, (value,)).fetchall()


def safe_plan(document):
    allowed = ('Node Type', 'Plan Rows', 'Startup Cost', 'Total Cost')
    def node(value):
        answer = {key: value[key] for key in allowed if key in value}
        if 'Plans' in value:
            answer['Plans'] = [node(child) for child in value['Plans']]
        return answer
    result = node(document[0]['Plan'])
    def indexed(value):
        return 'Index' in value.get('Node Type', '') or any(indexed(child) for child in value.get('Plans', []))
    return {'index_node_present': indexed(result), 'root': result}


def count_prediction(phases, terms, nonnull_rows):
    observed = {name: sum(phase['profile']['named'][name]['calls'] for phase in phases.values())
                for name in ('term', 'derive', 'open_text', 'resolve')}
    expected = {'term': terms + nonnull_rows, 'derive': terms + 2 * nonnull_rows,
                'open_text': nonnull_rows, 'resolve': 2 * terms + 4 * nonnull_rows}
    return {'observed': observed, 'predicted': expected, 'matches': observed == expected}


def test_indexed_equality_in_cost_attribution():
    binding = verify_source()
    assert sqlalchemy.__version__ in ('2.1.3', '2.0.51')
    output = Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent / 'indexed-cost-profile.json'
    assert not output.exists(), 'Do not overwrite a prior diagnostic receipt.'
    report = {'source_before': binding, 'python': platform.python_version(),
              'sqlalchemy': sqlalchemy.__version__, 'scope': 'C8 unchanged S18 attribution; no speedup gate',
              'observations': [], 'native_controls': [], 'plans': [], 'gc_events': [],
              'resources': [], 'failure': None}
    gc_state = (gc.isenabled(), gc.get_threshold())
    scope = {'phase': 'setup'}
    def observe_gc(phase, info):
        report['gc_events'].append({'phase': phase, 'generation': info['generation'],
            'collected': info.get('collected', 0), 'uncollectable': info.get('uncollectable', 0),
            'scope': dict(scope), 'clocks': clocks()})
    gc.callbacks.append(observe_gc)
    try:
        with ExitStack() as stack:
            apps = {path: stack.enter_context(single_tenant_public_cascade_application(
                rows=1000, unique=False, public_table=False)) for path in ('native', 'protected')}
            run(apps['protected'], chunk_size=256)
            publish(apps['protected'])
            for app in apps.values():
                with app.owner.begin() as connection:
                    connection.exec_driver_sql(f'ANALYZE "{app.schema}".customer')
            factory = adapter.attach(apps['protected'].mapping, apps['protected'].runtime,
                lock=apps['protected'].plan.lock_bytes, keys=keys(TABLE_ID),
                deployment=(apps['protected'].plan, apps['protected'].pin))
            sessions = {'native': stack.enter_context(sessionmaker(apps['native'].runtime)()),
                        'protected': stack.enter_context(factory(tenant_id=TABLE_ID))}
            driver = stack.enter_context(psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
            captured = {}
            def capture(path):
                def after(conn, cursor, sql_text, parameters, context, many):
                    captured[path] = (sql_text, parameters)
                return after
            for path, app in apps.items():
                listener = capture(path)
                event.listen(app.runtime, 'after_cursor_execute', listener)
                stack.callback(event.remove, app.runtime, 'after_cursor_execute', listener)
            for family, value, terms, expected_count in FAMILIES:
                for projection in ('ids', 'text'):
                    scope.clear()
                    scope.update(phase='cell', family=family, projection=projection)
                    report['resources'].append({'boundary': 'before_cell', **scope, **usage()})
                    expected = independent(driver, apps['native'], family, value, projection)
                    assert len(expected) == expected_count
                    queries = {path: statement(app, family, value, projection) for path, app in apps.items()}
                    for mode, count in (('warmup', 3), ('timed', 10), ('profiled', 3)):
                        for pair in range(count):
                            order = ('native', 'protected') if pair % 2 == 0 else ('protected', 'native')
                            for path in order:
                                scope.update(phase=mode, pair=pair, path=path)
                                response, execute = measured(lambda: sessions[path].execute(queries[path]), mode == 'profiled')
                                try:
                                    rows, fetch = measured(response.all, mode == 'profiled')
                                finally:
                                    response.close()
                                assert [tuple(row) for row in rows] == expected
                                phases = {'execute': execute, 'fetch_all': fetch}
                                observation = {**scope, 'order': list(order), 'rows': len(rows), 'terms': terms,
                                               'exact_native': True, 'phases': phases}
                                if path == 'protected' and mode == 'profiled':
                                    nonnull = sum(row[1] is not None for row in expected) if projection == 'text' else 0
                                    observation['prediction'] = count_prediction(phases, terms, nonnull)
                                report['observations'].append(observation)
                    for path in apps:
                        sql_text, parameters = captured.pop(path)
                        document = driver.execute('EXPLAIN (FORMAT JSON) ' + sql_text, parameters).fetchone()[0]
                        report['plans'].append({'family': family, 'projection': projection, 'path': path,
                                                'plan': safe_plan(document)})
                    report['resources'].append({'boundary': 'after_cell', **scope, **usage()})
            for family, value in (('eq_null', None), ('in_empty', []), ('in_null', [None]), ('in_hot_null', ['exact', None])):
                for projection in ('ids', 'text'):
                    expected = independent(driver, apps['native'], family, value, projection)
                    for path, app in apps.items():
                        rows = sessions[path].execute(statement(app, family, value, projection)).all()
                        assert [tuple(row) for row in rows] == expected
                        report['native_controls'].append({'family': family, 'projection': projection,
                                                         'path': path, 'rows': len(rows), 'exact_native': True})
            captured.clear()
    except BaseException as error:
        report['failure'] = type(error).__name__
        raise
    finally:
        gc.callbacks.remove(observe_gc)
        report['gc_settings_unchanged'] = gc_state == (gc.isenabled(), gc.get_threshold())
        try:
            report['source_after'] = verify_source()
            report['source_unchanged'] = report['source_before'] == report['source_after']
        except BaseException as error:
            # Keep an earlier native/driver failure primary and retain this
            # independent evidence failure without exception arguments/locals.
            report['source_validation_error'] = type(error).__name__
            report['source_unchanged'] = False
        report['all_count_predictions_match'] = all(row['prediction']['matches'] for row in report['observations'] if 'prediction' in row)
        report['schedule_complete'] = (len(report['observations']) == 512 and
            len(report['plans']) == 32 and len(report['native_controls']) == 16)
        with output.open('x') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
    assert report['schedule_complete'] and report['source_unchanged'] and report['gc_settings_unchanged']
    assert report['all_count_predictions_match'], 'Diagnostic count prediction differed; preserve receipt and investigate.'
