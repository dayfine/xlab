from datetime import date
import os

from absl import logging

from xlab.data.provider import DataProvider
from xlab.net.http import requests


class IexDataProvider(DataProvider):

    API_URL = 'https://cloud.iexapis.com/stable/'

    def __init__(self):
        self.session = requests.requests_retry_session()
        self.token = os.getenv('IEX_API_SECRET_TOKEN')

    def get_quotes(self,
                   symbol: str,
                   start_date: date = date.today(),
                   end_date: date = date.today()):
        if end_date != date.today():
            pass
        return self.get_batch_quotes(symbol)

    @property
    def batch_url(self):
        return 'stock/market/batch'

    def get_params(self, symbol: str):
        return {
            'symbols': ','.join([symbol]),
            'types': ','.join(['quote', 'chart']),
            'range': '6m',
            'chartCloseOnly': True,
        }

    def get_batch_quotes(self, symbol):
        url = self.API_URL + self.batch_url
        params = self.get_params(symbol)
        params['token'] = self.token

        response = self.session.get(url=url, params=params)
        logging.info(f'REQUEST: {response.request.url}')
        logging.info(f'RESPONSE: {response.status_code}')
        # if response.status_code == requests.codes.ok:
        #     return response
        return response
