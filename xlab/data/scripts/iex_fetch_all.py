from absl import app
from absl import flags
from absl import logging

from xlab.base import time
from xlab.data.importer import iex
from xlab.data.importer.iex.api import symbols
from xlab.data.store import mongo
from xlab.util.status import errors

FLAGS = flags.FLAGS

flags.DEFINE_string(
    'start_date', None,
    'Staring from which past date to backfill, in YYYY-MM-DD format')


def main(argv):
    del argv  # Unused.

    symbol_api = symbols.IexSymbolsApi()
    all_symbols = symbol_api.get_symbols()
    logging.info('Got [%d] symbols', len(all_symbols))
    logging.info('First symbol: [%s]', all_symbols[0])

    iex_provider = iex.IexDataImporter()
    store = mongo.MongoDataStore()
    start_date = time.ParseCivilTime(FLAGS.start_date)

    for symbol_dict in all_symbols:
        symbol = symbol_dict['symbol']
        results = iex_provider.get_data(symbol, start_date)
        for data_type, data_entry_list in results.items():
            logging.info('%d items fetched for [%s|%s]', len(data_entry_list),
                         symbol, data_type)
            try:
                store.batch_add(data_entry_list)
            except Exception as e:
                logging.error('Error batch adding: %s', e)
                continue


if __name__ == '__main__':
    app.run(main)
