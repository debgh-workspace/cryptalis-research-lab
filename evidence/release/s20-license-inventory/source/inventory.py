"""Read-only declared-license evidence. No product imports, downloads or subprocesses."""
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import tomllib
from email.parser import BytesParser

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
class Invalid(ValueError):
    pass

def need(value, reason):
    if not value:
        raise Invalid(reason)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def norm(name):
    return re.sub(r'[-_.]+', '-', name).lower()

def parse(data):
    def hook(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, 'duplicate_json_key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=hook)

def input_pins():
    pins = {}
    for line in (HERE / 'inputs.sha256').read_text().splitlines():
        digest, name = line.split('  ', 1)
        path = BASE / name
        need(path.resolve().is_relative_to(BASE.resolve()), 'pin_path_escape')
        need(name not in pins, 'duplicate_pin')
        need(sha(path.read_bytes()) == digest, 'pin_mismatch:' + name)
        pins[name] = digest
    return pins

def record_rows(data):
    rows = list(csv.reader(io.StringIO(data.decode())))
    need(all(len(r) == 3 for r in rows), 'record_shape')
    need(len(rows) == len({r[0] for r in rows}), 'record_duplicates')
    # Do not resolve or read arbitrary RECORD paths (some legitimately reference bin/).
    return {r[0]: r[1:] for r in rows}

def member_evidence(relative, data, rows):
    need(data is not None, 'missing_notice')
    need(relative in rows, 'record_member_missing')
    encoded = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b'=').decode()
    need(rows[relative] == ['sha256=' + encoded, str(len(data))], 'member_hash_mismatch')
    return {'member':relative, 'sha256':sha(data), 'bytes':len(data), 'local_record_matches':True}

def vendor_parse(data):
    bom = parse(data)
    need(bom.get('bomFormat') == 'CycloneDX', 'vendor_format')
    need(isinstance(bom.get('components'), list), 'vendor_components')
    # Preserve vendor declarations verbatim; do not synthesize license identifiers.
    fields = ('name','version','bom-ref','purl','licenses','hashes')
    output = [{k:c[k] for k in fields if k in c} for c in bom['components']]
    root = bom.get('metadata', {}).get('component')
    return {'spec_version':bom.get('specVersion'), 'components':output,
            'root_component':{k:root[k] for k in fields if k in root} if root else None,
            'license_fields_present':sum('licenses' in c for c in bom['components']),
            'coverage':'Upstream declaration only; no completeness or binary-to-component identity established.'}

def main():
    before = input_pins()
    expected = parse((HERE / 'expected.json').read_bytes())
    mismatch = parse((HERE / 'environment-mismatch.json').read_bytes())
    lock = tomllib.loads((BASE / mismatch['lock_path']).read_text())
    locked = {p['name']:p['version'] for p in lock['package']}
    result, notices, rows_by_component = [], [], {}
    for c in expected['components']:
        need(locked[c['name']] == c['version'], 'component_lock_version')
        root = BASE / expected[c['origin']]
        info = root / c['directory']
        metadata_data = (info / 'METADATA').read_bytes()
        msg = BytesParser().parsebytes(metadata_data)
        need(norm(msg['Name']) == c['name'] and msg.get_all('Version') == [c['version']], 'metadata_identity')
        need(msg.get_all('License-Expression') == [c['expression']], 'license_expression')
        need(msg.get_all('License-File') == c['notices'], 'declared_notice_inventory')
        rows = record_rows((info / 'RECORD').read_bytes())
        rows_by_component[c['directory']] = rows
        member_evidence(c['directory'] + '/METADATA', metadata_data, rows)
        component_notices = []
        for name in c['notices']:
            need('/' not in name and name not in ('.','..'), 'notice_name')
            path = info / 'licenses' / name
            data = path.read_bytes() if path.is_file() else None
            evidence = member_evidence(c['directory'] + '/licenses/' + name, data, rows)
            evidence['path'] = str(path.relative_to(BASE))
            evidence['bytes_base64'] = base64.b64encode(data).decode()
            notices.append(evidence)
            component_notices.append(evidence)
        result.append({'name':c['name'], 'version':c['version'], 'declared_license_expression':msg['License-Expression'],
                       'metadata_path':str((info/'METADATA').relative_to(BASE)), 'metadata_sha256':sha(metadata_data),
                       'origin_kind':'local installed files' if c['origin']=='site' else 'local unpacked cache files',
                       'original_distribution_archive_digest_verified':False, 'notices':component_notices})
    need(len(result)==8 and len(notices)==expected['notice_count'], 'component_notice_count')
    site = BASE / expected['site']
    vendors = []
    for relative in expected['vendor_sboms']:
        data = (site / relative).read_bytes()
        evidence = member_evidence(relative, data, rows_by_component[relative.split('/')[0]])
        evidence['path'] = str((site/relative).relative_to(BASE))
        evidence['declared'] = vendor_parse(data)
        vendors.append(evidence)
    libs = sorted((site / 'psycopg_binary.libs').iterdir())
    need(len(libs)==expected['bundled_library_count'] and all(p.is_file() for p in libs), 'bundled_inventory')
    bundled = []
    for path in libs:
        relative = str(path.relative_to(site))
        item = member_evidence(relative, path.read_bytes(), rows_by_component['psycopg_binary-3.3.6.dist-info'])
        item['path'] = str(path.relative_to(BASE))
        item['license_assignment'] = 'UNKNOWN; no inference from filename or top-level license'
        bundled.append(item)
    observations = []
    for cell in mismatch['cells']:
        cellsite = BASE / cell['site_path']
        origin_data = (BASE / cell['origin_log_path']).read_bytes()
        need(sha(origin_data)==cell['origin_log_sha256'], 'origin_pin')
        origin = parse(origin_data)
        need(origin['package_origin']==str(cellsite/'cryptalis/__init__.py'), 'origin_path')
        wanted = dict(mismatch['runtime_union_locked_versions'])
        wanted.update(mismatch['test_only_locked_versions'])
        wanted['sqlalchemy'] = cell['intentional_sqlalchemy_version']
        wanted.update({m['name']:m['observed_version'] for m in mismatch['mismatches_in_both_cells']})
        present = {}
        for path in sorted(cellsite.glob('*.dist-info/METADATA')):
            data = path.read_bytes()
            msg = BytesParser().parsebytes(data)
            name = norm(msg['Name'])
            if name not in wanted:
                continue
            need(name not in present, 'duplicate_current_distribution')
            need(msg.get_all('Version')==[wanted[name]], 'current_version:' + name)
            need(str(path.relative_to(BASE)) in before, 'unfrozen_metadata')
            present[name] = {'version':msg['Version'], 'path':str(path.relative_to(BASE)), 'sha256':sha(data)}
        need(set(wanted)-set(present)==set(mismatch['absent_both_cells']), 'absent_current_components')
        for item in mismatch['mismatches_in_both_cells']:
            need(sha((cellsite/item['metadata_relative_path']).read_bytes())==item['metadata_sha256'], 'mismatch_metadata_pin')
            need(locked[item['name']]==item['locked_version'], 'mismatch_lock_version')
        observations.append({'cell':cell['cell'], 'current_metadata':present, 'absent':mismatch['absent_both_cells'],
                             'historical_execution_identity':'NOT_ESTABLISHED'})
    controls = []
    def negative(name, action, reason):
        try:
            action()
        except (Invalid,json.JSONDecodeError) as exc:
            need(reason in str(exc), 'negative_wrong_reason:' + name)
            controls.append({'id':name,'rejected':True,'reason':reason})
        else:
            raise Invalid('negative_accepted:' + name)
    negative('malformed_vendor_sbom', lambda:vendor_parse(b'{'), 'Expecting property name')
    first = notices[0]
    first_rows = rows_by_component[first['member'].split('/')[0]]
    negative('missing_notice', lambda:member_evidence(first['member'],None,first_rows), 'missing_notice')
    negative('notice_hash_mismatch', lambda:member_evidence(first['member'],b'altered',first_rows), 'member_hash_mismatch')
    need([c['id'] for c in controls]==expected['negative_controls'], 'control_count')
    need(input_pins()==before, 'after_integrity')
    print(json.dumps({'status':'PASS_SCOPED_EVIDENCE_INVENTORY','components':result,
                      'missing_union_components':expected['missing_union_components'],'vendor_sboms':vendors,
                      'bundled_library_files':bundled,'current_environment_observations':observations,
                      'negative_controls':controls,'input_pins':before,
                      'limits':['Declared identifiers/notices only; no legal compatibility or compliance conclusion.',
                                'Local RECORD consistency is not original downloaded wheel hash authentication.',
                                'Platform variants and native notice completeness remain unverified.',
                                'Current metadata cannot attest historical executed code.'],
                      'gates':{g:'UNKNOWN' for g in ['G-ADAPTER','G-CRYPTO','G-QUERY','G-LIFECYCLE','G-PROVIDER','G-POLICY','G-RELEASE']}},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
