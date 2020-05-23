from typing import Dict

from xlab.data import calc
from xlab.data.calc.producers import ema
from xlab.data.proto.data_type_pb2 import DataType

_FACTORIES: Dict[int, calc.CalcProducerFactory] = {
    DataType.EMA_20D: ema.make_ema_20d_producer,
    DataType.EMA_50D: ema.make_ema_50d_producer,
    DataType.EMA_150D: ema.make_ema_150d_producer,
}
