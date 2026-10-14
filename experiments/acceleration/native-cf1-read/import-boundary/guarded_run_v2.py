"""Additive F provenance guard; unchanged original runner and ordinary loaders."""
import hashlib
import importlib.machinery
import json
import os
from pathlib import Path
import runpy
import sys
R = Path(__file__).absolute().parent
B = R.parent
F = B / 'candidate-native-read-admission-20261014'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')

def inventory(root, kind):
    paths = [p for p in Path(root).rglob('*') if p.is_file()]
    if kind == 'code':
        paths = [p for p in paths if p.suffix in ('.py', '.pyi', '.pyc', '.pth', '.so')]
    return sorted(str(p) for p in paths)

def check(freeze):
    if any(key in os.environ for key in freeze['reject_environment']):
        raise RuntimeError('Environment override')
    for entry in freeze['inventories']:
        if inventory(entry['root'], entry['kind']) != entry['paths']:
            raise RuntimeError('Source/cache inventory changed: ' + entry['root'])
    for name, expected in freeze['pins'].items():
        if sha(name) != expected:
            raise RuntimeError('Provenance pin mismatch: ' + name)

def module_origins(freeze):
    records = []
    for name, module in sorted(sys.modules.copy().items()):
        if module is None:
            continue
        file = getattr(module, '__file__', None)
        spec = getattr(module, '__spec__', None)
        cached = getattr(module, '__cached__', None)
        record = {'name': name, 'file': file, 'cached': cached,
                  'spec_origin': getattr(spec, 'origin', None),
                  'loader': type(getattr(spec, 'loader', None)).__name__}
        if file and not Path(file).is_file():
            raise RuntimeError('Missing file-backed module origin: ' + name + ': ' + str(file))
        if file and Path(file).is_file():
            file = str(Path(file).absolute())
            record.update(file_sha256=sha(file), file_bound=file in freeze['pins'])
            if not record['file_bound']:
                if not Path(file).is_relative_to(Path(freeze['stdlib_root'])):
                    raise RuntimeError('Unbound non-stdlib module: ' + name + ': ' + file)
        if cached:
            record['cache_exists'] = Path(cached).is_file()
            if record['cache_exists']:
                record['cache_sha256'] = sha(cached)
                record['cache_bound'] = str(Path(cached).absolute()) in freeze['pins']
                if record.get('file_bound') and not record['cache_bound']:
                    raise RuntimeError('Unbound observed candidate/dependency cache: ' + name)
        records.append(record)
    for name, expected in freeze['required_origins'].items():
        if name not in sys.modules or str(Path(sys.modules[name].__file__).absolute()) != expected:
            raise RuntimeError('Required module origin mismatch: ' + name)
    return records

def preimport_origins(freeze):
    records = []
    for name, expected in freeze['required_origins'].items():
        # Public finder with explicit parent path: no importing dotted-name parents.
        path = Path(expected)
        if path.name == '__init__.py':
            search = path.parent.parent
            lookup = path.parent.name
        else:
            search = path.parent
            lookup = path.name.split('.')[0]
        spec = importlib.machinery.PathFinder.find_spec(lookup, [str(search)])
        if spec is None or spec.origin != expected:
            raise RuntimeError('Pre-import origin mismatch: ' + name)
        if expected not in freeze['pins'] or sha(expected) != freeze['pins'][expected]:
            raise RuntimeError('Pre-import source/native not bound: ' + name)
        expected_loader = 'ExtensionFileLoader' if path.suffix == '.so' else 'SourceFileLoader'
        if type(spec.loader).__name__ != expected_loader:
            raise RuntimeError('Pre-import loader mismatch: ' + name)
        cached = spec.cached
        if cached and Path(cached).exists():
            if cached not in freeze['pins'] or sha(cached) != freeze['pins'][cached]:
                raise RuntimeError('Pre-import cache not bound: ' + name)
        records.append({'name': name, 'lookup': lookup, 'search_root': str(search),
                        'origin': spec.origin, 'cached': cached,
                        'cache_exists': bool(cached and Path(cached).exists()),
                        'loader': type(spec.loader).__name__})
    return records

def main():
    if len(sys.argv) != 3:
        raise RuntimeError('Expected mode and absolute new receipt path')
    mode, target_arg = sys.argv[1:]
    target = Path(target_arg)
    if not target.is_absolute() or target.parent.parent != R or target.exists():
        raise RuntimeError('Invalid output target')
    freeze_path = R / 'FREEZE_V2.json'
    freeze = json.loads(freeze_path.read_text())
    receipt = {'status': 'FAIL', 'mode': mode, 'optimize': sys.flags.optimize,
               'freeze_sha256': sha(freeze_path), 'before': 'NOT RUN', 'after': 'NOT RUN',
               'preimport_origins': [], 'import_origins': [], 'primary_failure': None,
               'integrity_errors': []}
    try:
        if (mode not in freeze['modes'] or sys.executable != freeze['python']
                or sys.version_info[:3] != (3, 12, 14) or sys.flags.optimize not in (0, 1)
                or not sys.flags.isolated or not sys.dont_write_bytecode):
            raise RuntimeError('Interpreter/flags/mode mismatch')
        check(freeze)
        receipt['preimport_origins'] = preimport_origins(freeze)
        receipt['before'] = 'PASS'
        sys.path.insert(0, str(F))
        sys.argv = [str(F / 'run.py'), mode, str(target)]
        runpy.run_path(str(F / 'run.py'), run_name='__main__')
    except BaseException as exc:
        receipt['primary_failure'] = {'type': type(exc).__name__, 'message': str(exc)}
        raise
    finally:
        # Postflight always runs, including unexpected import/harness failures.
        try:
            receipt['import_origins'] = module_origins(freeze)
        except BaseException as exc:
            receipt['integrity_errors'].append({'phase': 'observed-origins', 'type': type(exc).__name__, 'message': str(exc)})
        for entry in freeze['inventories']:
            try:
                if inventory(entry['root'], entry['kind']) != entry['paths']:
                    raise RuntimeError('Inventory mismatch: ' + entry['root'])
            except BaseException as exc:
                receipt['integrity_errors'].append({'phase': 'inventory', 'type': type(exc).__name__, 'message': str(exc)})
        for name, digest in freeze['pins'].items():
            try:
                if sha(name) != digest:
                    raise RuntimeError('Pin mismatch: ' + name)
            except BaseException as exc:
                receipt['integrity_errors'].append({'phase': 'pin', 'type': type(exc).__name__, 'message': str(exc)})
        if not receipt['integrity_errors'] and receipt['before'] == 'PASS':
            receipt['after'] = 'PASS'
            receipt['status'] = 'PASS'
        else:
            receipt['after'] = 'FAIL'
            receipt['status'] = 'FAIL_INTEGRITY'
        save(Path(str(target) + '-provenance.json'), receipt)
        if receipt['integrity_errors']:
            raise RuntimeError('Final provenance integrity failed; primary failure retained in receipt')

if __name__ == '__main__':
    main()
