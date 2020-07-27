from absl.testing import absltest
from google.protobuf import text_format
from hamcrest import assert_that, contains
from proto_matcher import equals_proto

from xlab.base import time
from xlab.data import calc
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.data.calc import input_util
from xlab.util.status import errors

_DataEntry = data_entry_pb2.DataEntry
_DataType = data_type_pb2.DataType


def get_input_shapes():
    return (
        text_format.Parse(
            f"""
            data_type: CLOSE_PRICE
            timestamp {{
                seconds: {time.as_seconds(2020, 1, 2)}
            }}""", _DataEntry()),
        text_format.Parse(
            f"""
            data_type: CLOSE_PRICE
            timestamp {{
                seconds: {time.as_seconds(2020, 1, 3)}
            }}""", _DataEntry()),
    )


def get_valid_inputs():
    return (
        text_format.Parse(
            f"""
            data_space: STOCK_DATA
            symbol: "SPY"
            data_type: CLOSE_PRICE
            value: 123.45
            timestamp {{
                seconds: {time.as_seconds(2020, 1, 2)}
            }}""", _DataEntry()),
        text_format.Parse(
            f"""
            data_space: STOCK_DATA
            symbol: "SPY"
            data_type: CLOSE_PRICE
            value: 111.11
            timestamp {{
                seconds: {time.as_seconds(2020, 1, 3)}
            }}""", _DataEntry()),
    )


class CalcInputUtilTest(absltest.TestCase):

    def test_making_series_input_shape(self):
        got = input_util.series_source_inputs_shape(
            source_calc_type=_DataType.Enum.CLOSE_PRICE,
            t=time.FromUnixSeconds(1578009600),
            time_spec=calc.CalcTimeSpecs(num_periods=2,
                                         period_length=time.Hours(24)))
        expected = get_input_shapes()
        assert_that(
            got, contains(equals_proto(expected[0]), equals_proto(expected[1])))

    def test_making_series_input_shape_account_for_trading_days(self):
        got = input_util.series_source_inputs_shape(
            source_calc_type=_DataType.Enum.CLOSE_PRICE,
            t=time.FromCivil(time.CivilTime(2017, 12, 26)),
            time_spec=calc.CalcTimeSpecs(num_periods=2,
                                         period_length=time.Hours(24)))
        assert_that(
            got,
            contains(
                equals_proto(f"""
                    data_type: CLOSE_PRICE
                    timestamp {{
                        seconds: {time.as_seconds(2017, 12, 22)}
                    }}"""),
                equals_proto(f"""
                    data_type: CLOSE_PRICE
                    timestamp {{
                        seconds: {time.as_seconds(2017, 12, 26)}
                    }}""")))

    def test_making_recursive_input_shape(self):
        got = input_util.recursive_inputs_shape(
            base_calc_type=_DataType.Enum.EMA_20D,
            incr_calc_type=_DataType.Enum.CLOSE_PRICE,
            t=time.FromUnixSeconds(1578009600),
            time_spec=calc.CalcTimeSpecs(num_periods=20,
                                         period_length=time.Hours(24)))
        assert_that(
            got,
            contains(
                equals_proto(f"""
                    data_type: EMA_20D
                    timestamp {{
                        seconds: {time.as_seconds(2020, 1, 2)}
                    }}"""),
                equals_proto(f"""
                    data_type: CLOSE_PRICE
                    timestamp {{
                        seconds: {time.as_seconds(2020, 1, 3)}
                    }}""")))

    def test_making_recursive_input_shape_account_for_trading_days(self):
        got = input_util.recursive_inputs_shape(
            base_calc_type=_DataType.Enum.EMA_20D,
            incr_calc_type=_DataType.Enum.CLOSE_PRICE,
            t=time.FromCivil(time.CivilTime(2017, 12, 26)),
            time_spec=calc.CalcTimeSpecs(num_periods=20,
                                         period_length=time.Hours(24)))
        assert_that(
            got,
            contains(
                equals_proto(f"""
                    data_type: EMA_20D
                    timestamp {{
                        seconds: {time.as_seconds(2017, 12, 22)}
                    }}"""),
                equals_proto(f"""
                    data_type: CLOSE_PRICE
                    timestamp {{
                        seconds: {time.as_seconds(2017, 12, 26)}
                    }}""")))

    def test_sort_to_inputs_shape(self):
        inputs = reversed(get_valid_inputs())
        got = input_util.sort_to_inputs_shape(inputs, get_input_shapes())
        expected = get_valid_inputs()
        assert_that(
            got, contains(equals_proto(expected[0]), equals_proto(expected[1])))

    def test_not_enough_data_to_sort_to_inputs_shape(self):
        inputs = get_valid_inputs()[:1]
        with self.assertRaisesRegex(errors.InvalidArgumentError,
                                    'Cannot sort inputs to the given shape'):
            input_util.sort_to_inputs_shape(inputs, get_input_shapes())

    def test_more_data_than_needed_to_sort_to_inputs_shape(self):
        inputs = [*reversed(get_valid_inputs()), *get_valid_inputs()]
        got = input_util.sort_to_inputs_shape(inputs, get_input_shapes())
        expected = get_valid_inputs()
        assert_that(
            got, contains(equals_proto(expected[0]), equals_proto(expected[1])))

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
