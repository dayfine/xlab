import datetime
import numpy as np

from typing import Dict, List

from xlab.data.proto import data_entry_pb2, data_type_pb2
from xlab.data import importer
from xlab.data.importer.iex import api


class IexDataImporter(importer.DataImporter):

    def __init__(self, iex_client: api.IexApiHttpClient = api.IexApiHttpClient()):
        self._iex_client = iex_client

    # TODO: map to canonical error space.
    def get_data(
        self,
        symbol: str,
        start_date: datetime.date,
        end_date: datetime.date
    ) -> Dict[str, List[data_entry_pb2.DataEntry]]:
        # TODO: handle dates properly.
        date_range = self._get_date_range(start_date, end_date)
        data = self._iex_client.get_batch_quotes(symbol, date_range, start_date)

        now = datetime.datetime.now()
        close_results = []
        volume_results = []
        chart_series = data[symbol]['chart']
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

    def _get_date_range(self, start_date: datetime.datetime, end_date: datetime.datetime):
        '''
        calculate date range by counting no. of days between start and end days
        '''

        date_range = {
            (0, 6): '5d',
            (6, 28): '1m',
            (28, 28*3): '3m',
            (84, 28*6): '6m',
            (168, 365): '1y',
            (365, 365*2): '2y',
            (730, 365*5+1): '5y', # consider 1 leap year
            (1826, 365*15+3): 'max', # consider 3 leap years in 15 years period
        }

        timedelta = (end_date - start_date).days + 1
        timedelta_to_today = (datetime.datetime.now() - start_date).days

        if timedelta < 0:
            raise ValueError('Start date cannot be smaller than end date!')
        elif timedelta_to_today >= 5478:
            raise ValueError('Start date must be within past 15 years!')
        else:
            for key, value in date_range.items():
                if key[0] <= timedelta < key[1]:
                    return value
