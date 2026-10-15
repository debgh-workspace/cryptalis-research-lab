"""HELD SOURCE-ONLY packet: synthetic SELECT-only PostgreSQL representation proof.

No product/reference imports or fixture DDL. Root must separately admit this
packet through the unchanged cold runner, fresh preflight and latest closed
predecessor. Preparation does not authorize collection or execution.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
from uuid import UUID

import psycopg
import pytest

B = Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
EVIDENCE = B/'evidence/abort-envelope-native-probe-v1-sa21-20261015'
LIMIT = 16 * 1024 * 1024
MAX_PARAMETER_BYTES = LIMIT + 1
MAX_DIAGNOSTIC_TRANSFER = LIMIT + 32
TABLE = '00000000-0000-0000-0000-000000000001'
TABLE_TWO = '00000000-0000-0000-0000-000000000003'
SOURCE = '00000000-0000-0000-0000-000000000002'
UUID_MAX = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1

FAMILIES = (
    ('f_uuid_empty', False, 'uuid', 0, 'plain'),
    ('r_uuid_empty', True, 'uuid', 0, 'plain'),
    ('f_uuid_one', False, 'uuid', 1, 'plain'),
    ('r_uuid_one', True, 'uuid', 1, 'plain'),
    ('f_int64_one', False, 'int64', 1, 'plain'),
    ('r_int64_one', True, 'int64', 1, 'plain'),
    ('f_two_mixed', False, 'mixed', 10, 'plain'),
    ('r_two_mixed', True, 'mixed', 10, 'plain'),
    ('f_unicode', False, 'uuid', 10, 'unicode'),
    ('r_unicode', True, 'uuid', 10, 'unicode'),
    ('f_controls', False, 'uuid', 10, 'controls'),
    ('r_controls', True, 'uuid', 10, 'controls'),
    ('f_count9', False, 'uuid', 9, 'plain'),
    ('f_count10', False, 'uuid', 10, 'plain'),
    ('f_count9999', False, 'uuid', 9999, 'plain'),
    ('f_count10000', False, 'uuid', 10000, 'plain'),
    ('f_count2p53m1', False, 'uuid', 2**53-1, 'plain'),
    ('f_count2p53', False, 'uuid', 2**53, 'plain'),
    ('f_count17digits', False, 'uuid', 10**16, 'plain'),
)
BOUNDARIES = (
    ('canonical_below', 'canonical', -1), ('canonical_equal', 'canonical', 0),
    ('canonical_above', 'canonical', 1), ('native_below', 'native', -1),
    ('native_equal', 'native', 0), ('native_above', 'native', 1),
)
REJECTIONS = (
    ('nul', '{"x":"\\u0000"}'),
    ('high_surrogate', '{"x":"\\ud800"}'),
    ('low_surrogate', '{"x":"\\udfff"}'),
)

LENGTH_SQL = '''WITH supplied AS (SELECT %s::pg_catalog.text AS wire),
parsed AS (SELECT wire, wire::pg_catalog.jsonb AS j FROM supplied)
SELECT pg_catalog.octet_length(pg_catalog.convert_to(wire, 'UTF8')),
       pg_catalog.octet_length(pg_catalog.convert_to(j::pg_catalog.text, 'UTF8')),
       pg_catalog.jsonb_typeof(j) FROM parsed'''
TEXT_SQL = 'SELECT %s::pg_catalog.jsonb::pg_catalog.text'


def need(condition, code):
    if not condition:
        raise AssertionError(code)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def separators(value):
    # Structural punctuation count; never scan a large string byte by byte.
    if type(value) is dict:
        return len(value) + max(len(value)-1, 0) + sum(separators(v) for v in value.values())
    if type(value) is list:
        return max(len(value)-1, 0) + sum(separators(v) for v in value)
    return 0


def pairs(items):
    result = {}
    for key, value in items:
        need(type(key) is str and key.isascii() and key not in result, 'DUPLICATE_OR_NONASCII_KEY')
        result[key] = value
    return result


def reject_number(_token):
    raise AssertionError('NONINTEGER_JSON_NUMBER')


def exact(left, right, depth=1):
    need(type(left) is type(right), 'ROUNDTRIP_TYPE')
    if type(left) is dict:
        need(depth <= 32 and left.keys() == right.keys(), 'ROUNDTRIP_KEYS_OR_DEPTH')
        for key in left:
            exact(left[key], right[key], depth+1)
    elif type(left) is list:
        need(depth <= 32 and len(left) == len(right), 'ROUNDTRIP_LIST_OR_DEPTH')
        for a, b in zip(left, right):
            exact(a, b, depth+1)
    else:
        need(left == right, 'ROUNDTRIP_VALUE')


def write(kind, record):
    need(kind in {'connection', 'state', 'domain', 'rejection', 'omission'}, 'RECORD_KIND')
    directory = Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent
    need(directory == EVIDENCE, 'EVIDENCE_PATH')
    # Only bounded counts, hashes, IDs, codes and public synthetic domain values.
    data = (json.dumps({'kind': kind, **record}, sort_keys=True, ensure_ascii=True) + '\n').encode()
    need(len(data) <= 8192, 'OBSERVATION_RECORD_LIMIT')
    fd = os.open(directory/'envelope-observations.jsonl',
                 os.O_CREAT | os.O_APPEND | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'ab') as stream:
        stream.write(data)


def connection(case):
    need('_cryptalis_test_preflight' in sys.modules, 'FRESH_PREFLIGHT_REQUIRED')
    need(sys.dont_write_bytecode, 'COLD_SOURCE_REQUIRED')
    need(psycopg.__version__ == '3.3.6', 'DRIVER_IDENTITY')
    need(Path(sys.prefix) == B/'release-lab/integrated221-installed-20261015/sa21', 'SA21_ONLY')
    # Only the unchanged authorized runner reads credential files. Never print,
    # serialize, parse or retain its preflight-attested runtime URL here.
    c = psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL'],
                        autocommit=True, connect_timeout=5)
    try:
        with c.cursor() as cur:
            cur.execute('''SELECT current_setting('server_version_num')::pg_catalog.int4,
                current_setting('server_encoding'), current_setting('client_encoding'),
                current_database(), current_user, pg_backend_pid()''', prepare=False)
            row = cur.fetchone()
        need(type(row[0]) is int and row[0]//10000 == 16, 'POSTGRESQL16_REQUIRED')
        need(row[1] == row[2] == 'UTF8', 'UTF8_REQUIRED')
        need(type(row[3]) is str and type(row[4]) is str and type(row[5]) is int, 'TARGET_TYPES')
        write('connection', {'case': case, 'version': row[0], 'server_encoding': row[1],
                             'client_encoding': row[2], 'backend_pid': row[5],
                             'target_digest': hashlib.sha256(canonical([row[3], row[4]])).hexdigest()})
        return c
    except BaseException:
        c.close()
        raise


def observe(c, case, label, value):
    encoded = canonical(value)
    need(len(encoded) <= MAX_PARAMETER_BYTES, 'PARAMETER_DIAGNOSTIC_BOUND')
    text = encoded.decode('utf-8')
    with c.cursor(binary=False) as cur:
        cur.execute(LENGTH_SQL, (text,), prepare=False)
        lengths = cur.fetchone()
        length_oids = tuple(item.type_code for item in cur.description)
        length_formats = tuple(cur.pgresult.fformat(i) for i in range(3))
    need(type(lengths) is tuple and len(lengths) == 3, 'LENGTH_ROW')
    need(type(lengths[0]) is int and type(lengths[1]) is int, 'LENGTH_TYPES')
    need(0 <= lengths[1] <= MAX_DIAGNOSTIC_TRANSFER, 'NATIVE_DIAGNOSTIC_TRANSFER_BOUND')
    with c.cursor(binary=False) as cur:
        cur.execute(TEXT_SQL, (text,), prepare=False)
        row = cur.fetchone()
        text_oid = cur.description[0].type_code
        text_format = cur.pgresult.fformat(0)
    need(type(row) is tuple and len(row) == 1 and type(row[0]) is str, 'NATIVE_TEXT_TYPE')
    native = row[0].encode('utf-8')
    predicted = len(encoded) + separators(value)
    record = {'case': case, 'label': label, 'status': 'OBSERVED_BEFORE_ASSERTIONS',
              'canonical_bytes': len(encoded), 'supplied_bytes': lengths[0],
              'native_bytes': lengths[1], 'received_native_bytes': len(native),
              'candidate_native_bytes': predicted, 'canonical_sha256': hashlib.sha256(encoded).hexdigest(),
              'native_sha256': hashlib.sha256(native).hexdigest(), 'root_type': lengths[2],
              'length_oids': length_oids, 'length_formats': length_formats,
              'text_oid': text_oid, 'text_format': text_format,
              'canonical_within_limit': len(encoded) <= LIMIT,
              'native_within_limit': lengths[1] <= LIMIT}
    write('state', record)
    need(length_oids == (23, 23, 25) and length_formats == (0, 0, 0), 'LENGTH_OID_FORMAT')
    need(text_oid == 25 and text_format == 0, 'TEXT_OID_FORMAT')
    need(lengths[0] == len(encoded) and lengths[1] == len(native), 'OCTET_LENGTH_MISMATCH')
    need(lengths[2] == 'object', 'ROOT_OBJECT_REQUIRED')
    decoded = json.loads(row[0], object_pairs_hook=pairs, parse_int=int,
                         parse_float=reject_number, parse_constant=reject_number)
    exact(value, decoded)
    need(canonical(decoded) == encoded, 'CANONICAL_ROUNDTRIP_BYTES')
    need(lengths[1] == predicted, 'NATIVE_SPACING_HYPOTHESIS_FAILED')
    return record


def initial(reverse, codec, count, metadata='plain'):
    model = {'scope': {'count': count, 'membership': '0'*64}, 'cursor': None,
             'rows': 0, 'chunks': 0, 'schema': {}, 'guard': ['A']}
    if metadata != 'plain':
        need(metadata in {'unicode', 'controls'}, 'METADATA_PROFILE')
        special = ('é 雪 😀 e\u0301 \u2028 \u2029 " \\ / , : [] {}'
                   if metadata == 'unicode' else ''.join(chr(i) for i in range(1, 32)) + '\\"/:,')
        model['schema'] = {'columns': [{'name': special, 'nullable': True}], 'text': special}
        model['guard'] = ['A', 30, True, 0, 'public', 'guard_fn', False,
                          ['search_path=pg_catalog', special], special, 'owner',
                          [['pause', 'A', special, special, False, ['search_path=pg_catalog'], 'owner']]]
    result = {'phase': 'EXPANDED', 'models': {TABLE: model}}
    codecs = {TABLE: 'uuid' if codec == 'mixed' else codec}
    if codec == 'mixed':
        result['models'][TABLE_TWO] = copy.deepcopy(model)
        codecs[TABLE_TWO] = 'int64'
    if reverse:
        result.update(layout_version=101, source_operation_id=SOURCE, source_plan_digest='1'*64)
    return result, codecs


def envelope(expanded, codecs, reverse):
    # Independent source-derived representative; no product/reference helper.
    value = copy.deepcopy(expanded)
    value['phase'] = 'BACKFILLED'
    for table, progress in value['models'].items():
        n = progress['scope']['count']
        progress.update(rows=n, chunks=n,
                        cursor=None if n == 0 else UUID_MAX if codecs[table] == 'uuid' else str(INT64_MIN))
    if not reverse:
        value['verification'] = {table: 'f'*64 for table in value['models']}
    return value


def states(expanded, codecs, reverse):
    count = expanded['models'][TABLE]['scope']['count']
    values = [('expanded', copy.deepcopy(expanded))]
    for label, rows in ([('partial', 1)] if count else []) + [('backfilled', count), ('verified', count)]:
        value = copy.deepcopy(expanded)
        value['phase'] = {'partial': 'EXPANDED', 'backfilled': 'BACKFILLED', 'verified': 'VERIFIED'}[label]
        for table, progress in value['models'].items():
            last = None if rows == 0 else str(UUID(int=rows-1)) if codecs[table] == 'uuid' else str(INT64_MIN+rows-1)
            progress.update(cursor=last, rows=rows, chunks=(rows+4999)//5000)
        if label == 'verified' and not reverse:
            value['verification'] = {table: 'f'*64 for table in value['models']}
        values.append((label, value))
    return values + [('abort_'+label, {**copy.deepcopy(value), 'phase': 'ABORTED'}) for label, value in values]


@pytest.mark.parametrize('codec', ('uuid', 'int64'), ids=('uuid', 'int64'))
def test_native_cursor_domains(codec):
    case = 'domain_'+codec
    with connection(case) as c:
        if codec == 'uuid':
            expected = (UUID(int=0), UUID(int=1), UUID(int=2**128-1))
            sql = '''SELECT v, v::pg_catalog.text FROM
                (VALUES (%s::pg_catalog.uuid), (%s::pg_catalog.uuid), (%s::pg_catalog.uuid)) q(v) ORDER BY v'''
            parameters = tuple(reversed(expected))
            oid, width = 2950, 36
        else:
            expected = (INT64_MIN, -9007199254740993, -1, 0, 9007199254740993, INT64_MAX)
            sql = '''SELECT v, v::pg_catalog.text FROM
                (VALUES (%s::pg_catalog.int8), (%s::pg_catalog.int8), (%s::pg_catalog.int8),
                        (%s::pg_catalog.int8), (%s::pg_catalog.int8), (%s::pg_catalog.int8)) q(v) ORDER BY v'''
            parameters = tuple(reversed(expected))
            oid, width = 20, 20
        with c.cursor(binary=False) as cur:
            cur.execute(sql, parameters, prepare=False)
            rows = cur.fetchall()
            oids = tuple(item.type_code for item in cur.description)
            formats = tuple(cur.pgresult.fformat(i) for i in range(2))
        need(oids == (oid, 25) and formats == (0, 0), 'DOMAIN_OID_FORMAT')
        need(len(rows) == len(expected), 'DOMAIN_ROW_COUNT')
        for (actual, text), wanted in zip(rows, expected):
            need(type(actual) is type(wanted) and actual == wanted, 'DOMAIN_NATIVE_VALUE_OR_ORDER')
            need(type(text) is str and text == str(wanted), 'DOMAIN_CANONICAL_TEXT')
        need(max(len(row[1]) for row in rows) == width, 'DOMAIN_TEXT_WIDTH')
        write('domain', {'case': case, 'oids': oids, 'formats': formats,
                         'texts': [row[1] for row in rows], 'maximum_ascii_characters': width})


@pytest.mark.parametrize('case,reverse,codec,count,metadata', FAMILIES, ids=[v[0] for v in FAMILIES])
def test_jsonb_state_families(case, reverse, codec, count, metadata):
    expanded, codecs = initial(reverse, codec, count, metadata)
    maximum = envelope(expanded, codecs, reverse)
    with connection(case) as c:
        bound = observe(c, case, 'envelope', maximum)
        for label, value in states(expanded, codecs, reverse):
            observed = observe(c, case, label, value)
            need(observed['canonical_bytes'] <= bound['canonical_bytes'], 'CANONICAL_ENVELOPE_UNDERESTIMATE')
            need(observed['native_bytes'] <= bound['native_bytes'], 'NATIVE_ENVELOPE_UNDERESTIMATE')


@pytest.mark.parametrize('case,basis,margin', BOUNDARIES, ids=[v[0] for v in BOUNDARIES])
def test_jsonb_full_size_edges(case, basis, margin):
    expanded, codecs = initial(False, 'uuid', 1)
    maximum = envelope(expanded, codecs, False)
    maximum['models'][TABLE]['schema'] = {'fill': ''}
    # Independently hand-derived from accepted literal 391-byte fixture:
    # replacing {} by {"fill":""} adds 9 bytes and one separator: 400 / 422.
    need(len(canonical(maximum)) == 400 and separators(maximum) == 22, 'BOUNDARY_FIXED_OVERHEAD')
    filler = LIMIT + margin - (400 if basis == 'canonical' else 422)
    maximum['models'][TABLE]['schema']['fill'] = 'x'*filler
    expected_canonical = LIMIT+margin if basis == 'canonical' else LIMIT+margin-22
    expected_native = expected_canonical+22
    aborted = {**maximum, 'phase': 'ABORTED'}
    with connection(case) as c:
        observed = observe(c, case, 'envelope', maximum)
        need(observed['canonical_bytes'] == expected_canonical, 'BOUNDARY_CANONICAL_BYTES')
        need(observed['native_bytes'] == expected_native, 'BOUNDARY_NATIVE_BYTES')
        terminal = observe(c, case, 'aborted', aborted)
        need(terminal['canonical_bytes'] == expected_canonical-3, 'BOUNDARY_ABORT_CANONICAL')
        need(terminal['native_bytes'] == expected_native-3, 'BOUNDARY_ABORT_NATIVE')
        need(observed['canonical_within_limit'] is (expected_canonical <= LIMIT), 'CANONICAL_GATE_CLASSIFICATION')
        need(observed['native_within_limit'] is (expected_native <= LIMIT), 'NATIVE_GATE_CLASSIFICATION')


@pytest.mark.parametrize('case,raw', REJECTIONS, ids=[v[0] for v in REJECTIONS])
def test_jsonb_unrepresentable_unicode(case, raw):
    with connection('reject_'+case) as c:
        code = None
        try:
            with c.cursor(binary=False) as cur:
                cur.execute(TEXT_SQL, (raw,), prepare=False)
                cur.fetchone()
        except psycopg.DataError as error:
            code = error.sqlstate
        write('rejection', {'case': case, 'sqlstate': code, 'raw_ascii_sha256': hashlib.sha256(raw.encode('ascii')).hexdigest()})
        need(type(code) is str and len(code) == 5 and code.startswith('22'), 'NATIVE_UNICODE_REJECTION_REQUIRED')


def test_native_reservation_omission_controls():
    case = 'omission_controls'
    expanded, codecs = initial(False, 'uuid', 10**16)
    correct = envelope(expanded, codecs, False)
    # Independent complete ABORTED input. Use one-row chunks, so the source
    # permits the 17-digit rows and chunks widths independently of E's builder.
    actual = {'phase': 'ABORTED', 'models': {TABLE: {
        'scope': {'count': 10**16, 'membership': '0'*64},
        'cursor': UUID_MAX, 'rows': 10**16, 'chunks': 10**16,
        'schema': {}, 'guard': ['A']}}, 'verification': {TABLE: 'f'*64}}
    with connection(case) as c:
        good = observe(c, case, 'correct_envelope', correct)
        terminal = observe(c, case, 'independent_abort', actual)
        need(terminal['native_bytes'] <= good['native_bytes'], 'POSITIVE_BOUND_FAILED')
        killed = []
        for omission in ('verification', 'cursor', 'counters'):
            faulty = copy.deepcopy(correct)
            if omission == 'verification':
                del faulty['verification']
            elif omission == 'cursor':
                faulty['models'][TABLE]['cursor'] = None
            else:
                faulty['models'][TABLE].update(rows=0, chunks=0)
            measured = observe(c, case, 'omit_'+omission, faulty)
            need(terminal['canonical_bytes'] > measured['canonical_bytes'], 'CANONICAL_OMISSION_NOT_DETECTED')
            need(terminal['native_bytes'] > measured['native_bytes'], 'NATIVE_OMISSION_NOT_DETECTED')
            killed.append(omission)
        write('omission', {'case': case, 'killed': killed, 'status': 'THREE_INDEPENDENT_SIZE_UNDERESTIMATES_DETECTED'})
