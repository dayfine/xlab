"""We always start with main"""
from abc import ABC, abstractmethod
from collections import OrderedDict
import datetime


class DataProvider(ABC):
    @abstractmethod
    def get_quote(self, symbol: str, day: datetime.date):
        pass

    def update_position():
        pass


class PortfolioManager(ABC):
    @abstractmethod
    def get_pnl(self):
        pass


class TradingSystem(ABC):
    @abstractmethod
    def maybe_trade(self):
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


class TradeExecutor(ABC):
    @abstractmethod
    def execute(self):
        pass


class RealTimeExecutor(TradeExecutor):
    pass


class EndOfDayExecutor(TradeExecutor):
    pass


class SimulationEodExecutor(EndOfDayExecutor):
    def __init__(self,
                 data_provider: DataProvider = None,
                 portfolio_manager: PortfolioManager = None,
                 trading_system: TradingSystem = None):
        self.data_provider = data_provider
        self.portfolio_manager = portfolio_manager
        self.trading_system = trading_system

    def simulate(end_date: datetime.date, num_days=360):
        daily_pnls = []
        for day in get_date_range(end_date, num_days):
            daily_pnls.append((day, _simulate_day(day)))
        return daily_pnls

    def _simulate_day(date: datetime.date) -> float:
        self.execute()
        return self.portfolio_manager.get_pnl()

    def execute():
        pass


def get_date_range(end_date: datetime.date, num_days: int):
    start_date = end_date - datetime.timedelta(days=num_days)
    return (start_date + datetime.timedelta(days=d)
            for d in range(0, (end_date - start_date).days + 1))
