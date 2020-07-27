import os

from typing import Any, Callable, Dict, Union

from requests import exceptions as request_exceptions
from xlab.net.http import requests
from xlab.util.status import errors

RequestParams = Dict[str, Any]


class SimpleIexApiHttpClient:

    _API_URL = 'https://cloud.iexapis.com/stable/'

    def __init__(self, token: str, endpoint_url: Union[str, Callable[..., str]],
                 param_builder: Callable[..., RequestParams]):
        self._session = requests.requests_retry_session()
        self._token = token or os.getenv('IEX_API_SECRET_TOKEN')
        self._endpoint_url_builder = ((lambda *args, **kwargs: endpoint_url) \
            if isinstance(endpoint_url, str) else endpoint_url)
        self._param_builder = param_builder

    def call(self, *args, **kwargs):
        params = self._param_builder(*args, **kwargs)
        params['token'] = self._token
        endpoint_url = self._endpoint_url_builder(*args, **kwargs)
        response = self._session.get(url=self._API_URL + endpoint_url,
                                     params=params)

        try:
            response.raise_for_status()
        except request_exceptions.HTTPError as e:
            if response.status_code >= 500:
                raise errors.InternalError(e)
            raise errors.InvalidArgumentError(e)
        return response.json()
