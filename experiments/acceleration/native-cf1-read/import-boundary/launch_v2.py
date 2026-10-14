"""Finite ten-child F exact-oracle plan. Execute only after independent clearance."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
R = Path(__file__).absolute().parent

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')

def require(value, message):
    if not value:
        raise RuntimeError(message)

def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b

def exact_traceback(stderr):
    lines = stderr.splitlines()
    return (len(lines) >= 3 and lines[0] == 'Traceback (most recent call last):'
            and lines[-1] == 'RuntimeError: Exact admission mismatch'
            and all(line.startswith('  File "') or line.startswith('    ') for line in lines[1:-1])
            and sum(line == 'Traceback (most recent call last):' for line in lines) == 1)

def execute(out, freeze, summary):
    manifest = json.loads(Path(freeze['manifest']).read_text())
    # Import only after parent pins/inventories have passed; public ordinary import.
    sys.path.insert(0, str(R))
    from supervisor_v2 import bounded
    records = []
    positive = None
    for optimize in (0, 1):
        for mode in freeze['modes']:
            target = out / f'{mode}-o{optimize}.json'
            cmd = [sys.executable, '-I', '-B'] + (['-O'] if optimize else []) + [str(R / 'guarded_run_v2.py'), mode, str(target)]
            child = bounded(cmd, 180, 1048576, out / f'{mode}-o{optimize}-supervisor.json')
            require(child['reason'] is None and child['process_reaped'], 'Bounded child failure')
            require(not integrity(freeze), 'Post-child integrity failure')
            provenance = Path(str(target) + '-provenance.json')
            record = {'command': cmd, 'exit': child['exit_code'], 'stdout': child['stdout'],
                      'stderr': child['stderr'], 'result_sha256': sha(target) if target.exists() else None,
                      'provenance_sha256': sha(provenance) if provenance.exists() else None}
            save(out / f'{mode}-o{optimize}-launch.json', record)
            records.append(record)
            require(target.exists() and provenance.exists(), 'Missing receipt')
            p = json.loads(provenance.read_text())
            require(p['status'] == p['before'] == p['after'] == 'PASS'
                    and p['freeze_sha256'] == sha(R / 'FREEZE_V2.json') and p['optimize'] == optimize and p['mode'] == mode
                    and not p['integrity_errors'], 'Provenance failure')
            r = json.loads(target.read_text())
            require(not child['stdout'] and r['optimize'] == optimize and r['mode'] == mode, 'Unexpected stdout/mode')
            require(r['manifest_sha256'] == sha(freeze['manifest']), 'Manifest receipt mismatch')
            if mode == 'positive':
                require(child['exit_code'] == 0 and not child['stderr'] and r['status'] == 'PASS', 'Positive failure')
                require([x['id'] for x in r['observations']] == [x['id'] for x in manifest['cases']], 'Ordered coverage mismatch')
                for case, actual in zip(manifest['cases'], r['observations']):
                    require(same(actual['actual'], case['expected']), 'Exact public oracle mismatch')
                    require(actual['decode_hook_completed'] == (case.get('source_kind') == 'decode-expiry'), 'Decode hook mismatch')
                    require(actual['synthetic_nonce_calls'] == (1 if case['kind'] == 'seal' else 0), 'Nonce count mismatch')
                if positive is not None:
                    require(same(positive, r['observations']), 'Optimization correspondence mismatch')
                positive = r['observations']
            else:
                n = r.get('negative')
                control = next(c for c in manifest['negative_controls'] if c['mode'] == mode)
                case = next(c for c in manifest['cases'] if c['id'] == control['case_id'])
                require(child['exit_code'] == 1 and r['status'] == 'FAIL' and not r['observations']
                        and r.get('error_type') == 'RuntimeError' and r.get('error') == 'Exact admission mismatch'
                        and exact_traceback(child['stderr']), 'Wrong negative failure')
                require(n and n['mode'] == mode and n['original_verified'] and n['case_id'] == case['id']
                        and same(n['original'], case['expected']), 'Wrong negative original')
                mutation = copy.deepcopy(n['original'])
                if mode == 'text':
                    mutation['value'] += '!ADMISSION-NEGATIVE!'
                elif mode == 'type':
                    mutation['value_type'] = 'bytes'
                elif mode == 'stage':
                    mutation['stage'] = 'deliberately-wrong-stage'
                else:
                    mutation['trace'] += mutation['trace'][:1]
                require(same(n['mutated'], mutation) and not same(n['original'], mutation), 'Wrong negative mutation')
            for name, digest in freeze['pins'].items():
                require(sha(name) == digest, 'Post-child pin mismatch: ' + name)
    save(out / 'launches.json', records)
    summary['status'] = 'PASS'

def inventory(root, kind):
    paths = [p for p in Path(root).rglob('*') if p.is_file()]
    if kind == 'code':
        paths = [p for p in paths if p.suffix in ('.py', '.pyi', '.pyc', '.pth', '.so')]
    return sorted(str(p) for p in paths)

def integrity(freeze):
    errors = []
    for entry in freeze['inventories']:
        try:
            require(inventory(entry['root'], entry['kind']) == entry['paths'], 'Inventory mismatch: ' + entry['root'])
        except BaseException as exc:
            errors.append({'phase': 'inventory', 'type': type(exc).__name__, 'message': str(exc)})
    for name, digest in freeze['pins'].items():
        try:
            require(sha(name) == digest, 'Pin mismatch: ' + name)
        except BaseException as exc:
            errors.append({'phase': 'pin', 'type': type(exc).__name__, 'message': str(exc)})
    return errors

def main():
    require(len(sys.argv) == 2 and sys.argv[1] and all(c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in sys.argv[1]), 'Safe unique output directory required')
    freeze_path = R / 'FREEZE_V2.json'
    freeze = json.loads(freeze_path.read_text())
    out = R / sys.argv[1]
    out.mkdir()
    summary = {'status': 'FAIL', 'freeze_sha256': sha(freeze_path), 'primary_failure': None, 'integrity_errors': []}
    try:
        require(sys.executable == freeze['python'] and sys.flags.isolated and sys.dont_write_bytecode, 'Pinned isolated no-write launcher required')
        require(not any(k in os.environ for k in freeze['reject_environment']), 'Environment override')
        require(not integrity(freeze), 'Initial integrity failure')
        execute(out, freeze, summary)
    except BaseException as exc:
        summary['primary_failure'] = {'type': type(exc).__name__, 'message': str(exc)}
        raise
    finally:
        summary['integrity_errors'] = integrity(freeze)
        if summary['integrity_errors']:
            summary['status'] = 'FAIL_INTEGRITY'
        save(out / 'FINAL_INTEGRITY.json', summary)
        if summary['integrity_errors']:
            raise RuntimeError('Final parent integrity failed; primary failure retained in receipt')

if __name__ == '__main__':
    main()
