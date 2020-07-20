from typing import Dict, List, Optional

from xlab.base import time
from xlab.data.proto import data_entry_pb2, data_type_pb2
from xlab.data import importer
from xlab.data.importer.iex.api import batch
from xlab.net.proto import time_util
from xlab.util.status import errors

_DataType = data_type_pb2.DataType
_DataEntry = data_entry_pb2.DataEntry

# A map of data types to their data fields on IEX Chart API's response.
_DATA_TYPE_TO_CHART_FIELD_MAP = {
    _DataType.CLOSE_PRICE: 'close',
    _DataType.VOLUME: 'volume',
}


class IexDataImporter(importer.DataImporter):

    def __init__(self, batch_api: batch.IexBatchApi = batch.IexBatchApi()):
        self._batch_api = batch_api

    def get_data(
        self,
        symbol: str,
        start_date: Optional[time.CivilTime] = None,
        end_date: Optional[time.CivilTime] = None,
    ) -> Dict[int, List[_DataEntry]]:
        if not end_date:
            end_date = time.ToCivil(time.Now())
        if not start_date:
            start_date = end_date
        if start_date > end_date:
            raise errors.InvalidArgumentError(
                f'start_date {start_date} is later than end_date {end_date}')

        data = self._batch_api.get_batch_quotes(symbol)
        chart_series = data[symbol]['chart']

        now = time.Now()
        data_types_to_import = _DATA_TYPE_TO_CHART_FIELD_MAP.keys()
        results = {data_type: [] for data_type in data_types_to_import}
        for chart_data in chart_series:
            data_date = time.ParseCivilTime(chart_data['date'])

            for data_type in data_types_to_import:
                data = self._make_data_base(symbol, data_date, now)
                data.data_type = data_type
                data.value = chart_data[
                    _DATA_TYPE_TO_CHART_FIELD_MAP[data_type]]
                results[data_type].append(data)

        return results

    def _make_data_base(self, symbol: str, data_date: time.CivilTime,
                        now: time.time) -> _DataEntry:
        data_entry = _DataEntry()
        data_entry.symbol = symbol
        data_entry.data_space = _DataEntry.STOCK_DATA
        data_entry.timestamp.CopyFrom(time_util.from_civil(data_date))
        data_entry.updated_at.CopyFrom(time_util.from_time(now))
        return data_entry
