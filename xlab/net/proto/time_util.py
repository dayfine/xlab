from xlab.base import time
from google.protobuf import timestamp_pb2


def to_time(pb: timestamp_pb2.Timestamp) -> time.Time:
    return time.FromUnixNanos(pb.ToNanoseconds())


def from_time(t: time.Time) -> timestamp_pb2.Timestamp:
    pb = timestamp_pb2.Timestamp()
    pb.FromNanoseconds(time.ToUnixNanos(t))
    return pb
