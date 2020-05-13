from typing import Callable, Dict, List, Tuple

from google.protobuf import json_format, timestamp_pb2
import pymongo
from pymongo import client_session

from xlab.data.proto import data_entry_pb2
from xlab.data.store import interface, key
from xlab.data.store.mongo import db_client
from xlab.util.status import errors


class MongoDataStore(interface.DataStore):

    _DATABASE = 'xlab'
    _DATA_ENTRY_COLLECTION = 'data_entries'

    def __init__(self, client: pymongo.MongoClient = db_client.connect()):
        self._client = client
        self._db = self._client[self._DATABASE]
        self._coll = self._db[self._DATA_ENTRY_COLLECTION]

    def add(self, data_entry: data_entry_pb2.DataEntry):
        # TODO: causal_consistency should be supported with |start_session|;
        # however, this is not supported by the mock: https://github.com/mongomock/mongomock/issues/614
        lookup_key = key.make_lookup_key(data_entry)
        record = self._coll.find_one(self._get_filter(lookup_key))
        if record is not None:
            raise errors.AlreadyExistsError(
                f'The data entry to add already exists: {record}')

        self._coll.insert_one(
            json_format.MessageToDict(data_entry, use_integers_for_enums=True))

    def batch_add(self, data_entries: data_entry_pb2.DataEntries):
        self._coll.insert_many([
            json_format.MessageToDict(d, use_integers_for_enums=True)
            for d in data_entries.entries
        ])

    def read(self, lookup_key: interface.LookupKey) -> data_entry_pb2.DataEntry:
        record = self._coll.find_one(self._get_filter(lookup_key))
        if record is None:
            raise errors.NotFoundError(
                f'Cannot find data matching lookup key: {lookup_key}')
        return self._parse(record)

    def lookup(self,
               lookup_key: interface.LookupKey) -> data_entry_pb2.DataEntries:
        cursor = self._coll.find(self._get_filter(lookup_key))
        entries = [self._parse(record) for record in cursor]
        result = data_entry_pb2.DataEntries()
        result.entries.extend(entries)
        return result

    def each(self, fn: Callable[[data_entry_pb2.DataEntry], None]):
        all_cursor = self._coll.find()
        for record in all_cursor:
            fn(self._parse(record))

    def _parse(self, document: Dict) -> data_entry_pb2.DataEntry:
        # ParseDict takes a message type and also return it as results
        # ignore_unknown_fields is used to ignore mongo's _id field.
        return json_format.ParseDict(document,
                                     data_entry_pb2.DataEntry(),
                                     ignore_unknown_fields=True)

    def _get_filter(self, lookup_key: interface.LookupKey) -> Dict:
        res = {}
        if lookup_key.data_space:
            res['dataSpace'] = lookup_key.data_space
        if lookup_key.symbol:
            res['symbol'] = lookup_key.symbol
        if lookup_key.data_type:
            res['dataType'] = lookup_key.data_type
        if lookup_key.timestamp:
            timestamp_proto = timestamp_pb2.Timestamp()
            timestamp_proto.FromSeconds(lookup_key.timestamp)
            res['timestamp'] = timestamp_proto.ToJsonString()
        return res
