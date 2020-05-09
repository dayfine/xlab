import abc
import dataclasses
import datetime
from typing import Callable, List, Optional

from xlab.data.proto import data_entry_pb2
from xlab.data.store import units


# Fields for retrieving data entries.
@dataclasses.dataclass
class LookupKey:
    # An xlab.DataEntry.DataSpace Enum. Incompatible with Optional type.
    data_space: Optional[int] = None
    symbol: Optional[str] = None
    data_type: Optional[str] = None
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
