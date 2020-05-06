import pymongo

_LOCAL_HOST = 'localhost'
_DEFAULT_PORT = 27017


def connect(host: str = _LOCAL_HOST,
            port: int = _DEFAULT_PORT) -> pymongo.MongoClient:
    return pymongo.MongoClient(host, port)
