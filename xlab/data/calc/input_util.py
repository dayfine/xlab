import functools
import itertools
from typing import List, Optional, Tuple

from xlab.base import time
from xlab.data import calc
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.net.proto import time_util
from xlab.trading.dates import trading_days
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


def _make_input_shape_key(data_entry: DataEntry) -> Tuple[int, time.Time]:
    return (data_entry.data_type, time_util.to_time(data_entry.timestamp))


# Sort a list of data entries with no assumed ordering into the given inputs
# shape. Raises if such sorting cannot produce the expected inputs shape.
def sort_to_inputs_shape(data_entries: List[DataEntry],
                         inputs_shape: calc.CalcInputs) -> calc.CalcInputs:
    data_entry_dict = {_make_input_shape_key(d): d for d in data_entries}
    try:
        return [
            data_entry_dict[_make_input_shape_key(input_shape)]
            for input_shape in inputs_shape
        ]
    except KeyError as e:
        nl = '\n'
        raise errors.InvalidArgumentError(
            f'Cannot sort inputs to the given shape: {e}{nl}'
            f'Inputs are: {nl.join(str(d) for d in data_entries)}')


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
    # TODO: right now this is still no properly generalized. For time span
    # longer than a day, they should all work. However for day and shorter span,
    # they need to be checked against trading days and trading hours.
    # NOTE: both FromCivil and ToCivil assumes UTC, which later might
    # be updated to take into account the exchange timezone of a
    # security.
    timestamps = [
        time.FromCivil(day) for day in trading_days.get_last_n(
            time.ToCivil(t), time_spec.num_periods)
    ]
    return [
        DataEntry(
            data_type=source_calc_type,
            timestamp=time_util.from_time(timestmap),
        ) for timestmap in timestamps
    ]


def recursive_inputs_shape(
        base_calc_type: DataType.Enum, incr_calc_type: DataType.Enum,
        t: time.Time, time_spec: calc.CalcTimeSpecs) -> calc.RecursiveInputs:
    # TODO: same here, think about how to get it work with period other than
    # days. e.g week-based moving averages.
    the_day_before = trading_days.get_last_n(time.ToCivil(t),
                                             1,
                                             include_input_date=False)[0]
    return (DataEntry(
        data_type=base_calc_type,
        timestamp=time_util.from_time(time.FromCivil(the_day_before)),
    ), DataEntry(
        data_type=incr_calc_type,
        timestamp=time_util.from_time(t),
    ))
