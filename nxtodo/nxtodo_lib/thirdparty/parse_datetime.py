from datetime import datetime
from datetime import timedelta
from datetime import date
from .enums import Weekdays


def parse_datetime(dtlist, format):
    if format == 'y/m/d h:m:s':
        if dtlist is None:
            return None
        try:
            dt = datetime(*map(int, dtlist[0].split('/')), *map(int, dtlist[1].split(':')))
        except:
            raise ValueError
        return dt

    if format == 'w:d:h:m':
        if dtlist is None:
            return None
        try:
            arglist = list(map(int, dtlist.split(':')))
            td = timedelta(weeks=arglist[0], days=arglist[1], hours=arglist[2], minutes=arglist[3])
        except:
            raise ValueError
        return td

    if format == 'y/m/d h:m:s ... y/m/d h:m:s':
        if dtlist is None:
            return None
        try:
            list_of_dates = []
            for i in range(0, len(dtlist), 2):
                list_of_dates.append(parse_datetime([dtlist[i], dtlist[i + 1]], 'y/m/d h:m:s'))
        except:
            raise ValueError
        return list_of_dates

    if format == 'weekdays':
        if dtlist is None:
            return None
        try:
            weekdays_ints = [Weekdays[i].value for i in dtlist]
        except:
            raise ValueError
        return weekdays_ints

    if format == 'y/m/d':
        if dtlist is None:
            return None
        try:
            dt = date(*map(int, dtlist.split('/')))
        except:
            raise ValueError
        return dt

