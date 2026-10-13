"""Executed with Python -I -S: no site packages or Cryptalis, real psql workload."""
import importlib.util,json,os,subprocess,sys
assert importlib.util.find_spec('cryptalis') is None
schema=sys.argv[1]
assert schema.startswith('cryptalis_migration_') and all(x.isalnum() or x=='_' for x in schema)
t='"'+schema+'".customer'
env=dict(os.environ)
query=f'''BEGIN;
SELECT coalesce(json_agg(json_build_array(id,name) ORDER BY id),'[]'::json) FROM {t};
INSERT INTO {t}(id,tenant_id,name,label) VALUES ('00000000-0000-0000-0000-000000000999','00000000-0000-0000-0000-0000000001f8','package-free 雪','native');
UPDATE {t} SET name='package-free updated' WHERE id='00000000-0000-0000-0000-000000000999';
SELECT count(*) FROM {t} WHERE name LIKE 'package-free%' AND name IS NOT NULL;
DELETE FROM {t} WHERE id='00000000-0000-0000-0000-000000000999';
COMMIT;
'''
r=subprocess.run(['psql','-X','-q','-A','-t','-v','ON_ERROR_STOP=1'],input=query,text=True,env=env,capture_output=True,timeout=15)
if r.returncode:raise RuntimeError('Native workload failed; database diagnostics withheld')
lines=r.stdout.strip().splitlines();rows=json.loads(lines[0]);assert lines[1]=='1'
print(json.dumps({'package_absent':True,'rows':rows,'insert_update_query_delete':'passed'}))
