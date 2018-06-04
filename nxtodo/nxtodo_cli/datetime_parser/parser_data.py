import enum


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

