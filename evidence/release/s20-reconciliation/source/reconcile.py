"""Static artifact reconciliation only; no product/dependency imports or extraction.
Run from any directory with Python >=3.12 -I -B after independent review.
Prints one JSON receipt; never writes inputs, invokes subprocesses or uses network.
"""
import base64
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SOURCE = BASE / 'candidate-accel-payload-integrated-20261014'
DIST = BASE / 'release-lab/s20-payload-preparation-20261014/dist-1'
SBOM = BASE / 'evidence/w9-license-fix/runtime-sbom.json'

class Invalid(ValueError):
    pass

def require(condition, reason):
    if not condition:
        raise Invalid(reason)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique_json(data):
    def hook(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate_json_key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=hook)

def pins():
    result = {}
    for line in (HERE / 'inputs.sha256').read_text().splitlines():
        digest, name = line.split('  ', 1)
        path = BASE / name
        require(path.resolve().is_relative_to(BASE.resolve()), 'input_path_escape')
        require(name not in result, 'duplicate_input_pin')
        require(sha(path.read_bytes()) == digest, 'input_pin_mismatch:' + name)
        result[name] = digest
    return result

def wheel_files(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), 'duplicate_wheel_member')
        require(all(not n.startswith('/') and '..' not in n.split('/') for n in names), 'wheel_path')
        return {n: archive.read(n) for n in names if not n.endswith('/')}

def sdist_files(path):
    with tarfile.open(path, 'r:gz') as archive:
        members = archive.getmembers()
        names = [m.name for m in members]
        require(len(names) == len(set(names)), 'duplicate_sdist_member')
        require(all(not n.startswith('/') and '..' not in n.split('/') for n in names), 'sdist_path')
        require(all(m.isfile() or m.isdir() for m in members), 'sdist_special_member')
        return {m.name: archive.extractfile(m).read() for m in members if m.isfile()}

def metadata_checks(data, expected):
    msg = BytesParser().parsebytes(data)
    for field, value in [('Name', expected['name']), ('Version', expected['version']),
                         ('License-Expression', expected['license']), ('License-File', 'LICENSE'),
                         ('Requires-Python', expected['requires_python'])]:
        require(msg.get_all(field) == [value], 'metadata:' + field)
    require(sorted(msg.get_all('Requires-Dist', [])) == expected['direct_requires_dist'], 'direct_dependencies')

def artifact_checks(wheel, sdist, expected, license_bytes):
    prefix = 'cryptalis-0.1.0.dist-info/'
    require(wheel.get(prefix + 'licenses/LICENSE') == license_bytes, 'wheel_license')
    require(sdist.get('cryptalis-0.1.0/LICENSE') == license_bytes, 'sdist_license')
    metadata_checks(wheel[prefix + 'METADATA'], expected)
    metadata_checks(sdist['cryptalis-0.1.0/PKG-INFO'], expected)
    require(not any(n.endswith('.pth') for n in wheel), 'wheel_pth')
    record_name = prefix + 'RECORD'
    rows = list(csv.reader(io.StringIO(wheel[record_name].decode())))
    require(all(len(r) == 3 for r in rows), 'record_format')
    require(len(rows) == len({r[0] for r in rows}), 'record_duplicates')
    require({r[0] for r in rows} == set(wheel), 'record_coverage')
    hashed = 0
    for name, digest, length in rows:
        if name == record_name:
            require(digest == length == '', 'record_self')
            continue
        data = wheel[name]
        actual = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b'=').decode()
        require(digest == 'sha256=' + actual and length == str(len(data)), 'record_digest')
        hashed += 1
    require(hashed == expected['record_hashed_entries'], 'record_count')
    source_modules = {str(p.relative_to(SOURCE / 'src')): p.read_bytes()
                      for p in (SOURCE / 'src/cryptalis').rglob('*.py')}
    require(len(source_modules) == expected['runtime_module_count'], 'source_module_count')
    require({n for n in wheel if n.endswith('.py')} == set(source_modules), 'wheel_module_set')
    require({n.removeprefix('cryptalis-0.1.0/src/') for n in sdist if n.endswith('.py')} == set(source_modules), 'sdist_module_set')
    for name, data in source_modules.items():
        require(wheel[name] == sdist['cryptalis-0.1.0/src/' + name] == data, 'module_bytes:' + name)
    return {'modules': len(source_modules), 'record_hashed_entries': hashed,
            'sdist_has_lock': 'cryptalis-0.1.0/uv.lock' in sdist}

def graph_checks(bom, lock, project, expected):
    require(bom['bomFormat'] == 'CycloneDX' and bom['specVersion'] == '1.5', 'sbom_format')
    packages = {p['name']: p for p in lock['package']}
    require(len(packages) == len(lock['package']), 'duplicate_lock_package')
    root = packages['cryptalis']
    require(root['version'] == expected['version'], 'lock_project_version')
    require(sorted(x.lower() for x in project['project']['dependencies']) == expected['direct_requires_dist'], 'project_dependencies')
    require(project['build-system']['requires'] == expected['build_requires'], 'build_dependencies')
    require(project['dependency-groups']['dev'] == expected['test_roots'], 'test_roots')
    # Union of all declared platform markers, retaining only requested extras.
    visited, edges, selected_extras = set(), {}, {}
    pending = [('cryptalis', ())]
    while pending:
        name, extras = pending.pop()
        old = selected_extras.setdefault(name, set())
        new = set(extras) - old
        if name in visited and not new:
            continue
        old.update(extras)
        visited.add(name)
        package = packages[name]
        deps = list(package.get('dependencies', []))
        for extra in sorted(old):
            deps.extend(package.get('optional-dependencies', {})[extra])
        edges[name] = {d['name'] for d in deps}
        pending.extend((d['name'], tuple(d.get('extra', []))) for d in deps)
    versions = {n: packages[n]['version'] for n in visited if n != 'cryptalis'}
    require(versions == expected['runtime_versions'], 'runtime_closure')
    test_pending = list(expected['test_roots'])
    test_seen = set()
    while test_pending:
        name = test_pending.pop()
        if name in test_seen:
            continue
        test_seen.add(name)
        test_pending.extend(d['name'] for d in packages[name].get('dependencies', []))
    require({n: packages[n]['version'] for n in test_seen - visited} == expected['test_only_versions'], 'test_closure')
    components = bom['components']
    require(len(components) == len({c['name'] for c in components}), 'duplicate_component')
    require({c['name']: c['version'] for c in components} == versions, 'sbom_versions')
    refs = {c['bom-ref']: c['name'] for c in components}
    project_component = bom['metadata']['component']
    require(project_component['name'] == 'cryptalis' and project_component['version'] == expected['version'], 'sbom_root')
    require(project_component['bom-ref'] not in refs and len(refs) == len(components), 'sbom_ref_duplicate')
    refs[project_component['bom-ref']] = 'cryptalis'
    dependency_rows = bom['dependencies']
    require(len(dependency_rows) == len({d['ref'] for d in dependency_rows}), 'duplicate_sbom_dependency')
    actual_edges = {refs[d['ref']]: {refs[v] for v in d.get('dependsOn', [])} for d in dependency_rows}
    require(actual_edges == edges, 'sbom_edges')
    distribution_count = 0
    for component in components:
        package = packages[component['name']]
        artifacts = [package['sdist']] if 'sdist' in package else []
        artifacts += package.get('wheels', [])
        wanted = {(a['url'], a['hash'].removeprefix('sha256:')) for a in artifacts}
        found = set()
        for ref in component.get('externalReferences', []):
            if ref['type'] != 'distribution':
                continue
            require(len(ref['hashes']) == 1 and ref['hashes'][0]['alg'] == 'SHA-256', 'sbom_distribution_hash')
            pair = (ref['url'], ref['hashes'][0]['content'])
            require(pair not in found, 'duplicate_distribution')
            found.add(pair)
        require(found == wanted, 'sbom_distribution_inventory:' + component['name'])
        distribution_count += len(found)
    return {'runtime_union': versions, 'test_only_union': expected['test_only_versions'],
            'build_requirement': expected['build_requires'], 'distribution_references': distribution_count,
            'markers_evaluated_for_installed_cell': False,
            'sbom_component_license_fields': sum('licenses' in c for c in components)}

def main():
    before = pins()
    expected = unique_json((HERE / 'expected.json').read_bytes())
    whl = DIST / 'cryptalis-0.1.0-py3-none-any.whl'
    sdist_path = DIST / 'cryptalis-0.1.0.tar.gz'
    require(sha(whl.read_bytes()) == expected['wheel_sha256'], 'wheel_hash')
    require(sha(sdist_path.read_bytes()) == expected['sdist_sha256'], 'sdist_hash')
    license_bytes = (SOURCE / 'LICENSE').read_bytes()
    require(sha(license_bytes) == expected['license_sha256'], 'license_hash')
    wheel, sdist = wheel_files(whl), sdist_files(sdist_path)
    project = tomllib.loads((SOURCE / 'pyproject.toml').read_text())
    lock = tomllib.loads((SOURCE / 'uv.lock').read_text())
    bom = unique_json(SBOM.read_bytes())
    artifacts = artifact_checks(wheel, sdist, expected, license_bytes)
    graph = graph_checks(bom, lock, project, expected)
    controls = []
    def negative(name, action, reason):
        try:
            action()
        except (Invalid, json.JSONDecodeError) as exc:
            require(reason in str(exc), 'wrong_negative_reason:' + name + ':' + str(exc))
            controls.append({'id': name, 'rejected': True, 'reason': reason})
        else:
            raise Invalid('negative_accepted:' + name)
    negative('malformed_sbom', lambda: unique_json(b'{'), 'Expecting property name')
    missing = dict(wheel)
    del missing['cryptalis-0.1.0.dist-info/licenses/LICENSE']
    negative('missing_wheel_license', lambda: artifact_checks(missing, sdist, expected, license_bytes), 'wheel_license')
    altered = dict(sdist)
    altered['cryptalis-0.1.0/LICENSE'] = b'wrong notice'
    negative('altered_sdist_license', lambda: artifact_checks(wheel, altered, expected, license_bytes), 'sdist_license')
    mismatch = copy.deepcopy(bom)
    mismatch['components'][0]['version'] = '0.0.0'
    negative('dependency_version_mismatch', lambda: graph_checks(mismatch, lock, project, expected), 'sbom_versions')
    edge = copy.deepcopy(bom)
    next(d for d in edge['dependencies'] if d.get('dependsOn'))['dependsOn'] = []
    negative('dependency_edge_mismatch', lambda: graph_checks(edge, lock, project, expected), 'sbom_edges')
    record = dict(wheel)
    key = 'cryptalis-0.1.0.dist-info/RECORD'
    record[key] = b'\n'.join(record[key].splitlines()[1:]) + b'\n'
    negative('missing_record_row', lambda: artifact_checks(record, sdist, expected, license_bytes), 'record_coverage')
    require([c['id'] for c in controls] == expected['negative_controls'], 'control_inventory')
    require(pins() == before, 'after_pin_mismatch')
    print(json.dumps({'status': 'PASS', 'input_pins': before, 'artifacts': artifacts, 'graph': graph,
                      'controls': controls, 'gates': {g: 'UNKNOWN' for g in ['G-ADAPTER','G-CRYPTO','G-QUERY','G-LIFECYCLE','G-PROVIDER','G-POLICY','G-RELEASE']},
                      'limits': ['Static existing artifact/lock/SBOM consistency only; not a build or runtime replay.',
                                 'Historical SBOM retained unchanged, not relabelled as generated for S20.',
                                 'Union graph includes conditional platform dependencies; not installed-cell inventory.',
                                 'Native vendored dependencies, dependency licensing, vulnerabilities, signing, independent builder identity and clean-machine reproducibility remain unqualified.']}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
