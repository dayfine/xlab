from typing import Generator, List

from absl import logging
import apache_beam as beam
from apache_beam.transforms import ptransform

from xlab.base import time
from xlab.data import calc
from xlab.data.calc import input_util
from xlab.data.calc import registry as calc_registry
from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.util.status import errors

DataEntry = data_entry_pb2.DataEntry
DataType = data_type_pb2.DataType
PCollection = beam.pvalue.PCollection


@ptransform.ptransform_fn
def produce_initial_calc_fn(inputs: PCollection, calc_type: DataType,
                            t: time.Time) -> PCollection:
    calc_producer = calc_registry.get_calc_producer(calc_type)
    inputs_shape = calc_producer.source_inputs_shape(t)
    return _produce_calc_fn(inputs, calc_producer, inputs_shape)


@ptransform.ptransform_fn
def produce_recursive_calc_fn(inputs: PCollection, calc_type: DataType,
                              t: time.Time) -> PCollection:
    calc_producer = calc_registry.get_calc_producer(calc_type)
    inputs_shape = calc_producer.recursive_inputs_shape(t)
    return _produce_calc_fn(inputs, calc_producer, inputs_shape)


# Note this convenience function is not decorated with @ptransform_fn.
def _produce_calc_fn(inputs: PCollection, calc_producer: calc.CalcProducer,
                     inputs_shape: calc.CalcInputs) -> PCollection:
    return (inputs \
        | 'FilterByInputsShape' >> beam.Filter(filter_by_input_shapes,
                                               inputs_shape) \
        | 'WithSymbolAsKey' >> beam.Map(lambda d: (d.symbol, d)) \
        | 'GroupByKey' >> beam.GroupByKey() \
        | 'Values' >> beam.Values() \
        | 'PerformCalc' >> beam.FlatMap(perform_calc, inputs_shape,
                                        calc_producer))


def filter_by_input_shapes(data_entry: DataEntry,
                           inputs_shape: calc.CalcInputs) -> bool:
    return any([
        input_util.is_same_input_shape(data_entry, input_shape)
        for input_shape in inputs_shape
    ])


def perform_calc(
        data_entries: List[DataEntry], inputs_shape: calc.CalcInputs,
        calc_producer: calc.CalcProducer) -> Generator[DataEntry, None, None]:
    try:
        calc_inputs = input_util.sort_to_inputs_shape(data_entries,
                                                      inputs_shape)
        result = calc_producer.calculate(calc_inputs)
        yield result
    except errors.InvalidArgumentError as e:
        logging.error(f'Error when trying to perform calc: {e}')
