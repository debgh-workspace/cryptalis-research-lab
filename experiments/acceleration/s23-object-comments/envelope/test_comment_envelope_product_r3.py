"""Future pure constructor/helper differential controls; NOT RUN in preparation.

Expected bytes come only from envelope_oracle's stdlib JSON. No DB/API effects,
monkeypatches, credential reads, subprocesses, or source writes are performed.
The isolated candidate must be selected explicitly through PYTHONPATH by root.
Synthetic inner schemas/lock facts are not compiler or native catalog evidence.
"""
import copy
import importlib
import hashlib
import json
import math
from pathlib import Path
import unittest
from uuid import UUID

import envelope_oracle as oracle


class CommentEnvelopeDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Verify the independently reviewed frozen source before any product import.
        base = Path(__file__).resolve().parents[2]
        candidate = base / 'candidate-s23-object-comments-correction-r3-20261014'
        manifest = base / 'experiments/s23-object-comments-green-r3-20261014/CANDIDATE_SOURCE_MANIFEST.json'
        manifest_bytes = manifest.read_bytes()
        if hashlib.sha256(manifest_bytes).hexdigest() != 'eef841a5ee605a8763784640b841a62931f15767e3616f33bb4bb40170b96323':
            raise RuntimeError('FROZEN_CANDIDATE_MANIFEST_MISMATCH')
        pins = json.loads(manifest_bytes)['source_sha256']
        if len(pins) != 214 or any(hashlib.sha256((candidate / rel).read_bytes()).hexdigest() != digest
                                   for rel, digest in pins.items()):
            raise RuntimeError('FROZEN_CANDIDATE_SOURCE_MISMATCH')
        # Imports occur only when an authorized coordinator executes this file.
        cls.helper = importlib.import_module('cryptalis._object_comments')
        cls.migration = importlib.import_module('cryptalis.migration')
        cls.reverse = importlib.import_module('cryptalis.deprotection')
        expected = candidate / 'src/cryptalis/_object_comments.py'
        if Path(cls.helper.__file__).resolve() != expected.resolve():
            raise RuntimeError('WRONG_ISOLATED_CANDIDATE_ORIGIN')

    def reject_forward(self, source):
        with self.assertRaises(self.migration.TransitionFailure) as caught:
            self.migration.MigrationPlan(oracle.canonical_bytes(source))
        self.assertEqual(caught.exception.code, 'invalid_plan')
        self.assertNotIn('quoted', str(caught.exception))

    def reject_reverse(self, reverse):
        with self.assertRaises(self.migration.TransitionFailure) as caught:
            self.reverse.DeprotectionPlan(oracle.canonical_bytes(reverse))
        self.assertEqual(caught.exception.code, 'invalid_reverse_plan')

    def test_independent_bound_matches_complete_encoded_skeleton(self):
        for payload in (None, '', oracle.ESCAPING_PREFIX, '雪' * 37, '\x01' * 63):
            with self.subTest(payload=repr(payload)):
                source = oracle.source_fixture(payload)
                expected = oracle.envelope_measurements(source)
                self.assertEqual(self.helper.reverse_envelope_bound(source), expected['bound_bytes'])
                self.helper.validate_forward(source)
                self.migration.MigrationPlan(oracle.canonical_bytes(source))
        self.assertEqual(self.helper.ACTIVE_SCHEMA_BYTES, oracle.SECTION_CAPS['active_schemas'])
        self.assertEqual(self.helper.HISTORY_BYTES, oracle.SECTION_CAPS['retirable_aborted'])
        self.assertEqual(self.helper.READINESS_BYTES, oracle.SECTION_CAPS['cutover_readiness'])

    def test_whole_reserved_bound_m_minus_one_m_m_plus_one(self):
        for delta in (-1, 0, 1):
            with self.subTest(delta=delta):
                source = oracle.calibrated_source_bound(oracle.MAX_BYTES + delta)
                expected = oracle.envelope_measurements(source)
                self.assertEqual(expected['bound_bytes'], oracle.MAX_BYTES + delta)
                self.assertLess(expected['source_bytes'], oracle.MAX_BYTES)
                self.assertEqual(self.helper.reverse_envelope_bound(source), expected['bound_bytes'])
                if delta <= 0:
                    self.helper.validate_forward(source)
                    self.migration.MigrationPlan(oracle.canonical_bytes(source))
                else:
                    with self.assertRaises(self.helper.ContractError) as caught:
                        self.helper.validate_forward(source)
                    self.assertEqual(caught.exception.code, 'object_comments_reverse_envelope_exceeded')
                    self.reject_forward(source)

    def test_per_section_adjacent_byte_limits_are_independent(self):
        errors = {'active_schemas': 'object_comments_schema_budget_exceeded',
                  'retirable_aborted': 'object_comments_history_budget_exceeded',
                  'cutover_readiness': 'object_comments_readiness_budget_exceeded'}
        for name, cap in oracle.SECTION_CAPS.items():
            for delta in (-1, 0, 1):
                with self.subTest(section=name, delta=delta):
                    reverse = oracle.reverse_fixture()
                    reverse[name] = oracle.section_at_size(name, cap + delta)
                    self.assertEqual(oracle.byte_size(reverse[name]), cap + delta)
                    self.assertLess(oracle.byte_size(reverse), oracle.MAX_BYTES)
                    if delta <= 0:
                        self.helper.validate_reverse(reverse)
                    else:
                        with self.assertRaises(self.helper.ContractError) as caught:
                            self.helper.validate_reverse(reverse)
                        self.assertEqual(caught.exception.code, errors[name])
                    if name == 'retirable_aborted':
                        # Padding is intentionally not a valid history member.
                        # The byte helper result must not be called reader admission.
                        self.reject_reverse(reverse)
                    elif delta <= 0:
                        self.reverse.DeprotectionPlan(oracle.canonical_bytes(reverse))
                    else:
                        self.reject_reverse(reverse)

    def test_actual_encoded_reverse_near_all_reservations_is_within_bound(self):
        source = oracle.calibrated_source_bound(oracle.MAX_BYTES)
        reverse = oracle.actual_reserved_reverse(source)
        expected_bound = oracle.envelope_measurements(source)['bound_bytes']
        actual_bytes = oracle.canonical_bytes(reverse)
        self.assertLessEqual(len(actual_bytes), expected_bound)
        self.assertLessEqual(len(actual_bytes), oracle.MAX_BYTES)
        self.helper.validate_forward(source)
        self.helper.validate_reverse(reverse)
        restored = self.reverse.DeprotectionPlan(actual_bytes)
        self.assertEqual(restored.artifact, actual_bytes)

    def test_nearest_valid_history_limit_and_one_more_entry(self):
        reverse = oracle.reverse_fixture()
        reverse['retirable_aborted'] = oracle.maximal_valid_history()
        self.assertLessEqual(oracle.byte_size(reverse['retirable_aborted']),
                             oracle.SECTION_CAPS['retirable_aborted'])
        self.reverse.DeprotectionPlan(oracle.canonical_bytes(reverse))
        reverse['retirable_aborted'].append({
            'operation_id': str(UUID(int=100 + len(reverse['retirable_aborted']))),
            'plan_digest': 'c' * 64})
        self.assertGreater(oracle.byte_size(reverse['retirable_aborted']),
                           oracle.SECTION_CAPS['retirable_aborted'])
        with self.assertRaises(self.helper.ContractError) as caught:
            self.helper.validate_reverse(reverse)
        self.assertEqual(caught.exception.code, 'object_comments_history_budget_exceeded')
        self.reject_reverse(reverse)

    def test_canonical_nonzero_forward_uuid_spellings(self):
        for path in (('operation_id',), ('target_id',),
                     ('object_comments', 'tables', 0, 'table_id')):
            for mutation in ('upper', 'hex', 'braces', 'zero', 'bool', 'int'):
                with self.subTest(path=path, mutation=mutation):
                    source = oracle.source_fixture()
                    parent = source
                    for part in path[:-1]:
                        parent = parent[part]
                    value = parent[path[-1]]
                    parent[path[-1]] = {'upper': value.upper(), 'hex': UUID(value).hex,
                        'braces': '{' + value + '}', 'zero': str(UUID(int=0)),
                        'bool': True, 'int': 1}[mutation]
                    self.assertFalse(oracle.canonical_uuid(parent[path[-1]]))
                    self.reject_forward(source)

    def test_canonical_nonzero_reverse_and_source_pin_uuid_spellings(self):
        for path in (('operation_id',), ('target_id',),
                     ('source_pin', 'operation_id'), ('source_pin', 'target_id')):
            for mutation in ('upper', 'hex', 'braces', 'zero', 'bool'):
                with self.subTest(path=path, mutation=mutation):
                    reverse = oracle.reverse_fixture()
                    parent = reverse
                    for part in path[:-1]:
                        parent = parent[part]
                    value = parent[path[-1]]
                    parent[path[-1]] = {'upper': value.upper(), 'hex': UUID(value).hex,
                        'braces': '{' + value + '}', 'zero': str(UUID(int=0)), 'bool': True}[mutation]
                    self.reject_reverse(reverse)

    def test_counters_exact_types_and_range(self):
        for name in oracle.COUNTER_NAMES:
            for value in (0, 2**53 - 1, -1, 2**53, True, False, 1.0, '1', None):
                with self.subTest(counter=name, value=repr(value)):
                    reverse = oracle.reverse_fixture()
                    reverse['estimates'][name] = value
                    if oracle.valid_counter(value):
                        self.helper.validate_reverse(reverse)
                        self.reverse.DeprotectionPlan(oracle.canonical_bytes(reverse))
                    else:
                        with self.assertRaises(self.helper.ContractError):
                            self.helper.validate_reverse(reverse)
                        self.reject_reverse(reverse)

    def test_rates_strict_values_and_layered_encoded_cap(self):
        valid = (1, 2**53 - 1, 1.5, 5e-324, float.fromhex('0x1.fffffffffffffp+1023'))
        for name in oracle.RATE_NAMES:
            for value in valid:
                with self.subTest(rate=name, value=value):
                    reverse = oracle.reverse_fixture()
                    reverse['estimates'][name] = value
                    self.assertTrue(oracle.valid_rate(value))
                    self.helper.validate_reverse(reverse)
                    self.reverse.DeprotectionPlan(oracle.canonical_bytes(reverse))
            for value in (0, -1, 0.0, -1.5, True, False, '1', None, float('nan'), float('inf')):
                with self.subTest(rate=name, invalid=repr(value)):
                    reverse = oracle.reverse_fixture()
                    reverse['estimates'][name] = value
                    with self.assertRaises(self.helper.ContractError):
                        self.helper.validate_reverse(reverse)
                    if type(value) is not float or math.isfinite(value):
                        self.reject_reverse(reverse)
                    else:
                        raw = json.dumps(reverse, sort_keys=True, separators=(',', ':'),
                                         ensure_ascii=False, allow_nan=True).encode('utf8')
                        with self.assertRaises(self.migration.TransitionFailure) as caught:
                            self.reverse.DeprotectionPlan(raw)
                        self.assertEqual(caught.exception.code, 'invalid_reverse_plan')
            for digits in (31, 32, 33):
                with self.subTest(rate=name, size_layer_digits=digits):
                    reverse = oracle.reverse_fixture()
                    reverse['estimates'][name] = 10 ** (digits - 1)
                    self.assertEqual(oracle.byte_size(reverse['estimates'][name]), digits)
                    self.assertFalse(oracle.valid_rate(reverse['estimates'][name]))
                    if digits <= 32:
                        self.helper.validate_reverse(reverse)
                    else:
                        with self.assertRaises(self.helper.ContractError) as caught:
                            self.helper.validate_reverse(reverse)
                        self.assertEqual(caught.exception.code, 'object_comments_rate_budget_exceeded')
                    # Existing complete-artifact integer grammar rejects all three.
                    self.reject_reverse(reverse)

    def test_role_utf8_and_escaped_byte_limits(self):
        for value in ('a' * 63, '雪' * 21, '\x01' * 63,
                      'a' * 64, '雪' * 22, '', '\x00', True, 1):
            with self.subTest(role=repr(value)):
                reverse = oracle.reverse_fixture()
                reverse['plaintext_runtime_role'] = value
                if oracle.valid_role(value):
                    self.assertLessEqual(oracle.byte_size(value), 380)
                    self.helper.validate_reverse(reverse)
                    self.reverse.DeprotectionPlan(oracle.canonical_bytes(reverse))
                else:
                    with self.assertRaises(self.helper.ContractError):
                        self.helper.validate_reverse(reverse)
                    self.reject_reverse(reverse)
        reverse = oracle.reverse_fixture()
        reverse['plaintext_runtime_role'] = reverse['runtime_role']
        self.reject_reverse(reverse)

    def test_forward_inventory_exact_keysets_null_and_missing(self):
        source = oracle.source_fixture(None)
        self.migration.MigrationPlan(oracle.canonical_bytes(source))
        paths = [(), ('object_comments',), ('object_comments', 'tables', 0),
                 ('object_comments', 'tables', 0, 'constraints', 0),
                 ('object_comments', 'tables', 0, 'indexes', 0)]
        for path in paths:
            for mode in ('extra', 'missing'):
                with self.subTest(path=path, mode=mode):
                    source = oracle.source_fixture(None)
                    container = source
                    for member in path:
                        container = container[member]
                    if mode == 'extra':
                        container['unreviewed_extension'] = None
                    else:
                        container.pop('object_comments' if not path else
                                      'comment' if 'comment' in container else next(iter(container)))
                    self.reject_forward(source)
        for value in (True, 1, [], {}):
            source = oracle.source_fixture(value)
            self.reject_forward(source)
        source = oracle.source_fixture()
        source['object_comments']['tables'][0]['indexes'][1]['constraint_name'] = None
        self.reject_forward(source)
        source = oracle.source_fixture()
        source['object_comments']['tables'][0]['indexes'].append(
            copy.deepcopy(source['object_comments']['tables'][0]['indexes'][0]))
        self.reject_forward(source)

    def test_reverse_exact_keysets_identity_links_and_policy_subset(self):
        for path in ((), ('source_pin',), ('estimates',)):
            for mode in ('extra', 'missing'):
                with self.subTest(path=path, mode=mode):
                    reverse = oracle.reverse_fixture()
                    container = reverse
                    for member in path:
                        container = container[member]
                    if mode == 'extra':
                        container['unreviewed_extension'] = None
                    else:
                        container.pop(next(iter(container)))
                    self.reject_reverse(reverse)
        reverse = oracle.reverse_fixture()
        reverse['estimates']['limits'] += ' extra'
        self.reject_reverse(reverse)
        reverse = oracle.reverse_fixture()
        reverse['source_pin']['plan_digest'] = '0' * 64
        self.reject_reverse(reverse)
        reverse = oracle.reverse_fixture()
        reverse['lock']['domain_id'] = str(UUID(int=999))
        self.reject_reverse(reverse)
        for policies in ({}, {oracle.TENANT_ID: 'a' * 64},
                         {oracle.TENANT_ID: 'a' * 64, oracle.OTHER_TENANT: 'b' * 64}):
            reverse = oracle.reverse_fixture()
            reverse['key_policies'] = policies
            self.helper.validate_reverse(reverse)
            self.reverse.DeprotectionPlan(oracle.canonical_bytes(reverse))
        for policies in ({oracle.TENANT_ID: 'c' * 64}, {str(UUID(int=99)): 'a' * 64}, []):
            reverse = oracle.reverse_fixture()
            reverse['key_policies'] = policies
            with self.assertRaises(self.helper.ContractError):
                self.helper.validate_reverse(reverse)
            self.reject_reverse(reverse)

    def test_canonical_bytes_duplicate_members_and_invalid_unicode_refuse(self):
        source = oracle.source_fixture()
        raw = oracle.canonical_bytes(source)
        self.migration.MigrationPlan(raw)
        escaped = json.dumps(source, sort_keys=True, separators=(',', ':'),
                             ensure_ascii=True, allow_nan=False).encode('utf8')
        self.assertNotEqual(escaped, raw)
        duplicate = raw.replace(b'"kind":"protect"',
                                b'"kind":"protect","kind":"protect"', 1)
        invalid_unicode = raw.replace('雪'.encode('utf8'), b'\\ud800', 1)
        for malformed in (escaped, duplicate, invalid_unicode):
            with self.subTest(kind=malformed[:12]):
                with self.assertRaises(self.migration.TransitionFailure) as caught:
                    self.migration.MigrationPlan(malformed)
                self.assertEqual(caught.exception.code, 'invalid_plan')

    def test_duplicate_lock_and_target_require_json_type_identity(self):
        # Each mutation leaves Python equality true, but changes canonical JSON.
        # These are ordinary invalid-artifact controls, without database effects.
        for mutation in ('nullable_bool_to_int', 'attnum_int_to_bool', 'port_int_to_bool'):
            with self.subTest(mutation=mutation):
                source = oracle.source_fixture()
                if mutation == 'attnum_int_to_bool':
                    source['lock']['models'][0]['source_schema']['columns'] = [
                        {'name': 'id', 'attnum': 1}]
                if mutation == 'port_int_to_bool':
                    source['target'][3] = 1
                self.migration.MigrationPlan(oracle.canonical_bytes(source))
                reverse = oracle.reverse_fixture(source)
                self.reverse.DeprotectionPlan(oracle.canonical_bytes(reverse))
                if mutation == 'nullable_bool_to_int':
                    reverse['lock']['models'][0]['fields'][0]['source']['nullable'] = 1
                    name = 'lock'
                elif mutation == 'attnum_int_to_bool':
                    reverse['lock']['models'][0]['source_schema']['columns'][0]['attnum'] = True
                    name = 'lock'
                else:
                    reverse['target'][3] = True
                    name = 'target'
                self.assertEqual(reverse[name], reverse['source_plan'][name])
                self.assertNotEqual(oracle.canonical_bytes(reverse[name]),
                                    oracle.canonical_bytes(reverse['source_plan'][name]))
                with self.assertRaises(self.helper.ContractError):
                    self.helper.validate_reverse(reverse)
                self.reject_reverse(reverse)

    def test_forward_policy_keys_and_fingerprints_are_strict(self):
        for policies in ({}, {oracle.TENANT_ID: '0' * 64},
                         {oracle.TENANT_ID: 'a' * 64, oracle.OTHER_TENANT: 'b' * 64}):
            source = oracle.source_fixture()
            source['key_policies'] = policies
            self.helper.validate_forward(source)
            self.migration.MigrationPlan(oracle.canonical_bytes(source))
        for name in (oracle.TENANT_ID.upper(), UUID(oracle.TENANT_ID).hex,
                     '{' + oracle.TENANT_ID + '}', str(UUID(int=0)), 'unknown'):
            with self.subTest(policy_key=name):
                source = oracle.source_fixture()
                source['key_policies'] = {name: 'a' * 64}
                self.reject_forward(source)
        for value in (True, False, 1, 1.0, None, [], {},
                      'a' * 63, 'a' * 65, 'A' * 64, 'z' * 64):
            with self.subTest(fingerprint=repr(value)):
                source = oracle.source_fixture()
                source['key_policies'] = {oracle.TENANT_ID: value}
                self.reject_forward(source)
        source = oracle.source_fixture()
        source['key_policies'] = []
        self.reject_forward(source)

    def test_numeric_policy_value_cannot_supply_equal_boolean_substitute(self):
        source = oracle.source_fixture()
        source['key_policies'][oracle.TENANT_ID] = 1
        reverse = oracle.reverse_fixture(source)
        reverse['key_policies'][oracle.TENANT_ID] = True
        self.assertEqual(reverse['key_policies'], reverse['source_plan']['key_policies'])
        self.assertNotEqual(oracle.canonical_bytes(reverse['key_policies']),
                            oracle.canonical_bytes(reverse['source_plan']['key_policies']))
        # Isolate the helper's equality check: the complete reader also refuses
        # the malformed source policy grammar, which alone could mask this check.
        with self.assertRaises(self.helper.ContractError):
            self.helper.validate_reverse(reverse)
        # New forward grammar rejects the malformed source itself as well.
        self.reject_forward(source)
        self.reject_reverse(reverse)

    def test_legacy_new_pairing_and_legacy_uuid_behavior_are_separate(self):
        source = oracle.source_fixture()
        source['format'] = 'cryptalis.transition/retained-native-research-v0'
        source.pop('object_comments')
        source['operation_id'] = UUID(source['operation_id']).hex
        self.migration.MigrationPlan(oracle.canonical_bytes(source))
        reverse = oracle.reverse_fixture()
        reverse['format'] = 'cryptalis.reverse/retained-native-research-v0'
        self.reject_reverse(reverse)
        reverse = oracle.reverse_fixture(source)
        self.reject_reverse(reverse)


if __name__ == '__main__':
    unittest.main()
