"""Explicit local candidate/interpreter binding for an owned bridge experiment."""
import hashlib
from pathlib import Path


def manifest(root):
    root = Path(root)
    result = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(root.rglob('*.py')) if '__pycache__' not in p.parts}
    if not result:
        raise ValueError('bridge source has no Python modules')
    return result


def binding(source, python, legacy):
    if not source or not python:
        raise ValueError('both --bridge-target-source and --bridge-target-python are required')
    legacy = Path(legacy).resolve()
    lab = legacy.parent
    target = Path(source).resolve()
    interpreter = Path(python).absolute()
    if target.parent != lab or not target.name.startswith('candidate-') or target == legacy:
        raise ValueError('bridge target must be a separate explicit candidate in this lab')
    if not interpreter.is_relative_to(lab / 'release-lab') or not interpreter.is_file():
        raise ValueError('bridge interpreter must be an existing installed release-lab interpreter')
    runner = target / 'scripts/test_postgres.py'
    if runner.read_bytes() != (legacy / 'scripts/test_postgres.py').read_bytes():
        raise ValueError('bridge target must retain the unchanged dual-role preflight')
    return {'source': str(target), 'python': str(interpreter),
            'runtime_modules': manifest(target / 'src/cryptalis'),
            'test_helpers': manifest(target / 'tests'),
            'runner_sha256': hashlib.sha256(runner.read_bytes()).hexdigest()}


def verify_source(selected):
    source = Path(selected['source'])
    if manifest(source / 'src/cryptalis') != selected['runtime_modules']:
        raise ValueError('bridge target runtime changed after explicit selection')
    if manifest(source / 'tests') != selected['test_helpers']:
        raise ValueError('bridge target test helpers changed after explicit selection')
    if hashlib.sha256((source / 'scripts/test_postgres.py').read_bytes()).hexdigest() != selected['runner_sha256']:
        raise ValueError('bridge target preflight changed after explicit selection')


def verify_package(package, selected):
    if manifest(package) != selected['runtime_modules']:
        raise ValueError('installed bridge package is not the complete selected runtime')
