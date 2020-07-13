from typing import Callable, Tuple

from absl.testing import absltest, parameterized
from hamcrest import assert_that
from google.protobuf import timestamp_pb2, text_format
from proto_matcher import equals_proto, ignoring_repeated_field_ordering

from xlab.data import store
from xlab.data.store import key
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.net.proto import time_util
from xlab.util.status import errors

_DataEntry = data_entry_pb2.DataEntry

StoreFactory = Callable[[], store.DataStore]


def get_data_entry_one():
    return text_format.Parse(
        """
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 290.87
        timestamp {
            seconds: 1234567
        }""", _DataEntry())


def get_data_entry_two():
    return text_format.Parse(
        """
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 300.01
        timestamp {
            seconds: 567890
        }""", _DataEntry())


def get_data_entry_three():
    return text_format.Parse(
        """
        data_space: STOCK_DATA
        symbol: "BA"
        data_type: CLOSE_PRICE
        value: 115.32
        timestamp {
            seconds: 1234567
        }
        """, _DataEntry())


def create(impl_factory: StoreFactory) -> absltest.TestCase:

    class DataStoreTestCase(absltest.TestCase):

        def setUp(self):
            self._store = impl_factory()

        def test_add_then_read(self):
            self._store.add(get_data_entry_one())

            lookup_key = key.make_lookup_key(get_data_entry_one())
            assert_that(self._store.read(lookup_key),
                        equals_proto(get_data_entry_one()))

        def test_add_data_entry_with_the_same_timestamp(self):
            self._store.add(get_data_entry_one())
            with self.assertRaises(errors.AlreadyExistsError):
                self._store.add(get_data_entry_one())

        def test_read_data_that_does_not_exist(self):
            self._store.add(get_data_entry_one())

            with self.assertRaises(errors.NotFoundError):
                lookup_key = store.DataStore.LookupKey(
                    data_space=int(_DataEntry.STOCK_DATA),
                    symbol="SPY",
                    data_type=data_type_pb2.DataType.CLOSE_PRICE,
                    timestamp=time_util.to_time(
                        timestamp_pb2.Timestamp(seconds=654321)))
                self._store.read(lookup_key)

        def test_each(self):
            self._store.add(get_data_entry_one())
            count = 0

            def inc(payload):
                assert isinstance(payload, _DataEntry)
                nonlocal count
                count += 1

            self._store.each(inc)
            self.assertEqual(count, 1)

    return DataStoreTestCase


def create_parameterized_test(
        impl_factory: StoreFactory) -> parameterized.TestCase:

    class ParameterizedLookupTest(parameterized.TestCase):

        @parameterized.named_parameters(
            ("Two matches", _DataEntry.STOCK_DATA, "SPY",
             data_type_pb2.DataType.CLOSE_PRICE,
             (get_data_entry_one(), get_data_entry_two())),
            ("One match", _DataEntry.STOCK_DATA, "BA",
             data_type_pb2.DataType.CLOSE_PRICE, (get_data_entry_three(),)),
            ("All matches", _DataEntry.STOCK_DATA, None, 0,
             (get_data_entry_one(), get_data_entry_two(),
              get_data_entry_three())),
            ("No match", _DataEntry.STOCK_DATA, "BA",
             data_type_pb2.DataType.OPEN_PRICE, ()))
        def test_lookup(self, data_space: _DataEntry.DataSpace, symbol: str,
                        data_type: data_type_pb2.DataType.Enum,
                        data_entries: Tuple[_DataEntry]):
            store_impl = impl_factory()
            store_impl.add(get_data_entry_one())
            store_impl.add(get_data_entry_two())
            store_impl.add(get_data_entry_three())

            lookup_key = store.DataStore.LookupKey(data_space=data_space,
                                                   symbol=symbol or "",
                                                   data_type=data_type)
            actual = store_impl.lookup(lookup_key)
            expected = data_entry_pb2.DataEntries()
            expected.entries.extend(data_entries)

            assert_that(
                actual,
                ignoring_repeated_field_ordering(equals_proto(expected)))

    return ParameterizedLookupTest
