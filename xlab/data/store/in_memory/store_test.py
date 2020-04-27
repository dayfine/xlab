from absl.testing import absltest

from xlab.data.store import impl_test_factory
from xlab.data.store.in_memory import store

# Test that the implementation fulfills the interface.
impl_test_factory.make_data_provider_test_case(store.InMemoryDataStore())

if __name__ == '__main__':
    absltest.main()
