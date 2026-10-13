"""Inactive, exact-inventory root-rewrap proposals for local investigation.

No database, journal, external pin, credentials, or custody files are modified.
This format is deliberately NOT admitted by runtime or maintenance dispatch.
A structurally valid artifact is neither authenticated nor currently active.
Wrapped policies remain caller-owned; this artifact contains only identities
and policy fingerprints, never root bytes or a substitute recovery wrapper.
"""
from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest
from uuid import UUID, uuid4

from cryptalis import migration as m
from cryptalis._transition_json import decode_transition_json
from cryptalis.crypto.keys import KeyContext, Keyring

FORMAT = 'cryptalis.root-rewrap/inactive-research-v1'
_FIELDS = {'format', 'kind', 'operation_id', 'target_id', 'source_operation_id',
           'source_artifact_digest', 'schema_lock_digest', 'source_key_policies',
           'target_key_policies', 'inventory'}
_CONTEXT_FIELDS = {'domain_id', 'tenant_id', 'purpose', 'root_id', 'generation'}
_INVENTORY_FIELDS = {'domain_id', 'tenant_id', 'payload_generation', 'search_generation', 'roots'}


def _uuid(value, *, nil=False):
    if type(value) is not str:
        raise ValueError
    parsed = UUID(value)
    if str(parsed) != value or (not nil and not parsed.int):
        raise ValueError
    return parsed


def _digest(value):
    if type(value) is not str or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
        raise ValueError


def _generation(value):
    if type(value) is not int or not 1 <= value <= 0xffffffff:
        raise ValueError


def _inventory(policy):
    return {'domain_id': str(policy.domain_id), 'tenant_id': str(policy.tenant_id),
            'payload_generation': policy.payload_generation, 'search_generation': policy.search_generation,
            'roots': [{'domain_id': str(w.context.domain_id), 'tenant_id': str(w.context.tenant_id),
                       'purpose': w.context.purpose, 'root_id': str(w.context.root_id),
                       'generation': w.context.generation}
                      for w in sorted(policy.wrappers, key=lambda w: (w.context.purpose, w.context.generation))]}


def _check_inventory(tenant, value):
    if type(value) is not dict or set(value) != _INVENTORY_FIELDS:
        raise ValueError
    domain = _uuid(value['domain_id'])
    if _uuid(value['tenant_id'], nil=True) != tenant:
        raise ValueError
    _generation(value['payload_generation'])
    if value['search_generation'] is not None:
        _generation(value['search_generation'])
    roots = value['roots']
    if type(roots) is not list or not 1 <= len(roots) <= 32:
        raise ValueError
    identities, root_ids, ordering = set(), set(), []
    for item in roots:
        if type(item) is not dict or set(item) != _CONTEXT_FIELDS:
            raise ValueError
        context = KeyContext(_uuid(item['domain_id']), _uuid(item['tenant_id'], nil=True),
                             item['purpose'], _uuid(item['root_id']), item['generation'])
        identity = (context.purpose, context.generation)
        if ((context.domain_id, context.tenant_id) != (domain, tenant)
                or identity in identities or context.root_id in root_ids):
            raise ValueError
        identities.add(identity); root_ids.add(context.root_id); ordering.append(identity)
    if (ordering != sorted(ordering)
            or ('payload', value['payload_generation']) not in identities
            or (value['search_generation'] is not None
                and ('search', value['search_generation']) not in identities)):
        raise ValueError


@dataclass(frozen=True)
class RootRewrapPlan:
    """Strict inactive proposal; construction does not verify roots or authority."""
    artifact: bytes

    def __post_init__(self):
        try:
            if type(self.artifact) is not bytes:
                raise ValueError
            d = decode_transition_json(self.artifact)
            if (set(d) != _FIELDS or d['format'] != FORMAT or d['kind'] != 'root_rewrap'
                    or m._canonical(d) != self.artifact):
                raise ValueError
            operation = _uuid(d['operation_id'])
            if operation == _uuid(d['source_operation_id']):
                raise ValueError
            _uuid(d['target_id'])
            for name in ('source_artifact_digest', 'schema_lock_digest'):
                _digest(d[name])
            inventory = d['inventory']
            if type(inventory) is not dict or not inventory:
                raise ValueError
            for name in ('source_key_policies', 'target_key_policies'):
                policies = d[name]
                if type(policies) is not dict or set(policies) != set(inventory):
                    raise ValueError
                for digest in policies.values():
                    _digest(digest)
            domains = set()
            for tenant, value in inventory.items():
                _check_inventory(_uuid(tenant, nil=True), value)
                domains.add(value['domain_id'])
            if len(domains) != 1:
                raise ValueError
        except Exception:
            raise m.TransitionFailure('invalid_rewrap_plan') from None

    @property
    def document(self):
        return decode_transition_json(self.artifact)

    @property
    def digest(self):
        return sha256(self.artifact).hexdigest()

    @property
    def target_id(self):
        return UUID(self.document['target_id'])

    @property
    def operation_id(self):
        return UUID(self.document['operation_id'])


def _source(source, pin):
    if type(source) is not m.MigrationPlan or type(pin) is not m.DeploymentPin:
        raise m.TransitionFailure('rewrap_source_not_active')
    m._admit(source, pin)
    if pin.phase != 'ACTIVE':
        raise m.TransitionFailure('rewrap_source_not_active', source.operation_id)
    # The source pin is a host assertion. This pure prerequisite does not
    # inspect the database or establish that the assertion is current.
    return source.document


def _rings(source, source_keys, target_keys):
    policies = source.document['key_policies']
    if (type(policies) is not dict or not policies
            or type(source_keys) is not dict or type(target_keys) is not dict):
        raise m.TransitionFailure('rewrap_inventory_mismatch', source.operation_id)
    tenants = tuple(sorted((_uuid(t, nil=True) for t in policies), key=lambda t: t.bytes))
    if (any(type(t) is not UUID for t in source_keys) or any(type(t) is not UUID for t in target_keys)
            or set(source_keys) != set(tenants) or set(target_keys) != set(tenants)):
        raise m.TransitionFailure('rewrap_inventory_mismatch', source.operation_id)
    # Copy the exact finite references before provider callbacks begin. No
    # callable resolver may silently supply an incomplete tenant inventory.
    pairs = []
    for tenant in tenants:
        old, new = source_keys[tenant], target_keys[tenant]
        m._ring(old, tenant, source)
        if (type(new) is not Keyring or _inventory(new.policy) != _inventory(old.policy)):
            raise m.TransitionFailure('rewrap_inventory_mismatch', source.operation_id)
        pairs.append((tenant, old, new))
    return tuple(pairs)


def _matches_source(plan, source, pin):
    d = _source(source, pin)
    if type(plan) is not RootRewrapPlan:
        raise m.TransitionFailure('invalid_rewrap_plan')
    p = plan.document
    if (p['source_operation_id'] != str(source.operation_id)
            or p['target_id'] != str(source.target_id)
            or p['source_artifact_digest'] != source.digest
            or p['schema_lock_digest'] != sha256(source.lock_bytes).hexdigest()
            or p['source_key_policies'] != d['key_policies']):
        raise m.TransitionFailure('rewrap_source_artifact_changed', plan.operation_id)


def verify(plan, source, *, source_pin, source_keys, target_keys):
    """Recheck every bound root; return no activation token or persistent receipt.

    Warm material can be used only within its already-issued lease. This does
    not immediately detect provider disablement, cancel blocking provider calls,
    establish external custody, or replace a publication-time database check.
    """
    try:
        _matches_source(plan, source, source_pin)
        pairs = _rings(source, source_keys, target_keys)
        d = plan.document
        snapshots = []
        for tenant, old, new in pairs:
            name = str(tenant)
            if (d['inventory'][name] != _inventory(old.policy)
                    or d['target_key_policies'][name] != m._policy(new)):
                raise m.TransitionFailure('rewrap_key_policy_changed', plan.operation_id)
            old_keys, new_keys = old.prepare(), new.prepare()
            for wrapper in old_keys.policy.wrappers:
                c = wrapper.context
                a = old_keys._resolve(c.domain_id, c.tenant_id, c.purpose, c.generation)
                b = new_keys._resolve(c.domain_id, c.tenant_id, c.purpose, c.generation)
                if a.context != c or b.context != c or not compare_digest(a.root, b.root):
                    raise m.TransitionFailure('rewrap_root_mismatch', plan.operation_id)
            snapshots.extend((old_keys, new_keys))
        # A later tenant/provider call cannot outlive any earlier root lease.
        for prepared in snapshots:
            for wrapper in prepared.policy.wrappers:
                c = wrapper.context
                prepared._resolve(c.domain_id, c.tenant_id, c.purpose, c.generation)
        # Callbacks must not change the policy after its initial admission.
        for tenant, old, new in pairs:
            if (m._policy(old) != d['source_key_policies'][str(tenant)]
                    or m._policy(new) != d['target_key_policies'][str(tenant)]):
                raise m.TransitionFailure('rewrap_key_policy_changed', plan.operation_id)
    except m.TransitionFailure:
        raise
    except Exception:
        raise m.TransitionFailure('rewrap_key_verification_failed',
                                  plan.operation_id if type(plan) is RootRewrapPlan else None) from None


def prepare(source, *, source_pin, source_keys, target_keys):
    """Bind already-wrapped candidates to one exact ACTIVE source proposal.

    The source must be an original MigrationPlan in this first bounded slice.
    Successor chains, journal publication and rollback are not implemented.
    Exact old wrappers must remain separately available for backup recovery.
    """
    try:
        d = _source(source, source_pin)
        pairs = _rings(source, source_keys, target_keys)
        artifact = m._canonical({'format': FORMAT, 'kind': 'root_rewrap',
            'operation_id': str(uuid4()), 'target_id': str(source.target_id),
            'source_operation_id': str(source.operation_id), 'source_artifact_digest': source.digest,
            'schema_lock_digest': sha256(source.lock_bytes).hexdigest(),
            'source_key_policies': d['key_policies'],
            'target_key_policies': {str(t): m._policy(new) for t, _, new in pairs},
            'inventory': {str(t): _inventory(old.policy) for t, old, _ in pairs}})
        plan = RootRewrapPlan(artifact)
        verify(plan, source, source_pin=source_pin, source_keys=source_keys, target_keys=target_keys)
        return plan
    except m.TransitionFailure:
        raise
    except Exception:
        raise m.TransitionFailure('rewrap_key_verification_failed') from None
