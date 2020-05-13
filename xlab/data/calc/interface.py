import abc
from typing import List, Callable

from xlab.base import time
from xlab.data.proto import data_entry_pb2, data_type_pb2


class CalcProducer(abc.ABC):

    # What type of calc does this class produce.
    @property
    @abc.abstractmethod
    def calc_type(self) -> data_type_pb2.DataType.Enum:
        pass

    # Compute the calc for a given security at a given timestamp.
    @abc.abstractmethod
    def calculate(self, symbol: str, t: time.Time,
                  **kwargs) -> data_entry_pb2.DataEntry:
        pass


CalcProducerFactory = Callable[..., CalcProducer]
