from absl.testing import absltest

import mongomock

from xlab.data.store import impl_test_factory
from xlab.data.store.mongo import store


class MongoDataStoreTest(
        impl_test_factory.create(
            lambda: store.MongoDataStore(mongomock.MongoClient()))):
    pass


if __name__ == '__main__':
    absltest.main()
