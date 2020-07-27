from typing import Any, Callable, Dict

from xlab.base import time
from xlab.data.importer.iex.api import base


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
        return self._client.call(symbol, start_date, end_date)


def _get_parmas(
    symbol: str,
    start_date: time.CivilTime,
    end_date: time.CivilTime,
) -> base.RequestParams:
    return {
        'symbols': ','.join([symbol]),
        'types': ','.join(['quote', 'chart']),
        'range': '6m',
        'chartCloseOnly': True,
    }
