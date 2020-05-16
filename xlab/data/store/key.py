from typing import Tuple

from xlab.base import time
from xlab.data import store
from xlab.data.proto import data_entry_pb2, data_type_pb2

DataKey = Tuple[int,  # Prot Enum data_entry_pb2.DataEntry.DataSpace
                str,  # symbol
                int,  # Proto Enum data_type_pb2.DataType.Enum
               ]


def make_key(data_entry: data_entry_pb2.DataEntry) -> DataKey:
    return (
        data_entry.data_space,
        data_entry.symbol,
        data_entry.data_type,
    )


def key_matches(data_key: DataKey,
                lookup_key: store.DataStore.LookupKey) -> bool:
    data_space, symbol, data_type = data_key
    return ((not lookup_key.data_space or lookup_key.data_space == data_space)
            and (not lookup_key.symbol or lookup_key.symbol == symbol) and
            (not lookup_key.data_type or lookup_key.data_type == data_type))


def from_lookup_key(lookup_key: store.DataStore.LookupKey) -> DataKey:
    return (lookup_key.data_space, lookup_key.symbol, lookup_key.data_type)


def make_lookup_key(
        data_entry: data_entry_pb2.DataEntry) -> store.DataStore.LookupKey:
    return store.DataStore.LookupKey(data_space=data_entry.data_space,
                                     symbol=data_entry.symbol,
                                     data_type=data_entry.data_type,
                                     timestamp=time.Seconds(
                                         data_entry.timestamp.ToSeconds()))
