"""Bounded recovery of legacy transitions that retired no native indexes.

Missing historical flags never mean false. An empty authenticated retirement
set permits preservation of current surviving native metadata; it does not
retroactively inventory an old artifact. External evidence import is separate.
"""
from . import _cluster_designation as clusters
from . import _object_comments as comments


def legacy(document):
    return clusters.source(document).get('format') in (comments.LEGACY_FORWARD, comments.FORWARD)


def recovery(document):
    if not legacy(document):
        return 'INVENTORIED'
    original = clusters.source(document)
    try:
        retired = any(comments._targets(model)[1] for model in original['lock']['models'])
    except (KeyError, TypeError, ValueError):
        comments._stop('invalid_legacy_designation_contract')
    return 'NATIVE_REPLAN_OR_EXTERNAL_METADATA_REQUIRED' if retired else 'NATIVE_UNRETIRED_RECOVERY'


def require_recoverable(document, operation_id=None):
    if recovery(document) == 'NATIVE_REPLAN_OR_EXTERNAL_METADATA_REQUIRED':
        comments._stop('legacy_designation_evidence_required', operation_id)


def capture_survivors(connection, document, operation_id=None):
    """Fresh native facts, not historical reconstruction or new authority.

Call beside the existing full phase schema checks. Extra unclustered transition
indexes remain permitted until those checks validate their exact definitions.
"""
    if not legacy(document):
        return None
    require_recoverable(document, operation_id)
    original = clusters.source(document)
    result = []
    for model in original['lock']['models']:
        expected = {item['name']: item['constraint_name'] for item in model['source_schema']['indexes']}
        observed = clusters._observe(connection, model, operation_id)
        native = {item['name']: item for item in observed}
        if any(name not in native or native[name]['constraint_name'] != constraint
               for name, constraint in expected.items()):
            comments._stop('legacy_native_index_changed', operation_id)
        if any(item['clustered'] and item['name'] not in expected for item in observed):
            comments._stop('legacy_transient_designation_requires_review', operation_id)
        result.append({'table_id': model['table_id'],
                       'indexes': [native[name] for name in sorted(expected)]})
    return result


def check_survivors(connection, document, before, operation_id=None):
    if capture_survivors(connection, document, operation_id) != before:
        comments._stop('legacy_native_designation_changed', operation_id)


def capture_abort_retained(connection, document, operation_id=None):
    """Current full native map for a reverse abort that retains every index.

The caller first validates the complete staged schema and holds transition locks.
Reverse staging adds columns only, with no indexes. Any unexpected staging index
therefore fails that existing schema check before cleanup. After cleanup, compare
all retained names, constraint links and flags before restoring source ACTIVE.
This is a live transaction observation, not missing historical metadata recovery.
"""
    if not legacy(document):
        return None
    return [{'table_id': model['table_id'],
             'indexes': clusters._observe(connection, model, operation_id)}
            for model in clusters.source(document)['lock']['models']]


def check_abort_retained(connection, document, before, operation_id=None):
    if capture_abort_retained(connection, document, operation_id) != before:
        comments._stop('legacy_native_designation_changed', operation_id)
