from datetime import datetime

from absl.testing import absltest, parameterized
from google.protobuf import text_format, timestamp_pb2

from xlab.data.store.interface import LookupKey
from xlab.data.store.in_memory.impl import InMemoryDataStore
from xlab.data.proto.data_entry_pb2 import DataEntry
from xlab.util.status import errors


class InMemoryDataStoreTest(absltest.TestCase):
    def setUp(self):
        self._store = InMemoryDataStore()
        self._default_data_entry = DataEntry()
        text_format.Merge(
            """
          data_space: STOCK_DATA
          symbol: "SPY"
          data_type: "close"
          value: 290.87
          timestamp {
            seconds: 1234567
            nanos: 89101112
          }
        """, self._default_data_entry)

    def test_add_then_read(self):
        self._store.add(self._default_data_entry)

        lookup_key = LookupKey(
            data_space=int(DataEntry.STOCK_DATA),
            symbol="SPY",
            data_type="close",
            timestamp=timestamp_pb2.Timestamp(seconds=1234567,
                                              nanos=89101112).ToDatetime())
        self.assertEqual(self._store.read(lookup_key),
                         self._default_data_entry)

    def test_add_data_entry_with_the_same_timestamp(self):
        self._store.add(self._default_data_entry)
        with self.assertRaises(errors.AlreadyExistsError):
            self._store.add(self._default_data_entry)

    def test_read_data_that_does_not_exist(self):
        self._store.add(self._default_data_entry)

        with self.assertRaises(LookupError):
            lookup_key = LookupKey(
                data_space=int(DataEntry.STOCK_DATA),
                symbol="SPY",
                data_type="close",
                timestamp=timestamp_pb2.Timestamp(seconds=1234567,
                                                  nanos=1234567).ToDatetime())
            self._store.read(lookup_key)

    def test_lookup(self):
        data_entry1 = DataEntry()
        data_entry1.CopyFrom(self._default_data_entry)

        data_entry2 = DataEntry()
        data_entry2.CopyFrom(self._default_data_entry)
        data_entry2.timestamp.FromDatetime(datetime(2020, 12, 31))

        data_entry3 = DataEntry()
        data_entry3.CopyFrom(self._default_data_entry)
        data_entry3.symbol = "BA"

        self._store.add(data_entry1)
        self._store.add(data_entry2)
        self._store.add(data_entry3)

        lookup_key = LookupKey(data_space=int(DataEntry.STOCK_DATA),
                               symbol="SPY",
                               data_type="close")
        self.assertEqual(self._store.lookup(lookup_key),
                         [data_entry1, data_entry2])

        lookup_key = LookupKey(data_space=int(DataEntry.STOCK_DATA),
                               symbol="BA",
                               data_type="close")
        self.assertEqual(self._store.lookup(lookup_key), [data_entry3])

        lookup_key = LookupKey(data_space=int(DataEntry.STOCK_DATA))
        self.assertEqual(self._store.lookup(lookup_key),
                         [data_entry1, data_entry2, data_entry3])

        lookup_key = LookupKey(data_space=int(DataEntry.STOCK_DATA),
                               symbol="BA",
                               data_type="open")
        self.assertEqual(self._store.lookup(lookup_key), [])

    def test_each(self):
        self._store.add(self._default_data_entry)
        count = 0

        def inc(_):
            nonlocal count
            count += 1

        self._store.each(inc)
        self.assertEqual(count, 1)


if __name__ == '__main__':
    absltest.main()
