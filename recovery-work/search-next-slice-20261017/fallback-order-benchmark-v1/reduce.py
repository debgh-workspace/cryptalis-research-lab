"""Read-only finite paired-sample reduction; no product imports or reruns."""
import hashlib
import json
import os
from pathlib import Path
import stat
import statistics
import sys

ROOT = Path('/workspace/scratch/cb28ee9f5f4a/recovery-work/search-next-slice-20261017/fallback-order-benchmark-v1')
CAPTURES = Path('/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/search-fallback-order-benchmark-20261017')
CAP = 1024 * 1024

def metadata(path):
    p = Path(path)
    assert p.is_absolute() and '..' not in p.parts
    for parent in p.parents:
        s = parent.lstat(); assert stat.S_ISDIR(s.st_mode) and not stat.S_ISLNK(s.st_mode)
    s = p.lstat(); assert stat.S_ISREG(s.st_mode) and s.st_nlink >= 1 and 0 <= s.st_size <= CAP
    return (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)

def read(path, stamp):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        s = os.fstat(f.fileno())
        assert (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns) == stamp
        data = f.read(CAP+1)
    assert len(data) <= CAP and metadata(path) == stamp
    return data

def digest(data): return hashlib.sha256(data).hexdigest()
def median(values): return statistics.median(values)

def main():
    assert len(sys.argv) == 4
    source_seal, capture_manifest_path, capture_manifest_seal = sys.argv[1:]
    capture_manifest_path = Path(capture_manifest_path)
    assert capture_manifest_path == CAPTURES/'CAPTURE_MANIFEST.json'
    inputs = {str(ROOT/'SOURCE.sha256'): source_seal,
              str(capture_manifest_path): capture_manifest_seal}
    before = {p:metadata(p) for p in inputs}
    raw = {p:read(p,before[p]) for p in inputs}
    assert all(digest(raw[p]) == h for p,h in inputs.items())
    members = {}
    for line in raw[str(ROOT/'SOURCE.sha256')].decode().splitlines():
        h,n = line.split('  ',1); assert n not in members and not Path(n).is_absolute() and '..' not in Path(n).parts
        members[n] = h
    controls = ('reduce.py','WORKLOAD.json','VIEWS.json','DEPENDENCIES.json')
    for n in controls:
        p = str(ROOT/n); inputs[p] = members[n]; before[p] = metadata(p)
    for n in controls:
        p = str(ROOT/n); raw[p] = read(p,before[p]); assert digest(raw[p]) == inputs[p]
    workload = json.loads(raw[str(ROOT/'WORKLOAD.json')])
    views = json.loads(raw[str(ROOT/'VIEWS.json')]); deps = json.loads(raw[str(ROOT/'DEPENDENCIES.json')])
    manifest = json.loads(raw[str(capture_manifest_path)])
    assert manifest['source_seal'] == source_seal and manifest['quiet_window'] is True
    assert manifest['sequence'] == workload['sequence'] == ['baseline','candidate','candidate','baseline']*4
    assert len(manifest['captures']) == 16
    for index, item in enumerate(manifest['captures']):
        assert item['index'] == index and item['variant'] == workload['sequence'][index]
        assert set(item['files']) == {'stdout','stderr','exit','after_exit'}
        for spec in item['files'].values():
            p = spec['path']; assert Path(p).is_relative_to(CAPTURES) and p not in inputs
            inputs[p] = spec['sha256']
    # Metadata-before-expanded-hashes; preserve already read control stamps.
    complete = {p:metadata(p) for p in inputs}
    assert all(complete[p] == s for p,s in before.items()); before = complete
    raw = {p:read(p,before[p]) for p in inputs}
    assert all(digest(raw[p]) == h for p,h in inputs.items())
    samples = {}; flags = []
    expected_cells = {c['id']:c for c in workload['cells']}
    assert len(expected_cells) == 8
    for index, item in enumerate(manifest['captures']):
        content = {k:raw[v['path']] for k,v in item['files'].items()}
        assert content['exit'] == b'0\n' and content['after_exit'] == b'0\n' and content['stderr'] == b''
        lines = content['stdout'].decode().splitlines(); assert len(lines) == 1 and lines[0].startswith('BENCHMARK_JSON ')
        result = json.loads(lines[0][len('BENCHMARK_JSON '):])
        assert result['scope'] == workload['scope'] and result['index'] == index and result['variant'] == item['variant']
        assert result['status'] == 'PASS' and result['primary_type'] is None and result['primary_stage'] is None
        assert result['bytecode_absence'] == 'PASS' and result['admitted'] == 448
        closure = {x['path'] for x in views[item['variant']]} | set(deps['files']) | {
            str(ROOT/n) for n in ('SOURCE.sha256','benchmark.py','DEPENDENCIES.json','VIEWS.json','WORKLOAD.json','PLAN.md')}
        assert len(closure) == 448 and set(result['closure']) == closure and set(result['closure'].values()) == {'PASS'}
        order = list(expected_cells); pair = index//2; order = order[pair:]+order[:pair]
        if pair%2: order.reverse()
        assert len(result['samples']) == 8 and [s['cell'] for s in result['samples']] == order
        for pos,s in enumerate(result['samples']):
            assert s['status'] == 'COMPLETE' and s['position'] == pos and s['calls'] == s['outputs_verified'] == 4096 and s['warmup_calls'] == 128
            for key in ('wall_ns','cpu_ns','maxrss_before_kib','maxrss_after_kib','voluntary_switches','involuntary_switches','minor_faults','major_faults'):
                assert type(s[key]) is int and s[key] >= 0
            assert s['wall_ns'] > 0 and s['cpu_ns'] > 0 and s['maxrss_after_kib'] >= s['maxrss_before_kib']
            samples[(index,s['cell'])] = s
            if s['wall_ns'] < workload['screen']['minimum_wall_ns']: flags.append([index,s['cell'],'short_sample'])
            if max(0,s['wall_ns']-s['cpu_ns'])/s['wall_ns'] > workload['screen']['wall_cpu_gap_max']: flags.append([index,s['cell'],'wall_cpu_gap'])
            if s['involuntary_switches'] > workload['screen']['involuntary_switch_max'] or s['major_faults'] > 0: flags.append([index,s['cell'],'scheduling_or_major_fault'])
    rows = []
    for cell_id, cell in expected_cells.items():
        pairs = []
        for pair in range(8):
            a,b = 2*pair,2*pair+1
            if workload['sequence'][a] != 'baseline': a,b = b,a
            base,candidate = samples[(a,cell_id)],samples[(b,cell_id)]
            pairs.append({'pair':pair,'wall_ratio':candidate['wall_ns']/base['wall_ns'],
                'cpu_ratio':candidate['cpu_ns']/base['cpu_ns'],
                'maxrss_difference_kib':candidate['maxrss_after_kib']-base['maxrss_after_kib']})
        row = {'cell':cell_id,'pairs':pairs}
        for metric in ('wall','cpu'):
            ratios = [p[metric+'_ratio'] for p in pairs]; row[metric+'_median_ratio'] = median(ratios)
            if cell['tenant_form'] == 'canonical':
                if median(ratios) > workload['screen']['canonical_median_ratio_max'] or sum(r<1 for r in ratios) < workload['screen']['canonical_improved_pairs_min']:
                    flags.append([cell_id,metric,'canonical_benefit_not_established'])
            else:
                if median(ratios) > workload['screen']['fallback_median_ratio_max'] or sum(r<=1.10 for r in ratios) < workload['screen']['fallback_pairs_under_1_10_min']:
                    flags.append([cell_id,metric,'fallback_regression_screen'])
            for variant in ('baseline','candidate'):
                values = [s[metric+'_ns'] for (i,c),s in samples.items() if c==cell_id and workload['sequence'][i]==variant]
                center=median(values); relative_mad=median([abs(v-center) for v in values])/center
                row[variant+'_'+metric+'_relative_mad']=relative_mad
                if relative_mad > workload['screen']['relative_mad_max']: flags.append([cell_id,variant,metric,'dispersion'])
        if median([p['maxrss_difference_kib'] for p in pairs]) > workload['screen']['max_rss_regression_kib']:
            flags.append([cell_id,'maxrss_regression_screen'])
        rows.append(row)
    # Complete immutable input aftercheck; no data deletion or sample trimming.
    after = {p:metadata(p) for p in inputs}
    assert after == before
    assert all(digest(read(p,after[p])) == h for p,h in inputs.items())
    print(json.dumps({'status':'LOCAL_STEADY_STATE_SCREEN_PASS' if not flags else 'HOLD',
        'source_seal':source_seal,'capture_manifest_sha256':capture_manifest_seal,
        'processes':16,'pairs':8,'samples':len(samples),'timed_calls':16*8*4096,
        'warmup_calls':16*8*128,'rows':rows,'flags':flags,
        'construction_and_initialization':'excluded; tiny-resultset and end-to-end benefit unmeasured',
        'claims':'exploratory same-host steady-state result-processor screen only; no statistical significance or production claim'},sort_keys=True))
    return 0 if not flags else 1

if __name__ == '__main__': raise SystemExit(main())
