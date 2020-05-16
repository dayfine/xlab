import datetime
import json
from unittest.mock import patch, Mock

from absl.testing import absltest
import requests
from requests import exceptions as request_exceptions

from xlab.data.proto import data_type_pb2
from xlab.data.importer.iex import api, importer
from xlab.net.proto.testing import compare


def _make_response(conent: str,
                   status_code: int,
                   reason: str = None) -> requests.Response:
    response = requests.Response()
    response._content = conent.encode()
    response.status_code = status_code
    response.reason = reason
    return response


class IexDataImporterTest(absltest.TestCase):

    def setUp(self):
        self.importer = importer.IexDataImporter(
            api.IexApiHttpClient('fake_token'))

    @patch.object(importer, 'datetime', Mock(wraps=datetime))
    @patch('requests.Session.get')
    def test_get_quotes_success(self, mock_get):
        api_response_data = """{
          "SPY": {
            "chart": [
              {"date":"2020-03-02","close":319.69,"volume":242964067,"change":0,"changePercent":0,"changeOverTime":0},
              {"date":"2020-03-03","close":308.48,"volume":300862938,"change":-9.12,"changePercent":-2.9921,"changeOverTime":-0.029457}
            ]
          }
        }"""

        mock_get.return_value = _make_response(api_response_data, 200)
        importer.datetime.datetime.now.return_value = datetime.datetime(
            2020, 12, 31)

        results = self.importer.get_data('SPY')

        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params']['symbols'], 'SPY')

        close_data = results[data_type_pb2.DataType.CLOSE_PRICE]
        self.assertEqual(len(close_data), 2)
        compare.assertProtoEqual(
            self, close_data[0], """
            symbol: "SPY"
            data_space: STOCK_DATA
            data_type: CLOSE_PRICE
            value: 319.69
            timestamp { seconds: 1583107200 }
            updated_at { seconds: 1609372800 }""")
        compare.assertProtoEqual(
            self, close_data[1], """
            symbol: "SPY"
            data_space: STOCK_DATA
            data_type: CLOSE_PRICE
            value: 308.48
            timestamp { seconds: 1583193600 }
            updated_at { seconds: 1609372800 }""")

        volume_data = results[data_type_pb2.DataType.VOLUME]
        self.assertEqual(len(volume_data), 2)
        compare.assertProtoEqual(
            self, volume_data[0], """
            symbol: "SPY"
            data_space: STOCK_DATA
            data_type: VOLUME
            value: 242964067.0
            timestamp { seconds: 1583107200 }
            updated_at { seconds: 1609372800 }""")
        compare.assertProtoEqual(
            self, volume_data[1], """
            symbol: "SPY"
            data_space: STOCK_DATA
            data_type: VOLUME
            value: 300862938.0
            timestamp { seconds: 1583193600 }
            updated_at { seconds: 1609372800 }""")

    def test_get_quotes_default_single_day(self):
        pass

    def test_get_quotes_default_end_date(self):
        pass

    @patch.object(importer, 'datetime', Mock(wraps=datetime))
    @patch('requests.Session.get')
    def test_get_quotes_backend_failure(self, mock_get):
        mock_get.return_value = _make_response('', 400, 'Invalid argument!')
        importer.datetime.datetime.now.return_value = datetime.datetime(
            2020, 12, 31)

        with self.assertRaisesRegex(request_exceptions.HTTPError,
                                    '400 Client Error: Invalid argument'):
            self.importer.get_data('SPY')

    def test_get_quotes_invalid_dates(self):
        pass

    def test_get_quotes_empty_symbol(self):
        pass


if __name__ == '__main__':
    absltest.main()
