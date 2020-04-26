import datetime

from absl.testing import absltest, parameterized

from xlab.data.store import key
from xlab.data.proto import data_entry_pb2


class DataStoreKeyTest(absltest.TestCase):

    class KeyParameterizedTest(parameterized.TestCase):

        @parameterized.parameters(
            (data_entry_pb2.DataEntry.STOCK_DATA, "IBM", "close",
             datetime.datetime(1969, 12, 31)),
            (data_entry_pb2.DataEntry.STOCK_METADATA, "BA", "open",
             datetime.datetime(2100, 1, 1)))
        def test_make_key(self, data_space, symbol, data_type, timestamp):
            data_entry = data_entry_pb2.DataEntry(data_space=data_space,
                                                  symbol=symol,
                                                  data_type=data_type,
                                                  timestamp=timestamp)
            self.assertEqual(key.make_key(data_entry),
                             (data_space, symbol, data_type, timestamp))


if __name__ == '__main__':
    absltest.main()
