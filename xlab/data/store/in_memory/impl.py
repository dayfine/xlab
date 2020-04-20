import bisect
from collections import defaultdict
from typing import Callable, Dict, List, Tuple

from xlab.data.proto.data_entry_pb2 import DataEntry
from xlab.data.store.interface import DataStore, LookupKey
from xlab.data.store.key import make_key
from xlab.util.status import errors


class InMemoryDataStore(DataStore):
    def __init__(self):
        # In memory data store has empty initial state
        self.data: Dict[Tuple, List[DataEntry]] = defaultdict(list)

    def add(self, data_entry: DataEntry):
        key = make_key(data_entry)[:3]  # Do not use timestamp in key
        data_entries = self.data[key]
        if data_entry.timestamp.ToDatetime() in {
                e.timestamp.ToDatetime()
                for e in data_entries
        }:
            raise errors.AlreadyExistsError(
                f'The data entry to add already exists: {data_entry}')
        self.data[key].append(data_entry)
        self.data[key].sort(key=lambda e: e.timestamp.ToDatetime())

    def read(self, lookup_key: LookupKey) -> DataEntry:
        expected_key = (lookup_key.data_space, lookup_key.symbol,
                        lookup_key.data_type)
        data_entries = self.data[expected_key]
        try:
            return next(e for e in data_entries
                        if e.timestamp.ToDatetime() == lookup_key.timestamp)
        except StopIteration:
            raise LookupError(
                f'Cannot find data matching lookup key: {lookup_key}')

    def lookup(self, lookup_key: LookupKey) -> List[DataEntry]:
        results = []
        for key, data_entries in self.data.items():
            if not self._key_matches(key, lookup_key): continue
            results.extend(
                (e for e in data_entries if lookup_key.timestamp is None
                 or e.timestamp.ToDatetime() == lookup_key.timestamp))
        return results

    def each(self, fn: Callable[[DataEntry], None]):
        for key, data_entries in self.data.items():
            for data_entry in data_entries:
                fn(data_entry)

    def _key_matches(self, key: Tuple, lookup_key: LookupKey) -> bool:
        (data_space, symbol, data_type) = key
        return not (
            (lookup_key.data_space is not None
             and lookup_key.data_space != data_space) or
            (lookup_key.symbol is not None and lookup_key.symbol != symbol) or
            (lookup_key.data_type is not None
             and lookup_key.data_type != data_type))