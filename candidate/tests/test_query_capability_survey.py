"""Executable capability cells: refusal PASS is not native-query support."""
import json
from pathlib import Path
import pytest
from sqlalchemy import select, func, and_, or_, text, update, cast, Text, event, bindparam
from sqlalchemy.orm import aliased
from sqlalchemy.exc import DBAPIError
from cryptalis.sqlalchemy import UnsupportedProtectedOperation
from test_sqlalchemy_search import search_application, _row

CASES={
    'is_null':True, 'is_not_null':True, 'equal':True, 'not_equal':True,
    'in':True, 'in_null':True, 'in_empty':True, 'not_in':True, 'range':False,
    'between':False, 'ordering':False, 'pagination_public_order':True,
    'distinct':False, 'group_by':False, 'count_protected':False,
    'count_star':True, 'min':False, 'like':False, 'ilike':False,
    'lower':False, 'length':False, 'cast':False, 'full_text':False,
    'json_function':False, 'nested_boolean':True, 'subquery':True,
    'public_join':True, 'protected_join':False, 'raw_sql':False, 'bulk_update':False,
}
RESULTS=[]
@pytest.fixture(scope='module',autouse=True)
def survey_evidence():
    yield
    destination=Path(__file__).resolve().parents[2]/'evidence/cp08-query-capabilities.json'
    destination.write_text(json.dumps(RESULTS,indent=2)+'\n')

def statement(app,name):
    c=app.Customer
    base=select(c.rank).order_by(c.rank)
    predicates={
        'is_null':lambda:c.name.is_(None),'is_not_null':lambda:c.name.is_not(None),
        'equal':lambda:c.name=='alpha','not_equal':lambda:c.name!='alpha',
        'in':lambda:c.name.in_(['alpha','beta']), 'in_null':lambda:c.name.in_(['alpha',None]),
        'in_empty':lambda:c.name.in_([]), 'not_in':lambda:c.name.not_in(['alpha',None]),
        'range':lambda:c.name<'beta', 'between':lambda:c.name.between(bindparam('lo','alpha',type_=Text()),bindparam('hi','beta',type_=Text())),
        'like':lambda:c.name.like('alpha%'), 'ilike':lambda:c.name.ilike('ALPHA%'),
        'nested_boolean':lambda:and_(or_(c.name=='alpha',c.name.is_(None)),c.rank>=0),
        'full_text':lambda:func.to_tsvector('simple',c.name).op('@@')(func.plainto_tsquery('simple','alpha')),
    }
    if name in predicates:return base.where(predicates[name]())
    if name=='ordering':return select(c.name).order_by(c.name.nulls_last(),c.rank)
    if name=='pagination_public_order':return select(c.name).order_by(c.rank).offset(1).limit(2)
    if name=='distinct':return select(c.name).distinct()
    if name=='group_by':return select(c.name,func.count()).group_by(c.name)
    if name=='count_protected':return select(func.count(c.name))
    if name=='count_star':return select(func.count()).select_from(c).where(c.name.in_(['alpha','beta']))
    if name=='min':return select(func.min(c.name))
    if name=='lower':return select(func.lower(c.name)).order_by(c.rank)
    if name=='length':return select(func.length(c.name)).order_by(c.rank)
    if name=='cast':return select(cast(c.name,Text)).order_by(c.rank)
    if name=='json_function':return select(func.json_build_object('value',c.name)).order_by(c.rank)
    if name=='subquery':
        sub=select(c.rank).where(c.name=='alpha').subquery()
        return select(sub.c.rank)
    if name in ('public_join','protected_join'):
        other=aliased(c)
        on=c.rank==other.rank if name=='public_join' else c.name==other.name
        return select(c.rank,other.name).join(other,on).order_by(c.rank)
    if name=='raw_sql':return text(f'SELECT name FROM "{app.schema}".customer ORDER BY rank')
    if name=='bulk_update':return update(c).where(c.rank==0).values(name='updated')
    raise AssertionError(name)

@pytest.mark.parametrize('name',CASES)
def test_query_capability_matches_native_or_refuses_before_sql(name):
    outcomes=[]
    for protected in (False,True):
        with search_application(protected) as app:
            with app.sessions(tenant_id=app.tenant) as seed:
                seed.add_all([_row(app,value,i) for i,value in enumerate([None,'alpha','alphabet','beta'])])
                seed.commit()
            emitted=[]
            def cursor(*args):emitted.append('SQL')
            event.listen(app.engine,'before_cursor_execute',cursor)
            with app.sessions(tenant_id=app.tenant) as session:
                try:
                    result=session.execute(statement(app,name))
                    actual=result.rowcount if name=='bulk_update' else [tuple(r) for r in result]
                    outcomes.append(actual)
                except DBAPIError as exc:
                    print("SURVEY_DATABASE_FAILURE",name,"protected",protected,"sqlstate",getattr(exc.orig,"sqlstate",None),"type",type(exc.orig).__name__)
                    if not protected:
                        print("NATIVE_SQL_TEMPLATE", exc.statement)
                        print("NATIVE_DIAGNOSTIC", exc.orig.diag.message_primary, exc.orig.diag.statement_position)
                    raise
                except UnsupportedProtectedOperation:
                    assert protected and not CASES[name]
                    assert emitted==[]
                    RESULTS.append(dict(operation=name,status='VERIFIED_REFUSAL',native_executed=True,protected_sql=0))
                    return
            assert not protected or CASES[name],f'{name} unexpectedly admitted'
    assert outcomes[0]==outcomes[1]
    RESULTS.append(dict(operation=name,status='VERIFIED_EXACT_CELL',native_executed=True,protected_executed=True))


@pytest.mark.parametrize('shape',['and_over_or','or_over_and','double','double_chained','projection','grouped_not_equal','grouped_function'])
def test_grouped_predicates_preserve_truth_and_reject_unadmitted_children(shape):
    from sqlalchemy.sql.elements import Grouping
    outcomes=[]
    denied=shape == 'grouped_function'
    for protected in (False,True):
        with search_application(protected) as app:
            c=app.Customer
            with app.sessions(tenant_id=app.tenant) as seed:
                seed.add_all([_row(app,v,i) for i,v in enumerate([None,'alpha','beta','alphabet'])])
                seed.commit()
            if shape=='and_over_or':predicate=and_(or_(c.name=='alpha',c.name.is_(None)),c.rank>=0)
            elif shape=='or_over_and':predicate=or_(and_(c.name=='alpha',c.rank>=1),and_(c.name=='beta',c.rank<3))
            elif shape in ('double','double_chained'):predicate=Grouping(Grouping(or_(c.name=='alpha',c.name.is_(None))))
            elif shape=='projection':predicate=Grouping(or_(c.name=='alpha',c.name=='beta'))
            elif shape=='grouped_not_equal':predicate=Grouping(or_(c.name=='alpha',c.name!='beta'))
            else:predicate=Grouping(func.lower(c.name)=='alpha')
            query=(select(c.rank,predicate).order_by(c.rank) if shape=='projection'
                   else select(c.rank).where(predicate).order_by(c.rank))
            if shape=='double_chained':query=query.where(c.rank>=0)
            emitted=[]
            event.listen(app.engine,'before_cursor_execute',lambda *args:emitted.append('SQL'))
            with app.sessions(tenant_id=app.tenant) as session:
                if protected and denied:
                    with pytest.raises(UnsupportedProtectedOperation):session.execute(query)
                    assert emitted==[]
                else:
                    outcomes.append([tuple(r) for r in session.execute(query)])
    if not denied:assert outcomes[0]==outcomes[1]
