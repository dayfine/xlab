from google.protobuf import text_format
from google.protobuf.message import Message


def parse_text_proto(T, text: str):
    assert (issubclass(T, Message))
    msg = T()
    text_format.Merge(text, msg)
    return msg
