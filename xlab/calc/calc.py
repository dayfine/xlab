from abc import ABC, abstractmethod


class CalcProvider(ABC):
    @abstractmethod
    def get_calc(self, symbol: str, day: datetime.date):
        pass
