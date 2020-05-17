from typing import List

from xlab.data.calc import interface as calc
from xlab.data.calc.producers import factories
from xlab.data.proto import data_type_pb2
from xlab.util.status import errors


# Calc types that have their CalcProducer implemented.
def available_calc_types() -> List[int]:  #data_type_pb2.DataType.Enum
    return factories._FACTORIES.keys()


def get_producer_factory(
        calc_type: data_type_pb2.DataType.Enum) -> calc.CalcProducerFactory:
    try:
        return factories._FACTORIES[calc_type]
    except KeyError:
        raise errors.NotFoundError('No available calc factory for {}'.format(
            data_type_pb2.DataType.Enum.Name(calc_type)))
