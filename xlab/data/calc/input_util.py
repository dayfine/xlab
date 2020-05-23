import functools
import itertools
from typing import Optional

from xlab.base import time
from xlab.data import calc
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.net.proto import time_util
from xlab.util.status import errors

DataEntry = data_entry_pb2.DataEntry
DataType = data_type_pb2.DataType


def is_same_input_shape(input: Optional[DataEntry],
                        input_shape: Optional[DataEntry]) -> bool:
    if not input or not input_shape:
        return False
    return all([
        input.data_type == input_shape.data_type,
        time_util.to_time(input.timestamp) == time_util.to_time(
            input_shape.timestamp),
    ])


def are_for_stock(inputs: calc.CalcInputs) -> str:
    if not inputs:
        raise errors.InvalidArgumentError('Cannot get stock for empty input')
    symbol = inputs[0].symbol
    for input in inputs:
        if input.data_space != DataEntry.STOCK_DATA or input.symbol != symbol:
            raise errors.InvalidArgumentError(
                f'Expecting data series all for stock: {symbol}, got: {input}')
    return symbol


def validate_inputs(inputs: calc.CalcInputs, inputs_shapes: calc.CalcInputs):
    for input, input_shape in itertools.zip_longest(inputs, inputs_shapes):
        if not is_same_input_shape(input, input_shape):
            raise errors.InvalidArgumentError(
                f'Expecting data with input shape: {input_shape}, got: {input}')


def series_source_inputs_shape(
        source_calc_type: DataType.Enum, t: time.Time,
        time_spec: calc.CalcTimeSpecs) -> calc.SourceInputs:
    return [
        DataEntry(
            data_type=source_calc_type,
            timestamp=time_util.from_time(t - i * time_spec.period_length),
        ) for i in range(time_spec.num_periods - 1, -1, -1)
    ]


def recursive_inputs_shape(
        base_calc_type: DataType.Enum, incr_calc_type: DataType.Enum,
        t: time.Time, time_spec: calc.CalcTimeSpecs) -> calc.RecursiveInputs:
    return (DataEntry(
        data_type=base_calc_type,
        timestamp=time_util.from_time(t - time_spec.period_length),
    ), DataEntry(
        data_type=incr_calc_type,
        timestamp=time_util.from_time(t),
    ))
