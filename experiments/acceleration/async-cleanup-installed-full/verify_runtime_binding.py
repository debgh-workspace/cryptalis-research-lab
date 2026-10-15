"""UNEXECUTED final-packet template: fail-closed data-only validation and source archive.
Materialize only after immutable installer/payload acceptance and independent review.
No product/dependency import, database action, process launch, or credential read.
"""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, re, stat

B = Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
SOURCE = B/'candidate-next-unblocked-correctness-20261014'
CLEAN = B/'experiments/async-cleanup-release-plan-20261015/source'
MAIN = B/'experiments/async-cleanup-installed-full-controls-20261015'
OPTIONAL = B/'experiments/async-cleanup-installed-sqlmodel-controls-20261015'
WHEEL = B/'experiments/async-cleanup-release-plan-20261015/run/direct-wheel/cryptalis-0.1.0-py3-none-any.whl'
WHEEL_SHA = '77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b'
SOURCE_MANIFEST_SHA = '4ba41f40c8dc32c80b2f863e5bc60fa7ce8434070c45b8b8f9cfc2a3cb145649'
DENIED = {'tests.json','readiness.json','package-origin.json','postgres-start.json','postgres-stop.json'}
HARNESS = {B/x for x in ('candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py','candidate-corpus-wrapper-v2-20261014/corpus_artifacts_v2.py','toolchain/lab_progress.py','toolchain/run_baseline.py','repo/scripts/test_postgres.py')}
# Exact V2 installer controls and safe receipt paths. These are path schemas,
# not assertions that any run exists or has been accepted. Every used path still
# needs the stage's externally anchored target/digest map and full admission.
MAIN_INSTALLER = B/'candidate-async-cleanup-main-installed-plan-v2-20261015'
OPTIONAL_INSTALLER = B/'candidate-async-cleanup-optional-installed-plan-v2-20261015'
MAIN_INSTALLED = B/'release-lab/async-cleanup-installed-20261015'
OPTIONAL_INSTALLED = B/'release-lab/async-cleanup-sqlmodel-installed-20261015'
INSTALLER_CONTROL_NAMES = frozenset(('plan.json','PATH_ADMISSION.json','FROZEN_TARGETS.json','SOURCE_PREPARATION.json','READ_ADMISSION_AUDIT.md','REVIEW.md','RUNTIME_REQUIREMENTS.md','PROPOSED_COMMANDS.txt','frozen-inputs.sha256','outer-frozen.sha256','install_verify.py','outer.py','preflight.py','supervisor_v2.py','source-original.json'))
INSTALLER_CONTROLS = {root/name for root in (MAIN_INSTALLER,OPTIONAL_INSTALLER) for name in INSTALLER_CONTROL_NAMES}
INSTALLER_CONTROLS |= {MAIN_INSTALLER/name for name in ('sa21-original.json','sa20-original.json')} | {OPTIONAL_INSTALLER/'sqlmodel-original.json'}
INSTALLER_RECEIPTS = {
 'main': {'installer_parent_result': MAIN_INSTALLER/'parent-results/parent-receipt.json',
          'installer_verification': MAIN_INSTALLED/'verification.json',
          **{f'{phase}_inode_{cell}': MAIN_INSTALLED/f'{cell}-{phase}-inodes.json' for cell in ('sa21','sa20') for phase in ('copy','installed')}},
 'optional38': {'installer_parent_result': OPTIONAL_INSTALLER/'parent-results/parent-receipt.json',
                'installer_verification': OPTIONAL_INSTALLED/'verification.json',
                **{f'{phase}_inode_sqlmodel': OPTIONAL_INSTALLED/f'sqlmodel-{phase}-inodes.json' for phase in ('copy','installed')}}}
SAFE_INSTALLER_EXTERNALS = INSTALLER_CONTROLS | {path for receipts in INSTALLER_RECEIPTS.values() for path in receipts.values()}

STAGES = {
 'sa21': (MAIN, 'BINDING_SA21.json', 'CLEARANCE_SA21.sha256', 'sa21'),
 'sa20': (MAIN, 'BINDING_SA20.json', 'CLEARANCE_SA20.sha256', 'sa20'),
 'optional38': (OPTIONAL, 'BINDING_OPTIONAL38.json', 'CLEARANCE_OPTIONAL38.sha256', 'installed38')}

def need(ok, reason):
    if not ok: raise RuntimeError(reason)

def lexical(p):
    need(p.is_absolute() and '..' not in p.parts, 'NONCANONICAL_PATH:'+str(p))
    need(p.name not in DENIED, 'RAW_PHASE_JSON_REFUSED')
    need(not any(x.lower() in {'__pycache__','.pytest_cache','cache','home','tmp','.env','environment','environment.json'} for x in p.parts[2:]), 'CACHE_OR_ENVIRONMENT_REFUSED')
    need(not any(x in str(p).lower() for x in ('password','credential','secret','.cryptalis-test')), 'SECRET_PATH_REFUSED')

def regular(p):
    lexical(p)
    need(p.is_relative_to(B), 'OUTSIDE_LAB:'+str(p))
    current = B
    need(B.resolve() == B, 'LAB_SYMLINK')
    for part in p.relative_to(B).parts:
        current /= part
        mode = current.lstat().st_mode
        need(not stat.S_ISLNK(mode), 'SYMLINK:'+str(current))
        need(stat.S_ISREG(mode) if current == p else stat.S_ISDIR(mode), 'TYPE:'+str(current))
    return p

def observed_link_chain(path):
    pending = list(path.parts[1:])
    current = Path('/')
    links = {}
    traversals = 0
    while pending:
        part = pending.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':
            current = current.parent
            continue
        current /= part
        mode = current.lstat().st_mode
        if stat.S_ISLNK(mode):
            traversals += 1
            need(traversals <= 40, 'INTERPRETER_LINK_LOOP')
            text = os.readlink(current)
            links[str(current)] = text
            target = Path(text)
            if target.is_absolute():
                current = Path('/')
                pending = list(target.parts[1:]) + pending
            else:
                current = current.parent
                pending = list(target.parts) + pending
        else:
            need(stat.S_ISDIR(mode) if pending else stat.S_ISREG(mode), 'INTERPRETER_LINK_TYPE')
    return current, links

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def safe_relative(value):
    p = PurePosixPath(value)
    need(not p.is_absolute() and str(p) == value and '..' not in p.parts and value, 'RELATIVE_PATH')
    return p

def parse_manifest(path):
    result = {}
    for line in regular(path).read_text().splitlines():
        m = re.fullmatch(r'([0-9a-f]{64})  (/[^\r\n]+)', line)
        need(m is not None, 'MANIFEST_ROW:'+str(path))
        h, name = m.groups()
        need(name not in result, 'DUPLICATE_TARGET:'+name)
        result[name] = h
    need(bool(result), 'EMPTY_MANIFEST:'+str(path))
    return result

def metadata_source_names(root):
    found = set()
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs: need(not (Path(directory)/name).is_symlink(), 'SOURCE_DIRECTORY_LINK')
        dirs[:] = [d for d in dirs if d not in {'__pycache__','.pytest_cache'}]
        for name in files:
            p = Path(directory)/name
            need(not p.is_symlink() and p.is_file(), 'SOURCE_FILE_TYPE')
            found.add(str(p.relative_to(root)))
    return found

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream: stream.write(data)
    need(path.read_bytes() == data, 'ARCHIVE_COPY_MISMATCH')

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--stage', choices=tuple(STAGES), required=True)
parser.add_argument('--binding-sha256', required=True)
parser.add_argument('--mode', choices=('before','after'), required=True)
parser.add_argument('--archive', type=Path)
a = parser.parse_args()
P, binding_name, stage_clearance, audit_name = STAGES[a.stage]
need(Path(__file__).absolute() == P/'verify_runtime_binding.py', 'UNMATERIALIZED_TEMPLATE')
need(re.fullmatch('[0-9a-f]{64}', a.binding_sha256) is not None, 'UNRESOLVED_BINDING_ANCHOR')
binding_path = regular(P/binding_name)
need(digest(binding_path) == a.binding_sha256, 'BINDING_ANCHOR_MISMATCH')
binding = json.loads(binding_path.read_bytes())
need(binding['status'] == 'BOUND_AFTER_INSTALLER_AND_INDEPENDENT_PLAN_ACCEPTANCE', 'UNRESOLVED_BINDING')
need(binding['stage'] == a.stage and binding['packet'] == str(P), 'WRONG_STAGE')
need(binding['installer_terminal_and_payload_accepted'] is True and binding['review_verdicts_checked_by_coordinator'] is True, 'ACCEPTANCE_NOT_RECORDED')
need(binding['wheel_sha256'] == WHEEL_SHA and binding['source_manifest_sha256'] == SOURCE_MANIFEST_SHA, 'IDENTITY_MISMATCH')

# Fixed controls are admitted before being opened. Never expand a historical inventory.
manifest_path = regular(P/'CANDIDATE_SOURCE_MANIFEST.json')
need(digest(manifest_path) == SOURCE_MANIFEST_SHA, 'SOURCE_MANIFEST_DRIFT')
source_pins = json.loads(manifest_path.read_bytes())['source_sha256']
need(len(source_pins) == 217, 'SOURCE_COUNT')
for name, h in source_pins.items():
    safe_relative(name)
    need(re.fullmatch('[0-9a-f]{64}', h) is not None, 'SOURCE_DIGEST')
source_targets = {root/name:h for root in (SOURCE,CLEAN) for name,h in source_pins.items()}
modules = {name.removeprefix('src/') for name in source_pins if name.startswith('src/cryptalis/') and name.endswith('.py')}
need(len(modules) == 41, 'MODULE_COUNT')
cells = ('sa21','sa20') if a.stage != 'optional38' else ('sqlmodel',)
roots = {c:B/f'release-lab/async-cleanup-installed-20261015/{c}' for c in cells} if a.stage != 'optional38' else {'sqlmodel':B/'release-lab/async-cleanup-sqlmodel-installed-20261015/sqlmodel'}
sites = {c:r/('lib/python3.14/site-packages' if c=='sqlmodel' else 'lib/python3.12/site-packages') for c,r in roots.items()}
need(binding['installed_roots'] == {c:str(r) for c,r in roots.items()}, 'INSTALLED_ROOTS')
installed = {s/n for s in sites.values() for n in modules} | {s/'cryptalis-0.1.0.dist-info/RECORD' for s in sites.values()}
need(set(binding['installed_records']) == {str(s/'cryptalis-0.1.0.dist-info/RECORD') for s in sites.values()}, 'INSTALLED_RECORD_SET')
for row in binding['installed_records'].values():
    need(row['rows'] in (50,51) and row['independent_record_hash_size_coverage_accepted'] is True, 'RECORD_ACCEPTANCE')
    need(row['rows'] == (51 if row['uv_cache_present'] else 50), 'RECORD_ROW_APPLICABILITY')
external = set() if a.stage != 'optional38' else {P/n for n in ('conftest.py','installed_origin.py','installed_sqlmodel_oracle_support.py','test_async_sqlmodel_public_hook.py')}
need(set(binding['external_sources']) == {str(p) for p in external}, 'EXTERNAL_SOURCE_SET')

contracts = binding['manifests']
need(set(contracts) == {'ENTRY.sha256','INPUTS.sha256','POSTINSTALL_CLEARANCE.sha256',stage_clearance}, 'MANIFEST_SET')
all_targets = {}
actual_manifests = {}
for name, contract in contracts.items():
    m = regular(P/name)
    need(re.fullmatch('[0-9a-f]{64}', contract['sha256']) is not None and digest(m) == contract['sha256'], 'MANIFEST_ANCHOR:'+name)
    targets = parse_manifest(m)
    need(targets == contract['targets'], 'MANIFEST_EXACT_TARGET_SET:'+name)
    actual_manifests[name] = targets
    for path, h in targets.items():
        need(path not in all_targets or all_targets[path] == h, 'CONFLICTING_DIGEST:'+path)
        all_targets[path] = h
need(set(binding['input_roles']) == set(all_targets), 'INPUT_ROLE_COVERAGE')
need({str(p) for p in source_targets} | {str(p) for p in HARNESS|installed|external|{WHEEL}} <= set(actual_manifests['INPUTS.sha256']), 'INPUT_CLOSURE_INCOMPLETE')
need(actual_manifests['INPUTS.sha256'][str(WHEEL)] == WHEEL_SHA, 'WHEEL_PIN')
need({str(p) for p in installed} <= set(actual_manifests['POSTINSTALL_CLEARANCE.sha256']), 'INSTALLED_CLEARANCE_PAYLOAD_SET')
required_receipts = {'payload_review','payload_audit','installer_verification','installer_parent_result'} | {f'{phase}_inode_{c}' for c in cells for phase in ('copy','installed')}
need(set(binding['accepted_installation_receipts']) == required_receipts, 'INSTALLATION_RECEIPT_ROLES')
expected_receipt_paths = INSTALLER_RECEIPTS['optional38' if a.stage == 'optional38' else 'main']
for role, path in expected_receipt_paths.items():
    need(binding['accepted_installation_receipts'][role] == str(path), 'INSTALLATION_RECEIPT_PATH:'+role)
for path in binding['accepted_installation_receipts'].values():
    need(path in actual_manifests['POSTINSTALL_CLEARANCE.sha256'], 'UNBOUND_INSTALLATION_RECEIPT')
required_reviews = {'source_sa21','source_sa20','build_artifact','installed_payload','final_runtime_plan'}
if a.stage in {'sa20','optional38'}: required_reviews.add('installed_sa21_terminal')
if a.stage == 'optional38': required_reviews |= {'installed_sa20_terminal','source_optional38'}
need(set(binding['accepted_stage_reviews']) == required_reviews, 'STAGE_REVIEW_ROLES')
for path in binding['accepted_stage_reviews'].values():
    need(path in actual_manifests[stage_clearance], 'UNBOUND_STAGE_REVIEW')

corpus_file = regular(P/'CORPUS_BASELINE.json')
corpus = json.loads(corpus_file.read_bytes())
need(len(corpus) == 26 and all('/' not in n and n.endswith('.json') for n in corpus), 'CORPUS_NAME_SCHEMA')
corpus_paths = {B/'evidence'/n for n in corpus}
found_corpus = {p for pattern in ('compatibility*corpus-v1-sa*.json','master-s4-compatibility*corpus-v1-sa*.json') for p in (B/'evidence').glob(pattern)}
need(found_corpus == corpus_paths, 'CORPUS_NAME_SET')
for p in corpus_paths: regular(p)
need({str(p) for p in corpus_paths} <= set(actual_manifests['INPUTS.sha256']), 'CORPUS_INPUT_CLOSURE')

# Fully admit ALL target paths/types/links before hashing ANY expanded payload.
# Safe external receipt paths are exact frozen declarations, not a directory glob.
allowed_external = {Path(x) for x in binding['safe_external_inputs']}
dependency_inputs = {Path(k):v for k,v in binding['dependency_inputs'].items()}
need(len(dependency_inputs) == (16 if a.stage == 'optional38' else 42), 'DEPENDENCY_SOURCE_METADATA_COUNT')
for p,h in dependency_inputs.items():
    need(any(p.is_relative_to(site) for site in sites.values()), 'DEPENDENCY_ROOT')
    need(p.suffix == '.py' or p.name == 'METADATA', 'DEPENDENCY_SOURCE_METADATA_TYPE')
    need(all_targets.get(str(p)) == h, 'DEPENDENCY_INPUT_PIN')
    need(p not in installed, 'DEPENDENCY_PRODUCT_OVERLAP')
if a.stage != 'optional38':
    for site in sites.values():
        expected_metadata = {p for p in dependency_inputs if p.is_relative_to(site) and p.name == 'METADATA'}
        observed_metadata = {p/'METADATA' for p in site.glob('*.dist-info') if (p/'METADATA').exists() or (p/'METADATA').is_symlink()}
        need(len(expected_metadata) == 14 and observed_metadata == expected_metadata, 'MAIN_METADATA_SET')
allowed_packet = {P/safe_relative(n) for n in binding['packet_members']}
allowed_targets = set(source_targets)|HARNESS|installed|external|{WHEEL}|allowed_external|allowed_packet|corpus_paths|set(dependency_inputs)
interps = {B/'repo/.venv/bin/python'} | {r/'bin/python' for r in roots.values()}
need(set(binding['interpreter_targets']) == {str(x) for x in interps}, 'INTERPRETER_SET')
need({str(p) for p in interps} <= set(actual_manifests['INPUTS.sha256']), 'INTERPRETER_INPUT_CLOSURE')
need({str(p) for p in dependency_inputs} <= set(actual_manifests['INPUTS.sha256']), 'DEPENDENCY_INPUT_CLOSURE')
need({str(p) for p in allowed_external} <= set(all_targets), 'UNUSED_EXTERNAL_ALLOWLIST_ENTRY')
allowed_targets |= interps
observed_links = {}
for text_path in all_targets:
    p = Path(text_path)
    lexical(p)
    need(p in allowed_targets, 'UNALLOWLISTED_INPUT:'+text_path)
    if p in interps:
        endpoint = Path(binding['interpreter_targets'][text_path])
        expected = B/'apps/runtime/python/cpython-3.14.8-linux-x86_64-gnu/bin/python3.14' if '/sqlmodel/' in text_path else Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12')
        need(endpoint == expected and p.resolve(strict=True) == endpoint and endpoint.is_file(), 'INTERPRETER_ENDPOINT')
        actual_endpoint, links = observed_link_chain(p)
        need(actual_endpoint == endpoint, 'INTERPRETER_CHAIN_ENDPOINT')
        observed_links.update(links)
    else:
        regular(p)
        if p in allowed_external and p not in dependency_inputs:
            need(p.suffix in {'.json','.md','.txt','.tsv','.sha256','.log','.xml','.py','.template'}, 'EXTERNAL_SUFFIX')
            need(p.is_relative_to(B/'reviewer-notes') or p in SAFE_INSTALLER_EXTERNALS or p.is_relative_to(B/'experiments/async-cleanup-release-plan-20261015'), 'EXTERNAL_ROOT')
need(observed_links == binding['allowed_symlinks'], 'EXACT_INTERPRETER_LINK_SET')
for p in source_targets: regular(p)
for root in (SOURCE,CLEAN): need(metadata_source_names(root) == set(source_pins), 'SOURCE_NAME_SET')
for name, h in binding['packet_members'].items():
    need(re.fullmatch('[0-9a-f]{64}', h) is not None, 'PACKET_DIGEST')
    regular(P/safe_relative(name))
for p, expected in source_targets.items(): need(all_targets[str(p)] == expected, 'SOURCE_INPUT_PIN')
for site in sites.values():
    for name in modules:
        need(all_targets[str(site/name)] == source_pins['src/'+name], 'INSTALLED_SOURCE_BYTES_PIN')
    record = str(site/'cryptalis-0.1.0.dist-info/RECORD')
    need(all_targets[record] == binding['installed_records'][record]['sha256'], 'INSTALLED_RECORD_PIN')
immutable_harness = {
 'candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py':'e5201530c7816a63e606b26352417daff6ca71aedeeccb7b569cea0edb309453',
 'candidate-corpus-wrapper-v2-20261014/corpus_artifacts_v2.py':'4c0429a182b5b7a2f7e561892936dba89ed279583bff181b18238f50485de86f',
 'toolchain/lab_progress.py':'673e3d41398f6be36876008f80110b313ad86553363052c8f14a25e1c47b93c1',
 'toolchain/run_baseline.py':'a88c24fa1699ce42a091c9d2da1168ba453d4548a811d542316fe95cb833d00f',
 'repo/scripts/test_postgres.py':'118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12'}
for name,h in immutable_harness.items(): need(all_targets[str(B/name)] == h, 'HARNESS_PIN')
need(source_pins['scripts/test_postgres.py'] == immutable_harness['repo/scripts/test_postgres.py'], 'PREFLIGHT_BYTES_PIN')
if a.stage == 'optional38':
    deps = json.loads(regular(P/'DEPENDENCY_SOURCE_PINS.json').read_bytes())
    need(len(deps) == 16, 'OPTIONAL_DEPENDENCY_PIN_COUNT')
    for name,h in deps.items():
        safe_relative(name)
        need(dependency_inputs[roots['sqlmodel']/name] == all_targets[str(roots['sqlmodel']/name)] == h, 'OPTIONAL_DEPENDENCY_PIN')
# Reject unsealed source additions in final packets. Only stage-gate JSON/manifests
# and run evidence may be additive; run evidence is never walked or consumed here.
packet_seen = set()
for directory, dirs, files in os.walk(P, followlinks=False):
    for name in dirs: need(not (Path(directory)/name).is_symlink(), 'PACKET_DIRECTORY_LINK')
    dirs[:] = [d for d in dirs if not (Path(directory)==P and d=='run') and d not in {'__pycache__','.pytest_cache'}]
    for name in files:
        q=Path(directory)/name
        need(not q.is_symlink() and q.is_file(), 'PACKET_FILE_TYPE')
        packet_seen.add(str(q.relative_to(P)))
additive = {'BINDING_SA21.json','BINDING_SA20.json','CLEARANCE_SA21.sha256','CLEARANCE_SA20.sha256'} if P==MAIN else {'BINDING_OPTIONAL38.json','CLEARANCE_OPTIONAL38.sha256'}
need(packet_seen-set(binding['packet_members'])-set(contracts)-{binding_name} <= additive, 'UNSEALED_PACKET_FILE')
for p, expected in all_targets.items(): need(digest(Path(p)) == expected, 'PAYLOAD_HASH:'+p)
for name, expected in binding['packet_members'].items(): need(digest(P/name) == expected, 'PACKET_MEMBER_HASH:'+name)
for name, expected in corpus.items(): need(digest(B/'evidence'/name) == expected, 'CORPUS_HASH:'+name)

if a.archive is not None:
    need(a.mode == 'before' and a.archive == P/'run'/audit_name/'frozen-inputs', 'ARCHIVE_DESTINATION')
    need(not a.archive.exists() and not a.archive.is_symlink(), 'EXISTING_ARCHIVE')
    a.archive.mkdir()
    archive_members = set(binding['packet_members']) | set(contracts) | {binding_name}
    for name in sorted(archive_members):
        p = regular(P/safe_relative(name))
        save(a.archive/'source-packet'/name, p.read_bytes())
    for name, expected in source_pins.items():
        data = (SOURCE/name).read_bytes()
        need(hashlib.sha256(data).hexdigest() == expected, 'SOURCE_CHANGED_DURING_ARCHIVE')
        save(a.archive/'source217'/name, data)
    for p in sorted(external):
        data = p.read_bytes()
        need(hashlib.sha256(data).hexdigest() == all_targets[str(p)], 'EXTERNAL_CHANGED_DURING_ARCHIVE')
        save(a.archive/'external-source'/p.name, data)
    save(a.archive/'archive-counts.json', (json.dumps({'source217':217,'packet_members':len(archive_members),'external_sources':len(external)}, sort_keys=True)+'\n').encode())
print(json.dumps({'status':'VERIFIED','stage':a.stage,'mode':a.mode,'binding_sha256':a.binding_sha256,'exact_input_count':len(all_targets),'source_files':217,'corpus_files':26,'installed_modules':41*len(cells),'external_sources':len(external),'verified_target_sha256':all_targets,'verified_packet_sha256':binding['packet_members'],'verified_corpus_sha256':corpus,'external_source_sha256':{str(p):all_targets[str(p)] for p in sorted(external)},'scope':'File identity and recorded gate binding only; no new authorization or imported-code attestation.'}, sort_keys=True))
