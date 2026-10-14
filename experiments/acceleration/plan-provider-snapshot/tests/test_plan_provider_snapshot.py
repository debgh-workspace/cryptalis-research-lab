"""Planning uses inspected policy metadata, not a second host resolution.

Real disposable PostgreSQL fixtures; run only through the approved lab wrapper.
No provider unwrap, active rotation, key preparation or publication is exercised.
"""
from collections import Counter
from dataclasses import replace
import gc
import hashlib
import json
import traceback
from uuid import UUID, uuid5
import weakref

import pytest

from cryptalis.crypto import Keyring
from cryptalis.crypto.keys import WrappedRoot
from cryptalis.manifest.compiler import SearchReview, Writer, WriterInventory
from cryptalis.migration import TransitionFailure
from test_migration import application, keys, DOMAIN, PROVIDER, TENANT
from test_migration_multitable import multiple_tables, OTHER_TENANT


PRIVATE = 'PRIVATE_SYNTHETIC_RESOLVER_DIAGNOSTIC'


class NoUnwrapProvider:
    provider_id = PROVIDER

    def __init__(self, calls):
        self.calls = calls

    def unwrap(self, *args, **kwargs):
        self.calls.append('unwrap')
        raise AssertionError('Read-only planning must not unwrap roots')

    async def unwrap_async(self, *args, **kwargs):
        self.calls.append('unwrap_async')
        raise AssertionError('Read-only planning must not unwrap roots')


def ring_for(tenant, provider_calls, *, extra=False):
    policy = keys(tenant).policy
    if extra:
        # Public inert wrapper metadata only: no material or active generation change.
        context = replace(policy.wrappers[0].context, generation=2,
                          root_id=uuid5(DOMAIN, 'planning-count-public:' + str(tenant)))
        policy = replace(policy, wrappers=policy.wrappers + (
            WrappedRoot(PROVIDER, context, b'PUBLIC INERT PLANNING WRAPPER'),))
    return Keyring(policy, {PROVIDER: NoUnwrapProvider(provider_calls)})


def policy_digest(policy):
    # Independent byte assembly of the recorded policy metadata fingerprint.
    value = {'domain': str(policy.domain_id), 'tenant': str(policy.tenant_id),
             'payload': policy.payload_generation, 'search': policy.search_generation,
             'wrappers': [{'provider': str(w.provider_id), 'context': {
                 'domain': str(w.context.domain_id), 'tenant': str(w.context.tenant_id),
                 'purpose': w.context.purpose, 'root': str(w.context.root_id),
                 'generation': w.context.generation},
                 'wrapper': hashlib.sha256(w.sealed).hexdigest()} for w in policy.wrappers]}
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def make_plan(app, resolver):
    declaration = app.plan.document['lock']['declaration']
    models = declaration['models']
    return app.m.plan(json.dumps(declaration).encode(), app.mapping, app.owner,
        writers=WriterInventory(True, tuple(Writer(UUID(model['table_id']), 'app',
            'sqlalchemy', evidence='existing synthetic planning fixture') for model in models)),
        search_reviews=tuple(SearchReview(UUID(field['field_id']), False, 'synthetic unbounded names')
            for model in models for field in model['fields'] if field['queries']),
        keys=resolver, runtime_role=app.role, target_id=app.plan.target_id,
        backfill_rows_per_second=1000, verify_rows_per_second=1000,
        temporary_bytes_per_row=700, wal_bytes_per_row=2000)


def native_snapshot(app):
    with app.owner.connect() as c:
        rows = {model['table']: c.exec_driver_sql(
            f'SELECT * FROM "{app.schema}"."{model["table"]}" ORDER BY id').all()
            for model in app.plan.document['lock']['models']}
        objects = c.exec_driver_sql('SELECT c.relname,c.relkind FROM pg_catalog.pg_class c '
            'JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace '
            'WHERE n.nspname=%s ORDER BY c.relname', (app.schema,)).all()
    return rows, objects


@pytest.mark.parametrize('late_result', ['raises', 'invalid_ring', 'different_policy'])
def test_estimate_uses_validated_observation_without_late_resolution(late_result):
    with application() as app:
        before = native_snapshot(app)
        calls, providers, references, expected = [], [], [], {}

        def resolver(tenant):
            calls.append(tenant)
            if len(calls) > 1:
                if late_result == 'raises':
                    raise RuntimeError(PRIVATE)
                if late_result == 'invalid_ring':
                    return None
                return ring_for(tenant, providers, extra=True)
            ring = ring_for(tenant, providers)
            references.append(weakref.ref(ring))
            expected[str(tenant)] = policy_digest(ring.policy)
            return ring

        plan = make_plan(app, resolver)
        assert calls == [TENANT]
        assert plan.document['key_policies'] == expected
        assert plan.document['estimates']['provider_unwraps_per_cold_preparation'] == 2
        assert not providers
        assert native_snapshot(app) == before
        gc.collect()
        assert all(ref() is None for ref in references), 'Plan retained a resolver keyring'
        assert PRIVATE.encode() not in plan.artifact


@pytest.mark.parametrize('failure', ['callback_exception', 'wrong_tenant_policy'])
def test_initial_policy_failure_remains_typed_and_sanitized(failure):
    with application() as app:
        before = native_snapshot(app)
        calls, providers = [], []

        def resolver(tenant):
            calls.append(tenant)
            if failure == 'callback_exception':
                raise RuntimeError(PRIVATE)
            return ring_for(OTHER_TENANT, providers)

        with pytest.raises(TransitionFailure) as caught:
            make_plan(app, resolver)
        assert caught.value.code == ('operation_failed_requires_inspection'
            if failure == 'callback_exception' else 'missing_key_policy')
        assert PRIVATE not in ''.join(traceback.format_exception(caught.value))
        assert caught.value.__cause__ is None
        assert calls == [TENANT] and not providers
        assert native_snapshot(app) == before


def test_multitable_tenants_count_once_and_match_last_validated_policy():
    with multiple_tables() as app:
        before = native_snapshot(app)
        calls, providers, expected, references = Counter(), [], {}, []

        def resolver(tenant):
            calls[tenant] += 1
            if calls[tenant] > 2:
                raise RuntimeError(PRIVATE)
            # Preserve existing per-model inspection. Last observed metadata
            # is what the existing policy dictionary records for that tenant.
            ring = ring_for(tenant, providers, extra=(tenant == OTHER_TENANT and calls[tenant] == 2))
            expected[str(tenant)] = policy_digest(ring.policy)
            references.append(weakref.ref(ring))
            return ring

        plan = make_plan(app, resolver)
        assert calls == Counter({TENANT: 2, OTHER_TENANT: 2})
        assert plan.document['key_policies'] == expected
        assert plan.document['estimates']['provider_unwraps_per_cold_preparation'] == 5
        assert not providers and native_snapshot(app) == before
        gc.collect()
        assert all(ref() is None for ref in references)


def test_direct_keyring_preserves_metadata_estimate_without_unwrap():
    with application() as app:
        providers = []
        ring = ring_for(TENANT, providers, extra=True)
        plan = make_plan(app, ring)
        assert plan.document['estimates']['provider_unwraps_per_cold_preparation'] == 3
        assert plan.document['key_policies'] == {str(TENANT): policy_digest(ring.policy)}
        assert not providers


def test_empty_scoped_table_does_not_resolve_or_unwrap():
    with application(rows=0) as app:
        def forbidden(*args):
            raise AssertionError('No tenant was observed in the empty scoped table')
        plan = make_plan(app, forbidden)
        assert plan.document['key_policies'] == {}
        assert plan.document['estimates']['provider_unwraps_per_cold_preparation'] == 0
