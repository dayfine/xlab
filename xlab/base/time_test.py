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
        epoch = time.FromCivil(time.CivilTime(1970, 1, 1, 0, 0, 0))
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

    def _test_conversion_round_trip(self, source, _from, to):
        self.assertEqual(to(_from(source)), source)

    def test_round_trip_time_conversion(self):
        self._test_conversion_round_trip(-1, time.FromUnixNanos,
                                         time.ToUnixNanos)
        self._test_conversion_round_trip(0, time.FromUnixNanos,
                                         time.ToUnixNanos)
        self._test_conversion_round_trip(1, time.FromUnixNanos,
                                         time.ToUnixNanos)
        self._test_conversion_round_trip(time.GetCurrentTimeNanos(),
                                         time.FromUnixNanos, time.ToUnixNanos)

        self._test_conversion_round_trip(-1, time.FromUnixMillis,
                                         time.ToUnixMillis)
        self._test_conversion_round_trip(0, time.FromUnixMillis,
                                         time.ToUnixMillis)
        self._test_conversion_round_trip(1, time.FromUnixMillis,
                                         time.ToUnixMillis)
        self._test_conversion_round_trip(time.GetCurrentTimeNanos() // 1000,
                                         time.FromUnixMillis, time.ToUnixMillis)

        self._test_conversion_round_trip(-1, time.FromUnixMicros,
                                         time.ToUnixMicros)
        self._test_conversion_round_trip(0, time.FromUnixMicros,
                                         time.ToUnixMicros)
        self._test_conversion_round_trip(1, time.FromUnixMicros,
                                         time.ToUnixMicros)
        self._test_conversion_round_trip(time.GetCurrentTimeNanos() // 1000_000,
                                         time.FromUnixMicros, time.ToUnixMicros)

        self._test_conversion_round_trip(-1, time.FromUnixSeconds,
                                         time.ToUnixSeconds)
        self._test_conversion_round_trip(0, time.FromUnixSeconds,
                                         time.ToUnixSeconds)
        self._test_conversion_round_trip(1, time.FromUnixSeconds,
                                         time.ToUnixSeconds)
        self._test_conversion_round_trip(
            time.GetCurrentTimeNanos() // 1000_000_000, time.FromUnixSeconds,
            time.ToUnixSeconds)

    def _test_relational(self, older, younger):
        self.assertFalse(older < older)
        self.assertFalse(older > older)
        self.assertTrue(older >= older)
        self.assertTrue(older <= older)
        self.assertFalse(younger < younger)
        self.assertFalse(younger > younger)
        self.assertTrue(younger >= younger)
        self.assertTrue(younger <= younger)
        self.assertEqual(older, older)
        self.assertNotEqual(older, younger)
        self.assertLess(older, younger)
        self.assertLessEqual(older, younger)
        self.assertGreater(younger, older)
        self.assertGreaterEqual(younger, older)

    def test_civil_time_relations(self):
        self._test_relational(time.CivilTime(2014, 1, 1, 0, 0, 0),
                              time.CivilTime(2015, 1, 1, 0, 0, 0))
        self._test_relational(time.CivilTime(2014, 1, 1, 0, 0, 0),
                              time.CivilTime(2014, 2, 1, 0, 0, 0))
        self._test_relational(time.CivilTime(2014, 1, 1, 0, 0, 0),
                              time.CivilTime(2014, 1, 2, 0, 0, 0))
        self._test_relational(time.CivilTime(2014, 1, 1, 0, 0, 0),
                              time.CivilTime(2014, 1, 1, 1, 0, 0))
        self._test_relational(time.CivilTime(2014, 1, 1, 1, 0, 0),
                              time.CivilTime(2014, 1, 1, 1, 1, 0))
        self._test_relational(time.CivilTime(2014, 1, 1, 1, 1, 0),
                              time.CivilTime(2014, 1, 1, 1, 1, 1))

        self._test_relational(time.CivilTime(2014, 1, 1),
                              time.CivilTime(2014, 1, 1, 1, 1))
        self._test_relational(time.CivilTime(2014, 1, 1),
                              time.CivilTime(2014, 2, 1))

    def test_timezone_conversion(self):
        est: time.Timezone = time.timezone('US/Eastern')
        fmt = '%a, %e %b %Y %H:%M:%S %z (%Z)'

        # A non-transition where the civil time is unique.
        nov01 = time.CivilTime(2013, 11, 1, 8, 30, 0)
        nov01_t = time.FromCivil(nov01, est)
        self.assertEqual("Fri,  1 Nov 2013 08:30:00 -0400 (EDT)",
                         time.FormatTime(nov01_t, est, fmt))

        # A Spring DST transition, when there is a gap in civil time
        # and we prefer the later of the possible interpretations of a
        # non-existent time.
        mar13 = time.CivilTime(2011, 3, 13, 2, 15, 0)
        mar_t = time.FromCivil(mar13, est)
        self.assertEqual("Sun, 13 Mar 2011 03:15:00 -0400 (EDT)",
                         time.FormatTime(mar_t, est, fmt))

        # A Fall DST transition, when civil times are repeated and
        # we prefer the earlier of the possible interpretations of an
        # ambiguous time.
        nov06 = time.CivilTime(2011, 11, 6, 1, 15, 0)
        nov_t = time.FromCivil(nov06, est)
        self.assertEqual("Sun,  6 Nov 2011 01:15:00 -0400 (EDT)",
                         time.FormatTime(nov_t, est, fmt))

        # Check that (time_t) -1 is handled correctly.
        minus1 = time.CivilTime(1969, 12, 31, 18, 59, 59)
        minus1_t = time.FromCivil(minus1, est)
        self.assertEqual("Wed, 31 Dec 1969 18:59:59 -0500 (EST)",
                         time.FormatTime(minus1_t, est, fmt))
        self.assertEqual("Wed, 31 Dec 1969 23:59:59 +0000 (UTC)",
                         time.FormatTime(minus1_t, time.UTC, fmt))

    def test_from_civil(self):
        fmt = "%a, %e %b %Y %H:%M:%S %z (%Z)"
        # Check that we're counting leap years correctly.
        t = time.FromCivil(time.CivilTime(1900, 2, 28, 23, 59, 59), time.UTC)
        self.assertEqual("Wed, 28 Feb 1900 23:59:59 +0000 (UTC)",
                         time.FormatTime(t, time.UTC, fmt))
        t = time.FromCivil(time.CivilTime(1900, 3, 1, 0, 0, 0), time.UTC)
        self.assertEqual("Thu,  1 Mar 1900 00:00:00 +0000 (UTC)",
                         time.FormatTime(t, time.UTC, fmt))
        t = time.FromCivil(time.CivilTime(2000, 2, 29, 23, 59, 59), time.UTC)
        self.assertEqual("Tue, 29 Feb 2000 23:59:59 +0000 (UTC)",
                         time.FormatTime(t, time.UTC, fmt))
        t = time.FromCivil(time.CivilTime(2000, 3, 1, 0, 0, 0), time.UTC)
        self.assertEqual("Wed,  1 Mar 2000 00:00:00 +0000 (UTC)",
                         time.FormatTime(t, time.UTC, fmt))

    def test_default_time_format(self):
        t = time.FromCivil(time.CivilTime(2015, 2, 3, 4, 5, 6))
        self.assertEqual("2015-02-03T04:05:06+00:00", time.FormatTime(t))
        t = time.FromCivil(time.CivilTime(2015, 2, 3, 4, 5))
        self.assertEqual("2015-02-03T04:05:00+00:00", time.FormatTime(t))
        t = time.FromCivil(time.CivilTime(2015, 2, 3, 4))
        self.assertEqual("2015-02-03T04:00:00+00:00", time.FormatTime(t))
        t = time.FromCivil(time.CivilTime(2015, 2, 3))
        self.assertEqual("2015-02-03T00:00:00+00:00", time.FormatTime(t))

    def test_format_civil_time(self):
        ct = time.CivilTime(1970, 1, 1)
        self.assertEqual("1970-01-01T00:00:00", time.FormatCivilTime(ct))
        ct = time.CivilTime(2015, 1, 2, 3, 4, 5)
        self.assertEqual("2015-01-02T03:04:05", time.FormatCivilTime(ct))

        ct = time.ToCivil(time.Time(1234567890 * 1e9))
        self.assertEqual("2009-02-13T23:31:30", time.FormatCivilTime(ct))
        est: time.Timezone = time.timezone('US/Eastern')
        ct = time.ToCivil(time.Time(1234567890 * 1e9), est)
        self.assertEqual("2009-02-13T18:31:30", time.FormatCivilTime(ct))

    def test_parse_civil_time(self):
        self.assertEqual(time.CivilTime(2015, 1, 2, 3, 4, 5),
                         time.ParseCivilTime("2015-01-02T03:04:05"))
        self.assertEqual(time.CivilTime(2015, 1, 2, 3, 4),
                         time.ParseCivilTime("2015-01-02T03:04:00"))
        self.assertEqual(time.CivilTime(2015, 1, 2, 3),
                         time.ParseCivilTime("2015-01-02T03:00:00"))
        self.assertEqual(time.CivilTime(2015, 1, 2, 3),
                         time.ParseCivilTime("2015-01-02T03:00"))
        self.assertEqual(time.CivilTime(2015, 1, 2),
                         time.ParseCivilTime("2015-01-02T00:00:00"))
        self.assertEqual(time.CivilTime(2015, 1, 2),
                         time.ParseCivilTime("2015-01-02T00:00"))
        self.assertEqual(time.CivilTime(2015, 1, 2),
                         time.ParseCivilTime("2015-01-02"))


if __name__ == '__main__':
    absltest.main()
