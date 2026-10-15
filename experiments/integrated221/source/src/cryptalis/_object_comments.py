"""Opt-in research restoration contract; the compiler lock is unchanged.

Only affected original UNIQUE constraints, standalone indexes and their backing
indexes are covered. Legacy artifacts are explicitly NOT_INVENTORIED.
"""
from copy import deepcopy
import hashlib
import math
from uuid import UUID

from psycopg import sql
from .manifest.compiler import _canonical
from .manifest.parser import MAX_DOCUMENT_BYTES

FORWARD = 'cryptalis.transition/retained-native-comments-research-v1'
REVERSE = 'cryptalis.reverse/retained-native-comments-research-v1'
CLUSTER_FORWARD = 'cryptalis.transition/retained-native-comments-cluster-research-v2'
CLUSTER_REVERSE = 'cryptalis.reverse/retained-native-comments-cluster-research-v2'
LEGACY_FORWARD = 'cryptalis.transition/retained-native-research-v0'
LEGACY_REVERSE = 'cryptalis.reverse/retained-native-research-v0'
INVENTORY = 'cryptalis.object-comments/research-v1'
ACTIVE_SCHEMA_BYTES = 4 * 1024 * 1024
HISTORY_BYTES = READINESS_BYTES = 1024 * 1024
REVERSE_LIMITS = 'Staging/DDL/publication delays excluded; plaintext enters WAL and backups.'
FORWARD_KEYS = frozenset(('format', 'kind', 'operation_id', 'target_id', 'target',
    'runtime_role', 'journal_schema', 'lock', 'source_lock_digest', 'key_policies',
    'scopes', 'estimates', 'object_comments'))
COUNTERS = ('rows', 'writer_pause_seconds_estimate', 'temporary_bytes_estimate', 'wal_bytes_estimate')
RATES = ('backfill_rows_per_second', 'verify_rows_per_second')


class ContractError(ValueError):
    """Safe code only; never retain artifact or comment text in errors."""
    def __init__(self, code='invalid_object_comment_contract'):
        self.code = code
        super().__init__(code)


def _require(condition):
    if not condition:
        raise ContractError()


def _stop(code, operation_id=None):
    from .migration import TransitionFailure
    raise TransitionFailure(code, operation_id)


def enabled(document):
    return document.get('format') in (FORWARD, CLUSTER_FORWARD)


def reverse_format(document):
    if document.get('format') == CLUSTER_FORWARD:
        return CLUSTER_REVERSE
    return REVERSE if enabled(document) else LEGACY_REVERSE


def status(document):
    if document.get('format') in (REVERSE, CLUSTER_REVERSE):
        document = document['source_plan']
    return 'INVENTORIED' if enabled(document) else 'NOT_INVENTORIED'


def _uuid(value):
    _require(type(value) is str and bool(UUID(value).int) and value == str(UUID(value)))


def _targets(model):
    constraints = {item['name'] for f in model['fields'] for item in f['original']['constraints']}
    standalone = {item['name'] for f in model['fields'] for item in f['original']['indexes']}
    indexes = {item['name']: item['constraint_name'] for item in model['source_schema']['indexes']
               if item['name'] in standalone or item['constraint_name'] in constraints}
    _require(standalone <= indexes.keys())
    _require({name for name in indexes.values() if name is not None} == constraints)
    _require(all(indexes[name] is None for name in standalone))
    return sorted(constraints), dict(sorted(indexes.items()))


def validate_inventory(document):
    inventory = document['object_comments']
    _require(type(inventory) is dict and set(inventory) == {'schema', 'tables'})
    _require(inventory['schema'] == INVENTORY and type(inventory['tables']) is list)
    models = document['lock']['models']
    _require(len(inventory['tables']) == len(models))
    for model, table in zip(models, inventory['tables'], strict=True):
        _require(type(table) is dict and set(table) == {'table_id', 'constraints', 'indexes'})
        _require(table['table_id'] == model['table_id'])
        _uuid(table['table_id'])
        constraints, indexes = _targets(model)
        for kind, names, members in (('constraints', constraints, {'name', 'comment'}),
                                     ('indexes', list(indexes), {'name', 'constraint_name', 'comment'})):
            entries = table[kind]
            _require(type(entries) is list and len(entries) == len(names))
            for name, entry in zip(names, entries, strict=True):
                _require(type(entry) is dict and set(entry) == members and entry['name'] == name)
                _require(type(entry['name']) is str)
                _require(entry['comment'] is None or type(entry['comment']) is str)
                if kind == 'indexes':
                    _require(entry['constraint_name'] is None or type(entry['constraint_name']) is str)
                    _require(entry['constraint_name'] == indexes[name])


def _size(value, code):
    try:
        return len(_canonical(value))
    except ValueError:
        raise ContractError(code) from None


def _within(value, limit, code):
    if _size(value, code) > limit:
        raise ContractError(code)


def reverse_envelope_bound(source):
    """Exact fixed skeleton plus independently enforced variable reservations."""
    maximum = 2**53 - 1
    try:
        source_digest = hashlib.sha256(_canonical(source)).hexdigest()
    except ValueError:
        raise ContractError('object_comments_reverse_envelope_exceeded') from None
    skeleton = {
        'format': reverse_format(source), 'kind': 'deprotect', 'operation_id': str(UUID(int=2)),
        'target_id': source['target_id'], 'source_plan': source,
        'source_pin': {'target_id': source['target_id'], 'operation_id': source['operation_id'],
                       'plan_digest': source_digest, 'phase': 'ACTIVE'},
        'lock': source['lock'], 'target': source['target'], 'runtime_role': source['runtime_role'],
        'journal_schema': source['journal_schema'], 'key_policies': source['key_policies'],
        'active_schemas': {}, 'retirable_aborted': [], 'cutover_readiness': {},
        'plaintext_runtime_role': 'x',
        'estimates': {**{name: maximum for name in COUNTERS},
                      **{name: 1 for name in RATES}, 'limits': REVERSE_LIMITS},
    }
    size = _size(skeleton, 'object_comments_reverse_envelope_exceeded')
    return (size + ACTIVE_SCHEMA_BYTES - 2 + HISTORY_BYTES - 2 + READINESS_BYTES - 2
            + 6 * 63 - 1 + 2 * (32 - 1))


def validate_forward(document):
    clustered = document.get('format') == CLUSTER_FORWARD
    keys = FORWARD_KEYS | {'cluster_designation'} if clustered else FORWARD_KEYS
    _require(set(document) == keys and enabled(document)
             and document['kind'] == 'protect')
    for name in ('operation_id', 'target_id'):
        _uuid(document[name])
    _require(type(document['key_policies']) is dict)
    for tenant, fingerprint in document['key_policies'].items():
        _uuid(tenant)
        _require(type(fingerprint) is str and len(fingerprint) == 64
                 and all(character in '0123456789abcdef' for character in fingerprint))
    validate_inventory(document)
    if clustered:
        from . import _cluster_designation
        _cluster_designation.validate(document)
    if reverse_envelope_bound(document) > MAX_DOCUMENT_BYTES:
        raise ContractError('object_comments_reverse_envelope_exceeded')


def validate_reverse(document):
    source = document['source_plan']
    _require(document['format'] == reverse_format(source) and enabled(source))
    # Python equality admits bool/int aliases with different encoded widths.
    # The envelope proof requires the duplicated bytes to be exactly equal.
    for name in ('lock', 'target', 'runtime_role', 'journal_schema'):
        _require(_canonical(document[name]) == _canonical(source[name]))
    for name in ('operation_id', 'target_id'):
        _uuid(document[name])
        _uuid(document['source_pin'][name])
    for item in document['retirable_aborted']:
        _uuid(item['operation_id'])
    role = document['plaintext_runtime_role']
    _require(type(role) is str and bool(role) and '\x00' not in role and len(role.encode('utf-8')) <= 63)
    policies = document['key_policies']
    _require(type(policies) is dict and policies.keys() <= source['key_policies'].keys()
             and all(_canonical(value) == _canonical(source['key_policies'][key])
                     for key, value in policies.items()))
    estimates = document['estimates']
    _require(type(estimates) is dict and set(estimates) == set(COUNTERS + RATES + ('limits',)))
    _require(estimates['limits'] == REVERSE_LIMITS)
    _require(all(type(estimates[name]) is int and 0 <= estimates[name] < 2**53 for name in COUNTERS))
    for name in RATES:
        rate = estimates[name]
        _require(type(rate) in (int, float) and math.isfinite(rate) and rate > 0)
        _within(rate, 32, 'object_comments_rate_budget_exceeded')
    for name, kind, limit, code in (
        ('active_schemas', dict, ACTIVE_SCHEMA_BYTES, 'object_comments_schema_budget_exceeded'),
        ('retirable_aborted', list, HISTORY_BYTES, 'object_comments_history_budget_exceeded'),
        ('cutover_readiness', dict, READINESS_BYTES, 'object_comments_readiness_budget_exceeded'),
    ):
        _require(type(document[name]) is kind)
        _within(document[name], limit, code)


def capture(connection, lock, operation_id=None):
    """Native catalog identity and independent constraint/backing-index linkage."""
    result = {'schema': INVENTORY, 'tables': []}
    for model in lock['models']:
        constraints, indexes = _targets(model)
        table_oid = connection.exec_driver_sql('''SELECT t.oid FROM pg_catalog.pg_class t
            JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace
            WHERE n.nspname=%s AND t.relname=%s''', (model['schema'], model['table'])).scalar_one_or_none()
        if table_oid is None:
            _stop('object_comment_target_changed', operation_id)
        cons = {row[0]: row for row in connection.exec_driver_sql('''
            SELECT conname, conindid, contype, pg_catalog.obj_description(oid,'pg_constraint')
            FROM pg_catalog.pg_constraint WHERE conrelid=%s''', (table_oid,))}
        observed = {row[0]: row for row in connection.exec_driver_sql('''
            SELECT ix.relname, i.indexrelid, co.conname,
                   pg_catalog.obj_description(i.indexrelid,'pg_class')
            FROM pg_catalog.pg_index i JOIN pg_catalog.pg_class ix ON ix.oid=i.indexrelid
            LEFT JOIN pg_catalog.pg_constraint co ON co.conindid=i.indexrelid AND co.contype IN ('p','u','x')
            WHERE i.indrelid=%s''', (table_oid,))}
        table = {'table_id': model['table_id'], 'constraints': [], 'indexes': []}
        for name in constraints:
            if name not in cons or cons[name][2] != 'u':
                _stop('object_comment_target_changed', operation_id)
            table['constraints'].append({'name': name, 'comment': cons[name][3]})
        for name, constraint in indexes.items():
            row = observed.get(name)
            if row is None or row[2] != constraint or (constraint is not None and cons[constraint][1] != row[1]):
                _stop('object_comment_target_changed', operation_id)
            table['indexes'].append({'name': name, 'constraint_name': constraint, 'comment': row[3]})
        result['tables'].append(table)
    return result


def check(connection, source, operation_id=None):
    if enabled(source) and capture(connection, source['lock'], operation_id) != source['object_comments']:
        _stop('object_comments_changed', operation_id)


def restore(connection, source, operation_id=None):
    if not enabled(source):
        return
    # Check object identity/linkage before any COMMENT; current comment values
    # are expected to differ because these objects were just recreated.
    capture(connection, source['lock'], operation_id)
    for model, table in zip(source['lock']['models'], source['object_comments']['tables'], strict=True):
        for item in table['constraints']:
            statement = sql.SQL('COMMENT ON CONSTRAINT {} ON {} IS {}').format(
                sql.Identifier(item['name']), sql.Identifier(model['schema'], model['table']), sql.Literal(item['comment']))
            connection.exec_driver_sql(statement.as_string(connection.connection.driver_connection))
        for item in table['indexes']:
            statement = sql.SQL('COMMENT ON INDEX {} IS {}').format(
                sql.Identifier(model['schema'], item['name']), sql.Literal(item['comment']))
            connection.exec_driver_sql(statement.as_string(connection.connection.driver_connection))


def schema_reservation(document, schemas):
    """Size-only upper copy; never replace observed journal catalog facts."""
    reserved = deepcopy(schemas)
    for model in document['lock']['models']:
        facts = reserved[model['table_id']]
        columns = {column['name']: column for column in facts['columns']}
        for field in model['fields']:
            if not field['source']['nullable']:
                columns[field['column']]['default_digest'] = '0' * 64
                columns[field['payload_column']]['nullable'] = False
                facts['dependencies'].extend([
                    {'column': field['column'], 'kind': 'pg_catalog.pg_attrdef'},
                    {'column': None, 'kind': 'pg_catalog.pg_attrdef'},
                ])
        facts['relation']['user_triggers'] = False
    return reserved


def check_schema_budget(document, schemas, operation_id=None, *, expanded=False):
    if not enabled(document):
        return
    if expanded:
        schemas = schema_reservation(document, schemas)
    try:
        _within(schemas, ACTIVE_SCHEMA_BYTES, 'object_comments_schema_budget_exceeded')
    except ContractError as exc:
        _stop(exc.code, operation_id)
