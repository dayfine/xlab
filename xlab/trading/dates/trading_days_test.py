import datetime

from absl.testing import absltest

from xlab.trading.dates import trading_days


class TradingDayFinderTest(absltest.TestCase):

    def test_is_trading_day(self):
        finder = trading_days.get_trading_day_finder()
        self.assertFalse(finder.is_trading_day(datetime.date(2017, 1, 2)))
        self.assertTrue(finder.is_trading_day(datetime.date(2017, 1, 3)))
        self.assertTrue(finder.is_trading_day(datetime.date(2018, 7, 3)))
        self.assertFalse(finder.is_trading_day(datetime.date(2018, 7, 4)))
        self.assertTrue(finder.is_trading_day(datetime.date(2020, 5, 22)))
        self.assertFalse(finder.is_trading_day(datetime.date(2020, 5, 25)))

    def test_is_trading_day_raises_for_unknown_dates(self):
        finder = trading_days.get_trading_day_finder()
        start, end = finder.range()
        with self.assertRaisesRegex(ValueError, f'{start}, {end}'):
            finder.is_trading_day(start - datetime.timedelta(days=1))
        with self.assertRaisesRegex(ValueError, f'{start}, {end}'):
            finder.is_trading_day(end + datetime.timedelta(days=1))

    def test_get_last_n(self):
        finder = trading_days.get_trading_day_finder()
        # 2020-05-25 is not a traiding date.
        self.assertSequenceEqual(
            finder.get_last_n(datetime.date(2020, 5, 25), 1),
            [datetime.date(2020, 5, 22)])
        self.assertSequenceEqual(
            finder.get_last_n(datetime.date(2020, 5, 22), 1),
            [datetime.date(2020, 5, 22)])
        self.assertSequenceEqual(
            finder.get_last_n(datetime.date(2020, 5, 25), 6), [
                datetime.date(2020, 5, 15),
                datetime.date(2020, 5, 18),
                datetime.date(2020, 5, 19),
                datetime.date(2020, 5, 20),
                datetime.date(2020, 5, 21),
                datetime.date(2020, 5, 22),
            ])

    def test_get_last_n_without_input_date(self):
        finder = trading_days.get_trading_day_finder()
        self.assertSequenceEqual(
            finder.get_last_n(datetime.date(2020, 5, 25),
                              1,
                              include_input_date=False),
            [datetime.date(2020, 5, 22)])
        self.assertSequenceEqual(
            finder.get_last_n(datetime.date(2020, 5, 22),
                              1,
                              include_input_date=False),
            [datetime.date(2020, 5, 21)])
        self.assertSequenceEqual(
            finder.get_last_n(datetime.date(2020, 5, 22),
                              6,
                              include_input_date=False), [
                                  datetime.date(2020, 5, 14),
                                  datetime.date(2020, 5, 15),
                                  datetime.date(2020, 5, 18),
                                  datetime.date(2020, 5, 19),
                                  datetime.date(2020, 5, 20),
                                  datetime.date(2020, 5, 21),
                              ])

    def test_get_last_n_at_start(self):
        finder = trading_days.get_trading_day_finder()
        start, _ = finder.range()
        self.assertSequenceEqual(finder.get_last_n(start, 1), [start])
        self.assertSequenceEqual(finder.get_last_n(start, 2), [start])
        self.assertSequenceEqual(finder.get_last_n(start, 20), [start])
        # The current range start is a Monday
        self.assertSequenceEqual(
            finder.get_last_n(start + datetime.timedelta(days=4), 5),
            [start + datetime.timedelta(days=i) for i in range(5)])

        self.assertSequenceEqual(
            finder.get_last_n(start, 1, include_input_date=False), [])
        self.assertSequenceEqual(
            finder.get_last_n(start, 2, include_input_date=False), [])

    def test_get_next_n(self):
        finder = trading_days.get_trading_day_finder()
        self.assertSequenceEqual(
            finder.get_next_n(datetime.date(2020, 5, 25), 1),
            [datetime.date(2020, 5, 26)])
        self.assertSequenceEqual(
            finder.get_next_n(datetime.date(2020, 5, 26), 1),
            [datetime.date(2020, 5, 27)])
        self.assertSequenceEqual(
            finder.get_next_n(datetime.date(2020, 5, 23), 6), [
                datetime.date(2020, 5, 26),
                datetime.date(2020, 5, 27),
                datetime.date(2020, 5, 28),
                datetime.date(2020, 5, 29),
                datetime.date(2020, 6, 1),
                datetime.date(2020, 6, 2),
            ])

    def test_get_next_n_with_input_date(self):
        finder = trading_days.get_trading_day_finder()
        self.assertSequenceEqual(
            finder.get_next_n(datetime.date(2020, 5, 25),
                              1,
                              include_input_date=True),
            [datetime.date(2020, 5, 26)])
        self.assertSequenceEqual(
            finder.get_next_n(datetime.date(2020, 5, 26),
                              1,
                              include_input_date=True),
            [datetime.date(2020, 5, 26)])
        self.assertSequenceEqual(
            finder.get_next_n(datetime.date(2020, 5, 26),
                              6,
                              include_input_date=True), [
                                  datetime.date(2020, 5, 26),
                                  datetime.date(2020, 5, 27),
                                  datetime.date(2020, 5, 28),
                                  datetime.date(2020, 5, 29),
                                  datetime.date(2020, 6, 1),
                                  datetime.date(2020, 6, 2),
                              ])

    def test_get_next_n_at_end(self):
        finder = trading_days.get_trading_day_finder()
        _, end = finder.range()
        self.assertSequenceEqual(finder.get_next_n(end, 1), [])
        self.assertSequenceEqual(finder.get_next_n(end, 2), [])
        self.assertSequenceEqual(finder.get_next_n(end, 20), [])
        # The current range end is a Tuesday
        self.assertSequenceEqual(
            finder.get_next_n(end - datetime.timedelta(days=1), 1), [end])

        self.assertSequenceEqual(
            finder.get_next_n(end, 1, include_input_date=True), [end])
        self.assertSequenceEqual(
            finder.get_next_n(end, 2, include_input_date=True), [end])


if __name__ == '__main__':
    absltest.main()
