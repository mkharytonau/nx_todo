from .enums import weekdays
from .enums import Formats
from datetime import datetime
from datetime import timedelta


def parse_datetime(dtlist, format, format_string):

    if dtlist is None:
        return None

    if format == Formats.datetime:
        data = dtlist[0] + ' ' + dtlist[1]
        return datetime.strptime(data, format_string)

    if format == Formats.datetime_list:
        date_list = []
        for i in range(0, len(dtlist), 2):
            date_list.append([dtlist[i], dtlist[i + 1]])
        return [parse_datetime(date, Formats.datetime, format_string) for date in date_list]

    if format == Formats.timedelta:
        arglist = list(map(int, dtlist.split(':')))
        return timedelta(weeks=arglist[0], days=arglist[1], hours=arglist[2], minutes=arglist[3])

    if format == Formats.weekdays:
        dtlist = list(set(dtlist))
        if format_string == 'strs':
            try:
                return sorted([weekdays[i] for i in dtlist])
            except KeyError:
                raise ValueError
        if format_string == 'ints':
            wdays = []
            for i in dtlist:
                if 0 <= int(i) <= 6:
                    wdays.append(int(i))
                else:
                    raise ValueError
            return sorted(wdays)
        raise ValueError

