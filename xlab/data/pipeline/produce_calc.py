import datetime

from absl import app
from absl import flags
from absl import logging
import apache_beam as beam

from xlab.base import time
from xlab.data.pipeline import mongo_util
from xlab.data.pipeline import produce_calc_fn
from xlab.data.proto import data_type_pb2
from xlab.trading.dates import trading_days

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

    day = time.ParseCivilTime(FLAGS.date)
    if not trading_days.is_trading_day(day):
        raise ValueError(f'Date requested {FLAGS.date} is not a trading day')
    t = time.FromCivil(day)

    MONGO_URI = 'mongodb://localhost:27017'
    DB = 'xlab'
    COLL = 'data_entries'

    read_option = mongo_util.MongoReadOption(uri=MONGO_URI, db=DB, coll=COLL)
    write_option = mongo_util.MongoWriteOption(uri=MONGO_URI, db=DB, coll=COLL)

    calc_type = DataType.Enum.Value(FLAGS.calc_type)
    calc_fn = produce_calc_fn.get_calc_fn(FLAGS.recursive_calc, calc_type, t)
    with beam.Pipeline() as p:
        (
          p \
          | mongo_util.ReadDataFromMongoDB(read_option)
          | "ProduceCalcs" >> calc_fn \
          | mongo_util.WriteDataToMongoDB(write_option)
        )


if __name__ == '__main__':
    app.run(main)
