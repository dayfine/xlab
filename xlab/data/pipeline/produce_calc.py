import datetime

from absl import app
from absl import flags
from absl import logging
import apache_beam as beam

from xlab.base import time
from xlab.data.calc import registry as calc_registry
from xlab.data.pipeline import mongo_util
from xlab.data.pipeline import produce_calc_fn
from xlab.data.proto import data_type_pb2
from xlab.net.proto import time_util
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

    calc_type = DataType.Enum.Value(FLAGS.calc_type)
    calc_producer = calc_registry.get_calc_producer(calc_type)
    inputs_shape = calc_producer.recursive_inputs_shape(
        t) if FLAGS.recursive_calc else calc_producer.source_inputs_shape(t)

    mongo_read_filter = {
        'timestamp': {
            '$gte': time_util.to_civl(inputs_shape[0].timestamp),
            '$lte': time_util.to_civl(inputs_shape[-1].timestamp)
        }
    }

    with beam.Pipeline() as p:
        (
          p \
          | mongo_util.ReadDataFromMongoDB(
              mongo_util.default_read_option(mongo_read_filter))
          | "ProduceCalcs" >> produce_calc_fn.produce_calc_fn(
              calc_producer, inputs_shape) \
          | mongo_util.WriteDataToMongoDB(mongo_util.default_write_option())
        )


if __name__ == '__main__':
    app.run(main)
