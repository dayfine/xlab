from absl.testing import absltest

from xlab.data.store import impl_test_factory
from xlab.data.store.in_memory import store

store_factory = store.InMemoryDataStore


class InMemoryDataStoreTest(impl_test_factory.create(store_factory)):
    pass


class InMemoryDataStoreParameterizedTest(
        impl_test_factory.create_parameterized_test(store_factory)):
    pass


if __name__ == '__main__':
    absltest.main()
