from typing import List

import pandas as pd

from xlab.base import time
from xlab.data import calc, store
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.net.proto import time_util
from xlab.util.status import errors


# CalcProducer for Exponential Moving Average:
#   https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
#   https://www.investopedia.com/terms/e/ema.asp
class _EmaProducer:

    def __init__(self, calc_type: data_type_pb2.DataType.Enum, periods: int,
                 period_length: time.Duration, data_store: store.DataStore):
        self.calc_type = calc_type
        self._periods = periods
        self._period_length = period_length
        self._store = data_store

    def calculate(self, symbol: str, t: time.Time) -> data_entry_pb2.DataEntry:
        try:
            ema = self._recur(symbol, t)
        except errors.FailedPreconditionError:
            ema = self._initial(symbol, t)

        result = data_entry_pb2.DataEntry()
        result.symbol = symbol
        result.data_space = data_entry_pb2.DataEntry.STOCK_DATA
        result.data_type = self.calc_type
        result.value = ema
        result.timestamp.CopyFrom(time_util.from_time(t))
        return result

    # EMA is computed based on previous EMA. However, it must starts somewhere,
    # where the first EMA need to calculated from X days of close prices.
    def _initial(self, symbol: str, t: time.Time) -> float:
        prices = []
        for i in range(self._periods - 1, -1, -1):
            data = self._get_stock_data(
                symbol,
                # This is not entirely correct, as there is likely no data for
                # nontrading dates.
                t - i * self._period_length,
                data_type_pb2.DataType.CLOSE_PRICE,
            )
            prices.append(data.value)

        return pd.DataFrame(prices).ewm(span=self._periods,
                                        adjust=False).mean().iloc[-1][0]

    def _recur(self, symbol: str, t: time.Time) -> float:
        try:
            ema_last = self._get_stock_data(symbol, t - self._period_length,
                                            self.calc_type)
        except errors.NotFoundError as e:
            raise errors.FailedPreconditionError(
                'Required data for recursively computing {} does not exist: {}'.
                format(data_type_pb2.DataType.Enum.Name(self.calc_type), e))
        close_now = self._get_stock_data(symbol, t,
                                         data_type_pb2.DataType.CLOSE_PRICE)


        return (2 / (self._periods + 1) * close_now.value \
          + (self._periods - 1) / (self._periods + 1) * ema_last.value)

    def _get_stock_data(
            self, symbol: str, t: time.Time,
            data_type: data_type_pb2.DataType.Enum) -> data_entry_pb2.DataEntry:
        lookup_key = store.DataStore.LookupKey(
            data_space=data_entry_pb2.DataEntry.DataSpace.STOCK_DATA,
            symbol=symbol,
            data_type=data_type,
            timestamp=t)
        return self._store.read(lookup_key)


_FACTORIES = {
    data_type_pb2.DataType.EMA_20D:
        lambda data_store: _EmaProducer(data_type_pb2.DataType.EMA_20D, 20,
                                        time.Hours(24), data_store),
    data_type_pb2.DataType.EMA_50D:
        lambda data_store: _EmaProducer(data_type_pb2.DataType.EMA_50D, 50,
                                        time.Hours(24), data_store),
    data_type_pb2.DataType.EMA_150D:
        lambda data_store: _EmaProducer(data_type_pb2.DataType.EMA_150D, 150,
                                        time.Hours(24), data_store),
}


def get_producer_factory(
        calc_type: data_type_pb2.DataType.Enum) -> calc.CalcProducerFactory:
    try:
        return _FACTORIES[calc_type]
    except KeyError:
        raise errors.NotFoundError('No available EMA factory for {}'.format(
            data_type_pb2.DataType.Enum.Name(calc_type)))


def available_calc_types() -> List[int]:  #data_type_pb2.DataType.Enum
    return _FACTORIES.keys()
