from absl import app
from absl import flags
from absl import logging

from xlab.data.provider import iex
from xlab.data.provider.iex import api
from xlab.data.store import textproto
from xlab.util.status import errors

FLAGS = flags.FLAGS

flags.DEFINE_string('symbol', None, 'Symbol of the stock to get data for')


class IexSymbolsApi:

    def __init__(self, token: str = ''):
        self._client = api.SimpleIexApiHttpClient(token, 'ref-data/symbols',
                                                  lambda: {})

    def get_symbols(self):
        return self._client.call()


def main(argv):
    del argv  # Unused.

    symbol_api = IexSymbolsApi()
    all_symbols = symbol_api.get_symbols()
    logging.info('Got [%d] symbols', len(all_symbols))
    logging.info('First symbol: [%s]', all_symbols[0])

    iex_provider = iex.IexDataProvider()
    text_data_store = textproto.TextProtoDataStore(
        FLAGS.textproto_store_directory)

    for symbol_dict in all_symbols:
        symbol = symbol_dict['symbol']
        results = iex_provider.get_data(symbol)
        for data_type, data_entry_list in results.items():
            logging.info('%d items fetched for [%s|%s]', len(data_entry_list),
                         symbol, data_type)
            for data_entry in data_entry_list:
                try:
                    text_data_store.add(data_entry, maybe_commit=False)
                except errors.AlreadyExistsError:
                    continue
            text_data_store.commit(unload_afterwards=True)


if __name__ == '__main__':
    app.run(main)
