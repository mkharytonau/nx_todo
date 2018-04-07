from datetime import datetime
from datetime import timedelta
from datetime import date


class Classes():
    task = 'task'
    event = 'event'


class Formats():
    ordinary = 'y/m/d h:m:s'
    date = 'y/m/d'
    delta = 'w:d:h:m'
    ordinary_list = 'y/m/d h:m:s ... y/m/d h:m:s'
    weekdays = 'weekdays'


class Weekdays():
    mon = 0
    tue = 1
    wed = 2
    thu = 3
    fri = 4
    sat = 5
    sun = 6


class Styles():
    terminal = 'terminal'
    gui = 'gui'


class Colors():
    red = 124
    yellow = 136
    grey = 240
    taskbg = 229
    eventbg = 131
    foreground = 235


class Parent():
    def __init__(self, title, deadline, *to_datetime):
        self.title = title
        self.deadline = deadline
        if len(to_datetime) > 0:
            self.to_datetime = to_datetime[0]

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y/%m/%d %H:%M:%S")
    if isinstance(obj, timedelta):
        return timedelta_tostr(obj)
    if isinstance(obj, date):
        return obj.strftime("%Y/%m/%d")
    return obj.__dict__


def timedelta_tostr(obj):
    weeks = obj.days // 7
    days = obj.days - weeks * 7
    hours = obj.seconds // 3600
    minutes = (obj.seconds - hours * 3600) // 60
    return '{w}:{d}:{h}:{m}'.format(w=weeks, d=days, h=hours, m=minutes)

def print_list(list, args):
    if not len(list):
        print('List is empty.')
        return
    i = 1
    for item in list:
        if args.full:
            print(str(i) + '. ' + item.to_full())
        else:
            print(str(i) + '. ' + item.to_short())
        i = i + 1


def get_notifications(arr, style):
    if not len(arr):
        print('List is empty.')
        return
    notifications = []
    for obj in arr:
        notification = obj.reminder.check(style)
        if notification is not None:
            notifications.append(notification)
    return notifications


def print_notifications(arr):
    if len(arr) == 0:
        print('List is empty.')
        return
    for n in arr:
        print(n)



