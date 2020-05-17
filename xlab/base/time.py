import datetime
import time


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
        return f"Seconds: {seconds}, Nanoseconds: {nanoseconds}"

    def __repr__(self):
        return f"Time({self})"


Duration = Time


def Now() -> Time:
    return Time(time.time_ns())


def UnixEpoch() -> Time:
    return Time()


# Return the RFC3339 Full representation of the time.
def FormatTime(t: Time, tz: datetime.timezone = None) -> str:
    if tz is None:
        tz = datetime.timezone.utc
    rfc3339_secs = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(int(t) / 1e9))
    tz_offset = datetime.time(tzinfo=tz).strftime('%z')
    # -0700 -> -07:00
    tz_offset = ''.join((tz_offset[:3], ':', tz_offset[3:]))
    return ''.join((rfc3339_secs, tz_offset))


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


def FromDatetime(dt: datetime.datetime) -> Time:
    return Time(time.mktime(dt.timetuple()) * 1e9)


def ToUnixNanos(t: Time) -> int:
    return int(t)


def ToUnixMillis(t: Time) -> int:
    return int(t) / 1e3


def ToUnixMicros(t: Time) -> int:
    return int(t) / 1e6


def ToUnixSeconds(time: Time) -> int:
    return int(t) / 1e9


def ToDatetime(t: Time) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(int(t) / 1e9)
