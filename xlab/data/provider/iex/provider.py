import datetime as dt

from typing import Dict, List

from xlab.data.proto import data_entry_pb2
from xlab.data.provider import interface
from xlab.data.provider.iex import api


class IexDataProvider(interface.DataProvider):
    def __init__(self, iex_client: api.IexApiHttpClient):
        self._iex_client = iex_client

    # TODO: map to canonical error space.
    def get_data(
        self,
        symbol: str,
        start_date: dt.date = dt.date.today(),
        end_date: dt.date = dt.date.today()
    ) -> Dict[str, List[data_entry_pb2.DataEntry]]:
        # TODO: handle dates properly.
        if end_date != dt.date.today():
            pass
        api_response = self._iex_client.get_batch_quotes(symbol)
        chart_series = api_response.json()[symbol]['chart']

        now = dt.datetime.now()
        close_results = []
        volume_results = []
        for chart_data in chart_series:
            data_date = dt.datetime.strptime(chart_data['date'], '%Y-%m-%d')

            close_data = self._make_data_base(symbol, data_date, now)
            close_data.data_type = 'close'
            close_data.value = chart_data['close']
            close_results.append(close_data)

            volume_data = self._make_data_base(symbol, data_date, now)
            volume_data.data_type = 'volume'
            volume_data.value = chart_data['volume']
            volume_results.append(volume_data)

        return {'close': close_results, 'volume': volume_results}

    def _make_data_base(self, symbol: str, data_date: dt.datetime,
                        now: dt.datetime) -> data_entry_pb2.DataEntry:
        data_entry = data_entry_pb2.DataEntry()
        data_entry.symbol = symbol
        data_entry.data_space = data_entry_pb2.DataEntry.STOCK_DATA
        data_entry.timestamp.FromDatetime(data_date)
        data_entry.updated_at.FromDatetime(now)
        return data_entry
