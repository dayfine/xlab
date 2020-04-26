from typing import Callable, Dict, List

from xlab.data.proto import data_entry_pb2
from xlab.data.store import interface, in_memory, key
from xlab.util.status import errors


class TextProtoDataStore(interface.DataStore):

    def __init__(self, data_store_path=""):
        self._mem_store = in_memory.InMemoryDataStore()
        self._data_store_path = data_store_path
        self.last_updated_key = None
        self._load()

    def _load(self):
        # Load from directory of files.
        pass

    def _commit(self):
        # update
        pass

    def add(self, data_entry: data_entry_pb2.DataEntry):
        self._mem_store.add(data_entry)
        self._commit()

    def read(self, lookup_key: interface.LookupKey) -> data_entry_pb2.DataEntry:
        return self._mem_store.read(key)

    def lookup(
            self,
            lookup_key: interface.LookupKey) -> List[data_entry_pb2.DataEntry]:
        return self._mem_store.lookup(key)

    def each(self, fn: Callable[[data_entry_pb2.DataEntry], None]):
        return self._mem_store.each(fn)
