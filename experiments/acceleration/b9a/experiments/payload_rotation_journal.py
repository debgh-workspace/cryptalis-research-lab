"""B9A test-local durable preparation. Never publishes or changes active policy.

One externally supplied, bounded artifact and one additional canonical journal
row bind an inactive stage. Hashes record evidence, not host authority. The host
must keep writers stopped between transactions and supply current authority on
EVERY entry. Only the explicit __main__ research command imports fixture code.
"""
from contextlib import contextmanager
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from uuid import UUID, uuid4

from cryptalis import migration as migration
from cryptalis.crypto.cf1 import FieldDescriptor, open_text
from cryptalis.crypto.keys import KeyUnavailable
from cryptalis.crypto._payload_rotation import _binding, prepare_payload_rotation_batch

SCHEMA = 'cryptalis.experiment.inactive-payload-preparation/v1'
KIND = 'INACTIVE_PAYLOAD_PREPARATION'
MAX_ROWS = 64
MAX_SOURCE_BYTES = 4 * 1024 * 1024
MAX_DOCUMENT_BYTES = 1024 * 1024
MAX_STATE_BYTES = 256 * 1024
_STATE_FIELDS = {'schema', 'kind', 'source_operation_id', 'source_plan_digest',
                 'artifact_digest', 'phase', 'source_revision', 'batches', 'verification'}
_BATCH_FIELDS = {'ordinal', 'cursor_before', 'cursor_after', 'rows',
                 'target_commitment', 'row_count', 'logical_bytes'}
_ARTIFACT_FIELDS = {'schema', 'kind', 'operation_id', 'source_operation_id',
    'source_plan_digest', 'target_id', 'target', 'models', 'stage', 'journal',
    'source', 'descriptor', 'descriptor_digest', 'tenant_id', 'source_pin_digest',
    'source_journal_digest', 'source_policy', 'target_policy', 'source_revision',
    'catalog_digest', 'inventory', 'bounds', 'maintenance_digest', 'revisions'}


class PreparationFailure(migration.TransitionFailure):
    """Typed sanitized refusal. Preserve the original operation for inspection."""
    stage = 'inactive preparation'


@dataclass(frozen=True)
class Result:
    status: str
    code: str
    committed_rows: int = 0
    committed_batches: int = 0


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def _digest(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


def _fail(code):
    raise PreparationFailure(code)


def _sanitized(exc, operation_id=None):
    if isinstance(exc, migration.TransitionFailure):
        return PreparationFailure(exc.code, operation_id or exc.operation_id, exc.sqlstate,
                                  cleanup_errors=exc.cleanup_errors)
    return PreparationFailure('binding_expired' if isinstance(exc, KeyUnavailable)
                              else 'preparation_refused', operation_id)


def _hex(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def _uuid(value):
    return type(value) is str and str(UUID(value)) == value


def _members(value, expected):
    if type(value) is not dict or set(value) != expected:
        _fail('invalid_artifact')


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            _fail('invalid_artifact')
        result[key] = value
    return result


def _decode(raw):
    if type(raw) is not bytes or len(raw) > MAX_DOCUMENT_BYTES:
        _fail('invalid_artifact')
    doc = json.loads(raw, object_pairs_hook=_pairs,
                     parse_constant=lambda _: _fail('invalid_artifact'))
    def visit(value, depth=0):
        if depth > 24:
            _fail('invalid_artifact')
        if type(value) is dict:
            if len(value) > 256:
                _fail('invalid_artifact')
            for key, member in value.items():
                if type(key) is not str or len(key) > 512:
                    _fail('invalid_artifact')
                visit(member, depth + 1)
        elif type(value) is list:
            if len(value) > 256:
                _fail('invalid_artifact')
            for member in value:
                visit(member, depth + 1)
        elif type(value) not in (str, int, bool, type(None)):
            _fail('invalid_artifact')
        elif type(value) is str and (len(value) > 8192 or '\x00' in value):
            _fail('invalid_artifact')
        elif type(value) is int and not -(2**63) <= value < 2**63:
            _fail('invalid_artifact')
    visit(doc)
    return doc


def _name(value):
    if type(value) is not str or not value or '\x00' in value or len(value.encode()) > 63:
        _fail('invalid_artifact')
    return '"' + value.replace('"', '""') + '"'


def _qualified(schema, table):
    return _name(schema) + '.' + _name(table)


def _revision_valid(value):
    _members(value, {'row_count', 'membership', 'content'})
    if (type(value['row_count']) is not int or not 0 <= value['row_count'] <= MAX_ROWS
            or not _hex(value['membership']) or not _hex(value['content'])):
        _fail('invalid_artifact')


@dataclass(frozen=True, repr=False)
class Artifact:
    canonical_bytes: bytes

    def __post_init__(self):
        try:
            d = _decode(self.canonical_bytes)
            _members(d, _ARTIFACT_FIELDS)
            if _canonical(d) != self.canonical_bytes or d['schema'] != SCHEMA or d['kind'] != KIND:
                _fail('invalid_artifact')
            for key in ('operation_id', 'source_operation_id', 'target_id', 'tenant_id'):
                if not _uuid(d[key]) or (key != 'tenant_id' and UUID(d[key]).int == 0):
                    _fail('invalid_artifact')
            if d['operation_id'] == d['source_operation_id']:
                _fail('invalid_artifact')
            for key in ('source_plan_digest', 'descriptor_digest', 'source_pin_digest',
                        'source_journal_digest', 'source_policy', 'target_policy',
                        'catalog_digest', 'maintenance_digest'):
                if not _hex(d[key]):
                    _fail('invalid_artifact')
            for key in ('source', 'stage', 'journal'):
                _members(d[key], {'schema', 'table', 'qualified_name', 'oid'})
                relation = d[key]
                if (relation['qualified_name'] != _qualified(relation['schema'], relation['table'])
                        or type(relation['oid']) is not int or relation['oid'] <= 0):
                    _fail('invalid_artifact')
            if len({d[k]['qualified_name'] for k in ('source', 'stage', 'journal')}) != 3:
                _fail('invalid_artifact')
            if (d['journal']['table'] != migration.JOURNAL or
                    len({d[k]['schema'] for k in ('source', 'stage', 'journal')}) != 1):
                _fail('invalid_artifact')
            if d['models'] != [[d['source']['schema'], d['source']['table']]]:
                _fail('invalid_artifact')
            field = FieldDescriptor.from_compiled(d['descriptor'], d['descriptor_digest'])
            if not field.equality or field.record_codec != 'uuid16/v1' or field.tenant_codec != 'uuid16/v1':
                _fail('unsupported_profile')
            if (type(d['target']) is not list or len(d['target']) != 5 or
                    type(d['target'][0]) is not str or type(d['target'][-1]) is not str):
                _fail('invalid_artifact')
            _members(d['bounds'], {'max_rows', 'max_bytes', 'source_rows', 'source_bytes'})
            b = d['bounds']
            if (any(type(v) is not int for v in b.values()) or not 1 <= b['max_rows'] <= MAX_ROWS
                    or not 1 <= b['max_bytes'] <= MAX_SOURCE_BYTES * 3 + MAX_ROWS * 32
                    or b['source_rows'] != MAX_ROWS or b['source_bytes'] != MAX_SOURCE_BYTES):
                _fail('invalid_artifact')
            _revision_valid(d['source_revision'])
            if (type(d['revisions']) is not dict or not d['revisions'] or
                    any(not _hex(v) for v in d['revisions'].values()) or
                    type(d['inventory']) is not list or not d['inventory']):
                _fail('invalid_artifact')
        except Exception:
            raise PreparationFailure('invalid_artifact') from None

    @property
    def document(self):
        return json.loads(self.canonical_bytes)

    @property
    def digest(self):
        return hashlib.sha256(self.canonical_bytes).hexdigest()

    @property
    def operation_id(self):
        return UUID(self.document['operation_id'])


def _revisions():
    root = Path(__file__).resolve().parents[1]
    if Path(migration.__file__).resolve() != root / 'src' / 'cryptalis' / 'migration.py':
        _fail('implementation_origin_changed')
    files = sorted((root / 'src' / 'cryptalis').rglob('*.py')) + [Path(__file__).resolve()]
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}


def _pin(pin):
    return {k: str(v) if isinstance(v, UUID) else v for k, v in asdict(pin).items()}


def _authority(plan, pin, source, target, maintenance, tenant):
    migration._admit(plan, pin)
    migration._approve_maintenance(plan, maintenance)
    if pin.phase != 'ACTIVE':
        _fail('source_authority_changed')
    models = plan.document['lock']['models']
    if len(models) != 1 or len(models[0]['fields']) != 1 or 'column' not in models[0]['tenancy']:
        _fail('unsupported_profile')
    model, field_doc = models[0], models[0]['fields'][0]
    field = FieldDescriptor.from_compiled(field_doc['descriptor'], field_doc['descriptor_digest'])
    if not field.equality or field.record_codec != 'uuid16/v1' or field.tenant_codec != 'uuid16/v1':
        _fail('unsupported_profile')
    migration._ring(source, tenant, plan)
    if (source.policy.payload_generation != 1 or target.policy.payload_generation != 2 or
            target.policy.tenant_id != tenant or target.policy.domain_id != field.domain_id or
            source.policy.search_generation != target.policy.search_generation):
        _fail('source_authority_changed')
    # Wrapper identity is host policy, not an inference from ciphertext headers.
    def search(ring):
        return tuple(w for w in ring.policy.wrappers if w.context.purpose == 'search')
    if search(source) != search(target):
        _fail('source_authority_changed')
    return model, field


@contextmanager
def _session(engine, plan, operation_id=None):
    if engine.echo or not engine.hide_parameters:
        _fail('unsafe_engine_logging')
    try:
        migration._previous_lock(plan.lock_bytes, plan.document['lock'], engine)
    except Exception:
        raise PreparationFailure('invalid_source_lock') from None
    with migration._connection(engine, operation_id or plan.operation_id, exclusive=True) as c:
        c.exec_driver_sql("SET lock_timeout = '5s'")
        c.exec_driver_sql("SET statement_timeout = '15s'")
        c.exec_driver_sql('SET synchronous_commit = on')
        if migration._target(c) != plan.document['target']:
            _fail('source_authority_changed')
        models = plan.document['lock']['models']
        scope = int.from_bytes(hashlib.sha256(_canonical([(m['schema'], m['table']) for m in models])).digest()[:8], 'big', signed=True)
        acquired = c.exec_driver_sql('SELECT pg_catalog.pg_try_advisory_lock(%s)', (scope,)).scalar_one()
        c.commit()
        yield c, acquired


def _lock(c, model):
    c.exec_driver_sql('LOCK TABLE ' + migration._table(c, model) + ' IN EXCLUSIVE MODE')
    c.exec_driver_sql('SET LOCAL search_path = pg_catalog')


def _relation(c, schema, table):
    q = _qualified(schema, table)
    oid = c.exec_driver_sql('SELECT pg_catalog.to_regclass(%s)::oid', (q,)).scalar_one()
    if oid is None:
        _fail('catalog_changed')
    return {'schema': schema, 'table': table, 'qualified_name': q, 'oid': oid}


def _catalog(c, plan, stage):
    """Bound relevant definitions, ACLs, ownership and complete schema inventory."""
    schema = stage['schema']
    inventory = [list(r) for r in c.exec_driver_sql('''SELECT c.oid,c.relname,c.relkind,
        c.relowner,c.relacl::text,c.relpersistence,c.relrowsecurity,c.relforcerowsecurity,
        c.relhasrules FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n
        ON n.oid=c.relnamespace WHERE n.nspname=%s ORDER BY c.oid''', (schema,)).all()]
    columns = [list(r) for r in c.exec_driver_sql('''SELECT a.attrelid,a.attnum,a.attname,
        a.atttypid,a.atttypmod,a.attcollation,a.attnotnull,a.attidentity,a.attgenerated,
        a.attacl::text,pg_catalog.pg_get_expr(d.adbin,d.adrelid)
        FROM pg_catalog.pg_attribute a JOIN pg_catalog.pg_class c ON c.oid=a.attrelid
        JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
        LEFT JOIN pg_catalog.pg_attrdef d ON d.adrelid=a.attrelid AND d.adnum=a.attnum
        WHERE n.nspname=%s AND a.attnum>0 AND NOT a.attisdropped ORDER BY a.attrelid,a.attnum''', (schema,)).all()]
    constraints = [list(r) for r in c.exec_driver_sql('''SELECT co.oid,co.conrelid,co.contype,
        co.convalidated,co.condeferrable,co.condeferred,pg_catalog.pg_get_constraintdef(co.oid)
        FROM pg_catalog.pg_constraint co JOIN pg_catalog.pg_namespace n ON n.oid=co.connamespace
        WHERE n.nspname=%s ORDER BY co.oid''', (schema,)).all()]
    indexes = [list(r) for r in c.exec_driver_sql('''SELECT i.indexrelid,i.indrelid,
        i.indisvalid,i.indisready,pg_catalog.pg_get_indexdef(i.indexrelid)
        FROM pg_catalog.pg_index i JOIN pg_catalog.pg_class c ON c.oid=i.indrelid
        JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname=%s ORDER BY i.indexrelid''', (schema,)).all()]
    triggers = [list(r) for r in c.exec_driver_sql('''SELECT t.oid,t.tgrelid,t.tgenabled,
        pg_catalog.pg_get_triggerdef(t.oid) FROM pg_catalog.pg_trigger t
        JOIN pg_catalog.pg_class c ON c.oid=t.tgrelid JOIN pg_catalog.pg_namespace n
        ON n.oid=c.relnamespace WHERE n.nspname=%s ORDER BY t.oid''', (schema,)).all()]
    defaults = [list(r) for r in c.exec_driver_sql('''SELECT d.defaclrole,d.defaclnamespace,
        d.defaclobjtype,d.defaclacl::text FROM pg_catalog.pg_default_acl d
        WHERE d.defaclnamespace=0 OR d.defaclnamespace=(SELECT oid FROM pg_catalog.pg_namespace
        WHERE nspname=%s) ORDER BY d.oid''', (schema,)).all()]
    namespace = list(c.exec_driver_sql('''SELECT oid,nspowner,nspacl::text
        FROM pg_catalog.pg_namespace WHERE nspname=%s''', (schema,)).one())
    return inventory, _digest([inventory, columns, constraints, indexes, triggers, defaults, namespace])


def _stage_permissions(c, plan, stage):
    owner = plan.document['target'][-1]
    model = plan.document['lock']['models'][0]
    migration._runtime_permissions(c, plan.document['runtime_role'], owner, [model], plan.operation_id,
        routine_allowlist=plan.document['lock']['declaration'].get('routine_allowlist', ()))
    # Include SET and ADMIN reachability as the canonical runtime admission does.
    roles = c.exec_driver_sql('''WITH RECURSIVE reachable(oid) AS (
        SELECT oid FROM pg_catalog.pg_roles WHERE rolname=%s UNION
        SELECT m.roleid FROM pg_catalog.pg_auth_members m JOIN reachable r
        ON (m.member=r.oid AND m.set_option) OR
           (m.admin_option AND pg_catalog.pg_has_role(r.oid,m.member,'USAGE')))
        SELECT oid FROM reachable''', (plan.document['runtime_role'],)).scalars().all()
    for role in roles:
        unsafe = c.exec_driver_sql('''SELECT
            pg_catalog.has_table_privilege(%s,%s::oid,'SELECT,INSERT,UPDATE,DELETE,TRUNCATE,REFERENCES,TRIGGER')
            OR pg_catalog.has_any_column_privilege(%s,%s::oid,'SELECT,INSERT,UPDATE,REFERENCES')''',
            (role, stage['oid'], role, stage['oid'])).scalar_one()
        if unsafe:
            _fail('unsafe_stage_privileges')
    actual_owner = c.exec_driver_sql('SELECT pg_catalog.pg_get_userbyid(relowner) FROM pg_catalog.pg_class WHERE oid=%s', (stage['oid'],)).scalar_one()
    if actual_owner != owner:
        _fail('unsafe_stage_owner')
    source_owner = c.exec_driver_sql('SELECT pg_catalog.pg_get_userbyid(relowner) FROM pg_catalog.pg_class WHERE oid=pg_catalog.to_regclass(%s)',
        (migration._table(c, model),)).scalar_one()
    if source_owner != owner:
        _fail('unsafe_source_owner')


def _layout(c, relation, stage=False):
    facts = migration._schema_facts(c, relation['schema'], relation['table'])
    r = facts['relation']
    if (r['relkind'] != 'r' or r['relpersistence'] != 'p' or r['relrowsecurity'] or
            r['relforcerowsecurity'] or r['relhasrules'] or r['inherited'] or r['user_triggers']):
        _fail('unsafe_metadata_layout')
    columns = c.exec_driver_sql('''SELECT attname,atttypid,attnotnull,attidentity,
        attgenerated,atthasdef FROM pg_catalog.pg_attribute WHERE attrelid=%s
        AND attnum>0 AND NOT attisdropped ORDER BY attnum''', (relation['oid'],)).all()
    expected = [('operation_id',2950,True),('record_id',2950,True),('tenant_id',2950,True),
                ('batch_ordinal',23,True),('source_commitment',17,True),('target_frame',17,False)] if stage else [
                ('operation_id',2950,True),('plan_digest',25,True),('state',3802,True)]
    if ([tuple(r[:3]) for r in columns] != expected or any(r[3] or r[4] or r[5] for r in columns)):
        _fail('unsafe_metadata_layout')
    definitions = c.exec_driver_sql('''SELECT pg_catalog.pg_get_constraintdef(oid),
        convalidated,condeferrable,condeferred FROM pg_catalog.pg_constraint
        WHERE conrelid=%s ORDER BY oid''', (relation['oid'],)).all()
    if len(facts['indexes']) != 1 or facts['dependencies']:
        _fail('unsafe_metadata_layout')
    expected_defs = {'PRIMARY KEY (operation_id, record_id)', 'CHECK ((batch_ordinal > 0))',
                     'CHECK ((octet_length(source_commitment) = 32))'} if stage else {'PRIMARY KEY (operation_id)'}
    if {r[0] for r in definitions} != expected_defs or any(not r[1] or r[2] or r[3] for r in definitions):
        _fail('unsafe_metadata_layout')


def _journal_rows(c, plan, operation=None):
    journal = migration._journal(c, plan)
    projected = c.exec_driver_sql(f'SELECT operation_id,plan_digest,octet_length(state::text) FROM {journal} ORDER BY operation_id LIMIT 3').all()
    allowed = {plan.operation_id} | ({operation} if operation is not None else set())
    if (len(projected) > len(allowed) or any(r[0] not in allowed or type(r[2]) is not int or r[2] > MAX_STATE_BYTES for r in projected)):
        _fail('unreviewed_journal_operations')
    source = c.exec_driver_sql(f'SELECT plan_digest,state FROM {journal} WHERE operation_id=%s', (plan.operation_id,)).one_or_none()
    if source is None or source[0] != plan.digest or source[1].get('phase') != 'ACTIVE':
        _fail('source_authority_changed')
    return source


def _source(c, plan, tenant, max_bytes):
    model = plan.document['lock']['models'][0]
    table = migration._table(c, model)
    record = migration._quote(c, model['record']['column'])
    tenant_column = migration._quote(c, model['tenancy']['column'])
    frame = migration._quote(c, model['fields'][0]['payload_column'])
    # Limit first; no unbounded materialization and no source bytea projection yet.
    projected = c.exec_driver_sql(f'SELECT {record},{tenant_column},{frame} IS NULL,octet_length({frame}) FROM {table} WHERE {tenant_column}=%s ORDER BY {record} LIMIT 65', (tenant,)).all()
    if len(projected) > MAX_ROWS:
        _fail('source_row_limit_exceeded')
    total = 0
    for r, t, null, size in projected:
        if type(r) is not UUID or type(t) is not UUID or t != tenant or type(null) is not bool:
            _fail('source_revision_changed')
        if null:
            if size is not None:
                _fail('source_revision_changed')
            cost = 32
        else:
            if type(size) is not int or size < 74:
                _fail('source_frame_invalid')
            total += size
            cost = 32 + 3 * size - 74
        if cost > max_bytes:
            _fail('row_exceeds_chunk_byte_limit')
    if total > MAX_SOURCE_BYTES:
        _fail('source_byte_limit_exceeded')
    rows = tuple((r, None if b is None else bytes(b)) for r, b in c.exec_driver_sql(
        f'SELECT {record},{frame} FROM {table} WHERE {tenant_column}=%s ORDER BY {record} LIMIT 65', (tenant,)).all())
    if (len(rows) != len(projected) or any(r != p[0] or (b is None) != p[2] or
            (None if b is None else len(b)) != p[3] for (r,b),p in zip(rows, projected))):
        _fail('source_revision_changed')
    commitments = [_row(r, b, tenant) for r, b in rows]
    revision = {'row_count': len(rows), 'membership': _digest([str(r) for r, _ in rows]),
                'content': _digest([{'record_id': str(r), 'source_commitment': h} for (r,_),h in zip(rows, commitments)])}
    return rows, revision


def _row(record, frame, tenant):
    return _digest({'record_id': str(record), 'tenant_id': str(tenant), 'is_null': frame is None,
                    'frame_sha256': None if frame is None else hashlib.sha256(frame).hexdigest()})


def _logical(rows):
    return sum(32 + (0 if b is None else 3 * len(b) - 74) for _, b in rows)


def _target_commitment(rows):
    return _digest([{'record_id': str(r), 'tenant_id': str(t), 'batch_ordinal': n,
        'source_commitment': h.hex(), 'is_null': b is None,
        'frame_sha256': None if b is None else hashlib.sha256(b).hexdigest()} for r,t,n,h,b in rows])


def _prepared(source, target, field, tenant):
    a, b = source.prepare(), target.prepare()
    _check_binding(field, tenant, a, b)
    return a, b


def _check_binding(field, tenant, source, target):
    try:
        _binding(field, tenant, source, target)
    except KeyUnavailable:
        _fail('binding_expired')


def _authenticate_source(rows, field, tenant, source):
    for r, b in rows:
        if b is not None and (int.from_bytes(b[6:10], 'big') != 1 or
                              int.from_bytes(b[10:14], 'big') != source.policy.search_generation):
            _fail('source_generation_changed')
        open_text(b, field, tenant, r, source)


def bind(source_plan, engine, *, current_pin, stage_table, tenant_id,
         source_keys, target_keys, maintenance, max_rows=2, max_bytes=4096):
    """Read-only artifact binding under the same full-plan scope/table locks."""
    try:
        model, field = _authority(source_plan, current_pin, source_keys, target_keys, maintenance, tenant_id)
        if (type(tenant_id) is not UUID or type(stage_table) is not tuple or len(stage_table) != 2 or
                stage_table[0] != model['schema'] or type(max_rows) is not int or
                not 1 <= max_rows <= MAX_ROWS or type(max_bytes) is not int or
                not 1 <= max_bytes <= MAX_SOURCE_BYTES * 3 + MAX_ROWS * 32):
            _fail('invalid_preparation_bound')
        with _session(engine, source_plan) as (c, acquired):
            if not acquired:
                _fail('executor_busy')
            _lock(c, model)
            stage = _relation(c, *stage_table)
            journal = _relation(c, source_plan.document['journal_schema'], migration.JOURNAL)
            source_relation = _relation(c, model['schema'], model['table'])
            _layout(c, stage, True); _layout(c, journal)
            _stage_permissions(c, source_plan, stage)
            source_state = _journal_rows(c, source_plan)
            migration._check_connection(source_plan, c, current_pin)
            if c.exec_driver_sql('SELECT EXISTS(SELECT 1 FROM ' + stage['qualified_name'] + ')').scalar_one():
                _fail('stage_not_empty')
            rows, revision = _source(c, source_plan, tenant_id, max_bytes)
            prepared_source, prepared_target = _prepared(source_keys, target_keys, field, tenant_id)
            _authenticate_source(rows, field, tenant_id, prepared_source)
            inventory, catalog = _catalog(c, source_plan, stage)
            doc = {'schema': SCHEMA, 'kind': KIND, 'operation_id': str(uuid4()),
                'source_operation_id': str(source_plan.operation_id), 'source_plan_digest': source_plan.digest,
                'target_id': str(source_plan.target_id), 'target': source_plan.document['target'],
                'models': [[model['schema'], model['table']]], 'stage': stage, 'journal': journal,
                'source': source_relation, 'descriptor': model['fields'][0]['descriptor'],
                'descriptor_digest': model['fields'][0]['descriptor_digest'], 'tenant_id': str(tenant_id),
                'source_pin_digest': _digest(_pin(current_pin)), 'source_journal_digest': _digest(list(source_state)),
                'source_policy': migration._policy(source_keys), 'target_policy': migration._policy(target_keys),
                'source_revision': revision, 'catalog_digest': catalog, 'inventory': inventory,
                'bounds': {'max_rows': max_rows, 'max_bytes': max_bytes, 'source_rows': MAX_ROWS, 'source_bytes': MAX_SOURCE_BYTES},
                'maintenance_digest': _digest(asdict(maintenance)), 'revisions': _revisions()}
            _check_binding(field, tenant_id, prepared_source, prepared_target)
            return Artifact(_canonical(doc))
    except Exception as exc:
        raise _sanitized(exc) from None


def _validate_entry(a, plan, pin, source, target, maintenance):
    d = a.document
    tenant = UUID(d['tenant_id'])
    try:
        model, field = _authority(plan, pin, source, target, maintenance, tenant)
        if (d['source_operation_id'] != str(plan.operation_id) or d['source_plan_digest'] != plan.digest
                or d['target_id'] != str(plan.target_id) or d['target'] != plan.document['target']
                or d['models'] != [[model['schema'], model['table']]]
                or d['descriptor'] != model['fields'][0]['descriptor']
                or d['descriptor_digest'] != model['fields'][0]['descriptor_digest']
                or d['source_pin_digest'] != _digest(_pin(pin))
                or d['maintenance_digest'] != _digest(asdict(maintenance))
                or d['source_policy'] != migration._policy(source)
                or d['target_policy'] != migration._policy(target)):
            _fail('source_authority_changed')
    except Exception:
        raise PreparationFailure('source_authority_changed') from None
    if d['revisions'] != _revisions():
        _fail('implementation_revision_changed')
    return d, tenant, model, field


def _state(a, state, rows, tenant):
    """Validate the entire bounded state before reading target frame bodies."""
    try:
        d = a.document
        if type(state) is not dict or set(state) != _STATE_FIELDS or len(_canonical(state)) > MAX_STATE_BYTES:
            _fail('prefix_inconsistent')
        _revision_valid(state['source_revision'])
        for key, expected in (('schema', SCHEMA), ('kind', KIND),
                ('source_operation_id', d['source_operation_id']),
                ('source_plan_digest', d['source_plan_digest']), ('artifact_digest', a.digest),
                ('source_revision', d['source_revision'])):
            if state[key] != expected:
                _fail('prefix_inconsistent')
        if state['phase'] not in ('PREPARING', 'PREPARED_INACTIVE') or type(state['batches']) is not list or len(state['batches']) > MAX_ROWS:
            _fail('prefix_inconsistent')
        offset, cursor = 0, None
        for ordinal, batch in enumerate(state['batches'], 1):
            if type(batch) is not dict or set(batch) != _BATCH_FIELDS:
                _fail('prefix_inconsistent')
            count = batch['row_count']
            if (type(count) is not int or not 1 <= count <= d['bounds']['max_rows']
                    or type(batch['ordinal']) is not int or batch['ordinal'] != ordinal
                    or batch['cursor_before'] != cursor or not _uuid(batch['cursor_after'])
                    or not _hex(batch['target_commitment']) or type(batch['logical_bytes']) is not int
                    or type(batch['rows']) is not list or len(batch['rows']) != count
                    or offset + count > len(rows)):
                _fail('prefix_inconsistent')
            subset = rows[offset:offset + count]
            expected = [{'record_id': str(r), 'source_commitment': _row(r,b,tenant), 'is_null': b is None} for r,b in subset]
            # Python bool/int equality must not admit wrong JSON discriminator types.
            if any(type(item) is not dict or set(item) != {'record_id','source_commitment','is_null'} or
                   type(item['is_null']) is not bool or not _uuid(item['record_id']) or
                   not _hex(item['source_commitment']) for item in batch['rows']):
                _fail('prefix_inconsistent')
            if (batch['rows'] != expected or batch['cursor_after'] != str(subset[-1][0])
                    or batch['logical_bytes'] != _logical(subset)
                    or batch['logical_bytes'] > d['bounds']['max_bytes']):
                _fail('prefix_inconsistent')
            offset += count
            cursor = str(subset[-1][0])
        if state['phase'] == 'PREPARING':
            if state['verification'] is not None:
                _fail('prefix_inconsistent')
        else:
            receipt = state['verification']
            if (offset != len(rows) or type(receipt) is not dict or set(receipt) != {'row_count','target_commitment'}
                    or type(receipt['row_count']) is not int or receipt['row_count'] != len(rows)
                    or not _hex(receipt['target_commitment'])):
                _fail('prefix_inconsistent')
        return offset
    except Exception:
        raise PreparationFailure('prefix_inconsistent') from None


def _prefix(c, a, state, rows, tenant, field, source, target):
    count = _state(a, state, rows, tenant)
    d, operation = a.document, a.operation_id
    stage = d['stage']['qualified_name']
    projected = c.exec_driver_sql(f'''SELECT operation_id,record_id,tenant_id,batch_ordinal,
        octet_length(source_commitment),target_frame IS NULL,octet_length(target_frame)
        FROM {stage} ORDER BY record_id LIMIT 65''').all()
    if len(projected) != count:
        _fail('prefix_inconsistent')
    expected_ordinals = [batch['ordinal'] for batch in state['batches'] for _ in batch['rows']]
    for (op,r,t,n,hsize,null,size),(record,frame),ordinal in zip(projected, rows, expected_ordinals):
        if (op != operation or r != record or t != tenant or n != ordinal or hsize != 32
                or null != (frame is None) or size != (None if frame is None else len(frame))):
            _fail('prefix_inconsistent')
    persisted = tuple((r,t,n,bytes(h),None if b is None else bytes(b)) for r,t,n,h,b in
        c.exec_driver_sql(f'SELECT record_id,tenant_id,batch_ordinal,source_commitment,target_frame FROM {stage} ORDER BY record_id LIMIT 65').all())
    try:
        for (r,t,n,h,b),(record,frame) in zip(persisted, rows):
            if r != record or t != tenant or h.hex() != _row(record,frame,tenant) or (b is None) != (frame is None):
                _fail('prefix_inconsistent')
            if b is not None and (len(b) != len(frame) or b[:6] != frame[:6]
                    or int.from_bytes(b[6:10], 'big') != 2 or b[10:46] != frame[10:46]):
                _fail('prefix_inconsistent')
            original = open_text(frame, field, tenant, record, source)
            transformed = open_text(b, field, tenant, record, target)
            if type(original) is not type(transformed) or original != transformed:
                _fail('prefix_inconsistent')
        offset = 0
        for batch in state['batches']:
            chunk = persisted[offset:offset + batch['row_count']]
            if batch['target_commitment'] != _target_commitment(chunk):
                _fail('prefix_inconsistent')
            offset += batch['row_count']
        if state['phase'] == 'PREPARED_INACTIVE' and state['verification']['target_commitment'] != _target_commitment(persisted):
            _fail('prefix_inconsistent')
    except KeyUnavailable:
        _fail('binding_expired')
    except Exception:
        raise PreparationFailure('prefix_inconsistent') from None
    return count, persisted


def _observe(observer, point, c, ordinal):
    # Test-only fault seam. The host callback is trusted executable code and
    # cannot be used as admission, persisted authority or a production API.
    if observer is not None:
        observer(point, connection=c, ordinal=ordinal)


def _result(state):
    return Result(state['phase'], 'inactive_only', sum(b['row_count'] for b in state['batches']), len(state['batches']))


def enter(artifact, engine, *, source_plan, current_pin, source_keys, target_keys,
          maintenance, action='step', observer=None):
    """Inspect current facts, then commit at most one inactive chunk.

    start is explicit and never inferred from missing progress. inspect does no
    target/journal DML. Each worker reconstructs providers through its host; no
    credentials, cached roots or provider objects are serialized by this module.
    """
    operation_id = None
    try:
        if not isinstance(artifact, Artifact) or action not in ('start', 'step', 'inspect'):
            _fail('invalid_entry')
        # Reparse immutable bytes instead of trusting a cached mutable document.
        a = Artifact(artifact.canonical_bytes)
        operation_id = a.operation_id
        d, tenant, model, field = _validate_entry(a, source_plan, current_pin, source_keys, target_keys, maintenance)
        with _session(engine, source_plan, operation_id) as (c, acquired):
            if not acquired:
                return Result('PENDING', 'executor_busy')
            _lock(c, model)
            for name in ('stage','source','journal'):
                rel = d[name]
                if _relation(c, rel['schema'], rel['table']) != rel:
                    _fail('catalog_changed')
            _layout(c, d['stage'], True); _layout(c, d['journal'])
            _stage_permissions(c, source_plan, d['stage'])
            source_state = _journal_rows(c, source_plan, a.operation_id)
            migration._check_connection(source_plan, c, current_pin)
            if _digest(list(source_state)) != d['source_journal_digest']:
                _fail('source_authority_changed')
            inventory, catalog = _catalog(c, source_plan, d['stage'])
            if inventory != d['inventory'] or catalog != d['catalog_digest']:
                _fail('catalog_changed')
            rows, revision = _source(c, source_plan, tenant, d['bounds']['max_bytes'])
            if revision != d['source_revision']:
                _fail('source_revision_changed')
            source, target = _prepared(source_keys, target_keys, field, tenant)
            _authenticate_source(rows, field, tenant, source)
            journal, stage = d['journal']['qualified_name'], d['stage']['qualified_name']
            saved = c.exec_driver_sql(f'SELECT plan_digest,state FROM {journal} WHERE operation_id=%s FOR UPDATE', (a.operation_id,)).one_or_none()
            if action == 'start':
                if saved is not None:
                    _fail('operation_already_started')
                if c.exec_driver_sql(f'SELECT EXISTS(SELECT 1 FROM {stage})').scalar_one():
                    _fail('prefix_inconsistent')
                state = {'schema': SCHEMA, 'kind': KIND,
                    'source_operation_id': d['source_operation_id'], 'source_plan_digest': d['source_plan_digest'],
                    'artifact_digest': a.digest, 'phase': 'PREPARING', 'source_revision': revision,
                    'batches': [], 'verification': None}
                result = c.exec_driver_sql(f'INSERT INTO {journal} (operation_id,plan_digest,state) VALUES (%s,%s,%s::jsonb)',
                    (a.operation_id, a.digest, _canonical(state).decode()))
                if result.rowcount != 1:
                    _fail('journal_marker_write_failed')
                previous = Result('UNSTARTED', 'not_initialized')
                ordinal = 0
            else:
                if saved is None:
                    _fail('missing_preparation_state')
                if saved[0] != a.digest:
                    _fail('prefix_inconsistent')
                state = saved[1]
                count, persisted = _prefix(c, a, state, rows, tenant, field, source, target)
                previous = _result(state)
                if action == 'inspect' or state['phase'] == 'PREPARED_INACTIVE':
                    _check_binding(field, tenant, source, target)
                    return previous
                old_state = _canonical(state).decode()
                if count < len(rows):
                    selected, budget = [], 0
                    for row in rows[count:count + d['bounds']['max_rows']]:
                        cost = _logical((row,))
                        if budget + cost > d['bounds']['max_bytes']:
                            break
                        selected.append(row); budget += cost
                    if not selected:
                        _fail('row_exceeds_chunk_byte_limit')
                    selected = tuple(selected)
                    transformed = prepare_payload_rotation_batch(selected, field, tenant,
                        source=source, target=target, max_rows=d['bounds']['max_rows'], max_bytes=d['bounds']['max_bytes'])
                    _check_binding(field, tenant, source, target)
                    if type(transformed) is not tuple or len(transformed) != len(selected):
                        _fail('invalid_transform_result')
                    ordinal = len(state['batches']) + 1
                    staged = []
                    for (r,frame), item in zip(selected, transformed):
                        if type(item) is not tuple or len(item) != 2 or item[0] != r:
                            _fail('invalid_transform_result')
                        new = item[1]
                        if ((new is None) != (frame is None) or
                                (new is not None and (type(new) is not bytes or len(new) != len(frame)
                                or new[:6] != frame[:6] or int.from_bytes(new[6:10], 'big') != 2
                                or new[10:46] != frame[10:46]))):
                            _fail('invalid_transform_result')
                        staged.append((r,tenant,ordinal,bytes.fromhex(_row(r,frame,tenant)),new))
                    result = c.exec_driver_sql(f'''INSERT INTO {stage}
                        (operation_id,record_id,tenant_id,batch_ordinal,source_commitment,target_frame)
                        VALUES (%s,%s,%s,%s,%s,%s)''', [(a.operation_id,) + row for row in staged])
                    if result.rowcount != len(staged):
                        _fail('stage_write_count_mismatch')
                    state['batches'].append({'ordinal': ordinal,
                        'cursor_before': None if count == 0 else str(rows[count-1][0]),
                        'cursor_after': str(selected[-1][0]),
                        'rows': [{'record_id': str(r), 'source_commitment': _row(r,b,tenant), 'is_null': b is None} for r,b in selected],
                        'target_commitment': _target_commitment(staged), 'row_count': len(selected), 'logical_bytes': budget})
                else:
                    # _prefix has just authenticated the entire membership, values,
                    # NULLs, exact generations and search bytes under the source lock.
                    ordinal = len(state['batches']) + 1
                    state['phase'] = 'PREPARED_INACTIVE'
                    state['verification'] = {'row_count': len(rows), 'target_commitment': _target_commitment(persisted)}
                _state(a, state, rows, tenant)
                updated = c.exec_driver_sql(f'''UPDATE {journal} SET state=%s::jsonb
                    WHERE operation_id=%s AND plan_digest=%s AND state=%s::jsonb''',
                    (_canonical(state).decode(), a.operation_id, a.digest, old_state))
                if updated.rowcount != 1:
                    _fail('journal_marker_write_failed')
            _observe(observer, 'after_dml', c, ordinal)
            _check_binding(field, tenant, source, target)
            _observe(observer, 'before_commit', c, ordinal)
            # Callback boundaries cannot postpone the final real lease/PID check.
            _check_binding(field, tenant, source, target)
            try:
                c.commit()
            except Exception:
                # Never retry in the uncertain physical session. Cleanup invalidates
                # it; a fresh worker must win the scope lock and inspect durable data.
                return Result('UNKNOWN', 'inspection_required', previous.committed_rows, previous.committed_batches)
            _observe(observer, 'after_commit', c, ordinal)
            return _result(state)
    except Exception as exc:
        raise _sanitized(exc, operation_id) from None


if __name__ == '__main__':
    # Explicit public synthetic fixture command, never an import-path dependency.
    from test_payload_rotation_journal import public_worker_main
    try:
        public_worker_main()
    except Exception:
        raise SystemExit('inactive preparation failed; inspect the original operation') from None
