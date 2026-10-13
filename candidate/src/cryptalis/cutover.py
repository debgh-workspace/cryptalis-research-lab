"""Read-only inventory of a protected-to-plaintext runtime role handoff.

No role, grant, session or deployment mutation is performed by this module.
Privileged operators remain outside the runtime threat boundary.
"""
from cryptalis import migration as m
from cryptalis.manifest.routines import routine_inventory
from psycopg import sql
import re

WRITE_PRIVILEGES = 'INSERT,UPDATE,DELETE,TRUNCATE,REFERENCES,TRIGGER'


def inventory(c,models,*,old_role,new_role,owner):
    """Return exact readiness findings; a planning observation is not authority."""
    findings=[]
    def issue(code,**context):findings.append({'code':code,**context})
    if type(new_role) is not str or not new_role or new_role==old_role:
        issue('distinct_plaintext_runtime_role_required')
    roles=c.exec_driver_sql('''WITH RECURSIVE reachable(oid) AS (
      SELECT oid FROM pg_catalog.pg_roles WHERE rolname=%s
      UNION SELECT membership.roleid FROM pg_catalog.pg_auth_members membership
      JOIN reachable ON (membership.member=reachable.oid AND membership.set_option)
        OR (membership.admin_option AND pg_catalog.pg_has_role(reachable.oid,membership.member,'USAGE')))
      SELECT role.oid,role.rolname,
        role.rolsuper OR role.rolcreaterole OR role.rolcreatedb OR role.rolbypassrls OR role.rolreplication
      FROM pg_catalog.pg_roles role JOIN reachable ON reachable.oid=role.oid''',(old_role,)).all()
    if not roles:issue('old_runtime_role_missing')
    for oid,name,administrative in roles:
        if administrative:issue('old_runtime_administrative_path',role=name)
        for model in models:
            target=m._table(c,model)
            row=c.exec_driver_sql('''SELECT t.oid,pg_catalog.pg_get_userbyid(t.relowner),
                pg_catalog.pg_has_role(%s,t.relowner,'USAGE'),
                pg_catalog.has_table_privilege(%s,t.oid,%s),
                pg_catalog.has_any_column_privilege(%s,t.oid,'INSERT,UPDATE,REFERENCES')
                FROM pg_catalog.pg_class t WHERE t.oid=pg_catalog.to_regclass(%s)''',
                (oid,oid,WRITE_PRIVILEGES,oid,target)).one_or_none()
            if row is None:issue('cutover_table_missing',table=target);continue
            if row[1]!=owner:issue('cutover_table_owner_changed',table=target)
            if row[2]:issue('old_runtime_table_ownership',role=name,table=target)
            if row[3] or row[4]:issue('old_runtime_write_path',role=name,table=target)
            if c.exec_driver_sql('''SELECT pg_catalog.pg_has_role(%s,nspowner,'USAGE')
                OR pg_catalog.has_schema_privilege(%s,oid,'CREATE')
                FROM pg_catalog.pg_namespace WHERE nspname=%s''',(oid,oid,model['schema'])).scalar_one():
                issue('old_runtime_schema_authority',role=name,schema=model['schema'])
            # Only the trusted table-creating owner's defaults for this scope.
            defaults=c.exec_driver_sql('''SELECT DISTINCT grantor.rolname,
                    CASE WHEN d.defaclnamespace=0 THEN '*' ELSE ns.nspname END,
                    CASE WHEN a.grantee=0 THEN 'PUBLIC' ELSE pg_catalog.pg_get_userbyid(a.grantee) END
                FROM pg_catalog.pg_default_acl d
                JOIN pg_catalog.pg_roles grantor ON grantor.oid=d.defaclrole
                LEFT JOIN pg_catalog.pg_namespace ns ON ns.oid=d.defaclnamespace
                CROSS JOIN LATERAL pg_catalog.aclexplode(d.defaclacl) a
                WHERE d.defaclobjtype='r' AND grantor.rolname=%s
                  AND (d.defaclnamespace=0 OR ns.nspname=%s)
                  AND a.privilege_type IN ('INSERT','UPDATE','DELETE','TRUNCATE','REFERENCES','TRIGGER')
                  AND (a.grantee=0 OR pg_catalog.pg_has_role(%s,a.grantee,'USAGE'))''',
                (owner,model['schema'],oid)).all()
            for grantor,scope,grantee in defaults:issue('old_runtime_default_write_path',role=name,grantor=grantor,scope=scope,grantee=grantee)
    if roles:
        for routine in routine_inventory(c,old_role,review_only=True):
            if routine['review_required']:
                issue('old_runtime_callable_definer',review_digest=routine['review_digest'],
                      schema=routine['schema'],name=routine['name'],owner=routine['owner'],
                      argument_types=routine['argument_types'],execute_grants=routine['execute_grants'])
    # Ordinary principals that can assume/inherit the old role are included.
    # Superuser and the exact trusted maintenance principal are host-controlled.
    sessions=c.exec_driver_sql('''SELECT a.pid,a.usename FROM pg_catalog.pg_stat_activity a
        JOIN pg_catalog.pg_roles login ON login.oid=a.usesysid
        JOIN pg_catalog.pg_roles retired ON retired.rolname=%s
        WHERE a.datid=(SELECT oid FROM pg_catalog.pg_database WHERE datname=current_database())
          AND a.pid<>pg_backend_pid() AND NOT login.rolsuper AND login.rolname<>%s
          AND pg_catalog.pg_has_role(login.oid,retired.oid,'MEMBER')''',(old_role,owner)).all()
    for pid,user in sessions:issue('old_runtime_session_open',pid=pid,role=user)
    exists=c.exec_driver_sql('SELECT EXISTS(SELECT 1 FROM pg_catalog.pg_roles WHERE rolname=%s)',(new_role,)).scalar_one()
    if not exists:issue('plaintext_runtime_role_missing')
    elif new_role!=old_role:
        try:m._runtime_permissions(c,new_role,owner,models)
        except m.TransitionFailure as exc:issue('plaintext_runtime_not_admitted',reason=exc.code)
        for model in models:
            for privilege in ('SELECT','INSERT','UPDATE','DELETE'):
                if not c.exec_driver_sql('SELECT pg_catalog.has_table_privilege(%s,pg_catalog.to_regclass(%s),%s)',
                                         (new_role,m._table(c,model),privilege)).scalar_one():
                    issue('plaintext_runtime_missing_privilege',table=m._table(c,model),privilege=privilege)
    # Deduplicate equivalent findings from multiple fields/tables in one schema.
    unique=[]
    for finding in findings:
        if finding not in unique:unique.append(finding)
    memberships=c.exec_driver_sql('''SELECT parent.rolname FROM pg_catalog.pg_auth_members m
        JOIN pg_catalog.pg_roles parent ON parent.oid=m.roleid
        JOIN pg_catalog.pg_roles child ON child.oid=m.member
        WHERE child.rolname=%s ORDER BY parent.rolname''',(old_role,)).scalars().all()
    return {'direct_memberships':memberships,'ready':not unique,'findings':unique,'old_role':old_role,'plaintext_role':new_role,
            'limits':'Read-only snapshot, not a catalog-change fence. Privileged concurrent grants/owner writers require host exclusion. Default checks cover the declared table owner.'}


def require_ready(c,models,*,old_role,new_role,owner,operation_id=None):
    report=inventory(c,models,old_role=old_role,new_role=new_role,owner=owner)
    if not report['ready']:
        raise m.TransitionFailure('runtime_cutover_not_ready',operation_id)
    return report


def procedure(source,new_role,*,create_role=True,inventory_report=None):
    """Print-only, review-required starting procedure; rerun inventory afterward.

    Transitive grants/definer routines reported by inventory require their own
    explicit revocations; this template never implies universal repair.
    """
    # Reuse the existing identifier/length validation and fresh-role template.
    fresh=source.runtime_role_template(new_role)
    d=source.document;old=d['runtime_role']
    if new_role==old:raise m.TransitionFailure('distinct_plaintext_runtime_role_required')
    q=lambda value:sql.Identifier(value).as_string()
    lines=['-- REVIEW: two runtime roles and deployment credential handoff are required.',
           '-- Stop old workers/reconnectors before running this procedure.',
           '-- Run as an authorized administrator. Cryptalis does not execute this SQL.',
           '-- Rerun inventory; inherited/SET/ADMIN/routine findings need explicit remediation.']
    if create_role:lines.append(fresh)
    else:
        lines.append('BEGIN;')
        for schema in sorted({x['schema'] for x in d['lock']['models']}):
            lines.append(f'GRANT USAGE ON SCHEMA {q(schema)} TO {q(new_role)};')
        for model in d['lock']['models']:
            table=q(model['schema'])+'.'+q(model['table'])
            lines.append(f'GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE {table} TO {q(new_role)};')
        lines.append('COMMIT;')
    lines.append('BEGIN;')
    if inventory_report is not None:
        lines.extend(_remediation(inventory_report,old,new_role))
    for model in d['lock']['models']:
        table=q(model['schema'])+'.'+q(model['table'])
        for recipient in (q(old),'PUBLIC'):
            lines.append(f'REVOKE {WRITE_PRIVILEGES} ON TABLE {table} FROM {recipient};')
            for col in model['source_schema']['columns']:
                names=q(col['name'])
                lines.append(f'REVOKE INSERT ({names}), UPDATE ({names}), REFERENCES ({names}) ON TABLE {table} FROM {recipient};')
    lines.append('COMMIT;')
    old_literal=sql.Literal(old).as_string();owner_literal=sql.Literal(d['target'][-1]).as_string()
    lines += ['-- Termination is separate from REVOKE: grants do not close sessions.',
        'SELECT pg_catalog.pg_terminate_backend(a.pid) FROM pg_catalog.pg_stat_activity a '
        'JOIN pg_catalog.pg_roles login ON login.oid=a.usesysid '
        f'JOIN pg_catalog.pg_roles retired ON retired.rolname={old_literal} '
        'WHERE a.datid=(SELECT oid FROM pg_catalog.pg_database WHERE datname=current_database()) '
        f'AND a.pid<>pg_backend_pid() AND NOT login.rolsuper AND login.rolname<>{owner_literal} '
        "AND pg_catalog.pg_has_role(login.oid,retired.oid,'MEMBER');",
        '-- Inspect every termination result. Rerun the read-only readiness check.',
        '-- Deploy the exact plaintext artifact using only the distinct plaintext role.']
    return '\n'.join(lines)


def _remediation(report,old_role,new_role):
    """Render bounded reviewed observations; never execute permission changes."""
    if report.get('old_role')!=old_role or report.get('plaintext_role')!=new_role:
        raise m.TransitionFailure('cutover_inventory_identity_mismatch')
    q=lambda value:sql.Identifier(value).as_string()
    commands=['-- REVIEW IMPACT: membership/PUBLIC revocations can affect other workloads.',
              '-- This inventory is a snapshot. Stop reconnectors and rerun readiness afterward.']
    for parent in report.get('direct_memberships',[]):
        commands.append(f'REVOKE {q(parent)} FROM {q(old_role)} RESTRICT;')
    identifier=r'(?:[a-z_][a-z_0-9$]*|"(?:[^"]|"")+")'
    for finding in report.get('findings',[]):
        code=finding['code']
        if code=='old_runtime_default_write_path':
            scope='' if finding['scope']=='*' else ' IN SCHEMA '+q(finding['scope'])
            grantee='PUBLIC' if finding['grantee']=='PUBLIC' else q(finding['grantee'])
            commands.append(f"ALTER DEFAULT PRIVILEGES FOR ROLE {q(finding['grantor'])}{scope} REVOKE {WRITE_PRIVILEGES} ON TABLES FROM {grantee};")
        elif code=='old_runtime_callable_definer':
            types=finding['argument_types']
            if not all(type(t) is str and re.fullmatch(identifier+r'\.'+identifier,t) for t in types):
                raise m.TransitionFailure('invalid_routine_identity_in_cutover_inventory')
            identity=q(finding['schema'])+'.'+q(finding['name'])+'('+', '.join(types)+')'
            recipients={g['grantee'] for g in finding['execute_grants'] if g['grantee']=='PUBLIC' or g['direct']}
            for recipient in sorted(recipients):
                commands.append(f"REVOKE EXECUTE ON ROUTINE {identity} FROM {'PUBLIC' if recipient=='PUBLIC' else q(recipient)} RESTRICT;")
            if finding['owner']==old_role:
                commands.append('-- BLOCKER: retired runtime owns a callable definer; explicitly review ownership transfer before continuing.')
        elif code in ('cutover_table_owner_changed','old_runtime_table_ownership','old_runtime_schema_authority','old_runtime_administrative_path'):
            commands.append('-- BLOCKER: '+code+' requires explicit owner/administrator remediation; this template does not choose a new owner.')
    return list(dict.fromkeys(commands))
