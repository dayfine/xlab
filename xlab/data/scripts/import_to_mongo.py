import glob

from absl import app
from absl import flags
from absl import logging
from google.protobuf import text_format

from xlab.data.proto import data_entry_pb2
from xlab.data.store import mongo
from xlab.util.status import errors

FLAGS = flags.FLAGS

# Use like: bazel run //xlab/data/scripts:import_to_mongo -- --project_root="$(pwd)"
flags.DEFINE_string('project_root', '', '')


def main(argv):
    del argv  # Unused.

    mongo_data_store = mongo.MongoDataStore()

    pattern = FLAGS.project_root + '/data/store/STOCK_DATA/*/*.textproto'
    logging.info(f'Matching for {pattern}...')
    files = glob.glob(pattern)
    logging.info(f'{len(files)} files matched')

    for path in glob.glob(pattern):
        try:
            logging.info(f'Opening {path}')
            with open(path, 'r') as f:
                data_entries = data_entry_pb2.DataEntries()
                text_format.Merge(f.read(), data_entries)

                logging.info(f'Importiong {path}')
                mongo_data_store.batch_add(data_entries)

        except BaseException as e:
            logging.warning(f'Error encountered: {e}',)


if __name__ == '__main__':
    app.run(main)
