import re
import enum
from datetime import datetime
from datetime import timedelta
from datetime import date


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
        if args is not None:
            if args.full:
                print(str(i) + '. ' + item.to_full())
            else:
                print(str(i) + '. ' + item.to_short())
        else:
            print(str(i) + '. ' + item)
        i = i + 1


def print_notifications(arr):
    if len(arr) == 0:
        print('List is empty.')
        return
    for n in arr:
        print(n)


def select_item(db, search_info):
    extend_found = []
    working_space = db.select_working_space(search_info.instance)
    for inst in working_space:
        value = inst.__getattribute__(search_info.attribute)
        if re.search(search_info.value, value) is not None:
            if not extend_found.__contains__(value):
                extend_found.append(value)
    if len(extend_found) == 0:
        raise ValueError
    if len(extend_found) > 1:
        print('Found multiple matches, please select one.')
        print_list(extend_found, None)
        choice = int(input('Your choice: '))
        return extend_found[choice - 1]
    else:
        return extend_found[0]


class SearchInfo:
    def __init__(self, instance, attribute, value, all):
        self.instance = instance
        self.attribute = attribute
        self.value = value
        self.all = all




