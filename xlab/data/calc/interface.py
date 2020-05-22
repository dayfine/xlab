import abc
import dataclasses
from typing import Callable, Optional, Sequence, Tuple, Union

from xlab.base import time
from xlab.data.proto.data_entry_pb2 import DataEntry
from xlab.data.proto.data_type_pb2 import DataType

# Recursive inputs consist of the prior period's calc and the current period's
# incremental input.
RecursiveInputs = Tuple[DataEntry, DataEntry]
# Source inputs consist of a series of calcs, which are often consecutive calcs
# of the same type or different types of calcs from the same time period.
SourceInputs = Sequence[DataEntry]
CalcInputs = Union[RecursiveInputs, SourceInputs]


# Specs about the time period of a calc and its inputs.
@dataclasses.dataclass(frozen=True)
class CalcTimeSpecs:
    num_periods: int = 1
    period_length: Optional[time.Duration] = None


class CalcProducer(abc.ABC):

    # What type of calc does this class produce.
    @property
    @abc.abstractmethod
    def calc_type(self) -> DataType.Enum:
        pass

    @property
    @abc.abstractmethod
    def time_spec(self) -> CalcTimeSpecs:
        pass

    # Compute the calc for a given security at a given timestamp.
    @abc.abstractmethod
    def calculate(self, inputs: CalcInputs) -> DataEntry:
        pass

    # List all input shapes that can be used to produce this type of calc.
    # An input shape is a sequence of DataEntry with specific data type,
    # symbol, and timestamps.
    @abc.abstractmethod
    def accepted_inputs_shapes(self, t: time.Time) -> Tuple[CalcInputs, ...]:
        pass


CalcProducerFactory = Callable[..., CalcProducer]
