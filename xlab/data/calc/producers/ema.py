import pandas as pd

from xlab.base import time
from xlab.data import calc
from xlab.data.proto.data_entry_pb2 import DataEntry
from xlab.data.proto.data_type_pb2 import DataType
from xlab.net.proto import time_util
from xlab.util.status import errors


# CalcProducer for Exponential Moving Average:
#   https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
#   https://www.investopedia.com/terms/e/ema.asp
class EmaProducer:

    def __init__(self, calc_type: DataType.Enum,
                 time_specs: calc.CalcTimeSpecs):
        self.calc_type = calc_type
        self.time_specs = time_specs

    def calculate(self, inputs: Sequence[DataEntry]) -> DataEntry:
        try:
            ema = self._recur(self._to_recursive_inputs(inputs))
        except errors.FailedPreconditionError:
            self.validate_initial_inputs(inputs)
            ema = self._initial(inputs)
        except errors.InvalidArgumentError as e:
            raise e

        result = data_entry_pb2.DataEntry()
        result.symbol = symbol
        result.data_space = data_entry_pb2.DataEntry.STOCK_DATA
        result.data_type = self.calc_type
        result.value = ema
        result.timestamp.CopyFrom(time_util.from_time(t))
        return result

    # EMA is computed based on previous EMA. However, it must starts somewhere,
    # where the first EMA need to calculated from X days of close prices.
    def _initial(self, inputs: Sequence[DataEntry]) -> float:
        prices = (data.value for data in inputs)
        return pd.DataFrame(prices).ewm(span=self._periods,
                                        adjust=False).mean().iloc[-1][0]

    def _recur(self, ema_last: DataEntry, close_now: DataEntry) -> float:
        return (2 / (self._periods + 1) * close_now.value \
          + (self._periods - 1) / (self._periods + 1) * ema_last.value)

    def _to_recursive_inputs(
            self, inputs: Sequence[DataEntry]) -> Tuple[DataEntry, DataEntry]:
        if (len(inputs) != 2 \
              or inputs[0].data_type != self.calc_type \
              or inputs[1].data_type != DataType.Enum.CLOSE_PRICE):
            raise errors.FailedPreconditionError(
                'Inputs cannot be used to recursively compute {}'.format(
                    DataType.Enum.Name(self.calc_type)))
        return (inputs[0], inputs[1])

    def accepted_input_shapes(self, symbol: str,
                              t: time.Time) -> Tuple[Sequence[DataEntry]]:
        return ()

    def _recursive_input_shape(self, symbol: str, t: time.Time):
        result = data_entry_pb2.DataEntry()
        result.symbol = symbol
        result.data_space = DataEntry.STOCK_DATA
        result.data_type = self.calc_type
        result.timestamp.CopyFrom(time_util.from_time(t))


make_ema_20d_producer: calc.CalcProducerFactory = lambda: EmaProducer(
    DataType.EMA_20D, calc.CalcTimeSpecs(20, time.Hours(24)))

make_ema_50d_producer: calc.CalcProducerFactory = lambda: EmaProducer(
    DataType.EMA_50D, calc.CalcTimeSpecs(50, time.Hours(24)))

make_ema_150d_producer: calc.CalcProducerFactory = lambda: EmaProducer(
    DataType.EMA_150D, calc.CalcTimeSpecs(150, time.Hours(24)))
