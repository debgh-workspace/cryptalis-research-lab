"""Additive bounded launcher. V1 sources stay frozen and are never rewritten."""
import hashlib
import json
from pathlib import Path
import resource

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
RECEIPTS=HERE/'parent-results-v3'
SUPERVISOR_SHA='b5cc92887125d1b923cb49f9d673a922a75d55f31f19efb4934992c02a1f0065'

def digest(data):return hashlib.sha256(data).hexdigest()

def verify_manifest(manifest,root):
    errors=[];count=0;seen=set()
    try:
        lines=manifest.read_text().splitlines()
        for line in lines:
            expected,name=line.split('  ',1)
            if name in seen:raise ValueError('duplicate_manifest_path:'+name)
            seen.add(name)
            path=Path(name) if name.startswith('/') else root/name
            try:
                actual=digest(path.read_bytes())
                if actual!=expected:errors.append({'path':str(path),'error':'digest_mismatch','expected':expected,'actual':actual})
            except BaseException as exc:errors.append({'path':str(path),'error':repr(exc)})
            count+=1
    except BaseException as exc:errors.append({'manifest':str(manifest),'error':repr(exc)})
    return {'manifest':str(manifest),'checked':count,'pass':not errors,'errors':errors}

def integrity():
    # All four checks execute even if a preceding group fails.
    return [verify_manifest(HERE/'outer-frozen-v3.sha256',HERE),
            verify_manifest(HERE/'frozen-inputs.sha256',HERE),
            verify_manifest(HERE/'original-source.sha256',BASE/'candidate-accel-payload-integrated-20261014'),
            verify_manifest(HERE/'derivative-source.sha256',HERE/'source')]

def main():
    # Exclusive parent evidence, distinct from V1's exclusive run/ output.
    RECEIPTS.mkdir(exist_ok=False)
    original_limits=None
    report={'status':'NOT_STARTED','wall_seconds':120,'captured_stream_cap_each':2097152,
            'child_regular_file_limit_bytes':8388608,'before':None,'after':None,
            'child':None,'errors':[], 'v1_artifacts_preserved':True}
    env={'PATH':'/usr/bin:/bin','HOME':str(RECEIPTS/'home'),'TMPDIR':str(RECEIPTS/'tmp'),
         'LC_ALL':'C.UTF-8','LANG':'C.UTF-8','TZ':'UTC','SOURCE_DATE_EPOCH':'0',
         'UV_OFFLINE':'1','UV_CACHE_DIR':str(RECEIPTS/'cache'),'PYTHONDONTWRITEBYTECODE':'1'}
    try:
        for name in ['home','tmp','cache']:(RECEIPTS/name).mkdir(exist_ok=False)
        report['before']=integrity()
        if not all(x['pass'] for x in report['before']):raise ValueError('preflight_integrity')
        if (HERE/'run').exists():raise ValueError('v1_run_output_exists')
        source=(HERE/'supervisor_v2.py').read_bytes()
        if digest(source)!=SUPERVISOR_SHA:raise ValueError('supervisor_identity')
        namespace={'__name__':'pinned_bounded_supervisor','__file__':str(HERE/'supervisor_v2.py')}
        exec(compile(source,str(HERE/'supervisor_v2.py'),'exec'),namespace)
        # Bound redirected per-step logs as well as supervisor-captured streams.
        # This limit is inherited by bash and its build/helper children.
        original_limits=resource.getrlimit(resource.RLIMIT_FSIZE)
        soft,hard=original_limits
        limit=8388608 if soft==resource.RLIM_INFINITY else min(8388608,soft)
        resource.setrlimit(resource.RLIMIT_FSIZE,(limit,hard))
        report['child_regular_file_limit_bytes']=limit
        report['parent_original_fsize_limits']=list(original_limits)
        report['child']=namespace['bounded'](['/bin/bash',str(HERE/'run-after-review.sh')],env,120,2097152)
        child=report['child']
        if child['reason'] is not None or child['exit_code']!=0 or child['cleanup_errors'] or not child['leader_reaped']:
            raise ValueError('child_failed_or_cleanup_incomplete')
        report['status']='PASS_BOUNDED_PACKAGING'
    except BaseException as exc:
        report['status']='FAIL'
        report['errors'].append(repr(exc))
    finally:
        # Child cleanup is complete before restoring the parent's original soft
        # limit. The hard limit was never lowered; restoration needs no privilege.
        if original_limits is not None:
            try:
                resource.setrlimit(resource.RLIMIT_FSIZE,original_limits)
                report['parent_fsize_limits_restored']=True
            except BaseException as exc:
                report['status']='FAIL'
                report['parent_fsize_limits_restored']=False
                report['errors'].append('restore_parent_fsize: '+repr(exc))
        # Always attempt each frozen-input/source integrity group, even on set-e
        # failure, supervisor timeout/cap, launch exception, or Python interruption.
        report['after']=integrity()
        if not all(x['pass'] for x in report['after']):report['status']='FAIL_INTEGRITY'
        report['outer_environment']=env
        report['inner_environment_note']='V1 replaces HOME/TMPDIR/UV_CACHE_DIR with run/home, run/tmp, run/cache; all other declared variables match V1 launcher.'
        with (RECEIPTS/'parent-receipt.json').open('x') as stream:
            json.dump(report,stream,indent=2,sort_keys=True);stream.write('\n')
    return 0 if report['status']=='PASS_BOUNDED_PACKAGING' else 1

if __name__=='__main__':raise SystemExit(main())
