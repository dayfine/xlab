from absl import app
from absl import flags
from absl import logging

from xlab.data.importer import iex
from xlab.data.store import textproto
from xlab.util.status import errors

FLAGS = flags.FLAGS

flags.DEFINE_string('symbol', None, 'Symbol of the stock to get data for')


def main(argv):
    del argv  # Unused.

    symbol = FLAGS.symbol
    logging.info(f'symbol is {FLAGS.symbol}')
    if not symbol:
        raise errors.InvalidArgumentError('Symbol cannot be empty')

    iex_provider = iex.IexDataImporter()
    results = iex_provider.get_data(symbol)

    text_data_store = textproto.TextProtoDataStore(
        FLAGS.textproto_store_directory)
    for data_type, data_entry_list in results.items():
        logging.info('%d items fetched for %s', len(data_entry_list), data_type)
        for data_entry in data_entry_list:
            text_data_store.add(data_entry)
    text_data_store.commit()


if __name__ == '__main__':
    app.run(main)
