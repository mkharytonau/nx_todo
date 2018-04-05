from datetime import datetime
from datetime import timedelta
from datetime import date
import thirdparty


def parse_datetime(dtlist, format):
    if format == thirdparty.Formats.ordinary:
        if dtlist is None:
            return None
        try:
            dt = datetime(*map(int, dtlist[0].split('/')), *map(int, dtlist[1].split(':')))
        except:
            print('Incorrect data. Please, try again...')
            raise ValueError
        return dt

    if format == thirdparty.Formats.delta:
        if dtlist is None:
            return None
        try:
            arglist = list(map(int, dtlist.split(':')))
            td = timedelta(weeks=arglist[0], days=arglist[1], hours=arglist[2], minutes=arglist[3])
        except:
            print('Incorrect data. Please, try again...')
            raise ValueError
        return td

    if format == thirdparty.Formats.ordinary_list:
        if dtlist is None:
            return None
        try:
            list_of_dates = []
            for i in range(0, len(dtlist), 2):
                list_of_dates.append(parse_datetime([dtlist[i], dtlist[i + 1]], 'y/m/d h:m:s'))
        except:
            raise ValueError
        return list_of_dates

    if format == thirdparty.Formats.weekdays:
        if dtlist is None:
            return None
        try:
            weekdays_ints = [getattr(thirdparty.Weekdays, i) for i in dtlist]
        except:
            print('Incorrect data. Please, try again...')
            raise ValueError
        return weekdays_ints

    if format == thirdparty.Formats.date:
        if dtlist is None:
            return None
        try:
            dt = date(*map(int, dtlist.split('/')))
        except:
            print('Incorrect data. Please, try again...')
            raise ValueError
        return dt

