import pymongo
from pymongo import database

_LOCAL_HOST = 'localhost'
_DEFAULT_PORT = 27017
_DATABASE = 'xlab'


def connect(host: str = _LOCAL_HOST,
            port: int = _DEFAULT_PORT,
            db: str = _DATABASE) -> database.Database:
    client = pymongo.MongoClient(host, port)
    return client[db]
