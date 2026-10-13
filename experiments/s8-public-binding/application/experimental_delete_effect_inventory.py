"""Read-only FK-effect inventory experiment. Never grants DELETE admission.
Catalog graph only: trigger function bodies and arbitrary code effects are unknown.
"""
from sqlalchemy import text

_RELATION = text('''SELECT c.oid::bigint AS oid,n.nspname AS schema,c.relname AS name,
 c.relkind,c.relispartition,c.relrowsecurity,c.relforcerowsecurity,
 EXISTS(SELECT 1 FROM pg_catalog.pg_inherits h WHERE h.inhrelid=c.oid OR h.inhparent=c.oid) AS inheritance,
 ARRAY(SELECT t.tgname FROM pg_catalog.pg_trigger t WHERE t.tgrelid=c.oid AND NOT t.tgisinternal ORDER BY t.tgname) AS user_triggers,
 EXISTS(SELECT 1 FROM pg_catalog.pg_rewrite r WHERE r.ev_class=c.oid) AS rewrite_rules
 FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace
 WHERE c.oid=:oid''')
_EDGES = text('''SELECT con.oid::bigint AS oid,con.conname AS name,
 con.confrelid::bigint AS parent_oid,con.conrelid::bigint AS child_oid,
 con.confdeltype AS action,con.condeferrable AS deferrable,con.condeferred AS deferred,
 con.convalidated AS validated,con.conkey::int[] AS child_columns,
 con.confkey::int[] AS parent_columns
 FROM pg_catalog.pg_constraint con WHERE con.contype='f' AND con.confrelid=:oid ORDER BY con.oid''')

_INDEXES = text('''SELECT ix.relname AS name,i.indisunique AS unique_index,
 i.indisvalid AS valid,i.indisready AS ready,i.indislive AS live,am.amname AS method,
 pg_catalog.pg_get_expr(i.indexprs,i.indrelid) AS expression,
 pg_catalog.pg_get_expr(i.indpred,i.indrelid) AS predicate
 FROM pg_catalog.pg_index i JOIN pg_catalog.pg_class ix ON ix.oid=i.indexrelid
 JOIN pg_catalog.pg_am am ON am.oid=ix.relam WHERE i.indrelid=:oid ORDER BY ix.relname''')

def inspect_delete_effects(connection, schema, table, *, max_relations=64):
    if not isinstance(max_relations,int) or isinstance(max_relations,bool) or max_relations<1:
        raise ValueError('positive relation budget required')
    root=connection.execute(text('SELECT pg_catalog.to_regclass(pg_catalog.format(\'%I.%I\',CAST(:schema AS text),CAST(:table AS text)))::oid::bigint'),{'schema':schema,'table':table}).scalar_one()
    if root is None:raise ValueError('target absent')
    queue=[root];nodes={};edges=[];unknown=[]
    while queue:
        oid=queue.pop(0)
        if oid in nodes:continue
        if len(nodes)>=max_relations:raise ValueError('effect inventory relation budget exceeded')
        relation=connection.execute(_RELATION,{'oid':oid}).mappings().one_or_none()
        if relation is None:raise ValueError('catalog changed during inventory')
        node=dict(relation);node["indexes"]=[dict(x) for x in connection.execute(_INDEXES,{"oid":oid}).mappings()];nodes[oid]=node
        for key in ('user_triggers','rewrite_rules','inheritance','relispartition','relrowsecurity','relforcerowsecurity'):
            if node[key]:unknown.append({'relation_oid':oid,'reason':key})
        if node['relkind']!='r':unknown.append({'relation_oid':oid,'reason':'nonordinary_relation'})
        incoming=[dict(x) for x in connection.execute(_EDGES,{'oid':oid}).mappings()]
        edges.extend(incoming)
        queue.extend(e['child_oid'] for e in incoming if e['child_oid'] not in nodes)
    return {'root_oid':root,'nodes':list(nodes.values()),'foreign_keys':edges,'unknown_effects':unknown,
            'catalog_fk_closure_complete':True,'admitted':False,
            'scope':'Read-only diagnostic graph; no stable-snapshot, locks, complete-effect, authorization, or protected DELETE qualification'}
