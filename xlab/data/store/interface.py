import abc
import dataclasses
import datetime
from typing import Callable, List, Optional

from xlab.data.proto import data_entry_pb2, data_type_pb2
from xlab.data.store import units


# Fields for retrieving data entries.
@dataclasses.dataclass(frozen=True)
class LookupKey:
    data_space: int = 0  # Prot Enum data_entry_pb2.DataEntry.DataSpace
    symbol: Optional[str] = None
    data_type: int = 0 # Proto Enum data_type_pb2.DataType.Enum
    timestamp: Optional[units.Seconds] = None


class DataStore(abc.ABC):
    # Add a single data entry to the store. No exception is thrown if the
    # operation is successful.
    @abc.abstractmethod
    def add(self, data_entry: data_entry_pb2.DataEntry):
        pass

    # Read a single data entry by a key. If the data entry is not found, throw
    # an exception (instead of returns None).
    # All fields of the LookupKey must be specified.
    @abc.abstractmethod
    def read(self, lookup_key: LookupKey) -> data_entry_pb2.DataEntry:
        pass

    # Read zero or more data entries matching the lookup key.
    @abc.abstractmethod
    def lookup(self, lookup_key: LookupKey) -> data_entry_pb2.DataEntries:
        pass

    # Go through all data entries, and apply |fn| to each of them.
    @abc.abstractmethod
    def each(self, fn: Callable[[data_entry_pb2.DataEntry], None]):
        pass
