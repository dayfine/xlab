from dataclasses import dataclass

from xlab.trading.enums import TradeSide


@dataclass
class Trade:
    symbol: str
    side: TradeSide
    price: float
    size: int
    timestamp: datetime.datetime
