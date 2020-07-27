from xlab.base import time


def _to_iex_api_date(date: time.CivilTime):
    return date.format('YYYYMMDD')
