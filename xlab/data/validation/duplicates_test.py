import copy

from absl.testing import absltest
from hamcrest import assert_that, equal_to
from google.protobuf import text_format

from xlab.base import time
from xlab.data.proto import data_entry_pb2
from xlab.data.validation import duplicates

_DataEntry = data_entry_pb2.DataEntry


def _as_seconds(ct: time.CivilTime) -> int:
    return time.ToUnixSeconds(time.FromCivil(ct))


def get_data_entry_one():
    return text_format.Parse(
        f"""
        id: "123"
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 290.87
        timestamp {{
            seconds: {_as_seconds(time.CivilTime(2017, 11, 20))}
        }}
        updated_at {{
            seconds: 5555555
        }}
        """, _DataEntry())


def get_data_entry_one_duplicate(duplicate_id):
    return text_format.Parse(
        f"""
        id: "{duplicate_id}"
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 290.87
        timestamp {{
            seconds: {_as_seconds(time.CivilTime(2017, 11, 20))}
        }}
        updated_at {{
            seconds: 5555666
        }}
        """, _DataEntry())


def get_data_entry_two():
    return text_format.Parse(
        f"""
        id: "234"
        data_space: STOCK_DATA
        symbol: "SPY"
        data_type: CLOSE_PRICE
        value: 300.01
        timestamp {{
            seconds: {_as_seconds(time.CivilTime(2017, 11, 21))}
        }}
        updated_at {{
            seconds: 5555555
        }}
        """, _DataEntry())


class DataValiationDuplicatesTestCase(absltest.TestCase):

    def test_find_no_duplicates_for_empty_list(self):
        assert_that(duplicates.find_all_duplicates([]), equal_to(([], {})))

    def test_find_no_duplicates_for_list_of_one_entry(self):
        assert_that(duplicates.find_all_duplicates([get_data_entry_one()]),
                    equal_to(([], {})))

    def test_find_no_duplicates_when_there_is_none(self):
        assert_that(
            duplicates.find_all_duplicates(
                [get_data_entry_one(),
                 get_data_entry_two()]), equal_to(([], {})))

    def test_find_single_duplicate(self):
        assert_that(
            duplicates.find_all_duplicates(
                [get_data_entry_one(),
                 get_data_entry_one_duplicate('124')]), equal_to((['124'], {})))

    def test_find_multiple_duplicates(self):
        assert_that(
            duplicates.find_all_duplicates([
                get_data_entry_one(),
                get_data_entry_one_duplicate('124'),
                get_data_entry_one_duplicate('125')
            ]), equal_to((['124', '125'], {})))

    def test_find_duplicates_with_different_values(self):
        diff_one_a = get_data_entry_one_duplicate('666')
        diff_one_a.value = 1245.67
        diff_one_b = get_data_entry_one_duplicate('777')
        diff_one_b.value = 1245.67

        diff_two = copy.deepcopy(get_data_entry_two())
        diff_two.id = 'abcdefg'
        diff_two.value = 0.9999
        diff_two.updated_at.seconds += 1

        assert_that(
            duplicates.find_all_duplicates([
                get_data_entry_one(),
                get_data_entry_one_duplicate('124'),
                get_data_entry_one_duplicate('125'), diff_one_a, diff_one_b,
                get_data_entry_two(), diff_two
            ]),
            equal_to((['124', '125'], {
                '123': [diff_one_a, diff_one_b],
                '234': [diff_two],
            })))


if __name__ == '__main__':
    absltest.main()
