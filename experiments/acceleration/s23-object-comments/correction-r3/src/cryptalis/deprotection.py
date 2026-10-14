"""Offline current-data deprotection with explicit external publication.

A PostgreSQL journal is progress, never restore authority. The host keeps the
current pin and excludes privileged writers. No plaintext erasure is promised.
"""
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import math
from uuid import UUID, uuid4
from psycopg import sql

from cryptalis import migration as m
from cryptalis import cutover
from cryptalis import _object_comments as _comments
from cryptalis._native_text import source_text_type
from cryptalis.crypto.cf1 import FieldDescriptor, open_text
from cryptalis.manifest.compiler import _canonical, _previous_lock
from cryptalis._transition_json import decode_transition_json

PHASES = ('PREPARED', 'EXPANDED', 'BACKFILLED', 'VERIFIED',
          'PLAINTEXT_PENDING', 'PLAINTEXT_ACTIVE')
PUBLICATION = ('PLAINTEXT_ACTIVATING', 'REMOVING', 'REMOVED')


@dataclass(frozen=True)
class DeprotectionPlan:
    artifact: bytes

    def __post_init__(self):
        try:
            d = decode_transition_json(self.artifact, reverse=True)
            if (d['format'] not in (_comments.LEGACY_REVERSE, _comments.REVERSE) or d['kind'] != 'deprotect'
                    or _canonical(d) != self.artifact):
                raise ValueError
            source = m.MigrationPlan(_canonical(d['source_plan']))
            if (d['format'] == _comments.REVERSE) != _comments.enabled(source.document):
                raise ValueError
            pin = m.DeploymentPin(**{**d['source_pin'],
                'target_id': UUID(d['source_pin']['target_id']),
                'operation_id': UUID(d['source_pin']['operation_id'])})
            m._admit(source, pin)
            source_operation_id = source.operation_id
            if (pin.phase != 'ACTIVE' or UUID(d['target_id']) != source.target_id
                    or not UUID(d['operation_id']).int
                    or UUID(d['operation_id']) == source_operation_id
                    or d['lock'] != source.document['lock']
                    or d['target'] != source.document['target']
                    or d['runtime_role'] != source.document['runtime_role']
                    or d['journal_schema'] != source.document['journal_schema']):
                raise ValueError
            if set(d)!={'format','kind','operation_id','target_id','source_plan','source_pin',
                        'lock','target','runtime_role','journal_schema','key_policies',
                        'active_schemas','retirable_aborted','estimates','plaintext_runtime_role','cutover_readiness'}:raise ValueError
            if (type(d['plaintext_runtime_role']) is not str or not d['plaintext_runtime_role']
                    or d['plaintext_runtime_role']==d['runtime_role']):raise ValueError
            if type(d['retirable_aborted']) is not list:raise ValueError
            retired=set()
            for item in d['retirable_aborted']:
                if set(item)!={'operation_id','plan_digest'}:raise ValueError
                identity=UUID(item['operation_id'])
                if identity in retired or identity in (UUID(d['operation_id']),source_operation_id):raise ValueError
                retired.add(identity)
                digest=item['plan_digest']
                if type(digest) is not str or len(digest)!=64 or any(ch not in '0123456789abcdef' for ch in digest):raise ValueError
            expected={v['table_id'] for v in d['lock']['models']}
            if set(d['active_schemas']) != expected: raise ValueError
            for name in ('backfill_rows_per_second','verify_rows_per_second'):
                value=d['estimates'][name]
                if type(value) not in (int,float) or not math.isfinite(value) or value<=0:raise ValueError
            if d['format'] == _comments.REVERSE:
                _comments.validate_reverse(d)
        except Exception:
            raise m.TransitionFailure('invalid_reverse_plan') from None

    def cutover_procedure(self, *, create_role=True):
        return cutover.procedure(self.source,self.document['plaintext_runtime_role'],create_role=create_role,
                                 inventory_report=self.document['cutover_readiness'])

    @property
    def document(self): return json.loads(self.artifact)
    @property
    def digest(self): return hashlib.sha256(self.artifact).hexdigest()
    @property
    def target_id(self): return UUID(self.document['target_id'])
    @property
    def operation_id(self): return UUID(self.document['operation_id'])
    @property
    def lock_bytes(self): return _canonical(self.document['lock'])
    @property
    def source(self): return m.MigrationPlan(_canonical(self.document['source_plan']))


@dataclass(frozen=True)
class PlaintextApproval:
    target_id: UUID
    operation_id: UUID
    plan_digest: str
    accept_plaintext_at_rest: bool
    retained_backup_recovery: str


@dataclass(frozen=True)
class RemovalApproval:
    plan_digest: str
    package_free_workload_evidence: str
    retained_backup_recovery_evidence: str
    old_workers_stopped: bool


def _consent(p, approval):
    if (type(approval) is not PlaintextApproval
            or (approval.target_id,approval.operation_id,approval.plan_digest) !=
               (p.target_id,p.operation_id,p.digest)
            or approval.accept_plaintext_at_rest is not True
            or type(approval.retained_backup_recovery) is not str
            or not approval.retained_backup_recovery.strip()):
        raise m.TransitionFailure('plaintext_approval_required',p.operation_id)


def _pin(p, pin):
    if (type(p) is not DeprotectionPlan or type(pin) is not m.DeploymentPin
            or (pin.target_id,pin.operation_id,pin.plan_digest) !=
               (p.target_id,p.operation_id,p.digest)
            or pin.phase not in PHASES + PUBLICATION):
        raise m.TransitionFailure('external_reverse_policy_mismatch')


def plan(source, engine, *, source_pin, keys, plaintext_runtime_role, backfill_rows_per_second,
         verify_rows_per_second, temporary_bytes_per_row, wal_bytes_per_row):
    """Read-only reverse proposal. No decrypt, staging or implicit consent."""
    m._admit(source,source_pin)
    if type(plaintext_runtime_role) is not str or not plaintext_runtime_role or plaintext_runtime_role==source.document['runtime_role']:
        raise m.TransitionFailure('distinct_plaintext_runtime_role_required')
    rates=(backfill_rows_per_second,verify_rows_per_second)
    if not m._valid_measured_rates(rates):
        raise m.TransitionFailure('missing_measured_rates')
    if any(type(v) is not int or not 1<=v<2**53 for v in (temporary_bytes_per_row,wal_bytes_per_row)):
        raise m.TransitionFailure('missing_measured_storage_or_wal_costs')
    _previous_lock(source.lock_bytes,source.document['lock'],engine)
    policies={}; schemas={}; count=0; aborted=[]
    with m._connection(engine,source.operation_id) as c:
        m._check_connection(source,c,source_pin)
        for operation,digest,state in c.exec_driver_sql(f'SELECT operation_id,plan_digest,state FROM {m._journal(c,source)} ORDER BY operation_id').all():
            if operation==source.operation_id:continue
            if (state.get('phase')!='ABORTED' or state.get('source_operation_id')!=str(source.operation_id)
                    or state.get('source_plan_digest')!=source.digest):
                raise m.TransitionFailure('unreviewed_journal_operations')
            aborted.append({'operation_id':str(operation),'plan_digest':digest})
        if m._target(c) != source.document['target']:
            raise m.TransitionFailure('maintenance_requires_planned_owner')
        for model in source.document['lock']['models']:
            schemas[model['table_id']]=m._facts(c,model)
            _admit_suffix(c,_model(model),source.operation_id)
            count+=c.exec_driver_sql(f'SELECT count(*) FROM {m._table(c,model)}').scalar_one()
            tenants=(c.exec_driver_sql(f'SELECT DISTINCT {m._quote(c,model["tenancy"]["column"])} FROM {m._table(c,model)}').scalars().all()
                     if 'column' in model['tenancy'] else [UUID(model['table_id'])])
            for tenant in tenants:
                ring=m._ring(keys,tenant,source)
                policies[str(tenant)]=m._policy(ring)
        readiness=cutover.inventory(c,source.document['lock']['models'],old_role=source.document['runtime_role'],
            new_role=plaintext_runtime_role,owner=source.document['target'][-1])
    _, _, pause_seconds = m._time_estimates(count, rates)
    estimates={'rows':count,'backfill_rows_per_second':rates[0],'verify_rows_per_second':rates[1],
               'writer_pause_seconds_estimate':pause_seconds,
               'temporary_bytes_estimate':count*temporary_bytes_per_row,
               'wal_bytes_estimate':count*wal_bytes_per_row,
               'limits':'Staging/DDL/publication delays excluded; plaintext enters WAL and backups.'}
    document = {'format':_comments.REVERSE if _comments.enabled(source.document) else _comments.LEGACY_REVERSE,'kind':'deprotect',
        'operation_id':str(uuid4()),'target_id':str(source.target_id),
        'source_plan':source.document,'source_pin':{'target_id':str(source_pin.target_id),
        'operation_id':str(source_pin.operation_id),'plan_digest':source_pin.plan_digest,'phase':source_pin.phase},
        'lock':source.document['lock'],'target':source.document['target'],
        'runtime_role':source.document['runtime_role'],'journal_schema':source.document['journal_schema'],
        'key_policies':policies,'active_schemas':schemas,'retirable_aborted':aborted,'estimates':estimates,
        'plaintext_runtime_role':plaintext_runtime_role,'cutover_readiness':readiness}
    if document['format'] == _comments.REVERSE:
        try: _comments.validate_reverse(document)
        except _comments.ContractError as exc: raise m.TransitionFailure(exc.code) from None
    return DeprotectionPlan(_canonical(document))


@contextmanager
def _executor(p,engine,pin,approval,consent):
    _pin(p,pin); m._approve_maintenance(p,approval); _consent(p,consent)
    try:_previous_lock(p.lock_bytes,p.document['lock'],engine)
    except ValueError:raise m.TransitionFailure('invalid_compiler_lock',p.operation_id) from None
    identity=[(x['schema'],x['table']) for x in p.document['lock']['models']]
    lock=int.from_bytes(hashlib.sha256(_canonical(identity)).digest()[:8],'big',signed=True)
    with m._connection(engine,p.operation_id,exclusive=True) as c:
        if m._target(c)!=p.document['target']:raise m.TransitionFailure('wrong_database_target',p.operation_id)
        m._runtime_permissions(c,p.document['runtime_role'],p.document['target'][-1],p.document['lock']['models'],p.operation_id,
                              routine_allowlist=p.document['lock']['declaration'].get('routine_allowlist',()))
        c.exec_driver_sql("SET lock_timeout = '5s'"); c.exec_driver_sql('SET synchronous_commit = on')
        acquired=c.exec_driver_sql('SELECT pg_catalog.pg_try_advisory_lock(%s)',(lock,)).scalar_one(); c.commit()
        if not acquired:raise m.TransitionFailure('executor_already_running',p.operation_id)
        yield c


def _state(c,p,pin,*,allow_aborted=False):
    row=c.exec_driver_sql(f'SELECT plan_digest,state FROM {m._journal(c,p)} WHERE operation_id=%s',(p.operation_id,)).one_or_none()
    if row is None:
        if pin.phase!='PREPARED':raise m.TransitionFailure('restored_or_missing_reverse_transition',p.operation_id)
        return None
    if row[0]!=p.digest:raise m.TransitionFailure('journal_identity_mismatch',p.operation_id)
    state=row[1]; phase=state.get('phase')
    if state.get('layout_version') != 101:
        raise m.TransitionFailure('reverse_staging_layout_requires_inspection',p.operation_id)
    if phase=='ABORTED' and allow_aborted and pin.phase in PHASES[:4]:return state
    if phase not in PHASES[1:]:raise m.TransitionFailure('unknown_or_aborted_reverse_state',p.operation_id)
    required=('PLAINTEXT_PENDING' if pin.phase=='PLAINTEXT_ACTIVATING' else
              'PLAINTEXT_ACTIVE' if pin.phase=='REMOVING' else pin.phase)
    if required not in PHASES or PHASES.index(phase)<PHASES.index(required):
        raise m.TransitionFailure('restored_state_behind_external_pin',p.operation_id)
    if phase=='PLAINTEXT_ACTIVE' and pin.phase not in ('PLAINTEXT_ACTIVATING','PLAINTEXT_ACTIVE','REMOVING'):
        raise m.TransitionFailure('external_policy_behind_database',p.operation_id)
    # The reverse marker is only one half of expansion's atomic journal pair.
    # Resume must not progress a one-sided restore or a changed predecessor.
    # Completed aborts return above: a newer reverse may now own that source.
    source=p.source
    if (state.get('source_operation_id')!=str(source.operation_id)
            or state.get('source_plan_digest')!=source.digest):
        raise m.TransitionFailure('source_state_changed',p.operation_id)
    predecessor=c.exec_driver_sql(
        f'SELECT plan_digest,state FROM {m._journal(c,p)} WHERE operation_id=%s',
        (source.operation_id,)).one_or_none()
    if (predecessor is None or predecessor[0]!=source.digest
            or type(predecessor[1]) is not dict or predecessor[1].get('phase')!='DEPROTECTING'):
        raise m.TransitionFailure('source_state_changed',p.operation_id)
    return state


def _model(model):
    result=json.loads(json.dumps(model))
    for f in result['fields']:f['payload_column']='_cryptalis_'+UUID(f['field_id']).hex+'_plain'
    protected={f['column']:f for f in result['fields']}
    columns=result['source_schema']['columns']
    first=min(i for i,col in enumerate(columns) if col['name'] in protected)
    targets=[];copies=[]
    for col in columns:
        name=col['name']
        if name not in protected:continue
        staging=(protected[name]['payload_column'] if name in protected else
                 '_cryptalis_'+UUID(model['table_id']).hex+'_copy_'+str(col['attnum']))
        target={'column':name,'payload_column':staging,'source':col}
        targets.append(target)
        if name not in protected:copies.append(target)
    result['target_columns']=targets;result['copied_columns']=copies
    # Streams read authenticated CF1 from the retained physical payload slot.
    for f, original in zip(result['fields'], model['fields']):
        f['column']=original['payload_column']
    return result


def _admit_suffix(c,model,operation_id):
    """Do not reconstruct public metadata. Require original visible ordinals."""
    facts=m._facts(c,model)
    staged={f['payload_column'] for f in model['target_columns']} | {f['column'] for f in model['fields']}
    current=[col['name'] for col in facts['columns'] if col['name'] not in staged]
    original=[col['name'] for col in model['source_schema']['columns']]
    if current!=original:
        raise m.TransitionFailure('inplace_research_legacy_layout_refused',operation_id)


def _guard(c,p,model):
    trigger,function=m._guard_names(p,model); fn=m._quote(c,model['schema'])+'.'+m._quote(c,function)
    owner=p.document['target'][-1].replace("'","''")
    body=f"BEGIN IF CURRENT_USER <> '{owner}' THEN RAISE EXCEPTION USING ERRCODE='55000', MESSAGE='Cryptalis maintenance: writers paused; retry only after matching deployment publication'; END IF; RETURN NULL; END"
    literal=sql.Literal(body).as_string(c.connection.driver_connection)
    c.exec_driver_sql(f'CREATE FUNCTION {fn}() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS {literal}')
    c.exec_driver_sql(f'REVOKE ALL ON FUNCTION {fn}() FROM PUBLIC')
    return fn


def _expand(c,p):
    m._lock_tables(c,p)
    source=p.source; sd=p.document['source_pin']
    source_pin=m.DeploymentPin(UUID(sd['target_id']),UUID(sd['operation_id']),sd['plan_digest'],sd['phase'])
    m._check_connection(source,c,source_pin)
    models={}; functions={}
    for original in p.document['lock']['models']:
        if m._facts(c,original)!=p.document['active_schemas'][original['table_id']]:
            raise m.TransitionFailure('active_schema_mismatch',p.operation_id)
        model=_model(original); table=m._table(c,model)
        _admit_suffix(c,model,p.operation_id)
        if model['schema'] not in functions:functions[model['schema']]=_guard(c,p,model)
        trigger,_=m._guard_names(p,model)
        c.exec_driver_sql(f'CREATE TRIGGER {m._quote(c,trigger)} BEFORE INSERT OR UPDATE OR DELETE OR TRUNCATE ON {table} FOR EACH STATEMENT EXECUTE FUNCTION {functions[model["schema"]]}()')
        c.exec_driver_sql(f'ALTER TABLE {table} ENABLE ALWAYS TRIGGER {m._quote(c,trigger)}')
        for f in model['target_columns']:
            col=f['source']
            native=source_text_type(col)
            if native is None:raise m.TransitionFailure('unsupported_reverse_source_type',p.operation_id)
            kind,limit=native
            storage_type=kind if limit is None else f'{kind}({limit})'
            collate=' COLLATE '+m._quote(c,col['collation_schema'])+'.'+m._quote(c,col['collation_name']) if col['collation_name'] else ''
            c.exec_driver_sql(f'ALTER TABLE {table} ADD COLUMN {m._quote(c,f["payload_column"])} {storage_type}{collate}')
        models[model['table_id']]={'scope':m._scope(c,model),'cursor':None,'rows':0,'chunks':0,
            'schema':m._facts(c,model),'guard':m._guard_facts(c,p,model)}
    state={'phase':'EXPANDED','layout_version':101,'models':models,'source_operation_id':str(source.operation_id),'source_plan_digest':source.digest}
    c.exec_driver_sql(f'INSERT INTO {m._journal(c,p)} VALUES (%s,%s,%s::jsonb)',(p.operation_id,p.digest,json.dumps(state)))
    source_state=m._state(c,source,source_pin);source_state['phase']='DEPROTECTING';m._save(c,source,source_state)
    return state


def _prepared_values(p,keys,model,rows,*,with_plain):
    descriptors=[FieldDescriptor.from_compiled(f['descriptor'],f['descriptor_digest']) for f in model['fields']]
    material={};out=[]
    for row in rows:
        scoped='column' in model['tenancy']; tenant=row[1] if scoped else UUID(model['table_id']); offset=2 if scoped else 1
        if tenant not in material:material[tenant]=m._prepare_chunk(keys,tenant,p)
        body=[]
        for i,f in enumerate(model['fields']):
            frame=row[offset+i*(2 if with_plain else 1)]
            frame=bytes(frame) if frame is not None else None
            policy=material[tenant].policy
            if frame is not None and (int.from_bytes(frame[6:10],'big')!=policy.payload_generation or
                    int.from_bytes(frame[10:14],'big')!=(policy.search_generation if f['queries'] else 0)):
                raise m.TransitionFailure('generation_mismatch',p.operation_id)
            value=open_text(frame,descriptors[i],tenant,row[0],material[tenant])
            if with_plain and (type(value)!=type(row[offset+2*i+1]) or value!=row[offset+2*i+1]):
                raise m.TransitionFailure('value_verification_failed',p.operation_id)
            body.append(value)
        out.append(tuple(body)+(row[0],))
    return out


def _backfill(c,p,state,keys,chunk_size,chunk_bytes):
    m._inspect_paused(c,p,state)
    for original in p.document['lock']['models']:
        model=_model(original);progress=state['models'][model['table_id']]
        rows=m._stream(c,model,after=progress['cursor'],limit=chunk_size,byte_limit=chunk_bytes)
        if not rows:continue
        params=_prepared_values(p,keys,model,rows,with_plain=False)
        assignments=[m._quote(c,f['payload_column'])+'=%s' for f in model['fields']]
        assignments += [m._quote(c,f['payload_column'])+'='+m._quote(c,f['column']) for f in model['copied_columns']]
        c.exec_driver_sql(f'UPDATE {m._table(c,model)} SET '+','.join(assignments)+
                         f' WHERE {m._quote(c,model["record"]["column"])}=%s',params)
        progress['cursor']=str(rows[-1][0]);progress['rows']+=len(rows);progress['chunks']+=1
        m._save(c,p,state);return
    state['phase']='BACKFILLED';m._save(c,p,state)


def _verify(c,p,state,keys,chunk_bytes):
    m._inspect_paused(c,p,state)
    for original in p.document['lock']['models']:
        model=_model(original);progress=state['models'][model['table_id']]
        if m._scope(c,model)!=progress['scope']:raise m.TransitionFailure('membership_changed',p.operation_id)
        if progress['rows']!=progress['scope']['count']:raise m.TransitionFailure('incomplete_backfill',p.operation_id)
        cursor=None
        while rows:=m._stream(c,model,payloads=True,after=cursor,byte_limit=chunk_bytes):
            _prepared_values(p,keys,model,rows,with_plain=True)
            cursor=str(rows[-1][0])
        for f in model['copied_columns']:
            source=m._quote(c,f['column']);target=m._quote(c,f['payload_column'])
            if c.exec_driver_sql(f"SELECT EXISTS (SELECT 1 FROM {m._table(c,model)} WHERE pg_catalog.convert_to({source},'UTF8') IS DISTINCT FROM pg_catalog.convert_to({target},'UTF8'))").scalar_one():
                raise m.TransitionFailure('public_copy_verification_failed',p.operation_id)


def _native_shape(facts):
    # Dropped-slot numbers may differ; visible order is native semantics.
    result=json.loads(json.dumps(facts))
    for col in result['columns']:col.pop('attnum',None)
    return result


def _ordinary_schema(c,p,*,fenced=False):
    for model in p.document['lock']['models']:
        actual=m._facts(c,model);wanted=json.loads(json.dumps(model['source_schema']))
        if fenced:wanted['relation']['user_triggers']=True
        if _native_shape(actual)!=_native_shape(wanted):raise m.TransitionFailure('ordinary_schema_mismatch',p.operation_id)
    _comments.check(c, p.document['source_plan'], p.operation_id)


def _switch(c,p,state,keys,chunk_bytes):
    m._lock_tables(c,p,verification=True);_verify(c,p,state,keys,chunk_bytes);m._lock_tables(c,p)
    m._require_no_other_snapshots(c,p)
    for original in p.document['lock']['models']:
        model=_model(original);table=m._table(c,model)
        _admit_suffix(c,model,p.operation_id)
        by_name={f['column']:f for f in original['fields']}
        for f in model['target_columns']:
            original=by_name[f['column']]
            # Preserve the original type and column identity; update row versions.
            c.exec_driver_sql(f'UPDATE {table} SET {m._quote(c,f["column"])}={m._quote(c,f["payload_column"])}')
            c.exec_driver_sql(f'ALTER TABLE {table} DROP COLUMN {m._quote(c,f["payload_column"])}, DROP COLUMN {m._quote(c,original["payload_column"])}')
            if not f['source']['nullable']:
                c.exec_driver_sql(f'ALTER TABLE {table} ALTER COLUMN {m._quote(c,f["column"])} DROP DEFAULT')
        for f in model['fields']:
            for constraint in f['original']['constraints']:
                c.exec_driver_sql(f'ALTER TABLE {table} ADD CONSTRAINT {m._quote(c,constraint["name"])} '+constraint['definition'])
            for index in f['original']['indexes']:c.exec_driver_sql(index['definition'])
        state['models'][model['table_id']]['active_schema']=m._facts(c,model)
    _comments.restore(c, p.document['source_plan'], p.operation_id)
    _ordinary_schema(c,p,fenced=True)
    state['phase']='PLAINTEXT_PENDING';m._save(c,p,state)


def _cutover_ready(c,p):
    return cutover.require_ready(c,p.document['lock']['models'],old_role=p.document['runtime_role'],
        new_role=p.document['plaintext_runtime_role'],owner=p.document['target'][-1],operation_id=p.operation_id)


def check_cutover(p,engine):
    """Read-only diagnostics with actionable finding codes; no grants or termination."""
    with m._connection(engine,p.operation_id) as c:
        return cutover.inventory(c,p.document['lock']['models'],old_role=p.document['runtime_role'],
            new_role=p.document['plaintext_runtime_role'],owner=p.document['target'][-1])


def _activate(c,p,state,pin):
    if pin.phase!='PLAINTEXT_ACTIVATING':raise m.TransitionFailure('matching_plaintext_publication_required',p.operation_id)
    m._lock_tables(c,p);m._active_schema(c,p,state)
    _comments.check(c, p.document['source_plan'], p.operation_id)
    _cutover_ready(c,p)
    for model in p.document['lock']['models']:
        if m._guard_facts(c,p,model)!=state['models'][model['table_id']]['guard']:
            raise m.TransitionFailure('writer_fence_changed',p.operation_id)
    m._drop_guards(c,p);_ordinary_schema(c,p)
    for model in p.document['lock']['models']:state['models'][model['table_id']]['active_schema']=m._facts(c,model)
    state['phase']='PLAINTEXT_ACTIVE';m._save(c,p,state)


def apply(p,engine,*,keys,pin,approval,plaintext_approval,chunk_size=1000,
          chunk_bytes=m.DEFAULT_CHUNK_BYTES,until='PLAINTEXT_PENDING'):
    if (type(chunk_size) is not int or not 1<=chunk_size<=5000 or
            type(chunk_bytes) is not int or not 1<=chunk_bytes<=m.MAX_CHUNK_BYTES or until not in PHASES[1:]):
        raise m.TransitionFailure('invalid_apply_bound')
    with _executor(p,engine,pin,approval,plaintext_approval) as c:
        state=_state(c,p,pin);c.commit()
        if state is None:
            with c.begin():state=_expand(c,p)
        while PHASES.index(state['phase'])<PHASES.index(until):
            with c.begin():
                if state['phase']=='EXPANDED':_backfill(c,p,state,keys,chunk_size,chunk_bytes)
                elif state['phase'] in ('BACKFILLED','VERIFIED'):
                    if until=='VERIFIED':
                        m._lock_tables(c,p,verification=True);_verify(c,p,state,keys,chunk_bytes)
                        state['phase']='VERIFIED';m._save(c,p,state)
                    else:_switch(c,p,state,keys,chunk_bytes)
                elif state['phase']=='PLAINTEXT_PENDING':_activate(c,p,state,pin)
        with c.begin():
            if state['phase'] in ('PLAINTEXT_PENDING','PLAINTEXT_ACTIVE'):
                m._active_schema(c,p,state)
                _comments.check(c, p.document['source_plan'], p.operation_id)
            else:m._inspect_paused(c,p,state)
        return m._progress(p,state)


def abort(p,engine,*,pin,approval,plaintext_approval):
    """Discard only pre-switch staging; never replace current application values."""
    with _executor(p,engine,pin,approval,plaintext_approval) as c:
        state=_state(c,p,pin,allow_aborted=True);c.commit()
        if state is None:return m.Progress(p.operation_id,'ABORTED',0,0,'No reverse effects existed.')
        if state['phase']=='ABORTED':return m._progress(p,state)
        if state['phase'] not in ('EXPANDED','BACKFILLED','VERIFIED'):
            raise m.TransitionFailure('plaintext_switch_requires_new_protect_transition',p.operation_id)
        with c.begin():
            m._lock_tables(c,p);m._inspect_paused(c,p,state)
            for original in p.document['lock']['models']:
                model=_model(original)
                for f in model['target_columns']:
                    c.exec_driver_sql(f'ALTER TABLE {m._table(c,model)} DROP COLUMN {m._quote(c,f["payload_column"])}')
            m._drop_guards(c,p)
            for model in p.document['lock']['models']:
                if m._facts(c,model)!=p.document['active_schemas'][model['table_id']]:
                    raise m.TransitionFailure('active_schema_mismatch',p.operation_id)
            source=p.source
            row=c.exec_driver_sql(f'SELECT plan_digest,state FROM {m._journal(c,p)} WHERE operation_id=%s',(source.operation_id,)).one()
            if row[0]!=source.digest or row[1]['phase']!='DEPROTECTING':
                raise m.TransitionFailure('source_state_changed',p.operation_id)
            source_state=row[1];source_state['phase']='ACTIVE';m._save(c,source,source_state)
            state['phase']='ABORTED';m._save(c,p,state)
        return m._progress(p,state)


def _removed(c,p):
    _cutover_ready(c,p)
    if m._target(c)[:-1]!=p.document['target'][:-1]:raise m.TransitionFailure('wrong_database_target',p.operation_id)
    _ordinary_schema(c,p)
    for schema in {x['schema'] for x in p.document['lock']['models']}:
        relation=m._quote(c,schema)+'.'+m._quote(c,m.JOURNAL)
        if c.exec_driver_sql('SELECT pg_catalog.to_regclass(%s)',(relation,)).scalar_one() is not None:
            raise m.TransitionFailure('removal_metadata_survives',p.operation_id)
        for operation in (p,p.source):
            fn=m._guard_names(operation,{'schema':schema})[1]
            if c.exec_driver_sql('SELECT EXISTS(SELECT 1 FROM pg_catalog.pg_proc p JOIN pg_catalog.pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname=%s AND p.proname=%s)',(schema,fn)).scalar_one():
                raise m.TransitionFailure('removal_guard_survives',p.operation_id)


def check_removed(p,engine,*,pin):
    """Read-only host startup/restore check, required outside a package-free app."""
    _pin(p,pin)
    if pin.phase!='REMOVED':raise m.TransitionFailure('removed_publication_required',p.operation_id)
    with m._connection(engine,p.operation_id) as c:_removed(c,p)


def remove(p,engine,*,pin,approval,plaintext_approval,removal_approval):
    """Retire metadata only after host-attested workload/backup verification.

    Attestation strings identify externally checked evidence; this function does
    not authenticate a backup or run the host application on the caller's behalf.
    """
    if type(p) is not DeprotectionPlan:
        raise m.TransitionFailure('external_reverse_policy_mismatch')
    if (type(removal_approval) is not RemovalApproval or removal_approval.plan_digest!=p.digest
            or removal_approval.old_workers_stopped is not True
            or any(type(v) is not str or not v.strip() for v in
                (removal_approval.package_free_workload_evidence,removal_approval.retained_backup_recovery_evidence))):
        raise m.TransitionFailure('removal_evidence_required',p.operation_id)
    if type(pin) is not m.DeploymentPin or pin.phase!='REMOVING':
        raise m.TransitionFailure('removal_publication_required',p.operation_id)
    with _executor(p,engine,pin,approval,plaintext_approval) as c:
        exists=c.exec_driver_sql('SELECT pg_catalog.to_regclass(%s)',(m._journal(c,p),)).scalar_one()
        c.commit()
        with c.begin():
            m._lock_tables(c,p);_cutover_ready(c,p)
            if exists is None:
                _removed(c,p)
                return m.Progress(p.operation_id,'REMOVED',0,0,'Retain external restore checks and encrypted-backup readers/keys.')
            state=_state(c,p,pin)
            if state['phase']!='PLAINTEXT_ACTIVE':raise m.TransitionFailure('plaintext_not_active',p.operation_id)
            m._active_schema(c,p,state);_ordinary_schema(c,p)
            rows=c.exec_driver_sql(f'SELECT operation_id,plan_digest,state FROM {m._journal(c,p)}').all()
            expected={p.operation_id:p.digest,p.source.operation_id:p.source.digest}
            expected.update({UUID(v['operation_id']):v['plan_digest'] for v in p.document['retirable_aborted']})
            if len(rows)!=len(expected) or {r[0]:r[1] for r in rows}!=expected:
                raise m.TransitionFailure('unreviewed_journal_operations',p.operation_id)
            for operation,_,observed in rows:
                if operation in (p.operation_id,p.source.operation_id):continue
                if (observed.get('phase')!='ABORTED' or observed.get('source_operation_id')!=str(p.source.operation_id)
                        or observed.get('source_plan_digest')!=p.source.digest):
                    raise m.TransitionFailure('unreviewed_journal_operations',p.operation_id)
            source_state=next(r[2] for r in rows if r[0]==p.source.operation_id)
            if source_state['phase']!='DEPROTECTING':raise m.TransitionFailure('source_state_changed',p.operation_id)
            # No CASCADE: every unexpected dependent object prevents retirement.
            c.exec_driver_sql(f'DROP TABLE {m._journal(c,p)}')
            _removed(c,p)
        return m.Progress(p.operation_id,'REMOVED',0,0,'Retain external restore checks and encrypted-backup readers/keys.')
