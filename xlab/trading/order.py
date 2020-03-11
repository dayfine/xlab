from dataclasses import dataclass

from xlab.trading.enums import TradeSide


@dataclass
class Order:
    symbol: str
    side: TradeSide
    price: float
    size: int
