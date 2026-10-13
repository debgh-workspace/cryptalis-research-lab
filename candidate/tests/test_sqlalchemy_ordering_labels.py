"""Protected output labels must not enable ciphertext ORDER BY.

Native PostgreSQL qualifies each textual ordering modifier and paginated public
control. Protected ordering is unsupported and must fail before driver entry.
"""
import asyncio
from uuid import UUID

import pytest
from sqlalchemy import Text, asc, desc, event, nulls_first, nulls_last, select, type_coerce

from cryptalis.sqlalchemy import UnsupportedProtectedOperation
from test_sqlalchemy_search import _async_factory, _row, search_application


MODIFIERS = (
    "plain", "asc", "desc", "nulls_first", "nulls_last",
    "asc_nulls_first", "asc_nulls_last", "desc_nulls_first", "desc_nulls_last",
    "coerced_asc", "coerced_desc_nulls_last", "coerced_outer_nulls_first",
)
VALUES = (None, "z", "a", "é", "", "雪", "a")
RANKS = (None, 3, 1, -1, 0, 2, 1)


def _ordered(value, modifier):
    if modifier == "coerced_asc":
        return type_coerce(asc(value), Text())
    if modifier == "coerced_desc_nulls_last":
        return type_coerce(nulls_last(desc(value)), Text())
    if modifier == "coerced_outer_nulls_first":
        return nulls_first(type_coerce(desc(value), Text()))
    if modifier == "plain":
        return value
    if modifier == "asc":
        return asc(value)
    if modifier == "desc":
        return desc(value)
    if modifier == "nulls_first":
        return nulls_first(value)
    if modifier == "nulls_last":
        return nulls_last(value)
    if modifier.startswith("asc_"):
        value = asc(value)
    else:
        value = desc(value)
    return nulls_first(value) if modifier.endswith("first") else nulls_last(value)


def _rows(app):
    rows = [_row(app, value, rank) for value, rank in zip(VALUES, RANKS)]
    for index, row in enumerate(rows):
        row.id = UUID(int=index + 1)
    return rows


def _protected_queries(app, modifier, named):
    c = app.Customer
    value = c.name.label("chosen_value") if named else c.name
    label = "chosen_value" if named else "name"
    base = select(c.id, value).where(c.tenant_id == app.tenant)
    candidate = base.order_by(_ordered(label, modifier), c.id).offset(1).limit(4)
    native = base.order_by(_ordered(c.name, modifier), c.id).offset(1).limit(4)
    return candidate, native


@pytest.mark.parametrize("protected", [False, True], ids=["native", "protected"])
@pytest.mark.parametrize("mode", ["sync", "async"])
@pytest.mark.parametrize("named", [False, True], ids=["column-label", "renamed-label"])
@pytest.mark.parametrize("modifier", MODIFIERS)
def test_protected_textual_ordering_modifiers_refuse_before_driver(protected, mode, named, modifier):
    with search_application(protected, attach_now=mode == "sync") as app:
        if mode == "sync":
            with app.sessions(tenant_id=app.tenant) as session:
                session.add_all(_rows(app))
                session.commit()
                candidate, native = _protected_queries(app, modifier, named)
                if not protected:
                    actual = [tuple(row) for row in session.execute(candidate)]
                    expected = [tuple(row) for row in session.execute(native)]
                    assert actual == expected and len(actual) == 4
                    return
                calls = []
                listener = lambda *args:calls.append(True)
                event.listen(app.engine, "before_cursor_execute", listener)
                try:
                    with pytest.raises(UnsupportedProtectedOperation):
                        session.execute(candidate)
                    assert calls == [], "Protected ORDER BY reached the driver"
                finally:
                    event.remove(app.engine, "before_cursor_execute", listener)
        else:
            async def scenario():
                engine, sessions = await _async_factory(app)
                try:
                    async with sessions(tenant_id=app.tenant) as session:
                        session.add_all(_rows(app))
                        await session.commit()
                        candidate, native = _protected_queries(app, modifier, named)
                        if not protected:
                            actual = [tuple(row) for row in await session.execute(candidate)]
                            expected = [tuple(row) for row in await session.execute(native)]
                            assert actual == expected and len(actual) == 4
                            return
                        calls = []
                        listener = lambda *args:calls.append(True)
                        event.listen(engine.sync_engine, "before_cursor_execute", listener)
                        try:
                            with pytest.raises(UnsupportedProtectedOperation):
                                await session.execute(candidate)
                            assert calls == [], "Protected ORDER BY reached the driver"
                        finally:
                            event.remove(engine.sync_engine, "before_cursor_execute", listener)
                finally:
                    await engine.dispose()
            asyncio.run(scenario())


@pytest.mark.parametrize("mode", ["sync", "async"])
@pytest.mark.parametrize("modifier", MODIFIERS)
def test_public_textual_ordering_modifiers_keep_native_values_and_page(mode, modifier):
    outcomes = []
    for protected in (False, True):
        with search_application(protected, attach_now=mode == "sync") as app:
            def queries():
                c = app.Customer
                base = select(c.id, c.rank.label("chosen_rank"), c.name).where(c.tenant_id == app.tenant)
                return (base.order_by(_ordered("chosen_rank", modifier), c.id).offset(1).limit(4),
                        base.order_by(_ordered(c.rank, modifier), c.id).offset(1).limit(4))
            if mode == "sync":
                with app.sessions(tenant_id=app.tenant) as session:
                    session.add_all(_rows(app))
                    session.commit()
                    labeled, direct = queries()
                    actual = [tuple(row) for row in session.execute(labeled)]
                    expected = [tuple(row) for row in session.execute(direct)]
                    assert actual == expected and len(actual) == 4
                    outcomes.append(actual)
            else:
                async def scenario():
                    engine, sessions = await _async_factory(app)
                    try:
                        async with sessions(tenant_id=app.tenant) as session:
                            session.add_all(_rows(app))
                            await session.commit()
                            labeled, direct = queries()
                            actual = [tuple(row) for row in await session.execute(labeled)]
                            expected = [tuple(row) for row in await session.execute(direct)]
                            assert actual == expected and len(actual) == 4
                            return actual
                    finally:
                        await engine.dispose()
                outcomes.append(asyncio.run(scenario()))
    assert outcomes[0] == outcomes[1]
