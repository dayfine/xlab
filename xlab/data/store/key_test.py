from absl.testing import absltest, parameterized

from xlab.data.store import key
from xlab.data.proto import data_entry_pb2, data_type_pb2


class DataStoreKeyParameterizedTest(parameterized.TestCase):

    @parameterized.parameters((
        data_entry_pb2.DataEntry.STOCK_DATA,
        "IBM",
        data_type_pb2.DataType.CLOSE_PRICE,
    ), (data_entry_pb2.DataEntry.STOCK_METADATA, "BA",
        data_type_pb2.DataType.OPEN_PRICE))
    def test_make_key(self, data_space, symbol, data_type):
        data_entry = data_entry_pb2.DataEntry(data_space=data_space,
                                              symbol=symbol,
                                              data_type=data_type)
        self.assertEqual(key.make_key(data_entry),
                         (data_space, symbol, data_type))


if __name__ == '__main__':
    absltest.main()
