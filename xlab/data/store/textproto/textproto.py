from typing import Dict, List

from xlab.data.store.interface import DataStore, LookupKey
from xlab.data.store.key import make_key
from xlab.util.status import errors

from xlab.data.proto.data_entry_pb2 import DataEntry, DataEntries


class TextProtoDataStore(DataStore):
    def __init__(self):
        self.data: Dict[str, DataEntries] = {}

    def add(self, data_entry: DataEntry):
        pass

    def read(self, key: LookupKey) -> DataEntry:
        pass

    def lookup(self, key: LookupKey) -> List[DataEntry]:
        pass

    def each(self, fn: Callable[[DataEntry], None]):
        pass

    def commit(self):
        pass
