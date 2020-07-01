from typing import Any, Dict

from google.protobuf import json_format

from xlab.base import time
from xlab.data.proto import data_entry_pb2

DataEntry = data_entry_pb2.DataEntry


def to_mongo_doc(data_entry: DataEntry) -> Dict[Any, Any]:
    bson = json_format.MessageToDict(data_entry, use_integers_for_enums=True)
    # Store the timestamp as mongo Date by passing a Datetime object.
    bson['timestamp'] = time.ParseCivilTime(bson['timestamp'])
    return bson


def from_mongo_doc(bson: Dict[Any, Any]) -> DataEntry:
    # NOTE: |isoformat| is used here, as the timestamp from mongo will be the
    # built-in datetime class. Also add the 'Z' which is expected by ParseDict
    # and is consistent withMessageToDict.
    bson['timestamp'] = bson['timestamp'].isoformat() + 'Z'
    bson['id'] = str(bson['_id'])

    # ParseDict takes a message type and also return it as results
    # ignore_unknown_fields is used to ignore mongo's _id field.
    return json_format.ParseDict(bson, DataEntry(), ignore_unknown_fields=True)
