import pymongo

from xlab.data.store.mongo import constants


def connect(host: str = constants.LOCAL_HOST,
            port: int = constants.MONGO_DEFAULT_PORT) -> pymongo.MongoClient:
    return pymongo.MongoClient(host, port)
