"""Finite future root-selected synthetic vector run. Source only until selected."""
import copy
import hashlib
import json
from pathlib import Path
import runpy
import sys
from types import ModuleType


B = Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
HERE = B / 'experiments/forward-aborted-successor-pure-v3-vectors-v1-20261016'
SOURCE = B / 'experiments/forward-aborted-successor-pure-v3-v1-20261016/successor_contract.py'
HOST = Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python')
STDLIB = HOST / 'lib/python3.12'
STDLIB_MAP = B / 'experiments/preview-doctor-dx-slice-20261015/proof-v2/STDLIB_SHA256.txt'
OUTPUT = Path('/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/forward-aborted-successor-pure-v3-vectors-v1-root-20261016')
PINS = {
    SOURCE: 'f1fabd4fd24dbf0532c0bc030f11799f76b9da186ac5c6388c7233352d7817cf',
    HERE / 'VECTORS.json': 'ca2353e9b501cbd2189079f1855be58b9fcfd2017c66fe7f65fc92344aa69e84',
    HERE / 'COMMITMENT_PREIMAGES.json': '1796ab05c1954dee5169c7cbdcd583bb18d976a8cc9673fbf3ae510f56a846e8',
    HERE / 'CASE_ORACLES.json': '1ca5eac7e10c4bc46418b267ccdd83512625f4d647757fa43c309ae8b4276267',
    STDLIB_MAP: 'a57c71aec1c9ddaeda162e088e4b18d94fa1bf978d7ae506f20906abcf6a6132',
}
COMPLETED_RESULTS = []


class DriverFailure(RuntimeError):
    pass


def need(condition, code):
    if not condition:
        raise DriverFailure(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def raw_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def snapshot(value):
    def special(item):
        if type(item) is bytes:
            return {'__test_bytes_hex__': item.hex()}
        raise TypeError('unexpected test value')
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False, default=special)


def emit(report):
    rendered = raw_json(report) + b'\n'
    if len(rendered) > 64 * 1024:
        # Hard failure, retaining ordered completed/failed IDs without emitting
        # an unbounded value. This never becomes a passing partial run.
        rendered = raw_json({'driver_failure': 'output_bound_exceeded',
                             'completed_case_ids': [r['id'] for r in COMPLETED_RESULTS],
                             'failed_case_ids': [r['id'] for r in COMPLETED_RESULTS if not r['pass']]}) + b'\n'
        sys.stdout.buffer.write(rendered)
        return False
    sys.stdout.buffer.write(rendered)
    return True


def read_pinned(path):
    raw = path.read_bytes()
    need(len(raw) <= 256 * 1024 and sha(raw) == PINS[path], 'input_identity_mismatch')
    return raw


def origin_files(admitted):
    found = set()
    for module_name, module in tuple(sys.modules.items()):
        if module is None:
            continue
        if not isinstance(module, ModuleType):
            # CPython typing exposes these two deprecated class namespaces in
            # sys.modules. They are not additional loaded source modules.
            need(module_name in ('typing.io', 'typing.re'), 'unexpected_nonmodule_alias')
            continue
        spec = getattr(module, '__spec__', None)
        if getattr(spec, 'origin', None) in ('built-in', 'frozen'):
            continue
        name = getattr(module, '__file__', None)
        need(type(name) is str, 'unbound_module_origin')
        path = Path(name)
        if path in (HERE / 'driver.py', SOURCE):
            continue
        need(path.is_absolute() and path.is_relative_to(STDLIB), 'nonstdlib_module_origin')
        relative = path.relative_to(STDLIB).as_posix()
        need(relative in admitted, 'unadmitted_stdlib_module_origin')
        found.add(relative)
    return sorted(found)


def main():
    need(len(sys.argv) == 1 and Path(__file__) == HERE / 'driver.py', 'wrong_entry')
    need(sys.executable == str(HOST / 'bin/python3.12'), 'wrong_interpreter')
    need(sys.flags.isolated and sys.flags.no_site and not sys.flags.optimize
         and sys.dont_write_bytecode, 'wrong_startup_flags')
    need(sys.pycache_prefix == str(OUTPUT / 'bytecode-absent')
         and not (OUTPUT / 'bytecode-absent').exists(), 'bytecode_prefix_not_absent')
    allowed_search = {str(HOST / 'lib/python312.zip'), str(STDLIB), str(STDLIB / 'lib-dynload')}
    need(set(sys.path) <= allowed_search and str(STDLIB) in sys.path
         and not (HOST / 'lib/python312.zip').exists(), 'unadmitted_search_route')
    raw_inputs = {path: read_pinned(path) for path in PINS}
    admitted = {}
    for line in raw_inputs[STDLIB_MAP].decode('ascii').splitlines():
        digest, name = line.split('  ', 1)
        relative = Path(name)
        need(name not in admitted and not relative.is_absolute()
             and '..' not in relative.parts and relative.as_posix() == name,
             'invalid_stdlib_map')
        admitted[name] = digest
    need(len(admitted) == 472, 'wrong_stdlib_declaration_count')
    origin_files(admitted)
    vectors = json.loads(raw_inputs[HERE / 'VECTORS.json'])
    oracles = json.loads(raw_inputs[HERE / 'CASE_ORACLES.json'])
    preimages = json.loads(raw_inputs[HERE / 'COMMITMENT_PREIMAGES.json'])['preimages']
    need(len(preimages) == 25 and len({p['name'] for p in preimages}) == 25, 'preimage_namespace')
    need(all(sha(p['canonical_utf8'].encode('utf-8')) == p['sha256'] for p in preimages), 'preimage_digest')
    # Exact source is externally frozen and pinned before/after by root. This
    # pre-read hash is not a continuous loaded-code or race-freedom attestation.
    m = runpy.run_path(str(SOURCE))
    refusal_type = m['ContractRefusal']
    ids, docs, rows, summaries = (vectors[k] for k in ('ids', 'documents', 'rows', 'summaries'))
    S = vectors['scope_digest']
    entries = []

    def add(name, function, args=(), kwargs=None):
        entries.append((name, function, copy.deepcopy({'args': list(args), 'kwargs': kwargs or {}})))

    def pin(key, artifact=None):
        raw = (vectors['artifacts'][key].encode('utf-8') if artifact is None else artifact)
        return {'target_id': ids['target'], 'operation_id': docs[key]['operation_id'],
                'plan_digest': sha(raw), 'phase': 'PREPARED'}

    def build(key, ordered, count=None, current=None):
        return {'aborted_predecessor': vectors['artifacts'][key].encode('utf-8'),
                'predecessor_pin': pin(key), 'decoded_predecessor': docs[key],
                'current_proposal': vectors['current_proposal'] if current is None else current,
                'rows_newest_first': ordered, 'journal_row_count': len(ordered) if count is None else count}

    def verify(ordered, summary=None, new_id=None):
        return (summaries['second'] if summary is None else summary, S, ordered), {'new_operation_id': ids['fresh'] if new_id is None else new_id}

    standard = [rows['second'], rows['first'], rows['v2']]
    add('scope_literal', 'scope_bytes', (docs['v2'],))
    for name in ('v0', 'v1', 'v2'):
        add('construct_' + name, 'construct_lineage', kwargs=build(name, [rows[name]]))
    add('construct_second_ancestor', 'construct_lineage', kwargs=build('first', [rows['first'], rows['v2']]))
    add('construct_third_ancestor', 'construct_lineage', kwargs=build('second', standard))
    args, kwargs = verify(standard)
    add('verify_three_ancestors', 'verify_lineage', args, kwargs)
    add('paired_absent', 'bind_predecessor', kwargs={'aborted_predecessor': None, 'predecessor_pin': None})
    binding = {'aborted_predecessor': vectors['artifacts']['v2'].encode('utf-8'),
               'predecessor_pin': pin('v2'), 'decoded_predecessor': docs['v2']}
    x = copy.deepcopy(binding); x['predecessor_pin'] = None
    add('missing_pin', 'bind_predecessor', kwargs=x)
    x = copy.deepcopy(binding); x['aborted_predecessor'] = None
    add('missing_artifact', 'bind_predecessor', kwargs=x)
    x = copy.deepcopy(binding); x['predecessor_pin']['phase'] = 'ABORTED'
    add('wrong_pin_phase', 'bind_predecessor', kwargs=x)
    x = copy.deepcopy(binding); x['predecessor_pin']['plan_digest'] = 'd' * 64
    add('wrong_pin_digest', 'bind_predecessor', kwargs=x)
    x = copy.deepcopy(binding); x['aborted_predecessor'] += b'\n'
    add('noncanonical_artifact', 'bind_predecessor', kwargs=x)
    x = copy.deepcopy(vectors['current_proposal']); x['lock']['declaration']['scope_marker'] = True
    add('scope_bool_int_alias', 'require_same_scope', (docs['v2'], x))
    x = copy.deepcopy(vectors['current_proposal']); x['lock']['required_readers'].reverse()
    add('scope_reader_order', 'require_same_scope', (docs['v2'], x))
    x = copy.deepcopy(vectors['current_proposal']); x['target'][-1] = 'different_owner'
    add('scope_target_owner', 'require_same_scope', (docs['v2'], x))
    x = copy.deepcopy(vectors['current_proposal']); x['key_policies'][ids['table']] = 'd' * 64
    add('changed_tenant_fingerprint', 'require_same_scope', (docs['v2'], x))
    x = copy.deepcopy(vectors['current_proposal'])
    x['lock']['writer_inventory']['evidence_kind'] = 'fresh synthetic observation'
    x['lock']['search_reviews'] = ['fresh synthetic review']; x['lock']['ddl'] = ['unvalidated new derived text']
    x['scopes'] = []; x['estimates'] = {}; x['object_comments'] = {}; x['cluster_designation'] = {}
    add('allowed_observation_refresh', 'require_same_scope', (docs['v2'], x))
    x = copy.deepcopy(summaries['second']); x['extra'] = 1
    add('summary_unknown_member', 'validate_summary', (x,))
    x = copy.deepcopy(summaries['second']); x['count'] = True
    add('summary_bool_count', 'validate_summary', (x,))
    x = copy.deepcopy(summaries['second']); x['count'] = 0
    add('summary_zero_count', 'validate_summary', (x,))
    x = copy.deepcopy(summaries['second']); x['root']['format'] = 'cryptalis.reverse/retained-native-research-v0'
    add('summary_reverse_root', 'validate_summary', (x,))
    x = copy.deepcopy(summaries['second']); x['root']['operation_id'] = ids['root'].replace('-', '')
    add('summary_noncanonical_uuid', 'validate_summary', (x,))
    x = copy.deepcopy(standard); x[0]['state']['phase'] = 'ACTIVE'
    args, kwargs = verify(x); add('phase_not_aborted', 'verify_lineage', args, kwargs)
    x = copy.deepcopy(standard); x[0]['state']['source_operation_id'] = ids['root']
    args, kwargs = verify(x); add('reverse_state_field', 'verify_lineage', args, kwargs)
    x = copy.deepcopy(standard); x[0]['state']['models'][ids['table']]['rows'] = 6
    args, kwargs = verify(x); add('terminal_member_tamper', 'verify_lineage', args, kwargs)
    args, kwargs = verify(standard[:-1]); add('missing_ancestor', 'verify_lineage', args, kwargs)
    args, kwargs = verify(standard + [rows['v2']]); add('extra_ancestor', 'verify_lineage', args, kwargs)
    args, kwargs = verify([rows['first'], rows['second'], rows['v2']]); add('reordered_ancestor', 'verify_lineage', args, kwargs)
    x = copy.deepcopy(standard); x[0]['plan_digest'] = 'd' * 64
    args, kwargs = verify(x); add('wrong_head_digest', 'verify_lineage', args, kwargs)
    x = copy.deepcopy(standard); x[0]['state']['aborted_forward']['count'] = 3
    args, kwargs = verify(x); add('prefix_count_mismatch', 'verify_lineage', args, kwargs)
    x = copy.deepcopy(standard); x[0]['state']['aborted_forward']['digest'] = 'd' * 64
    add('artifact_prefix_mismatch', 'construct_lineage', kwargs=build('second', x))
    add('journal_count_mismatch', 'construct_lineage', kwargs=build('second', standard, count=4))
    x = copy.deepcopy(vectors['current_proposal']); x['operation_id'] = ids['first']
    add('new_identity_is_ancestor', 'construct_lineage', kwargs=build('second', standard, current=x))
    x = copy.deepcopy(docs['v2']); x['aborted_forward'] = copy.deepcopy(summaries['v2'])
    raw = raw_json(x)
    add('historical_prefix_forbidden', 'bind_predecessor', kwargs={
        'aborted_predecessor': raw, 'predecessor_pin': pin('v2', raw), 'decoded_predecessor': x})
    add('nested_state_boundary', 'construct_lineage', kwargs=build('v2', [rows['nested_boundary']]))
    args, kwargs = verify([rows['unstable_second'], rows['first'], rows['v2']], summaries['unstable_second'])
    add('unstable_snapshot_boundary', 'verify_lineage', args, kwargs)
    add('journal_integer_above_artifact_range', 'canonical_bytes', ({'rows': 9007199254740992},))

    expected = oracles['cases']
    need(oracles['case_count'] == len(entries) == 38
         and [entry[0] for entry in entries] == [case['id'] for case in expected]
         and len({entry[0] for entry in entries}) == 38, 'case_namespace_mismatch')
    results = COMPLETED_RESULTS
    for (name, function, inputs), oracle in zip(entries, expected, strict=True):
        before = snapshot(inputs)
        detached = None
        try:
            value = m[function](*inputs['args'], **inputs['kwargs'])
            visible = ({'bytes_sha256': sha(value), 'bytes': len(value)} if type(value) is bytes else copy.deepcopy(value))
            actual = {'kind': 'value', 'value': visible}
            if type(value) is dict and value.get('schema') == 'cryptalis.aborted-forward-lineage/research-v1':
                value['root']['operation_id'] = ids['fresh']
                value['predecessor']['plan_digest'] = 'e' * 64
                detached = snapshot(inputs) == before
        except refusal_type as error:
            actual = {'kind': 'refusal', 'code': error.code}
        except Exception as error:
            actual = {'kind': 'unexpected_exception', 'class': type(error).__name__[:80]}
        unchanged = snapshot(inputs) == before
        passed = (raw_json(actual) == raw_json(oracle['expected_actual']) and unchanged
                  and detached == oracle['expected_detached_output'])
        results.append({'id': name, 'kind': oracle['kind'], 'actual': actual,
                        'inputs_unchanged': unchanged, 'detached_output': detached, 'pass': passed})
    files_unchanged = all(path.read_bytes() == raw for path, raw in raw_inputs.items())
    loaded = origin_files(admitted)
    prefix_absent = not (OUTPUT / 'bytecode-absent').exists()
    failures = [case['id'] for case in results if not case['pass']]
    if not files_unchanged: failures.append('input_files_changed')
    if not prefix_absent: failures.append('bytecode_prefix_created')
    report = {
        'scope': 'synthetic pure component only; native and decoder premises remain held',
        'component_sha256': PINS[SOURCE], 'case_count': 38,
        'results': results, 'failures': failures,
        'input_files_unchanged': files_unchanged, 'bytecode_prefix_absent': prefix_absent,
        'stdlib_map_sha256': PINS[STDLIB_MAP], 'loaded_stdlib_files': loaded,
        'authority': {'host_authenticated': False, 'native_state_admitted': False,
                      'exact_native_membership': False, 'retry_authorized': False,
                      'closure_established': False, 'publication_authorized': False},
    }
    emitted = emit(report)
    return 1 if failures or not emitted else 0


if __name__ == '__main__':
    try:
        code = main()
    except Exception as error:
        # Preserve a bounded failure; no repair, rerun or native continuation.
        emit({'scope': 'synthetic pure component only',
              'driver_failure': type(error).__name__[:80],
              'fixed_code': error.args[0] if isinstance(error, DriverFailure) else None,
              'completed_results': COMPLETED_RESULTS})
        code = 1
    raise SystemExit(code)
