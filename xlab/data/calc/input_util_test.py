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
          seconds: 1234567
        }""", DataEntry),
            parse.parse_test_proto(
                """
        data_type: CLOSE_PRICE
        timestamp {
          seconds: 2234567
        }""", DataEntry))


def get_valid_inputs():
    return (parse.parse_test_proto(
        """
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 123.45
        timestamp {
          seconds: 1234567
        }""", data_entry_pb2.DataEntry),
            parse.parse_test_proto(
                """
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 111.11
        timestamp {
          seconds: 2234567
        }""", data_entry_pb2.DataEntry))


class CalcInputUtilTest(absltest.TestCase):

    def test_making_series_input_shape(self):
        got = input_util.series_source_inputs_shape(
            source_calc_type=DataType.Enum.CLOSE_PRICE,
            t=time.FromUnixSeconds(2234567),
            time_spec=calc.CalcTimeSpecs(num_periods=2,
                                         period_length=time.Seconds(1000000)))
        compare.assertProtoSequencesEqual(self, got, get_input_shapes())

    def test_making_recursive_input_shape(self):
        got = input_util.recursive_inputs_shape(
            base_calc_type=DataType.Enum.EMA_20D,
            incr_calc_type=DataType.Enum.CLOSE_PRICE,
            t=time.FromUnixSeconds(2234567),
            time_spec=calc.CalcTimeSpecs(num_periods=20,
                                         period_length=time.Seconds(1000000)))
        compare.assertProtoSequencesEqual(self, got, ("""
            data_type: EMA_20D
            timestamp {
              seconds: 1234567
            }""", """
            data_type: CLOSE_PRICE
            timestamp {
              seconds: 2234567
            }"""))

    def test_valid_inputs_do_not_raise(self):
        inputs = get_valid_inputs()
        input_util.validate_inputs(inputs, get_input_shapes())
        input_util.are_for_stock(inputs, 'SPY')

    def test_raise_for_inputs_with_fewer_items(self):
        inputs = get_valid_inputs()[:1]
        input_util.are_for_stock(inputs, 'SPY')
        with self.assertRaisesRegex(errors.InvalidArgumentError,
                                    'Expecting data with input shape'):
            input_util.validate_inputs(inputs, get_input_shapes())

    def test_raise_for_inputs_with_more_items(self):
        inputs = [*get_valid_inputs(), *get_valid_inputs()]
        input_util.are_for_stock(inputs, 'SPY')
        with self.assertRaisesRegex(errors.InvalidArgumentError,
                                    'Expecting data with input shape'):
            input_util.validate_inputs(inputs, get_input_shapes())

    def test_raise_for_inputs_with_different_item(self):
        inputs = get_valid_inputs()
        inputs[0].symbol = 'IBM'
        input_util.validate_inputs(inputs, get_input_shapes())
        with self.assertRaisesRegex(
                errors.InvalidArgumentError,
                'Expecting data for stock: SPY, got: symbol: "IBM"'):
            input_util.are_for_stock(inputs, 'SPY')


if __name__ == '__main__':
    absltest.main()
