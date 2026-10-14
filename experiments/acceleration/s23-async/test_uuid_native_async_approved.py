"""Thirty previously missing UUID cells; real native and protected async paths."""
import asyncio
import json
import os
from pathlib import Path
import sys
from uuid import UUID

sys.path.insert(0, str(Path(__file__).resolve().parent / 'source' / 'tests'))

import pytest
import sqlalchemy
from sqlalchemy import event, select
from test_sqlalchemy_search import search_application, _row, _async_factory

FORMS = ('canonical', 'upper', 'hex', 'braces', 'four_groups')
OPERATIONS = ('get', 'equality', 'in')
IDENTITY = UUID('abcdef01-2345-6789-abcd-ef0123456789')


@pytest.mark.parametrize('form', FORMS)
@pytest.mark.parametrize('operation', OPERATIONS)
def test_approved_uuid_text_matches_native_async_without_changing_bind(form, operation):
    value = {
        'canonical': str(IDENTITY), 'upper': str(IDENTITY).upper(),
        'hex': IDENTITY.hex, 'braces': '{' + str(IDENTITY) + '}',
        'four_groups': '-'.join(IDENTITY.hex[i:i + 4] for i in range(0, 32, 4)),
    }[form]
    record = dict(id=f'uuid-text/{operation}/{form}', mode='async',
                  sqlalchemy=sqlalchemy.__version__, profile='standard',
                  classification='DEFECT', paths=[])
    # Require a run-local receipt destination before any database fixture opens.
    destination = Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent / 'uuid-async-approved-outcomes.jsonl'
    try:
        for protected in (False, True):
            path = dict(path='protected' if protected else 'native', completed=False,
                        native_bind_preserved=False)
            record['paths'].append(path)
            with search_application(protected, attach_now=False) as app:
                async def scenario():
                    engine, sessions = await _async_factory(app)
                    calls = []

                    def capture(conn, cursor, statement, parameters, context, many):
                        if 'SELECT' in statement.upper() and '.customer' in statement:
                            calls.append(parameters)

                    try:
                        async with sessions(tenant_id=app.tenant) as session:
                            row = _row(app, 'protected-value', 1)
                            row.id = IDENTITY
                            session.add(row)
                            await session.commit()
                        # A fresh session forces an actual SELECT instead of an
                        # identity-map hit, including AsyncSession.get.
                        event.listen(engine.sync_engine, 'before_cursor_execute', capture)
                        try:
                            async with sessions(tenant_id=app.tenant) as session:
                                if operation == 'get':
                                    result = await session.get(app.Customer, value)
                                else:
                                    expression = (app.Customer.id == value if operation == 'equality'
                                                  else app.Customer.id.in_([value]))
                                    result = (await session.scalars(select(app.Customer).where(expression))).one()
                                assert result is not None
                                assert type(result.id) is UUID and type(result.name) is str
                                assert (result.id, result.name) == (IDENTITY, 'protected-value')
                                assert calls
                                bound = [item for parameters in calls for item in
                                         (parameters.values() if isinstance(parameters, dict) else parameters)]
                                assert value in bound
                                path['native_bind_preserved'] = True
                                path['result'] = [str(result.id), result.name]
                        finally:
                            event.remove(engine.sync_engine, 'before_cursor_execute', capture)
                    finally:
                        await engine.dispose()
                asyncio.run(scenario())
            path['completed'] = True
        assert record['paths'][0]['result'] == record['paths'][1]['result']
        record['classification'] = 'IDENTICAL'
    finally:
        # No exception text, SQL, parameters, URLs or environment contents.
        # A refusal or native failure remains a failing test and DEFECT record.
        with destination.open('a') as stream:
            stream.write(json.dumps(record, sort_keys=True) + '\n')
