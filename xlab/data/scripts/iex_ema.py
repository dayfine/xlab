from absl import app
from absl import flags
from absl import logging

from xlab.data.provider import iex
from xlab.util.status import errors

FLAGS = flags.FLAGS

flags.DEFINE_string('symbol', None, 'Symbol of the stock to get data for')


def main(argv):
    del argv  # Unused.

    symbol = FLAGS.symbol
    logging.info(f'symbol is {FLAGS.symbol}')
    if not symbol:
        raise errors.InvalidArgumentError('Symbol cannot be empty')

    iex_provider = iex.IexDataProvider()
    results = iex_provider.get_data(symbol)
    logging.info(results)


if __name__ == '__main__':
    app.run(main)
