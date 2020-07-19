from typing import Iterable

from absl import app
from absl import flags
from absl import logging
import apache_beam as beam

from xlab.data.store.mongo import admin
from xlab.data.pipeline import mongo_util
from xlab.data.pipeline import find_duplicates_fn

FLAGS = flags.FLAGS

# Use like: bazel run //xlab/data/scripts:import_to_mongo -- --project_root="$(pwd)"
flags.DEFINE_string('project_root', '', '')


def delete_duplicates(ids: Iterable[str]):
    delete_result = admin.delete_by_ids(list(ids))
    yield delete_result.deleted_count


def run():
    with beam.Pipeline() as p:
        safe_to_delete_duplicate_ids, duplicates_with_different_values = (p \
            | mongo_util.ReadDataFromMongoDB(
                mongo_util.default_read_option())
            | 'FindDuplicates' >> find_duplicates_fn.find_duplicates_fn())

        (safe_to_delete_duplicate_ids \
            | beam.FlatMap(delete_duplicates) \
            | beam.CombineGlobally(sum) \
            | beam.FlatMap(lambda totol_deleted: logging.info(
                f'{totol_deleted} entries deleted')))

        duplicates_with_different_values | "write_unsafe_duplicates" >> beam.io.WriteToText(
            FLAGS.project_root + '/data/beam/unsafe_to_delete_duplicates.txt')


def main(argv):
    del argv  # Unused.

    logging.get_absl_handler().use_absl_log_file(log_dir='/tmp/')

    out = run()


if __name__ == '__main__':
    app.run(main)
