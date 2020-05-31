from typing import Any, Dict

from google.protobuf import json_format

from xlab.data.proto import data_entry_pb2

DataEntry = data_entry_pb2.DataEntry


def to_mongo_doc(data_entry: DataEntry) -> Dict[Any, Any]:
    return json_format.MessageToDict(data_entry, use_integers_for_enums=True)


def from_mongo_doc(document: Dict[Any, Any]) -> DataEntry:
    # ParseDict takes a message type and also return it as results
    # ignore_unknown_fields is used to ignore mongo's _id field.
    return json_format.ParseDict(document,
                                 DataEntry(),
                                 ignore_unknown_fields=True)
