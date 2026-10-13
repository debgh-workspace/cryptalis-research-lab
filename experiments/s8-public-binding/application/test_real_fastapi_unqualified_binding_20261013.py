"""Run the actual upstream suite twice; app outcomes are separate from harness completion."""
from pathlib import Path
import json,os,subprocess,sys,hashlib,shutil,xml.etree.ElementTree as ET
B=Path(__file__).resolve().parents[1]

def test_real_fastapi_native_then_attached_suite():
    evidence=Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent
    secrets=json.loads((B/'apps/runtime/private/fastapi-env.json').read_text())
    secrets.update({k:v for k,v in os.environ.items() if k in ('CRYPTALIS_TEST_DATABASE_URL','CRYPTALIS_TEST_RUNTIME_DATABASE_URL')})
    results=[]
    diagnostic=B/'apps/harness/fastapi_unqualified_binding_trial_20261013.py'
    diagnostic_before=hashlib.sha256(diagnostic.read_bytes()).hexdigest()
    worker=B/'apps/harness/fastapi_cascade_package_free_worker_20261012.py'
    worker_before=hashlib.sha256(worker.read_bytes()).hexdigest()
    shutil.copy(worker,evidence/worker.name)
    shutil.copy(diagnostic,evidence/diagnostic.name)
    for mode in ('native','protected'):
        target=evidence/mode
        run=subprocess.run([sys.executable,str(B/'apps/harness/fastapi_unqualified_binding_trial_20261013.py'),mode,str(target)],capture_output=True,text=True,timeout=180)
        output=run.stdout+run.stderr
        for key,value in secrets.items():
            if any(x in key for x in ('PASSWORD','SECRET','KEY','URL')) and value:output=output.replace(value,'<redacted>')
        (evidence/(mode+'-application.log')).write_text(output)
        assert run.returncode==0,mode+' harness failed; inspect sanitized evidence'
        result=json.loads((target/'application-result.json').read_text());assert result['source_unchanged']
        suite=ET.parse(target/'application-junit.xml').getroot().find('testsuite')
        result['counts']={k:int(suite.attrib[k]) for k in ('tests','failures','errors','skipped')}
        result.pop('source_hashes');results.append(result)
        if mode=='native':assert result['pytest_exit_code']==0,'Native baseline failed; do not attribute protected differences'
        else:assert result['pytest_exit_code']==0,'Protected full suite must pass for the cascade experiment'
    (evidence/'paired-application-results.json').write_text(json.dumps(results,indent=2))

    assert hashlib.sha256(diagnostic.read_bytes()).hexdigest()==diagnostic_before
    (evidence/'diagnostic-source-stability.json').write_text(json.dumps({'sha256':diagnostic_before,'unchanged':True,'scope':'External diagnostic harness copied before native/protected application runs'},indent=2)+'\n')

    assert hashlib.sha256(worker.read_bytes()).hexdigest()==worker_before
    (evidence/'package-free-worker-source-stability.json').write_text(json.dumps({'sha256':worker_before,'unchanged':True,'scope':'External package-free child verifier copied before execution'},indent=2)+'\n')
