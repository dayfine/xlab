from xlab.data.store import store
from xlab.util.status import errors

from xlab.data.proto import data_entry_pb2


class TextProtoDataStore(store.DataStore):
    def add(self, data_entry: data_entry_pb2.DataEntry):
        pass

    def read(self, key: str) -> data_entry_pb2.DataEntry:
        pass

    def each(self, fn: Callable[[data_entry_pb2.DataEntry], None]):
        pass
