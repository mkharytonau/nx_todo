from datetime import datetime
from datetime import timedelta


def check_deadline(deadline, now):
    if deadline and now > deadline:
        return deadline
    else:
        return None


def check_range(from_datetime, to_datetime, now):
    if not (from_datetime and to_datetime and now):
        return None
    if from_datetime <= now <= to_datetime:
        return from_datetime
    else:
        return None


def check_remind_in(remind_in, deadline, now):
    if not (remind_in and deadline and now):
        return None
    date = deadline - remind_in
    if date <= now < deadline:
        return date
    else:
        return None


def check_datetimes(datetimes, now):
    if not datetimes:
        return None
    counter = 0
    for dt in datetimes:
        if dt < now:
            counter += 1
    if counter:
        return datetimes[counter - 1]
    else:
        return None


def check_interval(start_remind_from, interval, now):
    if interval is None:
        return None
    counter = (now - start_remind_from) // interval
    if counter > 0:
        return start_remind_from + interval * counter
    else:
        return None


def check_weekdays(start_remind_from, weekdays, now):
    if weekdays is None:
        return None
    day = timedelta(days=1)
    date_now = now.date()
    while start_remind_from.date() <= date_now:
        if weekdays.__contains__(date_now.weekday()):
            return datetime(date_now.year, date_now.month, date_now.day, 0)
        date_now -= day
    return None