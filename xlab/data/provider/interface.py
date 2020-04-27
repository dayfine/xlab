import abc
import datetime
from typing import Dict, List

from xlab.data.proto import data_entry_pb2


class DataProvider(abc.ABC):

    # Data gets multiple types of data for the given symbol over a requested
    # period of time, and returns those data in a Dict, where the key is the
    # type of data, and the value is the data in a time-series in ascending
    # order.
    @abc.abstractmethod
    def get_data(
            self, symbol: str, start_date: datetime.date,
            end_date: datetime.date
    ) -> Dict[str, List[data_entry_pb2.DataEntry]]:
        pass
