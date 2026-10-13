"""Extreme host rate inputs must fail safely through the public planners."""
import pytest
from cryptalis.migration import TransitionFailure
from test_migration import application, run, publish, keys
from test_deprotection import api, plaintext_role
from test_transition_rate_estimates import protect_plan

@pytest.mark.parametrize('direction', ['protect','reverse'])
@pytest.mark.parametrize('rate', [10**400, -(10**400), 5e-324, 7e-308, 1e-15], ids=['oversized_integer','negative_oversized_integer','subnormal_float','sum_overflow','counter_overflow'])
def test_unrepresentable_rate_estimate_is_typed_and_read_only(direction, rate):
    with application() as app:
        if direction == 'reverse': run(app); publish(app)
        with app.owner.connect() as connection:
            before = connection.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id').all()
            columns = connection.exec_driver_sql('SELECT column_name FROM information_schema.columns WHERE table_schema=%s ORDER BY ordinal_position',(app.schema,)).all()
        kwargs = dict(backfill_rows_per_second=rate,verify_rows_per_second=rate,
                      temporary_bytes_per_row=700,wal_bytes_per_row=2000)
        with pytest.raises(TransitionFailure) as failure:
            if direction == 'protect': protect_plan(app,kwargs)
            else: api().plan(app.plan,app.owner,source_pin=app.pin,keys=keys,
                             plaintext_runtime_role=plaintext_role(),**kwargs)
        assert failure.value.code == ('missing_measured_rates' if type(rate) is int else 'unrepresentable_cost_estimates')
        assert failure.value.__suppress_context__ or type(rate) is int or rate == 1e-15
        with app.owner.connect() as connection:
            assert connection.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id').all() == before
            assert connection.exec_driver_sql('SELECT column_name FROM information_schema.columns WHERE table_schema=%s ORDER BY ordinal_position',(app.schema,)).all() == columns


def test_estimate_counter_boundary_and_empty_table():
    from cryptalis.migration import _time_estimates
    # Exact integer oracle; no enormous database fixture or timing claim.
    rows = (2**53 - 2) // 2
    assert _time_estimates(rows, (1,1)) == (rows,rows,2*rows)
    with pytest.raises(TransitionFailure, match='unrepresentable_cost_estimates'):
        _time_estimates(2**52, (1,1))
    assert _time_estimates(0, (5e-324,5e-324)) == (0,0,0)

@pytest.mark.parametrize('rows,rate', [(0,5e-324),(7,float.fromhex('0x1.fffffffffffffp+1023')),(7,2**53-1)])
def test_representable_extreme_rates_remain_accepted(rows,rate):
    with application(rows=rows) as app:
        kwargs = dict(backfill_rows_per_second=rate,verify_rows_per_second=rate,
                      temporary_bytes_per_row=700,wal_bytes_per_row=2000)
        plan = protect_plan(app,kwargs)
        assert type(plan)(plan.artifact).artifact == plan.artifact
        assert plan.document['estimates']['writer_pause_seconds_estimate'] == (0 if rows == 0 else 1)
        assert plan.document['estimates']['backfill_rows_per_second'] == rate
