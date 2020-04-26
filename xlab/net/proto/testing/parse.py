from google.protobuf import text_format
from google.protobuf.message import Message


def parse_test_proto(text: str, T=None):
    assert (issubclass(T, Message))
    proto = T()
    text_format.Merge(text, proto)
    return proto
