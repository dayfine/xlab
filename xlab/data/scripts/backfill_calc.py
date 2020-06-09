"""Backfill a calc to a date in the past by running daily calc sequentially."""
from absl import app
from absl import flags
from absl import logging

from xlab.base import time
from xlab.data.pipeline import produce_calc
from xlab.data.proto import data_type_pb2
from xlab.trading.dates import trading_days

DataType = data_type_pb2.DataType
FLAGS = flags.FLAGS

flags.DEFINE_string(
    'start_date', None,
    'Staring from which past date to backfill, in YYYY-MM-DD format')


def main(argv):
    del argv  # Unused.

    logging.get_absl_handler().use_absl_log_file(log_dir='/tmp/')

    date = time.ParseCivilTime(FLAGS.start_date)

    calc_type = DataType.Enum.Value(FLAGS.calc_type)
    today = time.CivilTime.today().naive()
    while date < today:
        if trading_days.is_trading_day(date):
            print('producing calc for ', time.FormatCivilTime(date))
            logging.info('producing calc for %s', time.FormatCivilTime(date))
            produce_calc.run(date, calc_type, is_recursive_calc=True)
        date = date.add(days=1)


if __name__ == '__main__':
    app.run(main)
