import argparse
import enum
from datetime import datetime, timedelta

from nxtodo_cli.commands import get_config


class Formats(enum.Enum):
    DATETIME = 'datetime'
    DATETIME_LIST = 'datetime_list'
    TIMEDELTA = 'timedelta'
    WEEKDAYS = 'weekdays'


WEEKDAYS = {
    'mon': 0,
    'tue': 1,
    'wed': 2,
    'thu': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6
}


def parse_datetime(input_string):
    config = get_config()
    try:
        return datetime.strptime(
            input_string, config['date_formats'][Formats.DATETIME.value])
    except ValueError:
        pattern = config['date_formats'][Formats.DATETIME.value]
        msg = '{} does not match {}, please check input data ' \
              'or config file.'.format(input_string, pattern)
        raise argparse.ArgumentTypeError(msg)


def parse_datetime_list(input_string):
    config = get_config()
    try:
        return datetime.strptime(
            input_string, config['date_formats'][Formats.DATETIME_LIST.value])
    except ValueError:
        pattern = config['date_formats'][Formats.DATETIME_LIST.value]
        msg = '{} does not match {}, please check input data ' \
              'or config file.'.format(input_string, pattern)
        raise argparse.ArgumentTypeError(msg)


def parse_timedelta(input_string):
    try:
        arglist = list(map(int, input_string.split(':')))
        return timedelta(weeks=arglist[0], days=arglist[1], hours=arglist[2],
                         minutes=arglist[3])
    except Exception:
        msg = 'Expected int:int:int:int.'
        raise argparse.ArgumentTypeError(msg)


def parse_weekdays(input_string):
    config = get_config()
    format_string = config['date_formats'][Formats.WEEKDAYS.value]
    try:
        if format_string == 'strs':
            return WEEKDAYS[input_string]
        if format_string == 'ints':
            weekday = int(input_string)
            if 0 <= weekday <= 6:
                return weekday
    except Exception:
        msg = "Error, when parsing '{}', please check input data " \
              "or config file.".format(input_string)
        raise argparse.ArgumentTypeError(msg)
