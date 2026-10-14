"""Independent stdlib byte oracle for the reviewed comments-v1 envelope design.

This is synthetic arithmetic and artifact-shape evidence, never compiler or
catalog admission. It imports no Cryptalis, test framework, database or driver.
"""
from copy import deepcopy
import hashlib
import json
import math
from uuid import UUID

MAX_BYTES = 16 * 1024 * 1024
SECTION_CAPS = {'active_schemas': 4 * 1024 * 1024,
                'retirable_aborted': 1024 * 1024,
                'cutover_readiness': 1024 * 1024}
FORWARD_FORMAT = 'cryptalis.transition/retained-native-comments-research-v1'
REVERSE_FORMAT = 'cryptalis.reverse/retained-native-comments-research-v1'
INVENTORY_FORMAT = 'cryptalis.object-comments/research-v1'
LIMITS_TEXT = 'Staging/DDL/publication delays excluded; plaintext enters WAL and backups.'
COUNTER_NAMES = ('rows', 'writer_pause_seconds_estimate',
                 'temporary_bytes_estimate', 'wal_bytes_estimate')
RATE_NAMES = ('backfill_rows_per_second', 'verify_rows_per_second')
SOURCE_OPERATION = 'abcdef01-2345-6789-abcd-ef0123456789'
TARGET_ID = 'abcdef02-2345-6789-abcd-ef0123456789'
TABLE_ID = 'abcdef03-2345-6789-abcd-ef0123456789'
REVERSE_OPERATION = 'abcdef04-2345-6789-abcd-ef0123456789'
TENANT_ID = 'abcdef05-2345-6789-abcd-ef0123456789'
OTHER_TENANT = 'abcdef06-2345-6789-abcd-ef0123456789'
ESCAPING_PREFIX = '雪😀e\u0301 "quoted" \\literal\\u96ea \x01\n\t'


def canonical_bytes(value):
    """No product canonicalizer and no cap: measure actual UTF-8 JSON bytes."""
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf8')


def byte_size(value):
    return len(canonical_bytes(value))


def canonical_uuid(value):
    if type(value) is not str:
        return False
    try:
        parsed = UUID(value)
    except (ValueError, AttributeError):
        return False
    return parsed.int != 0 and value == str(parsed)


def valid_counter(value):
    return type(value) is int and 0 <= value <= 2**53 - 1


def valid_rate(value):
    # Full-artifact integer grammar also bounds integer-valued rates.
    return (type(value) in (int, float) and math.isfinite(value) and value > 0
            and (type(value) is not int or valid_counter(value))
            and byte_size(value) <= 32)


def valid_role(value):
    if type(value) is not str or not value or '\x00' in value:
        return False
    try:
        return len(value.encode('utf8')) <= 63
    except UnicodeEncodeError:
        return False


def source_fixture(comment=ESCAPING_PREFIX):
    """Complete top-level fixture, deliberately synthetic inner lock/schema.

    It is adequate to isolate artifact parser and helper arithmetic boundaries;
    it does not claim compiler-admitted mappings or native PostgreSQL facts.
    """
    model = {
        'table_id': TABLE_ID, 'schema': 'fixture_schema', 'table': 'fixture_customer',
        'fields': [{'column': 'name', 'payload_column': '_fixture_payload',
                    'source': {'nullable': True},
                    'original': {'constraints': [{'name': 'name_unique'}],
                                 'indexes': [{'name': 'name_lookup'}]}}],
        'source_schema': {'indexes': [
            {'name': 'name_lookup', 'constraint_name': None},
            {'name': 'name_unique', 'constraint_name': 'name_unique'}]},
    }
    return {
        'format': FORWARD_FORMAT, 'kind': 'protect',
        'operation_id': SOURCE_OPERATION, 'target_id': TARGET_ID,
        'target': ['synthetic_database', '12345', '127.0.0.1', 5432, 'fixture_owner'],
        'runtime_role': 'protected_fixture', 'journal_schema': 'fixture_schema',
        'lock': {'schema': 'cryptalis.lock/v1', 'profile': 'cf1',
                 'domain_id': str(UUID(int=31)), 'declaration': {}, 'models': [model]},
        'source_lock_digest': None,
        'key_policies': {TENANT_ID: 'a' * 64, OTHER_TENANT: 'b' * 64},
        'scopes': [{'table_id': TABLE_ID, 'estimated_rows': 0}],
        'estimates': {'rows': 0, 'plaintext_bytes': 0,
                      'backfill_rows_per_second': 1.0,
                      'verify_rows_per_second': 1.0,
                      'writer_pause_seconds_estimate': 0, 'limits': 'synthetic'},
        'object_comments': {'schema': INVENTORY_FORMAT, 'tables': [{
            'table_id': TABLE_ID,
            'constraints': [{'name': 'name_unique', 'comment': None}],
            'indexes': [
                {'name': 'name_lookup', 'constraint_name': None, 'comment': comment},
                {'name': 'name_unique', 'constraint_name': 'name_unique', 'comment': None}],
        }]},
    }


def reverse_skeleton(source):
    """Construct all serialized fields independently from the design text."""
    source_digest = hashlib.sha256(canonical_bytes(source)).hexdigest()
    return {
        'format': REVERSE_FORMAT, 'kind': 'deprotect',
        'operation_id': REVERSE_OPERATION, 'target_id': source['target_id'],
        'source_plan': deepcopy(source),
        'source_pin': {'target_id': source['target_id'],
                       'operation_id': source['operation_id'],
                       'plan_digest': source_digest, 'phase': 'ACTIVE'},
        'lock': deepcopy(source['lock']), 'target': deepcopy(source['target']),
        'runtime_role': source['runtime_role'], 'journal_schema': source['journal_schema'],
        'key_policies': deepcopy(source['key_policies']),
        'active_schemas': {}, 'retirable_aborted': [], 'cutover_readiness': {},
        'plaintext_runtime_role': 'x',
        'estimates': {**{name: 2**53 - 1 for name in COUNTER_NAMES},
                      **{name: 1 for name in RATE_NAMES}, 'limits': LIMITS_TEXT},
    }


def envelope_measurements(source):
    skeleton = reverse_skeleton(source)
    size = byte_size(skeleton)
    replacements = {name: cap - byte_size(skeleton[name])
                    for name, cap in SECTION_CAPS.items()}
    # Role placeholder content has one byte; its two JSON quotes stay in S.
    replacements['role'] = (6 * 63 + 2) - byte_size(skeleton['plaintext_runtime_role'])
    replacements['rates'] = sum(32 - byte_size(skeleton['estimates'][name])
                                for name in RATE_NAMES)
    return {'source_bytes': byte_size(source), 'skeleton_bytes': size,
            'replacement_bytes': replacements, 'bound_bytes': size + sum(replacements.values())}


def reverse_fixture(source=None):
    result = reverse_skeleton(source if source is not None else source_fixture())
    result['plaintext_runtime_role'] = 'plaintext_fixture'
    result['active_schemas'] = {TABLE_ID: {'synthetic_catalog_payload': ''}}
    return result


def calibrated_source_bound(target_bytes, prefix=ESCAPING_PREFIX):
    """Pad exactly one comment, so source/B increase one byte per ASCII char."""
    source = source_fixture(prefix)
    missing = target_bytes - envelope_measurements(source)['bound_bytes']
    if missing < 0:
        raise ValueError('target smaller than fixture overhead')
    source['object_comments']['tables'][0]['indexes'][0]['comment'] += 'p' * missing
    actual = envelope_measurements(source)
    if actual['bound_bytes'] != target_bytes:
        raise AssertionError('independent byte calibration failed')
    return source


def section_at_size(name, target_bytes):
    """Exact size-layer containers, not full catalog/history admission.

    The padded history item deliberately has an extra field. Complete reverse
    readers MUST reject it even when the size-only helper accepts its size.
    """
    if name == 'active_schemas':
        value = {TABLE_ID: {'synthetic_catalog_payload': ''}}
        holder, member = value[TABLE_ID], 'synthetic_catalog_payload'
    elif name == 'retirable_aborted':
        value = [{'operation_id': str(UUID(int=100)), 'plan_digest': 'c' * 64,
                  'size_layer_padding': ''}]
        holder, member = value[0], 'size_layer_padding'
    elif name == 'cutover_readiness':
        value = {'synthetic_findings': ''}
        holder, member = value, 'synthetic_findings'
    else:
        raise ValueError('unknown section')
    missing = target_bytes - byte_size(value)
    if missing < 0:
        raise ValueError('target smaller than container overhead')
    holder[member] = 'p' * missing
    if byte_size(value) != target_bytes:
        raise AssertionError('independent section calibration failed')
    return value


def maximal_valid_history():
    """Nearest <=H list using exact entry keys and fixed-width UUID/digest."""
    template = {'operation_id': str(UUID(int=100)), 'plan_digest': 'c' * 64}
    entry_bytes = byte_size(template)
    # For n>0: '[' + entries + commas + ']' = 1 + n*(entry_bytes+1).
    count = (SECTION_CAPS['retirable_aborted'] - 1) // (entry_bytes + 1)
    entries = [{'operation_id': str(UUID(int=100+i)), 'plan_digest': 'c' * 64}
               for i in range(count)]
    size = byte_size(entries)
    if size > SECTION_CAPS['retirable_aborted'] or size + entry_bytes + 1 <= SECTION_CAPS['retirable_aborted']:
        raise AssertionError('history nearest-bound calculation failed')
    return entries


def actual_reserved_reverse(source):
    """Actual serialized envelope using valid scalar/history types near caps."""
    result = reverse_fixture(source)
    result['active_schemas'] = section_at_size('active_schemas', SECTION_CAPS['active_schemas'])
    result['retirable_aborted'] = maximal_valid_history()
    result['cutover_readiness'] = section_at_size('cutover_readiness', SECTION_CAPS['cutover_readiness'])
    # 63 non-NUL control code points attain six JSON bytes per UTF-8 byte.
    result['plaintext_runtime_role'] = '\x01' * 63
    for name in RATE_NAMES:
        result['estimates'][name] = float.fromhex('0x1.fffffffffffffp+1023')
    return result
