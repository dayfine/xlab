import os

from typing import Any, Callable, Dict

from xlab.net.http import requests


class SimpleIexApiHttpClient:

    _API_URL = 'https://cloud.iexapis.com/stable/'

    def __init__(self,
                 token: str = '',
                 endpoint_url: str = '',
                 param_builder: Callable[..., Dict[str, Any]] = None):
        self._session = requests.requests_retry_session()
        self._token = token or os.getenv('IEX_API_SECRET_TOKEN')
        self._endpoint_url = endpoint_url
        self._param_builder = param_builder

    def call(self, *args, **kwargs):
        params = self._param_builder(*args, **kwargs)
        params['token'] = self._token
        url = self._API_URL + self._endpoint_url
        response = self._session.get(url=url, params=params)
        # Raise if code is not 200.
        response.raise_for_status()
        return response.json()


class IexApiHttpClient:

    def __init__(self, token: str = ''):
        get_parmas: Callable[[str], Dict[str, Any]] = lambda symbol: {
            'symbols': ','.join([symbol]),
            'types': ','.join(['quote', 'chart']),
            'range': '6m',
            'chartCloseOnly': True,
        }

        self._client = SimpleIexApiHttpClient(token, 'stock/market/batch',
                                              get_parmas)

    def get_batch_quotes(self, symbol: str):
        return self._client.call(symbol)
