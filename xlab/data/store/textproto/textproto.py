from typing import Callable, Dict, List

from xlab.data.proto.data_entry_pb2 import DataEntry, DataEntries
from xlab.data.store.interface import DataStore, LookupKey
from xlab.data.store.in_memory.impl import InMemoryDataStore
from xlab.data.store.key import make_key
from xlab.util.status import errors


class TextProtoDataStore(DataStore):
    def __init__(self, data_store_path=""):
        self._mem_store = InMemoryDataStore()
        self._data_store_path = data_store_path
        self.last_updated_key = None
        self._load()

    def _load(self):
        # Load from directory of files.
        pass

    def _commit(self):
        # update
        pass

    def add(self, data_entry: DataEntry):
        self._mem_store.add(data_entry)
        self._commit()

    def read(self, key: LookupKey) -> DataEntry:
        return self._mem_store.read(key)

    def lookup(self, key: LookupKey) -> List[DataEntry]:
        return self._mem_store.lookup(key)

    def each(self, fn: Callable[[DataEntry], None]):
        return self._mem_store.each(fn)
