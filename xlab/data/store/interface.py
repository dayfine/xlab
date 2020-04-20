from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List, Optional

from xlab.data.proto.data_entry_pb2 import DataEntry


# Fields for retrieving data entries.
@dataclass
class LookupKey:
    # An xlab.DataEntry.DataSpace Enum. Incompatible with Optional type.
    data_space: Optional[int] = None
    symbol: Optional[str] = None
    data_type: Optional[str] = None
    timestamp: Optional[datetime] = None


class DataStore(ABC):
    # Add a single data entry to the store. No exception is thrown if the
    # operation is successful.
    @abstractmethod
    def add(self, data_entry: DataEntry):
        pass

    # Read a single data entry by a key. If the data entry is not found, throw
    # an exception (instead of returns None).
    # All fields of the LookupKey must be specified.
    @abstractmethod
    def read(self, lookup_key: LookupKey) -> DataEntry:
        pass

    # Read zero or more data entries matching the lookup key.
    @abstractmethod
    def lookup(self, lookup_key: LookupKey) -> List[DataEntry]:
        pass

    # Go through all data entries, and apply |fn| to each of them.
    @abstractmethod
    def each(self, fn: Callable[[DataEntry], None]):
        pass
