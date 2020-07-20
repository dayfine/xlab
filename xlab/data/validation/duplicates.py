import collections
from typing import Dict, List, Tuple

from xlab.data.proto import data_entry_pb2
from xlab.data.proto import data_type_pb2
from xlab.net.proto import time_util
from xlab.trading.dates import trading_days

_DataEntry = data_entry_pb2.DataEntry


def find_all_duplicates(
    data_entry_list: List[_DataEntry]
) -> Tuple[List[str], Dict[str, List[_DataEntry]]]:
    """Find all duplicate data in a given list of data entries.

    Args:
        data_entry_list: A list of data entries for the same security and of
          the same data type.

    Returns:
        A tuple of two values:
          safe_to_delete_duplicate_ids: IDs of all duplicate data entry that are
            safe to delete, i.e. have the same value of the authentic entries.
            The IDs of the authentic values are not included, and older values
            are assumed to be authentic.
          duplicates_with_different_values: a mapping where the key is the id of
            the authentic ids, and the value is all its duplicates that have a
            different value with the authentic ones. This allow returning all
            data candidates for further inspection, to determine which value
            should be kept as the authentic one.
    """
    safe_to_delete_duplicate_ids = []
    duplicates_with_different_values = collections.defaultdict(list)
    if len(data_entry_list) < 1:
        return safe_to_delete_duplicate_ids, duplicates_with_different_values

    data_entry_list.sort(key=lambda x: (time_util.to_civil(x.timestamp),
                                        time_util.to_civil(x.updated_at)))
    seen_data = {}
    expected_trading_day = time_util.to_civil(data_entry_list[0].timestamp)
    for data in data_entry_list:
        ct = time_util.to_civil(data.timestamp)

        seen = seen_data.get(ct)
        if seen:
            if data.value == seen.value:
                safe_to_delete_duplicate_ids.append(data.id)
            else:
                duplicates_with_different_values[seen.id].append(data)
            continue

        if ct != expected_trading_day:
            raise ValueError(
                f'Time error: expected({expected_trading_day}) got({ct}) while checking {data}')

        seen_data[ct] = data
        expected_trading_day = trading_days.get_next_n(expected_trading_day,
                                                       1)[0]

    return safe_to_delete_duplicate_ids, duplicates_with_different_values
