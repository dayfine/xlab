from typing import Callable, Tuple
import unittest

from absl.testing import absltest, parameterized
from google.protobuf import timestamp_pb2

from xlab.data import store
from xlab.data.store import key
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.net.proto import time_util
from xlab.net.proto.testing import compare
from xlab.net.proto.testing import parse
from xlab.util.status import errors

StoreFactory = Callable[[], store.DataStore]


def get_data_entry_one():
    return parse.parse_test_proto(
        """
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 290.87
        timestamp {
        seconds: 1234567
        }""", data_entry_pb2.DataEntry)


def get_data_entry_two():
    return parse.parse_test_proto(
        """
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 300.01
        timestamp {
        seconds: 567890
        }""", data_entry_pb2.DataEntry)


def get_data_entry_three():
    return parse.parse_test_proto(
        """
        data_space: STOCK_DATA
        symbol: "BA"
        data_type: CLOSE_PRICE
        value: 115.32
        timestamp {
        seconds: 1234567
        }
        """, data_entry_pb2.DataEntry)


def create(impl_factory: StoreFactory) -> absltest.TestCase:

    class DataStoreTestCase(absltest.TestCase):

        def setUp(self):
            self._store = impl_factory()

        def test_add_then_read(self):
            self._store.add(get_data_entry_one())

            lookup_key = key.make_lookup_key(get_data_entry_one())
            compare.assertProtoEqual(self, self._store.read(lookup_key),
                                     get_data_entry_one())

        def test_add_data_entry_with_the_same_timestamp(self):
            self._store.add(get_data_entry_one())
            with self.assertRaises(errors.AlreadyExistsError):
                self._store.add(get_data_entry_one())

        def test_read_data_that_does_not_exist(self):
            self._store.add(get_data_entry_one())

            with self.assertRaises(errors.NotFoundError):
                lookup_key = store.DataStore.LookupKey(
                    data_space=int(data_entry_pb2.DataEntry.STOCK_DATA),
                    symbol="SPY",
                    data_type=data_type_pb2.DataType.CLOSE_PRICE,
                    timestamp=time_util.to_time(
                        timestamp_pb2.Timestamp(seconds=654321)))
                self._store.read(lookup_key)

        def test_each(self):
            self._store.add(get_data_entry_one())
            count = 0

            def inc(payload):
                assert isinstance(payload, data_entry_pb2.DataEntry)
                nonlocal count
                count += 1

            self._store.each(inc)
            self.assertEqual(count, 1)

    return DataStoreTestCase


def create_parameterized_test(
        impl_factory: StoreFactory) -> parameterized.TestCase:

    class ParameterizedLookupTest(parameterized.TestCase):

        @parameterized.named_parameters(
            ("Two matches", data_entry_pb2.DataEntry.STOCK_DATA, "SPY",
             data_type_pb2.DataType.CLOSE_PRICE,
             (get_data_entry_one(), get_data_entry_two())),
            ("One match", data_entry_pb2.DataEntry.STOCK_DATA, "BA",
             data_type_pb2.DataType.CLOSE_PRICE, (get_data_entry_three(),)),
            ("All matches", data_entry_pb2.DataEntry.STOCK_DATA, None, 0,
             (get_data_entry_one(), get_data_entry_two(),
              get_data_entry_three())),
            ("No match", data_entry_pb2.DataEntry.STOCK_DATA, "BA",
             data_type_pb2.DataType.OPEN_PRICE, ()))
        def test_lookup(self, data_space: data_entry_pb2.DataEntry.DataSpace,
                        symbol: str, data_type: data_type_pb2.DataType.Enum,
                        data_entries: Tuple[data_entry_pb2.DataEntry]):
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

            # Sort to ignore repeated field ordering.
            actual.entries.sort(key=str)
            expected.entries.sort(key=str)
            compare.assertProtoEqual(self, actual, expected)

    return ParameterizedLookupTest
