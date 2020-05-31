'''Time module creates types and alias for all necessary time and date related operations'''
import datetime
import time
from typing import Optional

import pendulum


# For the rationales of theses classes: https://abseil.io/docs/cpp/guides/time
# Time class follows the interface of https://github.com/abseil/abseil-cpp/blob/master/absl/time/time.h.
class Time(int):

    def __new__(cls, ns=0):
        return super(Time, cls).__new__(cls, ns)

    def __add__(self, other):
        return self.__class__(super(Time, self).__add__(other))

    def __sub__(self, other):
        return self.__class__(super(Time, self).__sub__(other))

    def __mul__(self, other):
        return self.__class__(super(Time, self).__mul__(other))

    def __truediv__(self, other):
        return self.__class__(super(Time, self).__truediv__(other))

    def __str__(self):
        seconds, nanoseconds = divmod(self, 1e9)
        return f'Seconds: {seconds}, Nanoseconds: {nanoseconds}'

    def __repr__(self):
        return f'Time({self})'


Duration = Time

# CivilTime is timezone-agnostic / timezone-naive
# NOTE: to diff CivilTimes, convert them to Time first. For adding and
# substracting, use CivilTime.add(days=n) and CivilTime.substract(months=m)
# See https://pendulum.eustace.io/docs/#addition-and-subtraction.
CivilTime = pendulum.DateTime

Timezone = pendulum._Timezone
UTC: Timezone = pendulum.UTC


def timezone(name) -> Timezone:
    return pendulum.timezone(name)


def GetCurrentTimeNanos() -> int:
    return time.time_ns()


def Now() -> Time:
    return Time(GetCurrentTimeNanos())


def UnixEpoch() -> Time:
    return Time()


def FormatTime(t: Time, tz: Timezone = None, fmt: Optional[str] = None) -> str:
    dt = _to_datetime(t, tz)
    if fmt:
        return dt.strftime(fmt)
    return dt.isoformat()


def ZeroDuration() -> Duration:
    return Duration(0)


def Nanoseconds(n: int) -> Duration:
    return Duration(n)


def Microseconds(n: int) -> Duration:
    return Duration(n * 1e3)


def Milliseconds(n: int) -> Duration:
    return Duration(n * 1e6)


def Seconds(n: int) -> Duration:
    return Duration(n * 1e9)


def Minutes(n: int) -> Duration:
    return Duration(n * 1e9 * 60)


def Hours(n: int) -> Duration:
    return Duration(n * 1e9 * 60 * 60)


def FromUnixNanos(nanos: int) -> Time:
    return Time(nanos)


def FromUnixMillis(millis: int) -> Time:
    return Time(millis * 1e3)


def FromUnixMicros(micros: int) -> Time:
    return Time(micros * 1e6)


def FromUnixSeconds(seconds: int) -> Time:
    return Time(seconds * 1e9)


def ToUnixNanos(t: Time) -> int:
    return int(t)


def ToUnixMillis(t: Time) -> int:
    return int(t) / 1e3


def ToUnixMicros(t: Time) -> int:
    return int(t) / 1e6


def ToUnixSeconds(t: Time) -> int:
    return int(t) / 1e9


def FromCivil(ct: CivilTime, tz: Timezone = None) -> Time:
    dt = _make_datetime_with_preferred_dst(ct, tz or UTC)
    return Time(dt.timestamp() * 1e9)


def ToCivil(t: Time, tz: Timezone = None) -> CivilTime:
    return _to_datetime(t, tz).naive()


def FormatCivilTime(ct: CivilTime) -> str:
    return ct.to_iso8601_string()


def ParseCivilTime(isoformat: str) -> CivilTime:
    ct = CivilTime.fromisoformat(isoformat)
    return _make_datetime_with_preferred_dst(ct, UTC).naive()


def _to_datetime(t: Time, tz: Timezone = None) -> pendulum.DateTime:
    if not tz:
        tz = UTC
    dt = pendulum.from_timestamp(int(t) / 1e9, tz=tz)
    return _make_datetime_with_preferred_dst(dt, tz)


def _make_datetime_with_preferred_dst(dt: pendulum.DateTime,
                                      tz: Timezone = None) -> pendulum.DateTime:
    try:
        return _make_datetime(dt, tz, dst_rule=pendulum.TRANSITION_ERROR)
    except pendulum.tz.exceptions.AmbiguousTime:
        # Prefer the earlier of the possible interpretations of an ambiguous
        # time.
        return _make_datetime(dt, tz, dst_rule=pendulum.PRE_TRANSITION)
    except pendulum.tz.exceptions.NonExistingTime:
        # Prefer the later of the possible interpretations of a
        # non-existent time.
        return _make_datetime(dt, tz, dst_rule=pendulum.POST_TRANSITION)


def _make_datetime(dt: pendulum.DateTime, tz: Timezone,
                   dst_rule) -> pendulum.DateTime:
    return pendulum.datetime(dt.year,
                             dt.month,
                             dt.day,
                             dt.hour,
                             dt.minute,
                             dt.second,
                             dt.microsecond,
                             tz=tz,
                             dst_rule=dst_rule)
