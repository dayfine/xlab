import datetime
import random
from typing import List

from absl.testing import absltest
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to

from xlab.base import time
from xlab.data.pipeline import produce_calc_fn
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.net.proto import time_util
from xlab.net.proto.testing import parse

DataEntry = data_entry_pb2.DataEntry
DataType = data_type_pb2.DataType
produce_initial_calc_fn = produce_calc_fn.produce_initial_calc_fn
produce_recursive_calc_fn = produce_calc_fn.produce_recursive_calc_fn


def _make_close_price(symbol: str, value: float, t: time.Time) -> DataEntry:
    return DataEntry(
        symbol=symbol,
        data_space=DataEntry.STOCK_DATA,
        data_type=data_type_pb2.DataType.CLOSE_PRICE,
        value=value,
        timestamp=time_util.from_time(t),
    )


def get_close_prices_for_ema20(t: time.Time, symbol: str) -> List[DataEntry]:
    # INTC 2019-12-03 to 2019-12-31
    price_data = [
        56.07, 56.02, 56.08, 56.81, 56.53, 56.59, 57.07, 57.55, 57.79, 57.70,
        57.23, 57.17, 57.96, 58.95, 59.23, 59.41, 59.82, 60.08, 59.62, 59.85,
    ]  # yapf: disable

    close_prices = [
        _make_close_price(symbol, value, t - (19 - idx) * time.Hours(24))
        for idx, value in enumerate(price_data)
    ]
    random.shuffle(close_prices)
    return close_prices


def get_recursive_inputs_for_ema20(t: time.Time,
                                   symbol: str) -> List[DataEntry]:
    return [
        DataEntry(
            symbol=symbol,
            data_space=DataEntry.STOCK_DATA,
            data_type=DataType.EMA_20D,
            value=58.31,
            timestamp=time_util.from_time(t - time.Hours(24)),
        ),
        _make_close_price(symbol, 59.85, t)
    ]


def expected_ema20d_test() -> DataEntry:
    return parse.parse_test_proto(
        """
        symbol: "TEST"
        data_space: STOCK_DATA
        data_type: EMA_20D
        value: 58.255796513052346
        timestamp {
            seconds: 1577750400
        }""", DataEntry)


def expected_recursive_ema20d_test() -> DataEntry:
    return parse.parse_test_proto(
        """
        symbol: "TEST"
        data_space: STOCK_DATA
        data_type: EMA_20D
        value: 58.45666666666667
        timestamp {
            seconds: 1577750400
        }""", DataEntry)


class ProduceCalcFnTest(absltest.TestCase):

    def test_produce_initial_calc_fn_with_no_input(self):
        t = time.FromUnixSeconds(12345)
        inputs = []
        with TestPipeline() as p:
            out = (p \
                | beam.Create(inputs) \
                | produce_initial_calc_fn(DataType.EMA_20D, t))

            assert_that(out, equal_to([]))

    def test_produce_initial_calc_fn(self):
        t = time.FromDatetime(datetime.datetime(2019, 12, 31))
        inputs = get_close_prices_for_ema20(t, 'TEST')
        with TestPipeline() as p:
            out = (p \
                | beam.Create(inputs) \
                | produce_initial_calc_fn(DataType.EMA_20D, t))

            assert_that(out, equal_to([expected_ema20d_test()]))

    def test_produce_initial_calc_fn_ignores_irrelevant_data(self):
        t = time.FromDatetime(datetime.datetime(2019, 12, 31))
        inputs = get_close_prices_for_ema20(t, 'TEST')
        inputs.append(_make_close_price('X', 123.45, t))
        with TestPipeline() as p:
            out = (p \
                | beam.Create(inputs) \
                | produce_initial_calc_fn(DataType.EMA_20D, t))

            assert_that(out, equal_to([expected_ema20d_test()]))

    def test_produce_initial_calc_fn_not_enough_data(self):
        t = time.FromDatetime(datetime.datetime(2019, 12, 31))
        inputs = get_close_prices_for_ema20(t, 'TEST')[:19]
        with TestPipeline() as p:
            out = (p \
                | beam.Create(inputs) \
                | produce_initial_calc_fn(DataType.EMA_20D, t))

            assert_that(out, equal_to([]))

    def test_produce_initial_calc_fn_multiple_symbols(self):
        t = time.FromDatetime(datetime.datetime(2019, 12, 31))
        inputs = [
            *get_close_prices_for_ema20(t, 'TEST'),
            *get_close_prices_for_ema20(t, 'IBM')
        ]
        with TestPipeline() as p:
            out = (p \
                | beam.Create(inputs) \
                | produce_initial_calc_fn(DataType.EMA_20D, t))

            assert_that(
                out,
                equal_to([
                    expected_ema20d_test(),
                    parse.parse_test_proto(
                        """
                        symbol: "IBM"
                        data_space: STOCK_DATA
                        data_type: EMA_20D
                        value: 58.255796513052346
                        timestamp {
                            seconds: 1577750400
                        }""", DataEntry)
                ]))

    def test_produce_recursive_calc_fn(self):
        t = time.FromDatetime(datetime.datetime(2019, 12, 31))
        inputs = get_recursive_inputs_for_ema20(t, 'TEST')
        with TestPipeline() as p:
            out = (p \
                | beam.Create(inputs) \
                | produce_recursive_calc_fn(DataType.EMA_20D, t))

            assert_that(out, equal_to([expected_recursive_ema20d_test()]))

    def test_produce_recursive_calc_fn_with_swapped_inputs(self):
        t = time.FromDatetime(datetime.datetime(2019, 12, 31))
        inputs = reversed(get_recursive_inputs_for_ema20(t, 'TEST'))
        with TestPipeline() as p:
            out = (p \
                | beam.Create(inputs) \
                | produce_recursive_calc_fn(DataType.EMA_20D, t))

            assert_that(out, equal_to([expected_recursive_ema20d_test()]))

    def test_produce_recursive_calc_fn_with_extra_data(self):
        t = time.FromDatetime(datetime.datetime(2019, 12, 31))
        inputs = [
            *get_recursive_inputs_for_ema20(t, 'TEST'),
            *get_close_prices_for_ema20(t, 'IBM')
        ]
        with TestPipeline() as p:
            out = (p \
                | beam.Create(inputs) \
                | produce_recursive_calc_fn(DataType.EMA_20D, t))

            assert_that(out, equal_to([expected_recursive_ema20d_test()]))


if __name__ == '__main__':
    absltest.main()
