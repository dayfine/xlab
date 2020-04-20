from typing import Tuple

from xlab.data.proto.data_entry_pb2 import DataEntry


def make_key(data_entry: DataEntry) -> Tuple:
    return (
        data_entry.data_space,
        data_entry.symbol,
        data_entry.data_type,
        data_entry.timestamp,
    )
