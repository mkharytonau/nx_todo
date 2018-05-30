import unittest
from datetime import datetime
from datetime import timedelta
from nxtodo.reminding import check_deadline
from nxtodo.reminding import check_range
from nxtodo.reminding import check_remind_in
from nxtodo.reminding import check_datetimes
from nxtodo.reminding import check_interval
from nxtodo.reminding import check_weekdays


class TestCheckTimes(unittest.TestCase):

    def test_check_deadline(self):
        deadline = datetime(2018, 5, 29, 21, 48)
        now = datetime(2018, 5, 29, 22, 40)
        self.assertEqual(check_deadline(deadline, now), deadline)
        deadline = datetime(2018, 6, 29, 21, 48)
        now = datetime(2018, 6, 29, 20, 32)
        self.assertEqual(check_deadline(deadline, now), None)
        self.assertEqual(check_deadline(None, now), None)

    def test_check_range(self):
        from_datetime = datetime(2018, 5, 29, 21, 48, 0)
        to_datetime = datetime(2018, 5, 29, 22, 30, 30)
        now = datetime(2018, 5, 29, 21, 50)
        self.assertEqual(check_range(from_datetime, to_datetime, now),
                         from_datetime)
        self.assertEqual(check_range(from_datetime, to_datetime,
                                     datetime(2018, 5, 29, 23)), None)
        self.assertEqual(check_range(None, to_datetime,
                                     datetime(2018, 5, 29, 23)), None)

    def test_check_remind_in(self):
        deadline = datetime(2018, 5, 29, 21, 48)
        self.assertEqual(check_remind_in(timedelta(weeks=1), deadline,
                                         datetime(2018, 5, 25)),
                         datetime(2018, 5, 22, 21, 48))
        deadline = datetime(2018, 5, 29, 21, 48)
        self.assertEqual(check_remind_in(timedelta(weeks=1), deadline,
                                         datetime(2018, 5, 20)), None)
        self.assertEqual(check_remind_in(timedelta(weeks=1), None,
                                         datetime(2018, 5, 20)), None)

    def test_check_datetimes(self):
        datetimes = [datetime(2018, 5, 27, 13, 12),
                     datetime(2018, 5, 29, 18), datetime(2018, 5, 29, 23)]
        now = datetime(2018, 5, 29, 22, 5)
        self.assertEqual(check_datetimes(datetimes, now),
                         datetime(2018, 5, 29, 18))
        now = datetime(2018, 6, 29, 22, 5)
        self.assertEqual(check_datetimes(datetimes, now),
                         datetime(2018, 5, 29, 23))
        now = datetime(2018, 5, 24, 21, 5)
        self.assertEqual(check_datetimes(datetimes, now), None)
        self.assertEqual(check_datetimes(None, now), None)

    def test_check_interval(self):
        start_remind_from = datetime(2018, 6, 20, 18)
        interval = timedelta(hours=6)
        now = datetime(2018, 6, 22, 14)
        self.assertEqual(check_interval(start_remind_from, interval, now),
                         datetime(2018, 6, 22, 12))
        now = datetime(2018, 6, 20, 20)
        self.assertEqual(check_interval(start_remind_from, interval, now),
                         None)
        now = datetime(2018, 6, 19, 20)
        self.assertEqual(check_interval(start_remind_from, interval, now),
                         None)
        self.assertEqual(check_interval(start_remind_from, None, now), None)

    def test_check_weekdays(self):
        start_remind_from = datetime(2018, 6, 20, 18)
        weekdays = [0, 2, 3]
        now = datetime(2018, 6, 22, 14)
        self.assertEqual(check_weekdays(start_remind_from, weekdays, now),
                         datetime(2018, 6, 21, 0))
        now = datetime(2018, 6, 23, 14)
        self.assertEqual(check_weekdays(start_remind_from, weekdays, now),
                         datetime(2018, 6, 21, 0))
        now = datetime(2018, 6, 20, 20)
        weekdays = [5, 6]
        self.assertEqual(check_weekdays(start_remind_from,
                                        weekdays, now), None)
        now = datetime(2018, 6, 25, 20, 12, 13)
        self.assertEqual(check_weekdays(start_remind_from, weekdays, now),
                         datetime(2018, 6, 24, 0))


if __name__ == '__main__':
        unittest.main()