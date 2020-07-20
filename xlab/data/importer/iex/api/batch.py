from typing import Any, Callable, Dict

from xlab.data.importer.iex.api import base


class IexBatchApi:

    def __init__(self, token: str = ''):
        get_parmas: Callable[[str], Dict[str, Any]] = lambda symbol: {
            'symbols': ','.join([symbol]),
            'types': ','.join(['quote', 'chart']),
            'range': '6m',
            'chartCloseOnly': True,
        }

        self._client = base.SimpleIexApiHttpClient(token, 'stock/market/batch',
                                                   get_parmas)

    def get_batch_quotes(self, symbol: str):
        return self._client.call(symbol)
