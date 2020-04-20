from datetime import datetime

from absl.testing import absltest, parameterized

from xlab.data.store.key import make_key
from xlab.data.proto.data_entry_pb2 import DataEntry


class DataStoreKeyTest(absltest.TestCase):

    class KeyParameterizedTest(parameterized.TestCase):
        @parameterized.parameters(
            (DataEntry.STOCK_DATA, "IBM", "close", datetime(1969, 12, 31)),
            (DataEntry.STOCK_METADATA, "BA", "open", datetime(2100, 1, 1)))
        def test_make_key(self, data_space, symbol, data_type, timestamp):
            data_entry = DataEntry(data_space=data_space,
                                   symbol=symol,
                                   data_type=data_type,
                                   timestamp=timestamp)
            self.assertEqual(make_key(data_entry),
                             (data_space, symbol, data_type, timestamp))


if __name__ == '__main__':
    absltest.main()