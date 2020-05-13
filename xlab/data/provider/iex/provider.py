import datetime

from typing import Dict, List

from xlab.data.proto import data_entry_pb2, data_type_pb2
from xlab.data.provider import interface
from xlab.data.provider.iex import api


class IexDataProvider(interface.DataProvider):

    def __init__(self,
                 iex_client: api.IexApiHttpClient = api.IexApiHttpClient()):
        self._iex_client = iex_client

    # TODO: map to canonical error space.
    def get_data(
        self,
        symbol: str,
        start_date: datetime.date = datetime.date.today(),
        end_date: datetime.date = datetime.date.today()
    ) -> Dict[str, List[data_entry_pb2.DataEntry]]:
        # TODO: handle dates properly.
        if end_date != datetime.date.today():
            pass
        data = self._iex_client.get_batch_quotes(symbol)
        chart_series = data[symbol]['chart']

        now = datetime.datetime.now()
        close_results = []
        volume_results = []
        for chart_data in chart_series:
            data_date = datetime.datetime.strptime(chart_data['date'],
                                                   '%Y-%m-%d')

            close_data = self._make_data_base(symbol, data_date, now)
            close_data.data_type = data_type_pb2.DataType.CLOSE_PRICE
            close_data.value = chart_data['close']
            close_results.append(close_data)

            volume_data = self._make_data_base(symbol, data_date, now)
            volume_data.data_type = data_type_pb2.DataType.VOLUME
            volume_data.value = chart_data['volume']
            volume_results.append(volume_data)

        return {
            data_type_pb2.DataType.CLOSE_PRICE: close_results,
            data_type_pb2.DataType.VOLUME: volume_results
        }

    def _make_data_base(self, symbol: str, data_date: datetime.datetime,
                        now: datetime.datetime) -> data_entry_pb2.DataEntry:
        data_entry = data_entry_pb2.DataEntry()
        data_entry.symbol = symbol
        data_entry.data_space = data_entry_pb2.DataEntry.STOCK_DATA
        data_entry.timestamp.FromDatetime(data_date)
        data_entry.updated_at.FromDatetime(now)
        return data_entry
