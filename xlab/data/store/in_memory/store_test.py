from absl.testing import absltest

from xlab.data.store import impl_test_factory
from xlab.data.store.in_memory import store


class InMemoryDataStoreTest(
        impl_test_factory.create(lambda: store.InMemoryDataStore())):
    pass


if __name__ == '__main__':
    absltest.main()
