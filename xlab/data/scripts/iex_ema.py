from absl import app
from absl import flags
from absl import logging

from xlab.data.providers import iex

FLAGS = flags.FLAGS

flags.DEFINE_string('symbol', None, 'Symbol of the stock to get data for')


def main(argv):
    del argv  # Unused.

    logging.info(f'symbol is {FLAGS.symbol}')
    iex_client = iex.IexDataProvider()
    response = iex_client.get_quotes(FLAGS.symbol)
    print(response.json())


if __name__ == '__main__':
    app.run(main)
