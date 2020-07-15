import collections
from typing import Iterable, Callable, List, OrderedDict, TypeVar

T = TypeVar("T")
V = TypeVar("V")


def groupby(iterable: Iterable[T],
            key_fn: Callable[[T], V]) -> OrderedDict[V, List[T]]:
    res = collections.OrderedDict()
    for item in iterable:
        key = key_fn(item)
        res.setdefault(key, []).append(item)
    return res
