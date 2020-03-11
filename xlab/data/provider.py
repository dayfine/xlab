from abc import ABC, abstractmethod
import datetime


class DataProvider(ABC):
    @abstractmethod
    def get_quote(self, symbol: str, day: datetime.date):
        pass
