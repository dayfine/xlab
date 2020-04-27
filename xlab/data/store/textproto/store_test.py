from absl.testing import absltest

from xlab.data.store import impl_test_factory
from xlab.data.store.textproto import store

# Test that the implementation fulfills the interface.
impl_test_factory.make_data_provider_test_case(
    store.TextProtoDataStore(data_store_directory='/tmp'))

if __name__ == '__main__':
    absltest.main()
