import enum


class Formats(enum.Enum):
    datetime = 'datetime'
    datetime_list = 'datetime_list'
    timedelta = 'timedelta'
    weekdays = 'weekdays'


weekdays = {
    'mon': 0,
    'tue': 1,
    'wed': 2,
    'thu': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6
}

