from typing import Any, Callable, Dict

from xlab.base import time
from xlab.data.importer.iex.api import base
from xlab.data.importer.iex.api import util


class IexBatchApi:

    def __init__(self, token: str = ''):
        self._client = base.SimpleIexApiHttpClient(token, 'stock/market/batch',
                                                   _get_parmas)

    def get_batch_quotes(
        self,
        symbol: str,
        start_date: time.CivilTime,
        end_date: time.CivilTime,
    ):
        results = self._client.call(symbol, start_date, end_date)
        results[symbol]['chart'] = self._filter_only_requested_dates(
            results[symbol]['chart'], start_date, end_date)
        return results

    def _filter_only_requested_dates(self, all_results,
                                     start_date: time.CivilTime,
                                     end_date: time.CivilTime):
        results = []
        for result in all_results:
            date = time.ParseCivilTime(result['date'])
            if not (start_date <= date and date <= end_date):
                continue
            results.append(result)
        return results


def _get_parmas(
    symbol: str,
    start_date: time.CivilTime,
    end_date: time.CivilTime,
) -> base.RequestParams:
    return {
        'symbols': ','.join([symbol]),
        'types': ','.join(['quote', 'chart']),
        'range': util._get_shortest_historical_ranges(start_date),
        'chartCloseOnly': True,
    }
