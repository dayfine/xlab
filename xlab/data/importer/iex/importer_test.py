import json
from unittest import mock

from xlab.base import time
from absl.testing import absltest
from hamcrest import assert_that, contains
import requests

from proto_matcher import equals_proto

from xlab.data.proto import data_type_pb2
from xlab.data.importer.iex import importer
from xlab.data.importer.iex.api import batch
from xlab.util.status import errors


def _make_response(status_code: int,
                   conent: str,
                   reason: str = None) -> requests.Response:
    response = requests.Response()
    response._content = conent.encode()
    response.status_code = status_code
    response.reason = reason
    return response


@mock.patch('xlab.base.time.Now')
@mock.patch('requests.Session.get')
class IexDataImporterTest(absltest.TestCase):

    def setUp(self):
        self.importer = importer.IexDataImporter(
            batch.IexBatchApi('fake_token'))

    def test_get_quotes_success(self, mock_get, mock_now):
        mock_get.return_value = _make_response(
            200, """{
          "SPY": {
            "chart": [
              {"date":"2020-03-05","close":319.69,"volume":242964067,"change":0,"changePercent":0,"changeOverTime":0},
              {"date":"2020-03-06","close":308.48,"volume":300862938,"change":-9.12,"changePercent":-2.9921,"changeOverTime":-0.029457},
              {"date":"2020-03-09","close":301.01,"volume":123123131,"change":-7.47,"changePercent":-2.4216,"changeOverTime":-0.01311}
            ]
          }
        }""")
        mock_now.return_value = time.FromCivil(time.CivilTime(2020, 3, 11))

        results = self.importer.get_data('SPY', time.CivilTime(2020, 3, 5),
                                         time.CivilTime(2020, 3, 7))

        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params']['symbols'], 'SPY')
        self.assertEqual(kwargs['params']['range'], '1m')

        assert_that(
            results[data_type_pb2.DataType.CLOSE_PRICE],
            contains(
                equals_proto(f"""
                    symbol: "SPY"
                    data_space: STOCK_DATA
                    data_type: CLOSE_PRICE
                    value: 319.69
                    timestamp {{ seconds: {time.as_seconds(2020, 3, 5)} }}
                    updated_at {{ seconds: {time.as_seconds(2020, 3, 11)} }}
                """),
                equals_proto(f"""
                    symbol: "SPY"
                    data_space: STOCK_DATA
                    data_type: CLOSE_PRICE
                    value: 308.48
                    timestamp {{ seconds: {time.as_seconds(2020, 3, 6)} }}
                    updated_at {{ seconds: {time.as_seconds(2020, 3, 11)} }}
                """)))

        assert_that(
            results[data_type_pb2.DataType.VOLUME],
            contains(
                equals_proto(f"""
                    symbol: "SPY"
                    data_space: STOCK_DATA
                    data_type: VOLUME
                    value: 242964067.0
                    timestamp {{ seconds: {time.as_seconds(2020, 3, 5)} }}
                    updated_at {{ seconds: {time.as_seconds(2020, 3, 11)} }}
                """),
                equals_proto(f"""
                    symbol: "SPY"
                    data_space: STOCK_DATA
                    data_type: VOLUME
                    value: 300862938.0
                    timestamp {{ seconds: {time.as_seconds(2020, 3, 6)} }}
                    updated_at {{ seconds: {time.as_seconds(2020, 3, 11)} }}
                """)))

    def test_get_quotes_default_single_day(self, mock_get, mock_now):
        mock_get.return_value = _make_response(
            200, """{
          "ABC": {
            "chart": [
              {"date":"2020-03-11","close":300.00,"volume":231231312,"change":-0,"changePercent": 0.0,"changeOverTime":-0.04321}
            ]
          }
        }""")
        mock_now.return_value = time.FromCivil(time.CivilTime(2020, 3, 11))

        results = self.importer.get_data('ABC')

        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params']['symbols'], 'ABC')
        self.assertEqual(kwargs['params']['range'], '5d')

        assert_that(
            results[data_type_pb2.DataType.CLOSE_PRICE],
            contains(
                equals_proto(f"""
                    symbol: "ABC"
                    data_space: STOCK_DATA
                    data_type: CLOSE_PRICE
                    value: 300.00
                    timestamp {{ seconds: {time.as_seconds(2020, 3, 11)} }}
                    updated_at {{ seconds: {time.as_seconds(2020, 3, 11)} }}
                """)))

        assert_that(
            results[data_type_pb2.DataType.VOLUME],
            contains(
                equals_proto(f"""
                    symbol: "ABC"
                    data_space: STOCK_DATA
                    data_type: VOLUME
                    value: 231231312.0
                    timestamp {{ seconds: {time.as_seconds(2020, 3, 11)} }}
                    updated_at {{ seconds: {time.as_seconds(2020, 3, 11)} }}
                """)))

    def test_get_quotes_default_end_date(self, mock_get, mock_now):
        mock_get.return_value = _make_response(
            200, """{
          "SPY": {
            "chart": [
              {"date":"2020-03-05","close":319.69,"volume":242964067,"change":0,"changePercent":0,"changeOverTime":0},
              {"date":"2020-03-06","close":308.48,"volume":300862938,"change":-9.12,"changePercent":-2.9921,"changeOverTime":-0.029457}
            ]
          }
        }""")
        mock_now.return_value = time.FromCivil(time.CivilTime(2020, 3, 7))

        results = self.importer.get_data('SPY', time.CivilTime(2020, 3, 5))

        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params']['symbols'], 'SPY')
        self.assertEqual(kwargs['params']['range'], '5d')

        assert_that(
            results[data_type_pb2.DataType.CLOSE_PRICE],
            contains(
                equals_proto(f"""
                    symbol: "SPY"
                    data_space: STOCK_DATA
                    data_type: CLOSE_PRICE
                    value: 319.69
                    timestamp {{ seconds: {time.as_seconds(2020, 3, 5)} }}
                    updated_at {{ seconds: {time.as_seconds(2020, 3, 7)} }}
                """),
                equals_proto(f"""
                    symbol: "SPY"
                    data_space: STOCK_DATA
                    data_type: CLOSE_PRICE
                    value: 308.48
                    timestamp {{ seconds: {time.as_seconds(2020, 3, 6)} }}
                    updated_at {{ seconds: {time.as_seconds(2020, 3, 7)} }}
                """)))

        assert_that(
            results[data_type_pb2.DataType.VOLUME],
            contains(
                equals_proto(f"""
                    symbol: "SPY"
                    data_space: STOCK_DATA
                    data_type: VOLUME
                    value: 242964067.0
                    timestamp {{ seconds: {time.as_seconds(2020, 3, 5)} }}
                    updated_at {{ seconds: {time.as_seconds(2020, 3, 7)} }}
                """),
                equals_proto(f"""
                    symbol: "SPY"
                    data_space: STOCK_DATA
                    data_type: VOLUME
                    value: 300862938.0
                    timestamp {{ seconds: {time.as_seconds(2020, 3, 6)} }}
                    updated_at {{ seconds: {time.as_seconds(2020, 3, 7)} }}
                """)))

    def test_get_quotes_backend_failure(self, mock_get, mock_now):
        mock_get.return_value = _make_response(501, '', 'Server Unavailable')
        mock_now.return_value = time.FromCivil(time.CivilTime(2020, 12, 31))

        with self.assertRaisesRegex(errors.InternalError,
                                    '501 Server Error: Server Unavailable'):
            self.importer.get_data('SPY')

    def test_get_quotes_invalid_dates(self, mock_get, mock_now):
        mock_now.return_value = time.FromCivil(time.CivilTime(2020, 12, 31))
        with self.assertRaisesRegex(
                errors.InvalidArgumentError,
                'end_date 2021-01-01T00:00:00 must be in the past'):
            self.importer.get_data('SPY', end_date=time.CivilTime(2021, 1, 1))

    def test_get_quotes_empty_symbol(self, mock_get, mock_now):
        with self.assertRaisesRegex(errors.InvalidArgumentError,
                                    'Symbol not specified'):
            self.importer.get_data('')


if __name__ == '__main__':
    absltest.main()
