import datetime

from absl.testing import absltest

from xlab.base import time
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.data.calc.producers import ema
from xlab.data.store import in_memory
from xlab.net.proto import time_util
from xlab.net.proto.testing import compare
from xlab.util.status import errors


def _make_close_price(value: float, t: time.Time):
    data_entry = data_entry_pb2.DataEntry()
    data_entry.symbol = 'TEST'
    data_entry.data_space = data_entry_pb2.DataEntry.STOCK_DATA
    data_entry.data_type = data_type_pb2.DataType.CLOSE_PRICE
    data_entry.value = value
    data_entry.timestamp.CopyFrom(time_util.from_time(t))
    return data_entry


class EmaCalculationTest(absltest.TestCase):

    def setUp(self):
        self._data_store = in_memory.InMemoryDataStore()
        self._ema_producer = ema.make_ema_20d_producer(self._data_store)

    def test_ema_20_for_constant_list(self):
        date = time.FromDatetime(datetime.datetime(2000, 10, 10))
        for i in range(19, -1, -1):
            self._data_store.add(
                _make_close_price(200.0, date - i * time.Hours(24)))

        compare.assertProtoEqual(
            self, self._ema_producer.calculate('TEST', date), """
                symbol: "TEST"
                data_space: STOCK_DATA
                data_type: EMA_20D
                value: 200.0
                timestamp {
                    seconds: 971136000
                }""")

    def test_ema_20_initial_calculation(self):
        # INTC 2019-12-03 to 2019-12-31
        prices = [
            56.07, 56.02, 56.08, 56.81, 56.53, 56.59, 57.07, 57.55, 57.79, 57.70,
            57.23, 57.17, 57.96, 58.95, 59.23, 59.41, 59.82, 60.08, 59.62, 59.85,
        ]  # yapf: disable

        date = time.FromDatetime(datetime.datetime(2019, 12, 31))
        for idx, value in enumerate(prices):
            self._data_store.add(
                _make_close_price(value, date - (19 - idx) * time.Hours(24)))

        # Note: this is different than the actual EMA20 for Intel on 2019/12/31,
        # which is 58.46, because EMA accounts for *all* past data
        compare.assertProtoEqual(
            self, self._ema_producer.calculate('TEST', date), """
                symbol: "TEST"
                data_space: STOCK_DATA
                data_type: EMA_20D
                value: 58.255796513052346
                timestamp {
                    seconds: 1577750400
                }""")

    def test_ema20_recursive_calculation(self):
        date = time.FromDatetime(datetime.datetime(2020, 1, 1))
        self._data_store.add(_make_close_price(60.84, date))

        last_ema = data_entry_pb2.DataEntry()
        last_ema.symbol = 'TEST'
        last_ema.data_space = data_entry_pb2.DataEntry.STOCK_DATA
        last_ema.data_type = data_type_pb2.DataType.EMA_20D
        last_ema.value = 58.46
        last_ema.timestamp.CopyFrom(time_util.from_time(date - time.Hours(24)))
        self._data_store.add(last_ema)

        compare.assertProtoEqual(
            self, self._ema_producer.calculate('TEST', date), """
                symbol: "TEST"
                data_space: STOCK_DATA
                data_type: EMA_20D
                value: 58.68666666666667
                timestamp {
                    seconds: 1577836800
                }""")

    def test_raise_when_source_data_is_insufficient(self):
        date = time.FromDatetime(datetime.datetime(2000, 10, 10))
        for i in range(19, 0, -1):
            self._data_store.add(
                _make_close_price(200.0, date - i * time.Hours(24)))

        with self.assertRaisesRegex(errors.NotFoundError, 'Cannot find data'):
            self._ema_producer.calculate('TEST', date)


if __name__ == '__main__':
    absltest.main()
