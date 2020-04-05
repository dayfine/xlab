from abc import ABC, abstractmethod
import datetime


class DataProvider(ABC):
    @abstractmethod
    def get_quotes(self, symbol: str, start_date: datetime.date,
                   end_date: datetime.date):
        pass
