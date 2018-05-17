#!/usr/bin/python3.6

import sys, os
sys.path.append(os.path.dirname(__file__))

#Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import getpass
import configparser
import nxtodo_console as con
import nxtodo_lib as lib
from datetime import datetime
from colored import bg, fg, attr


user_choice_command = {
    'adduser': lambda args: add_user(args),
    'show': lambda args: show(args),
    'add': lambda args: add(args),
    'del': lambda args: delete(args),
    'do': lambda args: do(args),
    'remove': lambda args: remove(args),
    'edit': lambda args: edit(args),
    'check': lambda args: check(args)
}

user_choice_show = {
    'all': lambda search_info, calendar, args: show_all(search_info, calendar, args),
    'task': lambda search_info, calendar, args: show_task(search_info, calendar, args),
    'event': lambda search_info, calendar, args: show_event(search_info, calendar, args)
}

user_choice_add = {
    'task': lambda args: add_task(args),
    'event': lambda args: add_event(args)
}

user_choice_del = {
    'all': lambda args: del_all(args),
    'task': lambda args: del_task(args),
    'event': lambda args: del_event(args)
}

user_choice_do = {
    'all': lambda args: do_all(args),
    'task': lambda args: do_task(args),
    'event': lambda args: do_event(args)
}

user_choice_remove = {
    'all': lambda args: remove_all(args),
    'task': lambda args: remove_task(args),
    'event': lambda args: remove_event(args)
}

user_choice_edit = {
    'task': lambda args: edit_task(args),
    'event': lambda args: edit_event(args)
}

user_choice_check = {
    'all': lambda args: check_all(args),
    'task': lambda args: check_task(args),
    'event': lambda args: check_event(args)
}

def add_user(args):
    db.add_user(args.name)

def show(args):
    search_info = make_search_info(None, args)
    cal = con.nxCalendar(datetime.today())
    user_choice_show.get(args.kind)(search_info, cal, args)


def add(args):
    user_choice_add.get(args.kind)(args)


def delete(args):
    user_choice_del.get(args.kind)(args)


def do(args):
    user_choice_do.get(args.kind)(args)


def remove(args):
    user_choice_remove.get(args.kind)(args)


def edit(args):
    user_choice_edit.get(args.kind)(args)


def check(args):
    daemon = lib.MyDaemon('/tmp/nxtodo_daemon.pid')
    if args.kind == 'stop':
        daemon.stop()
        return
    search_info = user_choice_check.get(args.kind)(args)
    if search_info.instance == lib.enums.Instances.all:
        search_info.instance = lib.enums.Instances.task
        notifications_task = db.check(search_info, lib.enums.Styles.terminal)
        search_info.instance = lib.enums.Instances.event
        notifications_event = db.check(search_info, lib.enums.Styles.terminal)
        notifications = notifications_task + notifications_event
    else:
        notifications = db.check(search_info, lib.enums.Styles.terminal)
        lib.enums.print_notifications(notifications)
    if args.background:
        daemon.start(db, search_info)


def show_task(search_info, calendar, args):
    search_info.instance = lib.enums.Instances.task
    founded_tasks = db.show(search_info)
    calendar.linked_objects += [con.ColoredDate(task.deadline.year, task.deadline.month,
                                                  task.deadline.day, int(config['colors']['taskbg']))
                           for task in founded_tasks]
    calendar.show(config)
    lib.functions.print_list(founded_tasks, args)


def show_event(search_info, calendar, args):
    search_info.instance = lib.enums.Instances.event
    founded_events = db.show(search_info)
    calendar.linked_objects += [con.ColoredDate(event.from_datetime.year, event.from_datetime.month,
                                                  event.from_datetime.day, int(config['colors']['eventbg']))
                           for event in founded_events]
    calendar.show(config)
    lib.functions.print_list(founded_events, args)


def show_all(search_info, calendar, args):
    search_info.instance = lib.enums.Instances.task
    founded_tasks = db.show(search_info)
    search_info.instance = lib.enums.Instances.event
    founded_events = db.show(search_info)
    calendar.linked_objects += [con.ColoredDate(task.deadline.year, task.deadline.month,
                                                  task.deadline.day, int(config['colors']['taskbg']))
                           for task in founded_tasks]
    calendar.linked_objects += [con.ColoredDate(event.from_datetime.year, event.from_datetime.month,
                                                  event.from_datetime.day, int(config['colors']['eventbg']))
                           for event in founded_events]
    calendar.show(config)
    print('{csbg}{csfg}Tasks:{ce}'.format(csbg=bg('229'), csfg=fg(235), ce=attr('reset')))
    lib.functions.print_list(founded_tasks, args)
    print('{csbg}{csfg}Events:{ce}'.format(csbg=bg('indian_red_1a'), csfg=fg(235), ce=attr('reset')))
    lib.functions.print_list(founded_events, args)


def add_task(args):
    #try:
    #    deadline = lib.parse_datetime.parse_datetime(args.deadline, config['date_formats']['ordinary'])
    #    parent = lib.functions.Parent(args.title, deadline)
    #    reminder = lib.Reminder.parse_create(args, deadline, parent, lib.enums.Instances.task)
    #except ValueError:
    #    return
    db.add_task(args.title, args.description, 'will de reminder', args.category,
                args.deadline, args.priority, args.status, args.subtasks)


def add_event(args):
    try:
        from_datetime = lib.parse_datetime.parse_datetime(args.fromdt, config['date_formats']['ordinary'])
        to_datetime = lib.parse_datetime.parse_datetime(args.todt, config['date_formats']['ordinary'])
        parent = lib.functions.Parent(args.title, from_datetime, to_datetime)
        reminder = lib.Reminder.parse_create(args, from_datetime, parent, lib.enums.Instances.event)
    except ValueError:
        return
    db.add_event(args.title, args.description, reminder, args.category, from_datetime,
                 to_datetime, args.place, args.participants)


def del_all(args):
    del_task(args)
    del_event(args)


def del_task(args):
    search_info = make_search_info(lib.enums.Instances.task, args)
    db.delete(search_info)


def del_event(args):
    search_info = make_search_info(lib.enums.Instances.event, args)
    db.delete(search_info)


def do_all(args):
    do_task(args)
    do_event(args)


def do_task(args):
    search_info = make_search_info(lib.enums.Instances.task, args)
    db.do(search_info)


def do_event(args):
    search_info = make_search_info(lib.enums.Instances.event, args)
    db.do(search_info)


def remove_all(args):
    remove_task(args)
    remove_event(args)


def remove_task(args):
    search_info = make_search_info(lib.enums.Instances.task, args)
    db.remove(search_info)


def remove_event(args):
    search_info = make_search_info(lib.enums.Instances.event, args)
    db.remove(search_info)


def check_all(args):
    search_info = make_search_info(lib.enums.Instances.all, args)
    return search_info


def check_task(args):
    search_info = make_search_info(lib.enums.Instances.task, args)
    return search_info


def check_event(args):
    search_info = make_search_info(lib.enums.Instances.event, args)
    return search_info


def make_search_info(instance, args):
    if args.all:
        return lib.functions.SearchInfo(instance, args.status, None, None, True)
    for attribute in ['title', 'category']:
        if getattr(args, attribute) is not None and getattr(args, attribute) != False :
            return lib.functions.SearchInfo(instance, args.status, attribute, getattr(args, attribute), False)
    return None


def initialize():
    #global config
    #config_path = os.path.join('/', 'home', getpass.getuser(), '.nxtodo', 'config', 'config.ini')
    #config = configparser.ConfigParser()
    #config.read(config_path)
    global db
    db = lib.Database()
    #db.load(config)


def main():

    initialize()

    #arguments = 'del event -t testiruEm'.split()
    #arguments = 'add task TESTtask -d 2018/04/22 19:00 -rf 2018/04/05 13:00 -ri 0:0:0:5 -i 0:0:0:2 -wd sun'.split()
    #arguments = 'add task testask -d 2018/01/01 12:00'.split()
    arguments = 'show all -t t1'.split()
    args = con.parse(arguments)
    user_choice_command.get(args.command, lambda args: print("No such command."))(args)


if __name__ == "__main__":
    main()
