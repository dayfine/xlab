from absl.testing import absltest

import mongomock

from xlab.data.store import impl_test_factory
from xlab.data.store import mongo

store_factory = lambda: mongo.MongoDataStore(mongomock.MongoClient())


class MongoDataStoreTest(impl_test_factory.create(store_factory)):
    pass


class MongoDataStoreParameterizedTest(
        impl_test_factory.create_parameterized_test(store_factory)):
    pass


if __name__ == '__main__':
    absltest.main()
