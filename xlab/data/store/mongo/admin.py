from typing import Tuple

from bson import ObjectId
import pymongo

from xlab.data.store.mongo import constants
from xlab.data.store.mongo import db_client


def delete_by_ids(ids: Tuple[str]) -> pymongo.results.DeleteResult:
    client = db_client.connect()
    db = client[constants.XLAB_DB]
    coll = db[constants.DATA_ENTRY_COL]

    return coll.delete_many({'_id': {'$in': [ObjectId(_id) for _id in ids]}})
