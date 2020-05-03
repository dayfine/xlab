from absl.testing import absltest

import mongomock

from xlab.data.store import impl_test_factory
from xlab.data.store.mongo import store

mongo_store = store.MongoDataStore(mongomock.MongoClient().db)
# Test that the implementation fulfills the interface.
impl_test_factory.make_data_provider_test_case(mongo_store)

if __name__ == '__main__':
    absltest.main()
