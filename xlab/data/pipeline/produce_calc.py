import datetime

from absl import app
from absl import flags
from absl import logging
import apache_beam as beam

from xlab.base import time
from xlab.data.pipeline import mongo_util
from xlab.data.pipeline import produce_calc_fn
from xlab.data.proto import data_type_pb2

DataType = data_type_pb2.DataType
FLAGS = flags.FLAGS

flags.DEFINE_string('date', None,
                    'For which date to perform the calc, in YYYY-MM-DD format')
flags.DEFINE_bool('recursive_calc', False,
                  'Whether to perform the calc recursively')
flags.DEFINE_string('calc_type', None,
                    'Name of the calc type (DataType.Enum) to perform')


def main(argv):
    del argv  # Unused.

    MONGO_URI = 'mongodb://localhost:27017'
    DB = 'xlab'
    COLL = 'data_entries'

    read_option = mongo_util.MongoReadOption(uri=MONGO_URI, db=DB, coll=COLL)
    write_option = mongo_util.MongoWriteOption(uri=MONGO_URI, db=DB, coll=COLL)

    t = time.FromDatetime(datetime.datetime.strptime(FLAGS.date, '%Y-%m-%d'))
    calc_type = DataType.Enum.Value(FLAGS.calc_type)
    calc_fn = get_calc_fn(FLAGS.recursive_calc, calc_type, t)
    with beam.Pipeline() as p:
        (
          p \
          | mongo_util.ReadDataFromMongoDB(read_option)
          | "ProduceCalcs" >> calc_fn \
          | mongo_util.WriteDataToMongoDB(write_option)
        )


if __name__ == '__main__':
    app.run(main)
