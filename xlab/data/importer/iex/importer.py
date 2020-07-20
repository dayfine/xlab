from typing import Dict, List, Optional

from xlab.base import time
from xlab.data.proto import data_entry_pb2, data_type_pb2
from xlab.data import importer
from xlab.data.importer.iex import api
from xlab.net.proto import time_util
from xlab.util.status import errors

_DATA_TYPE_MAP = {

}

class IexDataImporter(importer.DataImporter):

    def __init__(self,
                 iex_client: api.IexApiHttpClient = api.IexApiHttpClient()):
        self._iex_client = iex_client

    def get_data(
        self,
        symbol: str,
        start_date: Optional[time.CivilTime] = None,
        end_date: Optional[time.CivilTime] = None,
    ) -> Dict[str, List[data_entry_pb2.DataEntry]]:
        if not end_date:
            end_date = time.ToCivil(time.Now())
        if not start_date:
            start_date = end_date
        if start_date > end_date:
            raise errors.InvalidArgumentError(
                f'start_date {start_date} is later than end_date {end_date}')

        data = self._iex_client.get_batch_quotes(symbol)
        chart_series = data[symbol]['chart']

        now = time.Now()
        close_results = []
        volume_results = []
        for chart_data in chart_series:
            data_date = time.ParseCivilTime(chart_data['date'])

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

    def _make_data_base(self, symbol: str, data_date: time.CivilTime,
                        now: time.time) -> data_entry_pb2.DataEntry:
        data_entry = data_entry_pb2.DataEntry()
        data_entry.symbol = symbol
        data_entry.data_space = data_entry_pb2.DataEntry.STOCK_DATA
        data_entry.timestamp.CopyFrom(time_util.from_civil(data_date))
        data_entry.updated_at.CopyFrom(time_util.from_time(now))
        return data_entry
