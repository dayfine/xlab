from xlab.data import calc
from xlab.data.calc.producers import factories
from xlab.data.proto import data_type_pb2
from xlab.util.status import errors

def get_factory(
        calc_type: data_type_pb2.DataType.Enum) -> calc.CalcProducerFactory:
    try:
        return factories._FACTORIES[calc_type]
    except KeyError:
        raise errors.NotFoundError('No available calc factory for {}'.format(
            data_type_pb2.DataType.Enum.Name(calc_type)))
