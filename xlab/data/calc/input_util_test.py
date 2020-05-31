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


def get_input_shapes():
    return (parse.parse_test_proto(
        """
        data_type: CLOSE_PRICE
        timestamp {
          seconds: 1577923200  # 2020-01-02
        }""", DataEntry),
            parse.parse_test_proto(
                """
        data_type: CLOSE_PRICE
        timestamp {
          seconds: 1578009600  # 2020-01-03
        }""", DataEntry))


def get_valid_inputs():
    return (parse.parse_test_proto(
        """
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 123.45
        timestamp {
          seconds: 1577923200
        }""", data_entry_pb2.DataEntry),
            parse.parse_test_proto(
                """
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 111.11
        timestamp {
          seconds: 1578009600
        }""", data_entry_pb2.DataEntry))


class CalcInputUtilTest(absltest.TestCase):

    def test_making_series_input_shape(self):
        got = input_util.series_source_inputs_shape(
            source_calc_type=DataType.Enum.CLOSE_PRICE,
            t=time.FromUnixSeconds(1578009600),
            time_spec=calc.CalcTimeSpecs(num_periods=2,
                                         period_length=time.Hours(24)))
        compare.assertProtoSequencesEqual(self, got, get_input_shapes())

    def test_making_recursive_input_shape(self):
        got = input_util.recursive_inputs_shape(
            base_calc_type=DataType.Enum.EMA_20D,
            incr_calc_type=DataType.Enum.CLOSE_PRICE,
            t=time.FromUnixSeconds(1578009600),
            time_spec=calc.CalcTimeSpecs(num_periods=20,
                                         period_length=time.Hours(24)))
        compare.assertProtoSequencesEqual(self, got, ("""
            data_type: EMA_20D
            timestamp {
              seconds: 1577923200
            }""", """
            data_type: CLOSE_PRICE
            timestamp {
              seconds: 1578009600
            }"""))

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
