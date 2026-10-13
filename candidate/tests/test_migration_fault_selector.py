"""Keep real-wire fault selection independent of aliases and SELECT spelling."""
import pytest
from migration_commit_proxy import is_verification_sql,matches_sql

FRAME='"_cryptalis_'+'0'*32+'"'
@pytest.mark.parametrize('query,expected',[
 ('SELECT id,name,'+FRAME+' FROM t',True),
 ('WITH candidates AS (SELECT id FROM t) SELECT d.'+FRAME+' FROM t d',True),
 ('SELECT id,tenant_id,name FROM t',False),
 ('WITH candidates AS (SELECT id,octet_length(name) FROM t) SELECT name FROM t',False),
 ('UPDATE t SET '+FRAME+'=NULL',False),
 ('',False),
])
def test_selector_matches_frame_reads_not_mutations_or_identity_scans(query,expected):
    assert is_verification_sql(query)==expected
    assert matches_sql(is_verification_sql,query.encode()+b'\0',b'Q')==expected
    assert matches_sql(is_verification_sql,b'fixture_statement\0'+query.encode()+b'\0\0\0',b'P')==expected
