from typing import List

from xlab.system.interface import TradingSystem
from xlab.trading.order import Order


class BasicTurtleSystem(TradingSystem):
    def __init__(self):
        pass

    def generate_orders(self) -> List[Order]:
        pass

    def maybe_init_position(self, symbol: str):
        pass

    def maybe_increase_position(self, symbol: str):
        pass

    def maybe_stop_loss(self, symbol: str):
        pass

    def maybe_take_profit(self, symbol: str):
        pass

    def should_buy(self, parameter_list):
        current_price
        pass
