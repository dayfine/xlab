from xlab.base import time
from xlab.util.status import errors


def _to_iex_api_date(date: time.CivilTime):
    return date.format('YYYYMMDD')


def _get_shortest_historical_ranges(start_date: time.CivilTime) -> str:
    """Get the shortest API range string that covers the requested number of
       days for the time period ending today.
       See: https://iexcloud.io/docs/api/#historical-prices.
    """
    num_days = 1 + time.ToCivil(time.Now()).diff(start_date).in_days()
    if num_days <= 5:
        return '5d'
    if num_days <= 28:  # Shortest month has 28 days
        return '1m'
    if num_days <= 90:
        return '3m'
    if num_days <= 182:
        return '6m'
    if num_days <= 365:
        return '1y'
    if num_days <= 730:
        return '2y'
    if num_days <= 365 * 5 + 1:
        return '5y'
    if num_days <= 365 * 15 + 3:
        return 'max'
    raise errors.InvalidArgumentError(
        'IEX does not support historical data older than 15 years')
