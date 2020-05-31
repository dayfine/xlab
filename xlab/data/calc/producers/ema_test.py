import datetime

from absl.testing import absltest

from xlab.base import time
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.data.calc.producers import ema
from xlab.net.proto import time_util
from xlab.net.proto.testing import compare
from xlab.util.status import errors

DataEntry = data_entry_pb2.DataEntry


def _make_close_price(value: float, t: time.Time) -> DataEntry:
    return DataEntry(
        symbol='TEST',
        data_space=DataEntry.STOCK_DATA,
        data_type=data_type_pb2.DataType.CLOSE_PRICE,
        value=value,
        timestamp=time_util.from_time(t),
    )


class EmaCalculationTest(absltest.TestCase):

    def test_ema_20_for_constant_list(self):
        date = time.FromDate(datetime.date(2000, 10, 10))
        close_prices = [
            _make_close_price(200.0, date - i * time.Hours(24))
            for i in range(19, -1, -1)
        ]

        compare.assertProtoEqual(
            self,
            ema.make_ema_20d_producer().calculate(close_prices), """
                symbol: "TEST"
                data_space: STOCK_DATA
                data_type: EMA_20D
                value: 200.0
                timestamp {
                    seconds: 971136000
                }""")

    def test_ema_20_initial_calculation(self):
        # INTC 2019-12-03 to 2019-12-31
        price_data = [
            56.07, 56.02, 56.08, 56.81, 56.53, 56.59, 57.07, 57.55, 57.79, 57.70,
            57.23, 57.17, 57.96, 58.95, 59.23, 59.41, 59.82, 60.08, 59.62, 59.85,
        ]  # yapf: disable

        date = time.FromDate(datetime.date(2019, 12, 31))
        close_prices = [
            _make_close_price(value, date - (19 - idx) * time.Hours(24))
            for idx, value in enumerate(price_data)
        ]

        # Note: this is different than the actual EMA20 for Intel on 2019/12/31,
        # which is 58.46, because EMA accounts for *all* past data
        compare.assertProtoEqual(
            self,
            ema.make_ema_20d_producer().calculate(close_prices), """
                symbol: "TEST"
                data_space: STOCK_DATA
                data_type: EMA_20D
                value: 58.255796513052346
                timestamp {
                    seconds: 1577750400
                }""")

    def test_ema20_recursive_calculation(self):
        date = time.FromDate(datetime.date(2020, 1, 1))
        close_now = _make_close_price(60.84, date)

        ema_last = DataEntry(
            symbol='TEST',
            data_space=DataEntry.STOCK_DATA,
            data_type=data_type_pb2.DataType.EMA_20D,
            value=58.46,
            timestamp=time_util.from_time(date - time.Hours(24)),
        )

        compare.assertProtoEqual(
            self,
            ema.make_ema_20d_producer().calculate((ema_last, close_now)), """
                symbol: "TEST"
                data_space: STOCK_DATA
                data_type: EMA_20D
                value: 58.68666666666667
                timestamp {
                    seconds: 1577836800
                }""")

    def test_raise_when_inputs_do_not_meet_accpeted_input_shapes(self):
        date = time.FromDate(datetime.date(2000, 10, 10))
        close_prices = [
            _make_close_price(200.0, date - i * time.Hours(24))
            for i in range(19, 0, -1)
        ]

        with self.assertRaisesRegex(
                errors.InvalidArgumentError,
                'Expecting data with input shape: data_type: CLOSE_PRICE'):
            ema.make_ema_20d_producer().calculate(close_prices)


if __name__ == '__main__':
    absltest.main()
