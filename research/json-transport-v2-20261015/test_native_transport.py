"""HELD native SELECT-only transport characterization; no product code imported.

All inputs are fixed public synthetic values. Run only through the independently
accepted cold wrapper and fresh dual-role preflight. No test fixture owns tables.
"""
import asyncio
import gc
import hashlib
import itertools
import json
import os
from pathlib import Path
import sys
import time
from uuid import UUID

import psycopg
from psycopg.pq import Format
from psycopg.types.json import (
    JsonLoader, JsonbLoader, JsonBinaryLoader, JsonbBinaryLoader, set_json_loads,
)
import pytest

B = Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
NIL = UUID('00000000-0000-0000-0000-000000000000')
RECORD = UUID('01234567-89ab-cdef-0123-456789abcdef')
TENANT = UUID('fedcba98-7654-3210-fedc-ba9876543210')
TABLE = '11111111-2222-3333-4444-555555555555'
INT_EXTRAS = (-9223372036854775808, -9007199254740993, -1, 0,
              9007199254740993, 9223372036854775807)
ROUTES = [(route, binary, mode, record, tenant)
          for route in ('sync', 'async') for binary in (False, True)
          for mode in ('default', 'shared', 'per_oid')
          for record in ('uuid', 'bigint') for tenant in ('uuid', 'text')]
ROUTE_IDS = [f'{r}-{"binary" if b else "text"}-{m}-{rk}-{tk}'
             for r, b, m, rk, tk in ROUTES]
NEGATIVES = [(route, binary) for route in ('sync', 'async') for binary in (False, True)]
NEGATIVE_IDS = [f'{r}-{"binary" if b else "text"}' for r, b in NEGATIVES]
COSTS = [(rows, length) for rows in (1, 143, 286) for length in (0, 74, 1024)]
COST_IDS = [f'rows{rows}-bytes{length}' for rows, length in COSTS]
ORDERS = tuple(itertools.permutations(('native', 'jsonb', 'json')))


def _url():
    assert '_cryptalis_test_preflight' in sys.modules, 'FRESH_PREFLIGHT_REQUIRED'
    assert sys.dont_write_bytecode, 'COLD_SOURCE_REQUIRED'
    assert psycopg.__version__ == '3.3.6', 'UNEXPECTED_DRIVER'
    assert Path(sys.prefix) in {B/'release-lab/integrated221-installed-20261015'/c
                                for c in ('sa21',)}, 'INSTALLED_CELL_REQUIRED'
    # Only the unchanged runner reads private files. Never persist or format this value.
    return os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']


def _write(kind, record):
    assert kind in {'transport', 'isolation', 'negative', 'cost'}
    evidence = Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent
    assert evidence in {B/f'evidence/json-transport-native-probe-v2-{c}-20261015'
                        for c in ('sa21',)}, 'EVIDENCE_PATH'
    path = evidence/f'{kind}-observations.jsonl'
    data = (json.dumps(record, sort_keys=True, ensure_ascii=True) + '\n').encode()
    fd = os.open(path, os.O_CREAT | os.O_APPEND | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'ab') as stream:
        stream.write(data)


def _bytes(length):
    return bytes((17 * i + 3) % 256 for i in range(length))


def _cases(record_type, tenant_type):
    record = RECORD if record_type == 'uuid' else 1
    tenant = TENANT if tenant_type == 'uuid' else TABLE
    cases = [(f'bytes{n}', (_bytes(n), record, tenant)) for n in (0, 1, 74, 1024)]
    for mask in range(8):
        values = (_bytes(74), record, tenant)
        cases.append((f'nullmask{mask}', tuple(None if mask & (1 << i) else v
                                             for i, v in enumerate(values))))
    extras = (NIL,) if record_type == 'uuid' else INT_EXTRAS
    cases.extend((f'record{i}', (_bytes(74), value, tenant)) for i, value in enumerate(extras))
    extras = (NIL,) if tenant_type == 'uuid' else ('', 'public synthetic tenant \u03bb')
    cases.extend((f'tenant{i}', (_bytes(74), record, value)) for i, value in enumerate(extras))
    assert len(cases) == {('uuid', 'uuid'): 14, ('uuid', 'text'): 15,
                          ('bigint', 'uuid'): 19, ('bigint', 'text'): 20}[(record_type, tenant_type)]
    return cases


def _query(record_type, tenant_type):
    assert record_type in {'uuid', 'bigint'} and tenant_type in {'uuid', 'text'}
    return ("SELECT p, r, t, jsonb_build_array(encode(p, 'hex'), r, t), "
            "json_build_array(encode(p, 'hex'), r, t) FROM "
            f"(VALUES (%s::bytea, %s::{record_type}, %s::{tenant_type})) AS v(p,r,t)")


def _snapshot():
    return tuple(psycopg.adapters.get_loader(oid, fmt)
                 for oid in (114, 3802) for fmt in (Format.TEXT, Format.BINARY))


def _install(connection, mode, calls):
    assert mode in {'default', 'shared', 'per_oid'}
    if mode == 'shared':
        def shared(data):
            calls.append(('shared', type(data).__name__, len(data)))
            return json.loads(bytes(data))
        set_json_loads(shared, context=connection)
    elif mode == 'per_oid':
        def tagged(base, tag):
            class Scoped(base):
                def load(self, data):
                    calls.append((tag, type(data).__name__, len(data)))
                    return {'adapter': tag, 'value': super().load(data)}
            return Scoped
        for name, text_loader, binary_loader in (
            ('json', JsonLoader, JsonBinaryLoader),
            ('jsonb', JsonbLoader, JsonbBinaryLoader),
        ):
            connection.adapters.register_loader(name, tagged(text_loader, name))
            connection.adapters.register_loader(name, tagged(binary_loader, name))


def _observed(cursor, row):
    return {'row': row, 'oids': tuple(c.type_code for c in cursor.description),
            'formats': tuple(cursor.pgresult.fformat(i) for i in range(5))}


def _expected(values):
    payload, record, tenant = values
    # Expected values use independently supplied typed inputs, never either builder.
    return [None if payload is None else payload.hex(),
            str(record) if isinstance(record, UUID) else record,
            str(tenant) if isinstance(tenant, UUID) else tenant]


def _validate(observed, values, record_type, tenant_type, binary, mode):
    row = observed['row']
    assert type(row) is tuple and len(row) == 5, 'NATIVE_ROW_SHAPE'
    expected_native_types = (bytes, UUID if record_type == 'uuid' else int,
                             UUID if tenant_type == 'uuid' else str)
    for actual, expected, datatype in zip(row[:3], values, expected_native_types):
        assert type(actual) is (type(None) if expected is None else datatype), 'NATIVE_TYPE'
        assert actual == expected, 'NATIVE_VALUE'
    assert observed['oids'] == (17, 2950 if record_type == 'uuid' else 20,
                                2950 if tenant_type == 'uuid' else 25, 3802, 114), 'NATIVE_OID'
    assert observed['formats'] == (int(binary),) * 5, 'CURSOR_FORMAT'
    expected = _expected(values)
    for actual, tag in zip(row[3:], ('jsonb', 'json')):
        if mode == 'per_oid':
            assert type(actual) is dict and set(actual) == {'adapter', 'value'}, 'SCOPED_LOADER_SHAPE'
            assert actual['adapter'] == tag, 'SCOPED_OID_DISPATCH'
            actual = actual['value']
        assert type(actual) is list and len(actual) == 3, 'DECODED_SHAPE'
        for value, wanted in zip(actual, expected):
            assert type(value) is type(wanted) and value == wanted, 'DECODED_TYPE_VALUE_OR_NULL'
    if mode == 'per_oid':
        assert row[3] != row[4], 'EXPECTED_CUSTOM_LOADER_DIVERGENCE'
    else:
        assert row[3] == row[4], 'DEFAULT_OR_SHARED_EQUIVALENCE'
    return expected


def _safe_projection(observed, expected, calls):
    return {'oids': list(observed['oids']), 'formats': list(observed['formats']),
            'native_types': [type(v).__name__ for v in observed['row'][:3]],
            'decoded_types': [type(v).__name__ for v in expected],
            'decoded_lengths': [len(v) if type(v) is str else None for v in expected],
            'null_positions': [i for i, v in enumerate(expected) if v is None],
            'expected_sha256': hashlib.sha256(json.dumps(expected, ensure_ascii=True).encode()).hexdigest(),
            'callback_events': calls, 'exact_comparison': True}


def _check_calls(mode, calls):
    expected_tags = {'default': [], 'shared': ['shared', 'shared'],
                     'per_oid': ['jsonb', 'json']}[mode]
    assert [item[0] for item in calls] == expected_tags, 'CALLBACK_DISPATCH'
    assert all(item[1] in {'bytes', 'memoryview', 'bytearray'} and item[2] > 0
               for item in calls), 'CALLBACK_INPUT_SHAPE'


def _sync_once(values, record_type, tenant_type, binary):
    with psycopg.connect(_url(), autocommit=True, connect_timeout=5) as connection:
        assert connection.info.server_version // 10000 == 16, 'PG16_REQUIRED'
        with connection.cursor(binary=binary) as cursor:
            cursor.execute(_query(record_type, tenant_type), values, prepare=False)
            row = cursor.fetchone()
            assert cursor.fetchone() is None, 'ONE_ROW_REQUIRED'
            result = _observed(cursor, row)
    assert connection.closed, 'CONNECTION_CLOSE'
    return result


async def _async_once(values, record_type, tenant_type, binary):
    async with await psycopg.AsyncConnection.connect(_url(), autocommit=True, connect_timeout=5) as connection:
        assert connection.info.server_version // 10000 == 16, 'PG16_REQUIRED'
        async with connection.cursor(binary=binary) as cursor:
            await cursor.execute(_query(record_type, tenant_type), values, prepare=False)
            row = await cursor.fetchone()
            assert await cursor.fetchone() is None, 'ONE_ROW_REQUIRED'
            result = _observed(cursor, row)
    assert connection.closed, 'CONNECTION_CLOSE'
    return result


def _record_case(case_id, name, observed, values, record_type, tenant_type, binary, mode, calls):
    expected = _validate(observed, values, record_type, tenant_type, binary, mode)
    _check_calls(mode, calls)
    _write('transport', {'case_id': case_id, 'input_id': name, 'mode': mode,
                         'outcome': 'INTENTIONAL_PER_OID_DIVERGENCE' if mode == 'per_oid'
                                    else 'EXACT_NATIVE_DEFAULT_OR_SHARED_MATCH',
                         **_safe_projection(observed, expected, calls)})


def _sync_characterize(case, case_id):
    _, binary, mode, record_type, tenant_type = case
    cases = _cases(record_type, tenant_type)
    first = cases[0][1]
    baseline = _snapshot()
    _validate(_sync_once(first, record_type, tenant_type, binary), first,
              record_type, tenant_type, binary, 'default')
    with psycopg.connect(_url(), autocommit=True, connect_timeout=5) as connection:
        assert connection.info.server_version // 10000 == 16, 'PG16_REQUIRED'
        calls = []
        _install(connection, mode, calls)
        for name, values in cases:
            calls.clear()
            with connection.cursor(binary=binary) as cursor:
                cursor.execute(_query(record_type, tenant_type), values, prepare=False)
                row = cursor.fetchone()
                assert cursor.fetchone() is None, 'ONE_ROW_REQUIRED'
                observed = _observed(cursor, row)
            _record_case(case_id, name, observed, values, record_type, tenant_type, binary, mode, calls)
    assert connection.closed and _snapshot() == baseline, 'SCOPED_REGISTRATION_LEAK'
    _validate(_sync_once(first, record_type, tenant_type, binary), first,
              record_type, tenant_type, binary, 'default')
    assert _snapshot() == baseline, 'FRESH_CONNECTION_GLOBAL_LEAK'


async def _async_characterize(case, case_id):
    _, binary, mode, record_type, tenant_type = case
    cases = _cases(record_type, tenant_type)
    first = cases[0][1]
    baseline = _snapshot()
    _validate(await _async_once(first, record_type, tenant_type, binary), first,
              record_type, tenant_type, binary, 'default')
    async with await psycopg.AsyncConnection.connect(_url(), autocommit=True, connect_timeout=5) as connection:
        assert connection.info.server_version // 10000 == 16, 'PG16_REQUIRED'
        calls = []
        _install(connection, mode, calls)
        for name, values in cases:
            calls.clear()
            async with connection.cursor(binary=binary) as cursor:
                await cursor.execute(_query(record_type, tenant_type), values, prepare=False)
                row = await cursor.fetchone()
                assert await cursor.fetchone() is None, 'ONE_ROW_REQUIRED'
                observed = _observed(cursor, row)
            _record_case(case_id, name, observed, values, record_type, tenant_type, binary, mode, calls)
    assert connection.closed and _snapshot() == baseline, 'SCOPED_REGISTRATION_LEAK'
    _validate(await _async_once(first, record_type, tenant_type, binary), first,
              record_type, tenant_type, binary, 'default')
    assert _snapshot() == baseline, 'FRESH_CONNECTION_GLOBAL_LEAK'


@pytest.mark.parametrize('case', ROUTES, ids=ROUTE_IDS)
def test_native_shapes_and_scoped_loaders(case):
    case_id = ROUTE_IDS[ROUTES.index(case)]
    if case[0] == 'sync':
        _sync_characterize(case, case_id)
    else:
        asyncio.run(_async_characterize(case, case_id))
    _write('isolation', {'case_id': case_id, 'global_adapter_classes_unchanged': True,
                         'fresh_default_before_and_after': True, 'connections_closed': True})


@pytest.mark.parametrize('route_binary', NEGATIVES, ids=NEGATIVE_IDS)
def test_observed_comparator_negatives(route_binary):
    route, binary = route_binary
    values = (_bytes(74), 9223372036854775807, TABLE)
    observed = (_sync_once(values, 'bigint', 'text', binary) if route == 'sync'
                else asyncio.run(_async_once(values, 'bigint', 'text', binary)))
    _validate(observed, values, 'bigint', 'text', binary, 'default')
    mutants = {}
    for label in ('null_slot', 'length', 'integer_type', 'integer_value', 'slot_order'):
        row = list(observed['row'])
        decoded = list(row[4])
        if label == 'null_slot': decoded[0] = None
        if label == 'length': decoded.pop()
        if label == 'integer_type': decoded[1] = str(decoded[1])
        if label == 'integer_value': decoded[1] -= 1
        if label == 'slot_order': decoded[0], decoded[2] = decoded[2], decoded[0]
        row[4] = decoded
        mutants[label] = {**observed, 'row': tuple(row)}
    mutants['oid'] = {**observed, 'oids': (*observed['oids'][:4], 3802)}
    mutants['format'] = {**observed, 'formats': (1 - int(binary),) * 5}
    row = list(observed['row']); row[1] -= 1
    mutants['native_value'] = {**observed, 'row': tuple(row)}
    for label, changed in mutants.items():
        with pytest.raises(AssertionError):
            _validate(changed, values, 'bigint', 'text', binary, 'default')
    _write('negative', {'case_id': NEGATIVE_IDS[NEGATIVES.index(route_binary)],
                        'actual_native_baseline_verified': True,
                        'actual_observation_mutations_rejected': sorted(mutants)})


def _cost_query(variant):
    # The record slot depends on the generated row even for empty payloads.
    # This prevents a constant envelope from standing in for per-row transport.
    expression = {'native': 'p, i::bigint, t',
                  'jsonb': "jsonb_build_array(encode(p, 'hex'), i::bigint, t)",
                  'json': "json_build_array(encode(p, 'hex'), i::bigint, t)"}[variant]
    return (f'SELECT i, {expression} FROM '
            '(VALUES (%s::bytea, %s::uuid)) AS v(p,t) '
            'CROSS JOIN generate_series(1, %s::integer) AS g(i) ORDER BY i')


def _timed_fetch(connection, variant, values, count):
    query = _cost_query(variant)
    cpu_start = time.process_time_ns()
    start = time.perf_counter_ns()
    with connection.cursor(binary=False) as cursor:
        cursor.execute(query, (*values, count), prepare=False)
        rows = cursor.fetchall()
        oids = tuple(column.type_code for column in cursor.description)
        formats = tuple(cursor.pgresult.fformat(i) for i in range(len(oids)))
    wall = time.perf_counter_ns() - start
    cpu = time.process_time_ns() - cpu_start
    assert cursor.closed, 'TIMED_CURSOR_CLOSE'
    assert len(rows) == count and [row[0] for row in rows] == list(range(1, count + 1)), 'COMPLETE_ORDERED_FETCH'
    assert formats == (0,) * len(oids), 'DEFAULT_TEXT_COST_FORMAT'
    if variant == 'native':
        assert oids == (23, 17, 20, 2950), 'NATIVE_COST_OID'
        for row in rows:
            assert tuple(type(v) for v in row[1:]) == (bytes, int, UUID), 'NATIVE_COST_TYPES'
            assert row[1:] == (values[0], row[0], values[1]), 'NATIVE_COST_VALUES'
    else:
        assert oids == (23, 3802 if variant == 'jsonb' else 114), 'JSON_COST_OID'
        for row in rows:
            wanted = _expected((values[0], row[0], values[1]))
            assert type(row[1]) is list and len(row[1]) == 3, 'COST_SHAPE'
            assert all(type(v) is type(w) and v == w for v, w in zip(row[1], wanted)), 'COST_EXACT_VALUES'
    return {'wall_ns': wall, 'client_process_cpu_ns': cpu, 'oids': list(oids),
            'formats': list(formats), 'complete_fetch_closed': True}


@pytest.mark.parametrize('rows_length', COSTS, ids=COST_IDS)
def test_counterbalanced_native_cost(rows_length):
    count, length = rows_length
    values = (_bytes(length), TENANT)
    assert gc.isenabled(), 'NORMAL_GC_REQUIRED'
    baseline = _snapshot()
    with psycopg.connect(_url(), autocommit=True, connect_timeout=5) as connection:
        assert connection.info.server_version // 10000 == 16, 'PG16_REQUIRED'
        for block, order in enumerate(ORDERS):
            for iteration in range(10):
                for position, variant in enumerate(order):
                    sample = _timed_fetch(connection, variant, values, count)
                    _write('cost', {'rows': count, 'payload_bytes': length, 'block': block,
                                    'order': list(order), 'position': position, 'variant': variant,
                                    'iteration': iteration, 'warmup': iteration < 2,
                                    'gc_enabled': gc.isenabled(), **sample})
    assert connection.closed and _snapshot() == baseline, 'COST_CLOSE_AND_ADAPTER_SCOPE'
