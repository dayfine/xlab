from absl.testing import absltest

from xlab.base import time
from xlab.data import calc
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.data.calc import input_util
from xlab.net.proto.testing import compare
from xlab.net.proto.testing import parse
from xlab.util.status import errors

DataEntry = data_entry_pb2.DataEntry
DataType = data_type_pb2.DataType

SECS_2020_01_02 = 1577923200
SECS_2020_01_03 = 1578009600
SECS_2017_12_22 = 1513900800
SECS_2017_12_26 = 1514246400


def get_input_shapes():
    return (parse.parse_test_proto(
        f"""
        data_type: CLOSE_PRICE
        timestamp {{
          seconds: {SECS_2020_01_02}
        }}""", DataEntry),
            parse.parse_test_proto(
                f"""
        data_type: CLOSE_PRICE
        timestamp {{
          seconds: {SECS_2020_01_03}
        }}""", DataEntry))


def get_valid_inputs():
    return (parse.parse_test_proto(
        f"""
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 123.45
        timestamp {{
          seconds: {SECS_2020_01_02}
        }}""", data_entry_pb2.DataEntry),
            parse.parse_test_proto(
                f"""
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 111.11
        timestamp {{
          seconds: {SECS_2020_01_03}
        }}""", data_entry_pb2.DataEntry))


class CalcInputUtilTest(absltest.TestCase):

    def test_making_series_input_shape(self):
        got = input_util.series_source_inputs_shape(
            source_calc_type=DataType.Enum.CLOSE_PRICE,
            t=time.FromUnixSeconds(1578009600),
            time_spec=calc.CalcTimeSpecs(num_periods=2,
                                         period_length=time.Hours(24)))
        compare.assertProtoSequencesEqual(self, got, get_input_shapes())

    def test_making_series_input_shape_account_for_trading_days(self):
        got = input_util.series_source_inputs_shape(
            source_calc_type=DataType.Enum.CLOSE_PRICE,
            t=time.FromCivil(time.CivilTime(2017, 12, 26)),
            time_spec=calc.CalcTimeSpecs(num_periods=2,
                                         period_length=time.Hours(24)))
        compare.assertProtoSequencesEqual(self, got, (f"""
            data_type: CLOSE_PRICE
            timestamp {{
                seconds: {SECS_2017_12_22}
            }}""", f"""
            data_type: CLOSE_PRICE
            timestamp {{
                seconds: {SECS_2017_12_26}
            }}"""))

    def test_making_recursive_input_shape(self):
        got = input_util.recursive_inputs_shape(
            base_calc_type=DataType.Enum.EMA_20D,
            incr_calc_type=DataType.Enum.CLOSE_PRICE,
            t=time.FromUnixSeconds(1578009600),
            time_spec=calc.CalcTimeSpecs(num_periods=20,
                                         period_length=time.Hours(24)))
        compare.assertProtoSequencesEqual(self, got, (f"""
            data_type: EMA_20D
            timestamp {{
                seconds: {SECS_2020_01_02}
            }}""", f"""
            data_type: CLOSE_PRICE
            timestamp {{
                seconds: {SECS_2020_01_03}
            }}"""))

    def test_making_recursive_input_shape_account_for_trading_days(self):
        got = input_util.recursive_inputs_shape(
            base_calc_type=DataType.Enum.EMA_20D,
            incr_calc_type=DataType.Enum.CLOSE_PRICE,
            t=time.FromCivil(time.CivilTime(2017, 12, 26)),
            time_spec=calc.CalcTimeSpecs(num_periods=20,
                                         period_length=time.Hours(24)))
        compare.assertProtoSequencesEqual(self, got, (f"""
            data_type: EMA_20D
            timestamp {{
                seconds: {SECS_2017_12_22}
            }}""", f"""
            data_type: CLOSE_PRICE
            timestamp {{
                seconds: {SECS_2017_12_26}
            }}"""))

    def test_sort_to_inputs_shape(self):
        inputs = reversed(get_valid_inputs())
        got = input_util.sort_to_inputs_shape(inputs, get_input_shapes())
        compare.assertProtoSequencesEqual(self, got, get_valid_inputs())

    def test_not_enough_data_to_sort_to_inputs_shape(self):
        inputs = get_valid_inputs()[:1]
        with self.assertRaisesRegex(errors.InvalidArgumentError,
                                    'Cannot sort inputs to the given shape'):
            input_util.sort_to_inputs_shape(inputs, get_input_shapes())

    def test_more_data_than_needed_to_sort_to_inputs_shape(self):
        inputs = [*reversed(get_valid_inputs()), *get_valid_inputs()]
        got = input_util.sort_to_inputs_shape(inputs, get_input_shapes())
        compare.assertProtoSequencesEqual(self, got, get_valid_inputs())

    def test_valid_inputs_do_not_raise(self):
        inputs = get_valid_inputs()
        input_util.validate_inputs(inputs, get_input_shapes())
        self.assertEqual(input_util.are_for_stock(inputs), 'SPY')

    def test_raise_for_inputs_with_fewer_items(self):
        inputs = get_valid_inputs()[:1]
        self.assertEqual(input_util.are_for_stock(inputs), 'SPY')
        with self.assertRaisesRegex(errors.InvalidArgumentError,
                                    'Expecting data with input shape'):
            input_util.validate_inputs(inputs, get_input_shapes())

    def test_raise_for_inputs_with_more_items(self):
        inputs = [*get_valid_inputs(), *get_valid_inputs()]
        self.assertEqual(input_util.are_for_stock(inputs), 'SPY')
        with self.assertRaisesRegex(errors.InvalidArgumentError,
                                    'Expecting data with input shape'):
            input_util.validate_inputs(inputs, get_input_shapes())

    def test_raise_for_inputs_with_different_item(self):
        inputs = get_valid_inputs()
        inputs[0].symbol = 'IBM'
        input_util.validate_inputs(inputs, get_input_shapes())
        with self.assertRaisesRegex(errors.InvalidArgumentError,
                                    'Expecting data series all for stock:'):
            input_util.are_for_stock(inputs)


if __name__ == '__main__':
    absltest.main()
