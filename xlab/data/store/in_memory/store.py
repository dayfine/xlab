import collections
from typing import Callable, Dict, List, Tuple

from xlab.data import store
from xlab.data.proto import data_entry_pb2
from xlab.data.store import key
from xlab.util.status import errors


class InMemoryDataStore(store.DataStore):

    def __init__(self):
        # In memory data store has empty initial state
        self._data: Dict[
            key.DataKey,
            List[data_entry_pb2.DataEntry]] = collections.defaultdict(list)

    # Load and unload are in-memory specific helpers to manage the data.
    def load(self, data_key: key.DataKey,
             data_entries: List[data_entry_pb2.DataEntry]):
        self._data[data_key] = data_entries

    def unload(self, data_key: key.DataKey):
        del self._data[data_key]

    def add(self, data_entry: data_entry_pb2.DataEntry):
        data_key = key.make_key(data_entry)
        data_entries = self._data[data_key]
        if data_entry.timestamp.ToSeconds() in {
                e.timestamp.ToSeconds() for e in data_entries
        }:
            raise errors.AlreadyExistsError(
                f'The data entry to add already exists: {data_entry}')
        self._data[data_key].append(data_entry)
        self._data[data_key].sort(key=lambda e: e.timestamp.ToSeconds())

    def read(self,
             lookup_key: store.DataStore.LookupKey) -> data_entry_pb2.DataEntry:
        data_entries = self._data[key.from_lookup_key(lookup_key)]
        try:
            return next(e for e in data_entries
                        if e.timestamp.ToSeconds() == lookup_key.timestamp)
        except StopIteration:
            raise errors.NotFoundError(
                f'Cannot find data matching lookup key: {lookup_key}')

    def lookup(
            self, lookup_key: store.DataStore.LookupKey
    ) -> data_entry_pb2.DataEntries:
        results = []
        for data_key, data_entries in self._data.items():
            if not key.key_matches(data_key, lookup_key):
                continue
            results.extend((e for e in data_entries
                            if lookup_key.timestamp is None or
                            e.timestamp.ToSeconds() == lookup_key.timestamp))
        # Return a value, as extend makes copies.
        data_entries = data_entry_pb2.DataEntries()
        data_entries.entries.extend(results)
        return data_entries

    def each(self, fn: Callable[[data_entry_pb2.DataEntry], None]):
        for key, data_entries in self._data.items():
            for data_entry in data_entries:
                fn(data_entry)
