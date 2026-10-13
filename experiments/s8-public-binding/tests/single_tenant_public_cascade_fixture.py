"""Explicit owned equality-indexed single-tenant retained-layout fixture."""
from test_migration import *
from sqlalchemy import ForeignKey

@contextmanager
def single_tenant_public_cascade_application(rows=7, *, unique=True, single_tenant=True, extra_blob=False, public_table=True):
    owner,runtime=engine('CRYPTALIS_TEST_DATABASE_URL'),engine('CRYPTALIS_TEST_RUNTIME_DATABASE_URL')
    schema='cryptalis_public_cascade_'+uuid4().hex
    mapping=registry(metadata=MetaData(schema=schema))
    columns=[Column('id',Uuid,primary_key=True,autoincrement=False),Column('name',Text(collation='C')),Column('label',Text)]
    if not single_tenant:columns.append(Column('tenant_id',Uuid,nullable=False))
    if extra_blob:
        from sqlalchemy import LargeBinary
        columns.append(Column('public_blob',LargeBinary))
    table=Table('customer',mapping.metadata,*columns)
    Index('name_native',*([table.c.tenant_id,table.c.name] if unique and not single_tenant else [table.c.name]),unique=unique)
    class Customer:pass
    mapping.map_imperatively(Customer,table)
    public_item=None;PublicItem=None
    if public_table:
        public_item=Table('public_item',mapping.metadata,Column('id',Uuid,primary_key=True,autoincrement=False),Column('label',Text),Column('parent_id',Uuid,ForeignKey(table.c.id,ondelete='CASCADE'),nullable=False))
        class PublicItem:pass
        mapping.map_imperatively(PublicItem,public_item)
    declaration={'schema':'cryptalis.protection/v1','profile':'cf1','domain_id':str(DOMAIN),
        'models':[{'model':'Customer','table_id':str(TABLE_ID),'tenancy':({'single_tenant':True} if single_tenant else {'column':'tenant_id'}),
        'fields':[{'name':'name','field_id':str(FIELD_ID),'protect':True,'queries':['equality','unique'] if unique else ['equality'],'accept_leakage':['equality','unique'] if unique else ['equality']}]}]}
    with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as c:role=c.execute('SELECT current_user').fetchone()[0]
    try:
        with owner.begin() as c:c.execute(text(f'CREATE SCHEMA "{schema}"'))
        mapping.metadata.create_all(owner)
        with psycopg.connect(os.environ['CRYPTALIS_TEST_DATABASE_URL']) as c:
            c.execute(sql.SQL('REVOKE ALL ON SCHEMA {} FROM PUBLIC').format(sql.Identifier(schema)))
            c.execute(sql.SQL('GRANT USAGE ON SCHEMA {} TO {}').format(sql.Identifier(schema),sql.Identifier(role)))
            c.execute(sql.SQL('GRANT SELECT,INSERT,UPDATE,DELETE ON {}.customer TO {}').format(sql.Identifier(schema),sql.Identifier(role)))
        if public_table:
            with psycopg.connect(os.environ['CRYPTALIS_TEST_DATABASE_URL']) as c:
                c.execute(sql.SQL('GRANT SELECT,INSERT,UPDATE,DELETE ON {}.public_item TO {}').format(sql.Identifier(schema),sql.Identifier(role)))
        source={UUID(int=i+100):(TABLE_ID if single_tenant else TENANT,[None,'','雪😀','e\u0301','é','exact','trailing '][i%7]) for i in range(rows)}
        with sessionmaker(runtime)() as s:
            s.add_all(Customer(id=k,name=v,label=f'label-{k.int}',**({} if single_tenant else {'tenant_id':t})) for k,(t,v) in source.items());s.commit()
            if public_table:
                s.add_all(PublicItem(id=UUID(int=10000+i),label=f'child-{i}',parent_id=k) for i,k in enumerate(source));s.commit()
        m=importlib.import_module('cryptalis.migration')
        proposal=m.plan(json.dumps(declaration).encode(),mapping,owner,
            writers=WriterInventory(True,(Writer(TABLE_ID,'app','sqlalchemy',evidence='owned single-tenant equality-indexed fixture'),)),
            search_reviews=(SearchReview(FIELD_ID,False,'Synthetic C-collated account labels; declared equality/frequency leakage'),),keys=keys,runtime_role=role,target_id=uuid4(),backfill_rows_per_second=1000,verify_rows_per_second=1000,temporary_bytes_per_row=700,wal_bytes_per_row=2000)
        pin=m.DeploymentPin(proposal.target_id,proposal.operation_id,proposal.digest,'PREPARED')
        yield SimpleNamespace(m=m,owner=owner,runtime=runtime,schema=schema,mapping=mapping,table=table,Customer=Customer,PublicItem=PublicItem,public_item=public_item,source=source,plan=proposal,pin=pin,role=role,approval=m.MaintenanceApproval('Synthetic fixture only; inventoried application is stopped',3600))
    finally:
        runtime.dispose()
        with owner.begin() as c:c.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
        owner.dispose();mapping.dispose()
