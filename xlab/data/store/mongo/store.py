from typing import Callable, Dict, List, Tuple

from google.protobuf import timestamp_pb2
import pymongo

from xlab.base import time
from xlab.data import store
from xlab.data.converters import mongo as mongo_converter
from xlab.data.proto import data_entry_pb2
from xlab.data.store import key
from xlab.data.store.mongo import constants
from xlab.data.store.mongo import db_client
from xlab.util.status import errors

DataEntry = data_entry_pb2.DataEntry


class MongoDataStore(store.DataStore):

    def __init__(self, client: pymongo.MongoClient = db_client.connect()):
        self._client = client
        self._db = self._client[constants.XLAB_DB]
        self._coll = self._db[constants.DATA_ENTRY_COL]

    def add(self, data_entry: DataEntry):
        # TODO: causal_consistency should be supported with |start_session|;
        # however, this is not supported by the mock: https://github.com/mongomock/mongomock/issues/614
        lookup_key = key.make_lookup_key(data_entry)
        record = self._coll.find_one(self._get_filter(lookup_key))
        if record is not None:
            raise errors.AlreadyExistsError(
                f'The data entry to add already exists: {record}')

        self._coll.insert_one(mongo_converter.to_mongo_doc(data_entry))

    def batch_add(self, data_entry_list: List[data_entry_pb2.DataEntry]):
        self._coll.insert_many(
            [mongo_converter.to_mongo_doc(d) for d in data_entry_list])

    def read(self, lookup_key: store.DataStore.LookupKey) -> DataEntry:
        record = self._coll.find_one(self._get_filter(lookup_key))
        if record is None:
            raise errors.NotFoundError(
                f'Cannot find data matching lookup key: {lookup_key}')
        return mongo_converter.from_mongo_doc(record)

    def lookup(
            self, lookup_key: store.DataStore.LookupKey
    ) -> data_entry_pb2.DataEntries:
        cursor = self._coll.find(self._get_filter(lookup_key))
        entries = [mongo_converter.from_mongo_doc(record) for record in cursor]
        result = data_entry_pb2.DataEntries()
        result.entries.extend(entries)
        return result

    def each(self, fn: Callable[[data_entry_pb2.DataEntry], None]):
        all_cursor = self._coll.find()
        for record in all_cursor:
            fn(mongo_converter.from_mongo_doc(record))

    def _get_filter(self, lookup_key: store.DataStore.LookupKey) -> Dict:
        res = {}
        if lookup_key.data_space:
            res['dataSpace'] = lookup_key.data_space
        if lookup_key.symbol:
            res['symbol'] = lookup_key.symbol
        if lookup_key.data_type:
            res['dataType'] = lookup_key.data_type
        if lookup_key.timestamp:
            res['timestamp'] = time.ToCivil(lookup_key.timestamp)
        return res
