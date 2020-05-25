from typing import Tuple

import pandas as pd

from xlab.base import time
from xlab.data import calc
from xlab.data.calc import input_util
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.net.proto import time_util
from xlab.util.status import errors

DataEntry = data_entry_pb2.DataEntry
DataType = data_type_pb2.DataType

SMOOTHING_FACTOR = 2


# CalcProducer for Exponential Moving Average:
#   https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
#   https://www.investopedia.com/terms/e/ema.asp
class EmaProducer:

    def __init__(self, calc_type: DataType.Enum,
                 time_specs: calc.CalcTimeSpecs):
        self.calc_type = calc_type
        self.time_specs = time_specs
        self._source_calc = DataType.Enum.CLOSE_PRICE

    def calculate(self, inputs: calc.CalcInputs) -> DataEntry:
        if not inputs:
            raise errors.InvalidArgumentError('Inputs cannot be empty')

        symbol = input_util.are_for_stock(inputs)
        t = time_util.to_time(inputs[-1].timestamp)
        try:
            input_util.validate_inputs(inputs, self.recursive_inputs_shape(t))
            ema = self._recur(inputs)
        except errors.InvalidArgumentError:
            input_util.validate_inputs(inputs, self.source_inputs_shape(t))
            ema = self._initial(inputs)
        except errors.InvalidArgumentError as e:
            raise e

        return DataEntry(
            symbol=symbol,
            data_space=data_entry_pb2.DataEntry.STOCK_DATA,
            data_type=self.calc_type,
            value=ema,
            timestamp=time_util.from_time(t),
        )

    # EMA is computed based on previous EMA. However, it must starts somewhere,
    # where the first EMA need to calculated from X days of close prices.
    def _initial(self, inputs: calc.CalcInputs) -> float:
        prices = (data.value for data in inputs)
        return pd.DataFrame(prices).ewm(span=self.time_specs.num_periods,
                                        adjust=False).mean().iloc[-1][0]

    def _recur(self, inputs: calc.CalcInputs) -> float:
        num_periods = self.time_specs.num_periods
        return (SMOOTHING_FACTOR / (num_periods + 1) * inputs[1].value \
          + (num_periods + 1 - SMOOTHING_FACTOR) / (num_periods + 1) * inputs[0].value)

    def recursive_inputs_shape(self, t: time.Time) -> calc.RecursiveInputs:
        return input_util.recursive_inputs_shape(self.calc_type,
                                                 self._source_calc, t,
                                                 self.time_specs)

    def source_inputs_shape(self, t: time.Time) -> calc.SourceInputs:
        return input_util.series_source_inputs_shape(self._source_calc, t,
                                                     self.time_specs)


make_ema_20d_producer: calc.CalcProducerFactory = lambda: EmaProducer(
    DataType.EMA_20D, calc.CalcTimeSpecs(20, time.Hours(24)))

make_ema_50d_producer: calc.CalcProducerFactory = lambda: EmaProducer(
    DataType.EMA_50D, calc.CalcTimeSpecs(50, time.Hours(24)))

make_ema_150d_producer: calc.CalcProducerFactory = lambda: EmaProducer(
    DataType.EMA_150D, calc.CalcTimeSpecs(150, time.Hours(24)))
