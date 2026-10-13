"""Read-only PostgreSQL 16 routine inventory. Never invoke inspected routines.

Every executable SECURITY DEFINER routine is conservatively review-required.
Catalog ACLs cannot prove that an owner's routines are harmless or enumerate
all transitive dynamic SQL dependencies. No schema or extension is exempt.
"""
import hashlib
import json

# Parameter: authenticated runtime role name. SET/ADMIN reachability matches
# migration admission; USAGE adds immediately inherited EXECUTE privileges.
ROUTINE_INVENTORY_SQL = '''WITH RECURSIVE reachable(oid) AS (
    SELECT oid FROM pg_catalog.pg_roles WHERE rolname=%s
    UNION
    SELECT m.roleid FROM pg_catalog.pg_auth_members m JOIN reachable r
      ON (m.member=r.oid AND m.set_option)
      OR (m.admin_option AND pg_catalog.pg_has_role(r.oid,m.member,'USAGE'))
)
SELECT p.oid, n.nspname AS schema, p.proname AS name,
       p.prokind::text AS kind, owner.rolname AS owner,
       p.prosecdef AS security_definer,
       COALESCE(p.proconfig, ARRAY[]::text[]) AS settings,
       ARRAY(SELECT setting FROM pg_catalog.unnest(p.proconfig) setting
             WHERE setting LIKE 'search_path=%%') AS search_path,
       ARRAY(SELECT pg_catalog.format('%%I.%%I', tn.nspname,t.typname)
             FROM pg_catalog.unnest(p.proargtypes) WITH ORDINALITY a(oid,pos)
             JOIN pg_catalog.pg_type t ON t.oid=a.oid
             JOIN pg_catalog.pg_namespace tn ON tn.oid=t.typnamespace
             ORDER BY a.pos) AS argument_types,
       ARRAY(SELECT role.rolname FROM reachable r
             JOIN pg_catalog.pg_roles role ON role.oid=r.oid
             WHERE pg_catalog.has_function_privilege(r.oid,p.oid,'EXECUTE')
             ORDER BY role.rolname) AS executable_as,
       (SELECT COALESCE(pg_catalog.jsonb_agg(
          pg_catalog.jsonb_build_object('grantee', CASE WHEN acl.grantee=0 THEN 'PUBLIC'
              ELSE pg_catalog.pg_get_userbyid(acl.grantee) END,
            'grantor',pg_catalog.pg_get_userbyid(acl.grantor),
            'grant_option',acl.is_grantable,
            'direct',acl.grantee=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname=%s),
            'via_membership', CASE WHEN acl.grantee=0 THEN false ELSE
               acl.grantee<>(SELECT oid FROM pg_catalog.pg_roles WHERE rolname=%s)
               AND EXISTS(SELECT 1 FROM reachable r
                 WHERE pg_catalog.pg_has_role(r.oid,acl.grantee,'USAGE')) END)
            ORDER BY acl.grantee,acl.grantor),'[]'::jsonb)
        FROM pg_catalog.aclexplode(COALESCE(p.proacl,
             pg_catalog.acldefault('f',p.proowner))) acl
        WHERE acl.privilege_type='EXECUTE') AS execute_grants,
       pg_catalog.to_jsonb(p) AS catalog_definition
FROM pg_catalog.pg_proc p
JOIN pg_catalog.pg_namespace n ON n.oid=p.pronamespace
JOIN pg_catalog.pg_roles owner ON owner.oid=p.proowner
WHERE p.prokind IN ('f','p','w') ORDER BY n.nspname,p.proname,p.oid'''


def routine_inventory(connection, runtime_role, *, review_only=False):
    """Return public inventory and target-local review fingerprints, not bodies.

    Missing schema USAGE is not a safety exemption: already resolved references
    can survive schema access changes. The fingerprint pins the full pg_proc row
    (including OID, ACL, owner, language, body and settings) and resolved identity.
    Recreate/restore or catalog changes require a fresh explicit review.
    """
    query = ROUTINE_INVENTORY_SQL
    if review_only:
        query = query.replace("WHERE p.prokind IN ('f','p','w')", "WHERE p.prokind IN ('f','p','w') AND p.prosecdef")
    rows = connection.exec_driver_sql(query,
                                     (runtime_role, runtime_role, runtime_role)).mappings()
    result = []
    for source in rows:
        row = dict(source)
        definition = row.pop('catalog_definition')
        identity = {k: row[k] for k in ('schema', 'name', 'kind', 'owner', 'argument_types')}
        row['review_digest'] = hashlib.sha256(json.dumps(
            [identity, definition], sort_keys=True, ensure_ascii=False,
            separators=(',', ':')).encode()).hexdigest()
        row['review_required'] = bool(row['security_definer'] and row['executable_as'])
        result.append(row)
    return result
