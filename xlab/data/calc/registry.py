import functools

from xlab.data import calc
from xlab.data.calc.producers import factories
from xlab.data.proto import data_type_pb2
from xlab.util.status import errors


@functools.lru_cache(maxsize=None)
def get_calc_producer(
        calc_type: data_type_pb2.DataType.Enum) -> calc.CalcProducer:
    try:
        return factories._FACTORIES[calc_type]()
    except KeyError:
        raise errors.NotFoundError('No available calc factory for {}'.format(
            data_type_pb2.DataType.Enum.Name(calc_type)))
