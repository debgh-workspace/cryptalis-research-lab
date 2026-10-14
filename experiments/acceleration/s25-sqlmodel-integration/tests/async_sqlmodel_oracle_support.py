"""Pinned owned-lab fixture closure. Importing this module performs no DB work."""
import hashlib
import hmac
import json
import os
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
import sys
from uuid import UUID

import psycopg
import pytest
import sqlalchemy
import sqlmodel
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from sqlalchemy import Column, Integer, Table, Text, Uuid, event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession as NativeAsyncSession
from sqlmodel import Session as NativeSession
from sqlmodel.sql.sqltypes import AutoString

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT.parent
PACKET = LAB / 'experiments/s25-async-sqlmodel-integration-20261014'
if ROOT != LAB / 'candidate-s25-async-sqlmodel-integration-20261014' or Path.cwd().resolve() != ROOT:
    raise RuntimeError('Exact reviewed S25 source root is required')
import test_sqlalchemy_search as fixture
import cryptalis
import cryptalis.sqlalchemy as adapter
import cryptalis._sqlmodel_support as support


def write_record(name, data):
    destination = Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent / name
    with destination.open('a') as stream:
        stream.write(json.dumps(data, sort_keys=True) + '\n')


def origin_check():
    if not __debug__ or sys.flags.optimize != 0:
        raise RuntimeError('Assertions must remain enabled')
    if sys.version_info[:3] != (3, 14, 8):
        raise RuntimeError('Expected existing Python 3.14.8 cell')
    if sqlalchemy.__version__ != '2.0.51' or sqlmodel.__version__ != '0.0.47' or psycopg.__version__ != '3.3.6':
        raise RuntimeError('Expected existing SQLModel 0.0.47 / SQLAlchemy 2.0.51 / psycopg 3.3.6 cell')
    expected_origins = {
        cryptalis: ROOT / 'src/cryptalis/__init__.py',
        adapter: ROOT / 'src/cryptalis/sqlalchemy.py',
        support: ROOT / 'src/cryptalis/_sqlmodel_support.py',
        fixture: ROOT / 'tests/test_sqlalchemy_search.py',
    }
    for module, expected in expected_origins.items():
        if Path(module.__file__).resolve() != expected.resolve():
            raise RuntimeError('Imported source origin differs from selected candidate')
    manifest_name = 'CANDIDATE_SOURCE_MANIFEST.json'
    manifest = json.loads((PACKET / manifest_name).read_text())
    if len(manifest['source_sha256']) != 216:
        raise RuntimeError('Expected complete 216-file input inventory')
    for relative, digest in manifest['source_sha256'].items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Selected source differs from frozen manifest: ' + relative)
    dependency_pins = json.loads((PACKET / 'DEPENDENCY_SOURCE_PINS.json').read_text())
    prefix = Path(sys.prefix).resolve()
    if prefix != (LAB / 'release-lab/cp84-adoption/sqlmodel-wheel-venv').resolve():
        raise RuntimeError('The reviewed existing dependency environment is required')
    for module in (sqlalchemy, sqlmodel, psycopg):
        if not Path(module.__file__).resolve().is_relative_to(prefix):
            raise RuntimeError('Dependency import origin is outside reviewed environment')
    for relative, digest in dependency_pins.items():
        if hashlib.sha256((prefix / relative).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Dependency source pin differs: ' + relative)
    from sqlmodel.ext.asyncio import session as native_module
    from sqlalchemy.ext.asyncio import result as result_module
    assert native_module.AsyncSession is NativeAsyncSession
    assert NativeAsyncSession.exec.__globals__['_ensure_sync_result'] is result_module._ensure_sync_result
    write_record('async-sqlmodel-origin.jsonl', {
        'source_root': str(ROOT), 'python': list(sys.version_info[:3]),
        'sqlalchemy': sqlalchemy.__version__, 'sqlmodel': sqlmodel.__version__,
        'psycopg': psycopg.__version__, 'source_files': 216,
        'dependency_files': len(dependency_pins),
        'origins': {module.__name__: str(Path(module.__file__).resolve()) for module in expected_origins},
        'native_async': str(Path(native_module.__file__).resolve()),
        'native_result': str(Path(result_module.__file__).resolve()),
        'status': 'verified_at_test_module_setup',
    })


def enable(monkeypatch):
    # On baseline this inert test attribute does not replace its refusal.
    monkeypatch.setattr(support, '_experimental_async_sqlmodel', True, raising=False)


@contextmanager
def application(protected, *, relationships=False, public_table=False):
    with fixture.search_application(protected, attach_now=False,
            field_type=AutoString(32, collation='C'), sqlmodel_model=True,
            relationship_model=relationships) as app:
        if public_table:
            table = Table('public_task', app.mapping.metadata,
                Column('id', Uuid, primary_key=True, autoincrement=False),
                Column('label', Text), Column('rank', Integer))
            class PublicTask:
                pass
            app.mapping.map_imperatively(PublicTask, table)
            table.create(app.owner_engine)
            with app.engine.connect() as connection:
                role = connection.exec_driver_sql('select current_user').scalar_one()
            with app.owner_engine.begin() as connection:
                quote = connection.dialect.identifier_preparer.quote_identifier
                target = quote(app.schema) + '.public_task'
                connection.exec_driver_sql('GRANT SELECT, INSERT, UPDATE, DELETE ON ' + target + ' TO ' + quote(role))
                connection.execute(table.insert(), [
                    {'id': UUID(int=2000), 'label': None, 'rank': 0},
                    {'id': UUID(int=2002), 'label': 'old-2', 'rank': 2},
                ])
            app.public_table, app.PublicTask = table, PublicTask
        yield app


@asynccontextmanager
async def sessions_for(app, *, keys=None, public_update=False):
    engine = create_async_engine('postgresql+psycopg://', echo=False, hide_parameters=True,
        async_creator=lambda: psycopg.AsyncConnection.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
    try:
        if app.protected:
            factory = await adapter.attach(app.mapping, engine, lock=app.plan.lock_bytes,
                keys=app.keys if keys is None else keys)
            if public_update:
                factory._owner._experimental_public_update_tables = (app.public_table,)
        else:
            native = async_sessionmaker(engine, class_=NativeAsyncSession)
            def factory(*, tenant_id, **options):
                return native(**options)
        yield engine, factory
        assert engine.sync_engine.pool.checkedout() == 0
    finally:
        await engine.dispose()


def row(app, value, rank, *, tenant=None):
    return app.Customer(id=UUID(int=1000 + rank), tenant_id=tenant or app.tenant,
        name=value, rank=rank, label='public-label')


def native_membership(session, protected):
    assert isinstance(session, NativeAsyncSession)
    assert isinstance(session.sync_session, NativeSession)
    if protected:
        assert isinstance(session, adapter._AsyncSession)
        assert isinstance(session.sync_session, adapter._Session)
        assert session.sync_session._asynchronous is True
    else:
        assert type(session) is NativeAsyncSession
        assert type(session.sync_session) is NativeSession


def owner_rows(app):
    with app.owner_engine.connect() as connection:
        return [tuple(value) for value in connection.exec_driver_sql(
            f'SELECT id,tenant_id,name,rank FROM "{app.schema}".customer ORDER BY rank')]


def public_rows(app):
    with app.owner_engine.connect() as connection:
        return [tuple(value) for value in connection.exec_driver_sql(
            f'SELECT id,label,rank FROM "{app.schema}".public_task ORDER BY id')]


def independent_open(app, body, tenant, record):
    """Independent CF1 framing/HKDF/HMAC path; existing development root unwrap.

    This does not qualify provider custody and does not call product frame open,
    product key derivation, or product result processors.
    """
    if body is None:
        return None
    descriptor = json.loads(app.plan.lock_bytes)['models'][0]['fields'][0]['descriptor']
    domain, field_id = fixture.DOMAIN, fixture.FIELD_ID
    def pack(*parts):
        return len(parts).to_bytes(4, 'big') + b''.join(len(p).to_bytes(4, 'big') + p for p in parts)
    def derive(purpose, info):
        wrapper = next(w for w in app.rings[tenant].policy.wrappers if w.context.purpose == purpose)
        context = wrapper.context
        root = app.provider.unwrap(wrapper, context)
        salt = hashlib.sha256(pack(b'CF1/root', domain.bytes, tenant.bytes,
            context.root_id.bytes, context.generation.to_bytes(4, 'big'))).digest()
        return hmac.digest(hmac.digest(salt, root, 'sha256'), info + b'\x01', 'sha256')
    assert body[:14] == bytes.fromhex('4346310001010000000100000001')
    header = body[:46]
    key = derive('payload', pack(b'CF1/payload-key', field_id.bytes, record.bytes))
    digest = hashlib.sha256(json.dumps(descriptor, sort_keys=True, separators=(',', ':')).encode()).digest()
    aad = pack(b'CF1/payload', domain.bytes, tenant.bytes, field_id.bytes, record.bytes, digest, header)
    value = AESGCMSIV(key).decrypt(body[46:58], body[58:], aad)
    search_key = derive('search', pack(b'CF1/search-key', field_id.bytes,
        b'utf8-exact/v1', b'identity/v1', b'equality'))
    assert hmac.compare_digest(header[14:46], hmac.digest(search_key, pack(b'equality', value), 'sha256'))
    return value.decode('utf8')


def parameter_leaves(value):
    if isinstance(value, dict):
        for part in value.values():
            yield from parameter_leaves(part)
    elif isinstance(value, (tuple, list)):
        for part in value:
            yield from parameter_leaves(part)
    else:
        yield value
