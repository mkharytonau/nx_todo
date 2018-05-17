#!/usr/bin/python3.6

import os

#Django
from django.core.exceptions import ObjectDoesNotExist
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()

import configparser
import nxtodo_console as con
import nxtodo_lib as lib
from datetime import datetime
from colored import bg, fg, attr


user_choice_command = {
    'adduser': lambda db, user, config, args: add_user(db, user, config, args),
    'show': lambda db, user, config, args: show(db, user, config, args),
    'add': lambda db, user, config, args: add(db, user, config, args),
    'del': lambda db, user, config, args: delete(db, user, config, args),
    'do': lambda db, user, config, args: do(db, user, config, args),
    'remove': lambda db, user, config, args: remove(db, user, config, args),
    'edit': lambda db, user, config, args: edit(db, user, config, args),
    'check': lambda db, user, config, args: check(db, user, config, args)
}

user_choice_show = {
    'all': lambda db, user, config, search_info, calendar, args:
            show_all(db, user, config, search_info, calendar, args),
    'task': lambda db, user, config, search_info, calendar, args:
            show_task(db, user, config, search_info, calendar, args),
    'event': lambda db, user, config, search_info, calendar, args:
            show_event(db, user, config, search_info, calendar, args)
}

user_choice_add = {
    'task': lambda db, user, config, args: add_task(db, user, config, args),
    'event': lambda db, user, config, args: add_event(db, user, config, args)
}

user_choice_del = {
    'all': lambda db, user, config, args: del_all(db, user, config, args),
    'task': lambda db, user, config, args: del_task(db, user, config, args),
    'event': lambda db, user, config, args: del_event(db, user, config, args)
}

user_choice_do = {
    'all': lambda db, user, config, args: do_all(db, user, config, args),
    'task': lambda db, user, config, args: do_task(db, user, config, args),
    'event': lambda db, user, config, args: do_event(db, user, config, args)
}

user_choice_remove = {
    'all': lambda db, user, config, args: remove_all(db, user, config, args),
    'task': lambda db, user, config, args: remove_task(db, user, config, args),
    'event': lambda db, user, config, args: remove_event(db, user, config, args)
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


def add_user(db, user, config, args):
    db.add_user(args.name)


def show(db, user, config, args):
    search_info = make_search_info(None, args)
    cal = con.nxCalendar(datetime.today())
    user_choice_show.get(args.kind)(db, user, config, search_info, cal, args)


def add(db, user, config, args):
    user_choice_add.get(args.kind)(db, user, config, args)


def delete(db, user, config, args):
    user_choice_del.get(args.kind)(db, user, config, args)


def do(db, user, config, args):
    user_choice_do.get(args.kind)(db, user, config, args)


def remove(db, user, config, args):
    user_choice_remove.get(args.kind)(db, user, config, args)


def edit(db, user, config, args):
    user_choice_edit.get(args.kind)(db, user, config, args)


def check(db, user, config, args):
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


def show_task(db, user, config, search_info, calendar, args):
    search_info.instance = lib.enums.Instances.task
    founded_tasks = db.show(user, search_info)
    #calendar.linked_objects += [con.ColoredDate(task.deadline.year, task.deadline.month,
    #                                              task.deadline.day, int(config['colors']['taskbg']))
    #                       for task in founded_tasks]
    calendar.show(config)
    lib.functions.print_list(founded_tasks, config, args)


def show_event(db, user, config, search_info, calendar, args):
    search_info.instance = lib.enums.Instances.event
    founded_events = db.show(user, search_info)
    #calendar.linked_objects += [con.ColoredDate(event.from_datetime.year, event.from_datetime.month,
    #                                              event.from_datetime.day, int(config['colors']['eventbg']))
    #                       for event in founded_events]
    calendar.show(config)
    lib.functions.print_list(founded_events, config, args)


def show_all(db, user, config, search_info, calendar, args):
    search_info.instance = lib.enums.Instances.task
    founded_tasks = db.show(user, search_info)
    search_info.instance = lib.enums.Instances.event
    founded_events = db.show(user, search_info)
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


def add_task(db, user, config, args):
    #try:
    #    deadline = lib.parse_datetime.parse_datetime(args.deadline, config['date_formats']['ordinary'])
    #    parent = lib.functions.Parent(args.title, deadline)
    #    reminder = lib.Reminder.parse_create(args, deadline, parent, lib.enums.Instances.task)
    #except ValueError:
    #    return
    db.add_task(user, args.title, args.description, 'will de reminder', args.category,
                args.deadline, args.priority, args.subtasks)


def add_event(db, user, config, args):
    try:
        from_datetime = lib.parse_datetime.parse_datetime(args.fromdt, config['date_formats']['ordinary'])
        to_datetime = lib.parse_datetime.parse_datetime(args.todt, config['date_formats']['ordinary'])
        parent = lib.functions.Parent(args.title, from_datetime, to_datetime)
        reminder = lib.Reminder.parse_create(args, from_datetime, parent, lib.enums.Instances.event)
    except ValueError:
        return
    db.add_event(args.title, args.description, reminder, args.category, from_datetime,
                 to_datetime, args.place, args.participants)


def del_all(db, user, config, args):
    del_task(db, user, config, args)
    del_event(db, user, config, args)


def del_task(db, user, config, args):
    search_info = make_search_info(lib.enums.Instances.task, args)
    db.delete(user, search_info)


def del_event(db, user, config, args):
    search_info = make_search_info(lib.enums.Instances.event, args)
    db.delete(user, search_info)


def do_all(db, user, config, args):
    do_task(db, user, config, args)
    do_event(db, user, config, args)


def do_task(db, user, config, args):
    search_info = make_search_info(lib.enums.Instances.task, args)
    db.do(user, search_info)


def do_event(db, user, config, args):
    search_info = make_search_info(lib.enums.Instances.event, args)
    db.do(user, search_info)


def remove_all(db, user, config, args):
    remove_task(db, user, config, args)
    remove_event(db, user, config, args)


def remove_task(db, user, config, args):
    search_info = make_search_info(lib.enums.Instances.task, args)
    db.remove(user, search_info)


def remove_event(db, user, config, args):
    search_info = make_search_info(lib.enums.Instances.event, args)
    db.remove(user, search_info)


def check_all(db, user, config, args):
    search_info = make_search_info(lib.enums.Instances.all, args)
    return search_info


def check_task(db, user, config, args):
    search_info = make_search_info(lib.enums.Instances.task, args)
    return search_info


def check_event(db, user, config, args):
    search_info = make_search_info(lib.enums.Instances.event, args)
    return search_info


def make_search_info(instance, args):
    if args.all:
        return lib.functions.SearchInfo(instance, getattr(args, 'status', None), None, None, True)
    for attribute in ['title', 'category']:
        if getattr(args, attribute) is not None and getattr(args, attribute) != False:
            return lib.functions.SearchInfo(instance, getattr(args, 'status', None), attribute, getattr(args, attribute), False)
    return None


def initialize():
    config_path = '/home/kharivitalij/nx_todo/config.ini'
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def load_user(db, config):
    try:
        return db.get_user(config['user']['name'])
    except ObjectDoesNotExist:
        print("User does not exist, please check your config file or use 'adduser' command.")
        return None


def main():

    # arguments = 'del event -t testiruEm'.split()
    # arguments = 'add task TESTtask -d 2018/04/22 19:00 -rf 2018/04/05 13:00 -ri 0:0:0:5 -i 0:0:0:2 -wd sun'.split()
    # arguments = 'add task testask -d 2018/01/01 12:00'.split()
    arguments = 'show task -a'.split()
    args = con.parse(arguments)

    db = lib.Database()
    config = initialize()
    if args.command != 'adduser':
        user = load_user(db, config)
        if user is None:
            return
    else:
        user = None

    user_choice_command.get(args.command, lambda args: print("No such command."))(db, user, config, args)


if __name__ == "__main__":
    main()
