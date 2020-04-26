import os

from typing import Mapping

from xlab.net.http import requests


class IexApiHttpClient:

    _API_URL = 'https://cloud.iexapis.com/stable/'
    _BATCH_ENDPOINT = 'stock/market/batch'

    def __init__(self, token=''):
        self._session = requests.requests_retry_session()
        self._token = token or os.getenv('IEX_API_SECRET_TOKEN')

    def get_batch_quotes(self, symbol: str):
        params = self._get_params_for_batch_quotes(symbol)
        return self._do_request(self._BATCH_ENDPOINT, params)

    def _get_params_for_batch_quotes(self, symbol: str):
        return {
            'symbols': ','.join([symbol]),
            'types': ','.join(['quote', 'chart']),
            'range': '6m',
            'chartCloseOnly': True,
        }

    def _do_request(self, url: str, params: Mapping[str, str]):
        url = self._API_URL + url
        params['token'] = self._token
        return self._session.get(url=url, params=params)
