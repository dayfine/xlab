from xlab.base import time
from google.protobuf import timestamp_pb2


def to_time(pb: timestamp_pb2.Timestamp) -> time.Time:
    return time.FromUnixNanos(pb.ToNanoseconds())


def from_time(t: time.Time) -> timestamp_pb2.Timestamp:
    pb = timestamp_pb2.Timestamp()
    pb.FromNanoseconds(time.ToUnixNanos(t))
    return pb


def to_civil(pb: timestamp_pb2.Timestamp) -> time.CivilTime:
    return time.ToCivil(to_time(pb))


def from_civil(ct: time.CivilTime) -> timestamp_pb2.Timestamp:
    return from_time(time.FromCivil(ct))
