from xlab.base import time
from xlab.data.importer.iex.api import base
from xlab.data.importer.iex.api import util


class IexHistoricalPriceApi:
    """See API Doc at https://iexcloud.io/docs/api/#historical-prices."""

    def __init__(self, token: str = ''):
        self._client = base.SimpleIexApiHttpClient(token, _get_endpoint_url,
                                                   _get_params)

    def get_historical_price(self, symbol: str, date: time.CivilTime):
        return self._client.call(symbol, date)


def _get_endpoint_url(symbol: str, date: time.CivilTime) -> str:
    return f'/stock/{symbol}/chart/date/{util._to_iex_api_date(date)}'


def _get_params(symbol: str, date: time.CivilTime) -> base.RequestParams:
    return {
        'chartByDay': True,
        'chartCloseOnly': True,
    }
