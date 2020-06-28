from abc import ABC, abstractmethod
from typing import List

from xlab.trading.proto import order_pb2


class TradingSystem(ABC):

    @abstractmethod
    def generate_orders(self) -> List[order_pb2.Order]:
        pass
