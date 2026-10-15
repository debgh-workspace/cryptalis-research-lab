"""Versioned remembered-index metadata, never physical heap order.

Compiler lock/v1 and historical transition formats do not inventory this fact.
Only the new transition profile binds this separate native catalog inventory.
"""
from psycopg import sql

from . import _object_comments as comments

INVENTORY = 'cryptalis.cluster-designation/research-v1'


def source(document):
    return document['source_plan'] if document.get('kind') == 'deprotect' else document


def enabled(document):
    return source(document).get('format') == comments.CLUSTER_FORWARD


def status(document):
    return 'INVENTORIED' if enabled(document) else 'NOT_INVENTORIED'


def validate(document):
    inventory = document['cluster_designation']
    require = comments._require
    require(type(inventory) is dict and set(inventory) == {'schema', 'tables'})
    require(inventory['schema'] == INVENTORY and type(inventory['tables']) is list)
    models = document['lock']['models']
    require(len(inventory['tables']) == len(models))
    for model, table in zip(models, inventory['tables'], strict=True):
        require(type(table) is dict and set(table) == {'table_id', 'indexes'})
        require(table['table_id'] == model['table_id'])
        expected = sorted(model['source_schema']['indexes'], key=lambda item: item['name'])
        require(len({item['name'] for item in expected}) == len(expected))
        require(type(table['indexes']) is list and len(table['indexes']) == len(expected))
        for item, native in zip(table['indexes'], expected, strict=True):
            require(type(item) is dict and set(item) == {'name', 'constraint_name', 'clustered'})
            require(type(item['name']) is str and item['name'] == native['name'])
            require(item['constraint_name'] == native['constraint_name'])
            require(item['constraint_name'] is None or type(item['constraint_name']) is str)
            require(type(item['clustered']) is bool)
        require(sum(item['clustered'] for item in table['indexes']) <= 1)


def _observe(connection, model, operation_id):
    table = connection.exec_driver_sql('''SELECT t.oid FROM pg_catalog.pg_class t
        JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace
        WHERE n.nspname=%s AND t.relname=%s AND t.relkind='r' ''',
        (model['schema'], model['table'])).scalar_one_or_none()
    if table is None:
        comments._stop('cluster_designation_target_changed', operation_id)
    rows = connection.exec_driver_sql('''SELECT ix.relname, i.indisclustered,
        co.conname, co.conrelid, i.indisvalid, i.indisready, i.indislive
        FROM pg_catalog.pg_index i JOIN pg_catalog.pg_class ix ON ix.oid=i.indexrelid
        LEFT JOIN pg_catalog.pg_constraint co ON co.conindid=i.indexrelid
            AND co.contype IN ('p','u','x')
        WHERE i.indrelid=%s ORDER BY ix.relname''', (table,)).all()
    if (len({row[0] for row in rows}) != len(rows)
            or any(row[2] is not None and row[3] != table for row in rows)
            or any(row[1] and not all(row[4:7]) for row in rows)
            or sum(row[1] for row in rows) > 1):
        comments._stop('cluster_designation_target_changed', operation_id)
    # Artifact ordering is independent of the database's identifier collation.
    return sorted(({'name': row[0], 'constraint_name': row[2], 'clustered': row[1]}
                   for row in rows), key=lambda item: item['name'])


def capture(connection, lock, operation_id=None):
    inventory = {'schema': INVENTORY, 'tables': []}
    for model in lock['models']:
        observed = _observe(connection, model, operation_id)
        expected = {item['name']: item['constraint_name'] for item in model['source_schema']['indexes']}
        if {item['name']: item['constraint_name'] for item in observed} != expected:
            comments._stop('cluster_designation_target_changed', operation_id)
        inventory['tables'].append({'table_id': model['table_id'], 'indexes': observed})
    return inventory


def check(connection, document, operation_id=None, *, protected=False):
    if not enabled(document):
        return
    original = source(document)
    for model, table in zip(original['lock']['models'], original['cluster_designation']['tables'], strict=True):
        observed = _observe(connection, model, operation_id)
        affected = comments._targets(model)[1]
        expected = {item['name'] for item in table['indexes']
                    if item['clustered'] and not (protected and item['name'] in affected)}
        actual = {item['name'] for item in observed if item['clustered']}
        if actual != expected:
            comments._stop('cluster_designation_changed', operation_id)
        by_name = {item['name']: item for item in observed}
        for item in table['indexes']:
            current = by_name.get(item['name'])
            if protected and item['name'] in affected:
                if current is not None:
                    comments._stop('cluster_designation_target_changed', operation_id)
                continue
            if current is None or current['constraint_name'] != item['constraint_name']:
                comments._stop('cluster_designation_target_changed', operation_id)
        # Full phase-specific definitions are checked by the existing schema
        # inspector. OIDs are deliberately not a durable recovery contract.


def restore(connection, document, operation_id=None):
    if not enabled(document):
        return
    original = source(document)
    # Newly recreated indexes must have the same native names/linkages.
    # Refuse unexpected current designation rather than overwriting drift.
    # At this point all affected indexes exist again but remain undesignated.
    # Check expected flags before changing metadata on any recreated object.
    for model, table in zip(original['lock']['models'], original['cluster_designation']['tables'], strict=True):
        current = _observe(connection, model, operation_id)
        affected = comments._targets(model)[1]
        expected = {item['name'] for item in table['indexes'] if item['clustered'] and item['name'] not in affected}
        if {item['name'] for item in current if item['clustered']} != expected:
            comments._stop('cluster_designation_changed', operation_id)
    capture(connection, original['lock'], operation_id)
    for model, wanted in zip(original['lock']['models'],
            original['cluster_designation']['tables'], strict=True):
        affected = comments._targets(model)[1]
        for item in wanted['indexes']:
            if item['clustered'] and item['name'] in affected:
                statement = sql.SQL('ALTER TABLE {} CLUSTER ON {}').format(
                    sql.Identifier(model['schema'], model['table']), sql.Identifier(item['name']))
                connection.exec_driver_sql(statement.as_string(connection.connection.driver_connection))
    check(connection, original, operation_id)
