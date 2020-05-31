import abc
import bisect
import datetime
import functools
from typing import List, Optional, Tuple

from rules_python.python.runfiles import runfiles


class TradingDayFinderInterface(abc.ABC):
    """Interface for working with US market trading days.

    The data is obtained from IEX:
      https://iexcloud.io/docs/api/#u-s-holidays-and-trading-dates
    """

    @abc.abstractmethod
    def is_trading_day(self, date: datetime.date) -> bool:
        pass

    @abc.abstractmethod
    def get_last_n(self,
                   date: datetime.date,
                   n: int,
                   include_input_date: bool = True) -> List[datetime.date]:
        pass

    @abc.abstractmethod
    def get_next_n(self,
                   date: datetime.date,
                   n: int,
                   include_input_date: bool = False) -> List[datetime.date]:
        pass


class TradingDayFinder(TradingDayFinderInterface):

    def __init__(self, trading_days: List[datetime.date]):
        self._trading_days = trading_days

    def range(self) -> Tuple[datetime.date, datetime.date]:
        return (self._trading_days[0], self._trading_days[-1])

    def is_trading_day(self, date: datetime.date) -> bool:
        start, end = self.range()
        if date < start or date > end:
            raise ValueError(
                f'Requested date {date} outside of known trading day range: ({start}, {end})'
            )

        try:
            idx = self._index(date)
            return self._trading_days[idx] == date
        except ValueError:
            return False

    def get_last_n(self,
                   date: datetime.date,
                   n: int,
                   include_input_date: bool = True) -> List[datetime.date]:
        if (n <= 0):
            raise ValueError('n must be greater than zero')
        i = self._index(date)
        i += include_input_date and self._trading_days[i] == date
        return self._trading_days[max(0, i - n):i]

    def get_next_n(self,
                   date: datetime.date,
                   n: int,
                   include_input_date: bool = False) -> List[datetime.date]:
        if (n <= 0):
            raise ValueError('n must be greater than zero')
        i = self._index(date)
        i += not include_input_date and self._trading_days[i] == date
        return self._trading_days[i:min(i + n, len(self._trading_days))]

    def _index(self, date: datetime.date) -> Optional[int]:
        return bisect.bisect_left(self._trading_days, date)


@functools.lru_cache()
def get_trading_day_finder():
    with open("xlab/trading/dates/data/us_trading_days.txt", "r") as f:
        dates = [
            datetime.date.fromisoformat(line.rstrip())
            for line in f.readlines()
        ]
        return TradingDayFinder(dates)


def is_trading_day(date: datetime.date) -> bool:
    return get_trading_day_finder().is_trading_day(date)


def get_last_n(date: datetime.date,
               n: int,
               include_input_date: bool = True) -> List[datetime.date]:
    return get_trading_day_finder().get_last_n(date, n, include_input_date)


def get_next_n(date: datetime.date,
               n: int,
               include_input_date: bool = False) -> List[datetime.date]:
    return get_trading_day_finder().get_next_n(date, n, include_input_date)
