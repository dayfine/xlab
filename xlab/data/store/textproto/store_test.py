from absl.testing import absltest

from xlab.data.store import impl_test_factory
from xlab.data.store.textproto import store


class TextProtoDataStoreTest(
        impl_test_factory.create(
            lambda: store.TextProtoDataStore(data_store_directory='/tmp'))):
    pass


if __name__ == '__main__':
    absltest.main()
