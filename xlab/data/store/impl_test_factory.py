from typing import Callable

from absl.testing import absltest, parameterized
from google.protobuf import timestamp_pb2

from xlab.data.store import interface, key, units
from xlab.data.proto import data_entry_pb2
from xlab.net.proto.testing import compare, parse
from xlab.util.status import errors

_DATA_ENTRY1 = """
data_space: STOCK_DATA
symbol: "SPY"
data_type: "close"
value: 290.87
timestamp {
  seconds: 1234567
}
"""

_DATA_ENTRY2 = """
data_space: STOCK_DATA
symbol: "SPY"
data_type: "close"
value: 300.01
timestamp {
  seconds: 567890
}
"""

_DATA_ENTRY3 = """
data_space: STOCK_DATA
symbol: "BA"
data_type: "close"
value: 115.32
timestamp {
  seconds: 1234567
}
"""


def create(impl_factory: Callable[[], interface.DataStore]):

    class DataStoreTestCaseBase(absltest.TestCase):

        def setUp(self):
            self._store = impl_factory()
            self._data_entry1 = parse.parse_test_proto(_DATA_ENTRY1,
                                                       data_entry_pb2.DataEntry)

        def test_add_then_read(self):
            self._store.add(self._data_entry1)

            lookup_key = key.make_lookup_key(self._data_entry1)
            compare.assertProtoEqual(self, self._store.read(lookup_key),
                                     _DATA_ENTRY1)

        def test_add_data_entry_with_the_same_timestamp(self):
            self._store.add(self._data_entry1)
            with self.assertRaises(errors.AlreadyExistsError):
                self._store.add(self._data_entry1)

        def test_read_data_that_does_not_exist(self):
            self._store.add(self._data_entry1)

            with self.assertRaises(errors.NotFoundError):
                lookup_key = interface.LookupKey(
                    data_space=int(data_entry_pb2.DataEntry.STOCK_DATA),
                    symbol="SPY",
                    data_type="close",
                    timestamp=units.Seconds(
                        timestamp_pb2.Timestamp(seconds=654321).ToSeconds()))
                self._store.read(lookup_key)

        class LookupTest(parameterized.TestCase):

            @parameterized.parameters(
                (data_entry_pb2.DataEntry.STOCK_DATA, "SPY", "close",
                 (_DATA_ENTRY1, _DATA_ENTRY2)),
                (data_entry_pb2.DataEntry.STOCK_DATA, "BA", "close",
                 (_DATA_ENTRY3)),
                (data_entry_pb2.DataEntry.STOCK_DATA, None, None,
                 (_DATA_ENTRY1, _DATA_ENTRY2, _DATA_ENTRY3)),
                (data_entry_pb2.DataEntry.STOCK_DATA, "BA", "open", ()))
            def test_lookup(self, data_space, symbol, data_type, data_entries):
                self._store.add(
                    parse.parse_test_proto(_DATA_ENTRY1,
                                           data_entry_pb2.DataEntry))
                self._store.add(
                    parse.parse_test_proto(_DATA_ENTRY2,
                                           data_entry_pb2.DataEntry))
                self._store.add(
                    parse.parse_test_proto(_DATA_ENTRY3,
                                           data_entry_pb2.DataEntry))

                lookup_key = interface.LookupKey(data_space=data_space,
                                                 symbol=symol,
                                                 data_type=data_type)
                expected = data_entry_pb2.DataEntries()
                expected.entries.extend(data_entries)
                compare.assertProtoEqual(self, self._store.lookup(lookup_key),
                                         expected)

        def test_each(self):
            self._store.add(self._data_entry1)
            count = 0

            def inc(payload):
                assert isinstance(payload, data_entry_pb2.DataEntry)
                nonlocal count
                count += 1

            self._store.each(inc)
            self.assertEqual(count, 1)

    return DataStoreTestCaseBase
