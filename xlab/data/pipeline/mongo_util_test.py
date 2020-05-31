from absl.testing import absltest
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
import pymongo

from xlab.base import time
from xlab.data.pipeline import mongo_util
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.net.proto import time_util

DataEntry = data_entry_pb2.DataEntry
DataType = data_type_pb2.DataType

# Note: this tests requires a local mongo connection.
_TEST_URI = 'mongodb://localhost:27017'
_TEST_DB = 'test'
_TEST_COLL = 'coll'


def get_data_entries():
    return [
        DataEntry(symbol='LANC',
                  data_space=DataEntry.DataSpace.STOCK_DATA,
                  data_type=DataType.Enum.VOLUME,
                  value=105344.0,
                  timestamp=time_util.from_time(time.FromUnixSeconds(1234567))),
        DataEntry(symbol='LANC',
                  data_space=DataEntry.DataSpace.STOCK_DATA,
                  data_type=DataType.Enum.VOLUME,
                  value=134612.0,
                  timestamp=time_util.from_time(time.FromUnixSeconds(2345678))),
    ]


class BeamMongoUtilTest(absltest.TestCase):

    def setUp(self):
        self._client = pymongo.MongoClient(_TEST_URI)

    def tearDown(self):
        self._client[_TEST_DB].drop_collection(_TEST_COLL)

    def test_beam_mongodb_write_and_read(self):
        with TestPipeline() as p:
            write_option = mongo_util.MongoWriteOption(uri=_TEST_URI,
                                                       db=_TEST_DB,
                                                       coll=_TEST_COLL)
            (p \
              | beam.Create(get_data_entries()) \
              | mongo_util.WriteDataToMongoDB(write_option))

        with TestPipeline() as p:
            read_option = mongo_util.MongoReadOption(uri=_TEST_URI,
                                                     db=_TEST_DB,
                                                     coll=_TEST_COLL)
            out = (p | mongo_util.ReadDataFromMongoDB(read_option))
            assert_that(out, equal_to(get_data_entries()))

    def test_beam_mongodb_read_filter(self):
        with TestPipeline() as p:
            write_option = mongo_util.MongoWriteOption(uri=_TEST_URI,
                                                       db=_TEST_DB,
                                                       coll=_TEST_COLL)
            (p \
                | beam.Create(get_data_entries())
                | mongo_util.WriteDataToMongoDB(write_option))

        read_filter = {'value': 134612.0}
        with TestPipeline() as p:
            read_option = mongo_util.MongoReadOption(uri=_TEST_URI,
                                                     db=_TEST_DB,
                                                     coll=_TEST_COLL,
                                                     filter=read_filter)
            out = (p | mongo_util.ReadDataFromMongoDB(read_option))
            assert_that(out, equal_to(get_data_entries()[1:]))


if __name__ == '__main__':
    absltest.main()
