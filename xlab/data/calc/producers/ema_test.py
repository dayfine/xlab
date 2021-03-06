from absl.testing import absltest

from hamcrest import assert_that
from proto_matcher import equals_proto, ignoring_repeated_field_ordering

from xlab.base import time
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.data.calc.producers import ema
from xlab.net.proto import time_util
from xlab.trading.dates import trading_days
from xlab.util.status import errors

_DataEntry = data_entry_pb2.DataEntry


def _make_close_price(value: float, t: time.Time) -> _DataEntry:
    return _DataEntry(
        symbol='TEST',
        data_space=_DataEntry.STOCK_DATA,
        data_type=data_type_pb2.DataType.CLOSE_PRICE,
        value=value,
        timestamp=time_util.from_time(t),
    )


class EmaCalculationTest(absltest.TestCase):

    def test_ema_20_for_constant_list(self):
        date = time.CivilTime(2017, 10, 10)
        close_prices = [
            _make_close_price(200.0, time.FromCivil(d))
            for d in trading_days.get_last_n(date, 20)
        ]

        assert_that(
            ema.make_ema_20d_producer().calculate(close_prices),
            equals_proto(f"""
                symbol: "TEST"
                data_space: STOCK_DATA
                data_type: EMA_20D
                value: 200.0
                timestamp {{
                    seconds: {time.as_seconds(2017, 10, 10)}
                }}"""))

    def test_ema_20_initial_calculation(self):
        # INTC 2019-12-03 to 2019-12-31
        price_data = [
            56.07, 56.02, 56.08, 56.81, 56.53, 56.59, 57.07, 57.55, 57.79, 57.70,
            57.23, 57.17, 57.96, 58.95, 59.23, 59.41, 59.82, 60.08, 59.62, 59.85,
        ]  # yapf: disable

        date = time.CivilTime(2019, 12, 31)
        close_prices = [
            _make_close_price(value, time.FromCivil(d))
            for value, d in zip(price_data, trading_days.get_last_n(date, 20))
        ]

        # Note: this is different than the actual EMA20 for Intel on 2019/12/31,
        # which is 58.46, because EMA accounts for *all* past data
        assert_that(
            ema.make_ema_20d_producer().calculate(close_prices),
            equals_proto(f"""
                symbol: "TEST"
                data_space: STOCK_DATA
                data_type: EMA_20D
                value: 58.255796513052346
                timestamp {{
                    seconds: {time.as_seconds(2019, 12, 31)}
                }}"""))

    def test_ema20_recursive_calculation(self):
        date = time.FromCivil(time.CivilTime(2020, 1, 1))
        close_now = _make_close_price(60.84, date)

        ema_last = _DataEntry(
            symbol='TEST',
            data_space=_DataEntry.STOCK_DATA,
            data_type=data_type_pb2.DataType.EMA_20D,
            value=58.46,
            timestamp=time_util.from_time(date - time.Hours(24)),
        )

        assert_that(
            ema.make_ema_20d_producer().calculate((ema_last, close_now)),
            equals_proto(f"""
                symbol: "TEST"
                data_space: STOCK_DATA
                data_type: EMA_20D
                value: 58.68666666666667
                timestamp {{
                    seconds: {time.as_seconds(2020, 1, 1)}
                }}"""))

    def test_raise_when_inputs_do_not_meet_accpeted_input_shapes(self):
        date = time.CivilTime(2017, 10, 10)
        close_prices = [
            _make_close_price(200.0, time.FromCivil(d))
            for d in trading_days.get_last_n(date, 19)
        ]

        with self.assertRaisesRegex(
                errors.InvalidArgumentError,
                'Expecting data with input shape: data_type: CLOSE_PRICE'):
            ema.make_ema_20d_producer().calculate(close_prices)


if __name__ == '__main__':
    absltest.main()
