from typing import Generator, Iterable

from absl import logging
import apache_beam as beam
from apache_beam.transforms import ptransform

from xlab.data.proto import data_entry_pb2
from xlab.data.validation import duplicates

_DataEntry = data_entry_pb2.DataEntry
_DoOutputsTuple = beam.pvalue.DoOutputsTuple
_PCollection = beam.pvalue.PCollection
_TaggedOutput = beam.pvalue.TaggedOutput


@ptransform.ptransform_fn
def find_duplicates_fn(inputs: _PCollection) -> _DoOutputsTuple:
    return (inputs \
        | 'WithSymbolAndDataTypeAsKey' >>
            beam.Map(lambda d: ((d.symbol, d.data_type), d)) \
        | 'GroupByKey' >> beam.GroupByKey() \
        | 'Values' >> beam.Values() \
        | "FindDuplicates" >> beam.FlatMap(find_duplicates).with_outputs(
            'duplicates_with_different_values',
            main='safe_to_delete_duplicate_ids'))


def find_duplicates(data_entries: Iterable[_DataEntry]):
    try:
        safe_to_delete_duplicate_ids, duplicates_with_different_values = \
            duplicates.find_all_duplicates(data_entries)
        if safe_to_delete_duplicate_ids:
            yield safe_to_delete_duplicate_ids
        if duplicates_with_different_values:
            yield _TaggedOutput('duplicates_with_different_values',
                                duplicates_with_different_values)
    except Exception as e:
        logging.error(f'Error when trying to produce duplicates: {e}')
