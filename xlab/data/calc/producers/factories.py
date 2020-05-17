from xlab.data.calc.producers import ema
from xlab.data.proto import data_type_pb2

_FACTORIES = {
    data_type_pb2.DataType.EMA_20D: ema.make_ema_20d_producer,
    data_type_pb2.DataType.EMA_50D: ema.make_ema_50d_producer,
    data_type_pb2.DataType.EMA_150D: ema.make_ema_150d_producer,
}
