import unittest
from datetime import datetime
from datetime import timedelta
from nxtodo_cli import parse_datetime
from nxtodo_cli import Formats


class TestDateTimeParser(unittest.TestCase):

    def test_datetime_format(self):
        self.assertEqual(parse_datetime(['2018/01/01', '19:34:23'], Formats.datetime, '%Y/%m/%d %H:%M:%S'),
                        datetime(2018, 1, 1, 19, 34, 23))
        self.assertEqual(parse_datetime(['10/04/2018', '19:34:23'], Formats.datetime, '%d/%m/%Y %H:%M:%S'),
                         datetime(2018, 4, 10, 19, 34, 23))
        with self.assertRaises(ValueError):
            parse_datetime(['2018/01/01', '19:34:23'], Formats.datetime, '%Y/%m/%d %H:%M:%')
        with self.assertRaises(ValueError):
            parse_datetime(['2018/01/01', '25:34:23'], Formats.datetime, '%Y/%m/%d %H:%M:%S')
        with self.assertRaises(ValueError):
            parse_datetime(['2btrwr018/01/01', '25:34:23'], Formats.datetime, '%Y/%m/%d %H:%M:%S')
        with self.assertRaises(ValueError):
            parse_datetime(['2018/01/01', '25:34'], Formats.datetime, '%Y/%m/%d %H:%M:%S')

    def test_datetime_list_format(self):
        self.assertEqual(parse_datetime(['2018/01/01', '19:34:23', '2019/02/03', '11:14:56'], Formats.datetime_list,
                                        '%Y/%m/%d %H:%M:%S'), [datetime(2018, 1, 1, 19, 34, 23),
                                                               datetime(2019, 2, 3, 11, 14, 56)])
        with self.assertRaises(ValueError):
            parse_datetime(['2018/01/01', '19:34:23', '2019/02/03', '11:1asf4:56'],
                           Formats.datetime_list, '%Y/%m/%d %H:%M:%S')
        with self.assertRaises(IndexError):
            parse_datetime(['2018/01/01', '19:34:23', '2018/02/09'], Formats.datetime_list, '%Y/%m/%d %H:%M:%S')

    def test_timedelta_format(self):
        self.assertEqual(parse_datetime('2:1:0:3', Formats.timedelta, 'w:d:h:m'), timedelta(15, 180))
        with self.assertRaises(ValueError):
            self.assertEqual(parse_datetime('2:1:wef0:3', Formats.timedelta, 'w:d:h:m'), timedelta(15, 180))
        with self.assertRaises(IndexError):
            self.assertEqual(parse_datetime('234:2', Formats.timedelta, 'w:d:h:m'), timedelta(15, 180))

    def test_weekdays_format(self):
        self.assertEqual(parse_datetime(['mon', 'fri', 'sun'], Formats.weekdays, 'strs'), [0, 4, 6])
        self.assertEqual(parse_datetime(['mon'], Formats.weekdays, 'strs'), [0])
        self.assertEqual(parse_datetime(['mon', 'fri', 'sun', 'sun', 'mon'], Formats.weekdays, 'strs'), [0, 4, 6])
        self.assertEqual(parse_datetime(['0', '1', '2', '4'], Formats.weekdays, 'ints'), [0, 1, 2, 4])
        self.assertEqual(parse_datetime(['0', '1', '2', '1'], Formats.weekdays, 'ints'), [0, 1, 2])
        with self.assertRaises(ValueError):
            self.assertEqual(parse_datetime(['mon', 'fri', 'suwefn'], Formats.weekdays, 'strs'), [0, 4, 6])
        with self.assertRaises(ValueError):
            self.assertEqual(parse_datetime(['0', '1', '23', '1'], Formats.weekdays, 'ints'), [0, 1, 2])


if __name__ == '__main__':
        unittest.main()