import os
from typing import Callable, Dict, List

from absl import flags
from absl import logging
from google.protobuf import text_format

from xlab.data.proto import data_entry_pb2, data_type_pb2
from xlab.data.store import interface, in_memory, key
from xlab.util.status import errors

FLAGS = flags.FLAGS

flags.DEFINE_string('textproto_store_directory', 'data/store',
                    'Path relative to workspace root that stores data in text')


# WARNING: this implementation has serve limitation and caveats. Prefer other
# implementation when possible.
class TextProtoDataStore(interface.DataStore):

    def __init__(self, data_store_directory=''):
        self._mem_store = in_memory.InMemoryDataStore()
        self._data_store_directory = data_store_directory
        self._last_added_key = None

    def _load(self, data_key: key.DataKey):
        if data_key in self._mem_store._data:
            return

        data_filepath = self._get_data_filepath(data_key)
        self._maybe_create_dir(data_filepath)

        try:
            with open(data_filepath, 'r') as f:
                data_entries = data_entry_pb2.DataEntries()
                text_format.Merge(f.read(), data_entries)
                self._mem_store.load(data_key, data_entries.entries)
        except FileNotFoundError:
            logging.warning('Trying to open [%s] but failed', data_filepath)

    def commit(self, unload_afterwards=False):
        data_filepath = self._get_data_filepath(self._last_added_key)
        logging.info('Committing to [%s]', data_filepath)
        self._maybe_create_dir(data_filepath)
        with open(data_filepath, 'w') as f:
            data_entries = data_entry_pb2.DataEntries()
            data_entries.entries.extend(
                self._mem_store._data[self._last_added_key])
            f.write(text_format.MessageToString(data_entries))

        if unload_afterwards:
            self._mem_store.unload(self._last_added_key)

    def add(self, data_entry: data_entry_pb2.DataEntry, maybe_commit=True):
        data_key = key.make_key(data_entry)
        self._load(data_key)

        self._mem_store.add(data_entry)

        if maybe_commit:
            # TODO: this might be incorrect.
            if self._last_added_key is not None and data_key != self._last_added_key:
                self.commit()
        self._last_added_key = data_key

    def read(self, lookup_key: interface.LookupKey) -> data_entry_pb2.DataEntry:
        self._load(key.from_lookup_key(lookup_key))
        return self._mem_store.read(lookup_key)

    def lookup(self,
               lookup_key: interface.LookupKey) -> data_entry_pb2.DataEntries:
        self._load(key.from_lookup_key(lookup_key))
        return self._mem_store.lookup(lookup_key)

    # A lazy ForEachRows, where only loaded data will be considered.
    def each(self, fn: Callable[[data_entry_pb2.DataEntry], None]):
        return self._mem_store.each(fn)

    def _get_data_filepath(self, data_key: key.DataKey) -> str:
        data_space, symbol, data_type = data_key
        return '/'.join([
            self._data_store_directory,
            data_entry_pb2.DataEntry.DataSpace.Name(data_space),
            symbol,
            data_type_pb2.DataType.Enum.Name(data_type) + '.textproto',
        ])

    def _maybe_create_dir(self, filepath: str):
        logging.info('Creating directory for: %s', filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
