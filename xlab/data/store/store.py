from abc import ABC, abstractmethod
from typing import Callable, List

from xlab.data.proto import data_entry_pb2


class DataStore(ABC):
    # Add a single data entry to the store. No exception is thrown if the
    # operation is successful.
    @abstractmethod
    def add(self, data_entry: data_entry_pb2.DataEntry):
        pass

    # Read a single data entry by a key. If the data entry is not found, throw
    # an exception (instead of returns None).
    # The schema of the key is determined by the particular implementation.
    @abstractmethod
    def read(self, key: str) -> data_entry_pb2.DataEntry:
        pass

    # Go through all data entries, and apply |fn| to each of them.
    @abstractmethod
    def each(self, fn: Callable[[data_entry_pb2.DataEntry], None]):
        pass
