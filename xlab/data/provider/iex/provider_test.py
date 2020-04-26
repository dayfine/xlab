from datetime import datetime
import json
from unittest.mock import patch, Mock

from absl.testing import absltest
import requests

from xlab.data.provider.iex import api, provider
from xlab.net.proto.testing import compare


def _make_response(conent: str, status_code: int) -> requests.Response:
    response = requests.Response()
    response._content = conent.encode()
    response.status_code = status_code
    return response


class IexDataProviderTest(absltest.TestCase):

    def setUp(self):
        self.provider = provider.IexDataProvider(
            api.IexApiHttpClient('fake_token'))

    @patch.object(provider, 'datetime', Mock(wraps=datetime))
    def test_get_quotes_success(self):
        expected_content = """
          {
            "SPY": {
              "chart": [
                {"date":"2020-03-02","close":319.69,"volume":242964067,"change":0,"changePercent":0,"changeOverTime":0},
                {"date":"2020-03-03","close":308.48,"volume":300862938,"change":-9.12,"changePercent":-2.9921,"changeOverTime":-0.029457}
              ]
            }
          }
        """

        with patch('requests.Session.get',
                   return_value=_make_response(expected_content,
                                               200)) as mock_get:
            provider.datetime.now.return_value = datetime(2020, 12, 31)
            results = self.provider.get_data('SPY')

            _, kwargs = mock_get.call_args
            self.assertEqual(kwargs['params']['symbols'], 'SPY')

            self.assertEqual(len(results['close']), 2)
            compare.assertProtoEqual(
                self, results['close'][0], """
                symbol: "SPY"
                data_space: STOCK_DATA
                data_type: "close"
                value: 319.69
                timestamp { seconds: 1583107200 }
                updated_at { seconds: 1609372800 }""")
            compare.assertProtoEqual(
                self, results['close'][1], """
                symbol: "SPY"
                data_space: STOCK_DATA
                data_type: "close"
                value: 308.48
                timestamp { seconds: 1583193600 }
                updated_at { seconds: 1609372800 }""")

            self.assertEqual(len(results['close']), 2)
            compare.assertProtoEqual(
                self, results['volume'][0], """
                symbol: "SPY"
                data_space: STOCK_DATA
                data_type: "volume"
                value: 242964067.0
                timestamp { seconds: 1583107200 }
                updated_at { seconds: 1609372800 }""")
            compare.assertProtoEqual(
                self, results['volume'][1], """
                symbol: "SPY"
                data_space: STOCK_DATA
                data_type: "volume"
                value: 300862938.0
                timestamp { seconds: 1583193600 }
                updated_at { seconds: 1609372800 }""")

    def test_get_quotes_default_single_day(self):
        pass

    def test_get_quotes_default_end_date(self):
        pass

    def test_get_quotes_backend_failure(self):
        pass

    def test_get_quotes_invalid_dates(self):
        pass

    def test_get_quotes_empty_symbol(self):
        pass


if __name__ == '__main__':
    absltest.main()
