from typing import Tuple

from xlab.data.proto import data_entry_pb2
from xlab.data.store import interface

# DataSpace, symbol, data_type
DataKey = Tuple[int, str, str]


def make_key(data_entry: data_entry_pb2.DataEntry) -> DataKey:
    return (
        data_entry.data_space,
        data_entry.symbol,
        data_entry.data_type,
    )


def key_matches(data_key: DataKey, lookup_key: interface.LookupKey) -> bool:
    return not ((lookup_key.data_space is not None and
                 lookup_key.data_space != data_key.data_space) or
                (lookup_key.symbol is not None and
                 lookup_key.symbol != data_key.symbol) or
                (lookup_key.data_type is not None and
                 lookup_key.data_type != data_key.data_type))


def from_lookup_key(lookup_key: interface.LookupKey) -> DataKey:
    return (lookup_key.data_space, lookup_key.symbol, lookup_key.data_type)
