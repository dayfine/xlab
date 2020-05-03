from typing import Callable, Dict, List, Tuple

from google.protobuf import json_format, timestamp_pb2
from pymongo import database

from xlab.data.proto import data_entry_pb2
from xlab.data.store import interface, key
from xlab.util.status import errors

from xlab.data.store.mongo import db_client


class MongoDataStore(interface.DataStore):

    _DATA_ENTRY_COLLECTION = 'data_entries'

    def __init__(self, db: database.Database = db_client.connect()):
        self._db = db
        self._coll = self._db[self._DATA_ENTRY_COLLECTION]

    def add(self, data_entry: data_entry_pb2.DataEntry):
        self._coll.insert_one(
            json_format.MessageToDict(data_entry, use_integers_for_enums=True))

    def batch_add(self, data_entries: data_entry_pb2.DataEntries):
        self._coll.insert_many([
            json_format.MessageToDict(d, use_integers_for_enums=True)
            for d in data_entries.entries
        ])

    def read(self, lookup_key: interface.LookupKey) -> data_entry_pb2.DataEntry:
        record = self._coll.find_one(get_filter(lookup_key))
        return json_format.ParseDict(record)

    def lookup(self,
               lookup_key: interface.LookupKey) -> data_entry_pb2.DataEntries:
        cursor = self._coll.find(get_filter(lookup_key))
        return [json_format.ParseDict(record) for record in cursor]

    def each(self, fn: Callable[[data_entry_pb2.DataEntry], None]):
        all_cursor = self._coll.find()
        for record in all_cursor:
            fn(json_format.ParseDict(record))

    def get_filter(self, lookup_key: interface.LookupKey) -> Dict:
        res = {}
        if lookup_key.data_space is not None:
            res['data_space'] = lookup_key.data_space
        if lookup_key.symbol is not None:
            res['symbol'] = lookup_key.symbol
        if lookup_key.data_type is not None:
            res['data_type'] = lookup_key.data_type
        if lookup_key.timestamp is not None:
            timestamp_proto = timestamp_pb2.Timestamp()
            timestamp_proto.FromDatetime(lookup_key.timestamp)
            res['timestamp'] = json_format.MessageToDict(timestamp_proto)
        return res
