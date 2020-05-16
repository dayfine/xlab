import shutil

from absl.testing import absltest

from xlab.data.store import impl_test_factory
from xlab.data.store import textproto

_TEST_STORE_DIR = '/tmp/xlab_bazel_store_test/'
store_factory = lambda: textproto.TextProtoDataStore(data_store_directory=
                                                     _TEST_STORE_DIR)


class TextProtoDataStoreTest(impl_test_factory.create(store_factory)):

    def tearDown(self):
        shutil.rmtree(_TEST_STORE_DIR)


class TextProtoDataStoreParameterizedTest(
        impl_test_factory.create_parameterized_test(store_factory)):

    def tearDown(self):
        shutil.rmtree(_TEST_STORE_DIR)


if __name__ == '__main__':
    absltest.main()
