from abc import ABC, abstractmethod
from typing import List

from xlab.trading.order import Order


class TradingSystem(ABC):
    @abstractmethod
    def generate_orders(self) -> List[Order]:
        pass

    @abstractmethod
    def maybe_init_position(self, symbol: str):
        pass

    @abstractmethod
    def maybe_increase_position(self, symbol: str):
        pass

    @abstractmethod
    def maybe_stop_loss(self, symbol: str):
        pass

    @abstractmethod
    def maybe_take_profit(self, symbol: str):
        pass
