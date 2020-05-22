import datetime

from absl.testing import absltest

from xlab.base import time


# Based on: https://github.com/abseil/abseil-cpp/blob/master/absl/time/time_test.cc
class TimeTest(absltest.TestCase):

    def test_const_expr(self):
        self.assertEqual(time.Time(), time.UnixEpoch())
        self.assertEqual(time.Time(), time.FromUnixNanos(0))
        self.assertEqual(time.Time(), time.FromUnixMillis(0))
        self.assertEqual(time.Time(), time.FromUnixMicros(0))
        self.assertEqual(time.Time(), time.FromUnixSeconds(0))

    def test_unix_epoch(self):
        epoch = time.FromDatetime(datetime.datetime(1970, 1, 1, 0, 0, 0))
        self.assertEqual(epoch, time.UnixEpoch())
        self.assertEqual(epoch - time.UnixEpoch(), time.ZeroDuration())

    def test_add(self):
        d = time.Nanoseconds(1)
        t0 = time.Time()
        t1 = t0 + d
        self.assertEqual(d, t1 - t0)
        self.assertEqual(-d, t0 - t1)
        self.assertEqual(t0, t1 - d)

        t = t0
        self.assertEqual(t0, t)
        t += d
        self.assertEqual(t0 + d, t)
        self.assertEqual(d, t - t0)
        t -= d
        self.assertEqual(t0, t)

        # Tests overflow between subseconds and seconds.
        t = time.UnixEpoch()
        t += time.Milliseconds(500)
        self.assertEqual(time.UnixEpoch() + time.Milliseconds(500), t)
        t += time.Milliseconds(600)
        self.assertEqual(time.UnixEpoch() + time.Milliseconds(1100), t)
        t -= time.Milliseconds(600)
        self.assertEqual(time.UnixEpoch() + time.Milliseconds(500), t)
        t -= time.Milliseconds(500)
        self.assertEqual(time.UnixEpoch(), t)

    def test_relational_operators(self):
        t1 = time.Nanoseconds(0)
        t2 = time.Nanoseconds(1)
        t3 = time.Nanoseconds(2)
        self.assertTrue(time.Time() == t1)
        self.assertTrue(t1 == t1)
        self.assertTrue(t2 == t2)
        self.assertTrue(t3 == t3)

        self.assertTrue(t1 < t2)
        self.assertTrue(t2 < t3)
        self.assertTrue(t1 < t3)

        self.assertTrue(t1 <= t1)
        self.assertTrue(t1 <= t2)
        self.assertTrue(t2 <= t2)
        self.assertTrue(t2 <= t3)
        self.assertTrue(t3 <= t3)
        self.assertTrue(t1 <= t3)

        self.assertTrue(t2 > t1)
        self.assertTrue(t3 > t2)
        self.assertTrue(t3 > t1)

        self.assertTrue(t2 >= t2)
        self.assertTrue(t2 >= t1)
        self.assertTrue(t3 >= t3)
        self.assertTrue(t3 >= t2)
        self.assertTrue(t1 >= t1)
        self.assertTrue(t3 >= t1)

    def test_floor_conversion(self):
        self.assertEqual(
            1, time.ToUnixNanos(time.UnixEpoch() + time.Nanoseconds(3) / 2))
        self.assertEqual(
            1, time.ToUnixNanos(time.UnixEpoch() + time.Nanoseconds(1)))
        self.assertEqual(
            0, time.ToUnixNanos(time.UnixEpoch() + time.Nanoseconds(1) / 2))
        self.assertEqual(
            0, time.ToUnixNanos(time.UnixEpoch() + time.Nanoseconds(0)))
        # NOTE: the following three assertions are different from absl::Time,
        # as nanoseconds is the ultimate precison here.
        self.assertEqual(
            0, time.ToUnixNanos(time.UnixEpoch() - time.Nanoseconds(1) / 2))
        self.assertEqual(
            -1, time.ToUnixNanos(time.UnixEpoch() - time.Nanoseconds(1)))
        self.assertEqual(
            -1, time.ToUnixNanos(time.UnixEpoch() - time.Nanoseconds(3) / 2))

        self.assertEqual(
            -500, time.ToUnixNanos(time.UnixEpoch() - time.Microseconds(1) / 2))
        self.assertEqual(
            -1000, time.ToUnixNanos(time.UnixEpoch() - time.Microseconds(1)))
        self.assertEqual(
            -1500,
            time.ToUnixNanos(time.UnixEpoch() - time.Microseconds(3) / 2))

    def test_format_time(self):
        t = time.FromDatetime(datetime.datetime(2015, 2, 3, 4, 5, 6))
        self.assertEqual("2015-02-03T04:05:06+00:00", time.FormatTime(t))
        t = time.FromDatetime(datetime.datetime(2015, 2, 3, 4, 5))
        self.assertEqual("2015-02-03T04:05:00+00:00", time.FormatTime(t))
        t = time.FromDatetime(datetime.datetime(2015, 2, 3, 4))
        self.assertEqual("2015-02-03T04:00:00+00:00", time.FormatTime(t))
        t = time.FromDatetime(datetime.datetime(2015, 2, 3))
        self.assertEqual("2015-02-03T00:00:00+00:00", time.FormatTime(t))


if __name__ == '__main__':
    absltest.main()
