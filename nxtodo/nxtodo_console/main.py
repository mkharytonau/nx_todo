#!/usr/bin/python3.6


import configparser
from colored import bg, fg, attr
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from datetime_parser import parse_datetime
from datetime_parser import Formats
from cmd_parser import parse
from nxtodo_lib import queries


user_choice_command = {
    'show': lambda args, config: show(args, config),
    'add': lambda args, config: add(args, config),
    'addto': lambda args, config: addto(args, config),
    'del': lambda args, config: delete(args, config),
    'do': lambda args, config: do(args, config),
    'remove': lambda args, config: remove(args, config),
    'edit': lambda args, config: edit(args, config),
    'check': lambda args, config: check(args, config)
}

user_choice_show = {
    'all': lambda user, config, search_info, calendar, args:
            show_all(user, config, search_info, calendar, args),
    'task': lambda user, config, search_info, calendar, args:
            show_task(user, config, search_info, calendar, args),
    'event': lambda user, config, search_info, calendar, args:
            show_event(user, config, search_info, calendar, args)
}

user_choice_add = {
    'user': lambda args, config: add_user(args, config),
    'task': lambda args, config: add_task(args, config),
    'event': lambda args, config: add_event(args, config),
    'reminder': lambda args, config: add_reminder(args, config)
}

user_choice_addto = {
    'task': lambda args, config: addto_task(args, config),
    'event': lambda args, config: addto_event(args, config)
}

user_choice_addto_task = {
    'reminders': lambda args, config: addto_task_reminders(args, config),
    'subtasks': lambda args, config: addto_task_subtasks(args, config),
    'owners': lambda args, config: addto_task_owners(args, config)
}

user_choice_addto_event = {
    'reminders': lambda args, config: addto_event_reminders(args, config),
    'participants': lambda args, config: addto_event_participants(args, config)
}

user_choice_del = {
    'all': lambda args, config: del_all(args, config),
    'task': lambda args, config: del_task(args, config),
    'event': lambda args, config: del_event(args, config)
}

user_choice_do = {
    'all': lambda args, config: do_all(args, config),
    'task': lambda args, config: do_task(args, config),
    'event': lambda args, config: do_event(args, config)
}

user_choice_remove = {
    'all': lambda args, config: remove_all(args, config),
    'task': lambda args, config: remove_task(args, config),
    'event': lambda args, config: remove_event(args, config)
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


def show(args, config):
    search_info = make_search_info(None, args)
    cal = con.nxCalendar(datetime.today())
    user_choice_show.get(args.kind)(user, config, search_info, cal, args)


def add(args, config):
    user_choice_add.get(args.kind)(args, config)


def addto(args, config):
    user_choice_addto.get(args.kind)(args, config)


def delete(args, config):
    user_choice_del.get(args.kind)(args, config)


def do(args, config):
    user_choice_do.get(args.kind)(args, config)


def remove(args, config):
    user_choice_remove.get(args.kind)(args, config)


def edit(args, config):
    user_choice_edit.get(args.kind)(args, config)


def check(db, args, config):
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


def add_user(args, config):
    queries.add_user(args.name)


def add_task(args, config):
    try:
        deadline = parse_datetime(args.deadline, Formats.datetime, config)
    except ValueError:
        print('Error when parsing, please check the entered data and formats in the config file.')
        return

    user = identify_user(args, config)
    if user is None:
        return

    try:
        queries.add_task(user, args.title, args.description, args.category, deadline,
                         args.priority, args.status, args.owners)
    except ObjectDoesNotExist as e:
        print(e)


def add_event(args, config):
    try:
        from_datetime = parse_datetime(args.fromdt, Formats.datetime, config)
        to_datetime = parse_datetime(args.todt, Formats.datetime, config)
    except ValueError:
        print('Error when parsing, please check the entered data and formats in the config file.')
        return

    user = identify_user(args, config)
    if user is None:
        return

    try:
        queries.add_event(user, args.title, args.description, args.category, from_datetime,
                          to_datetime, args.place, args.participants)
    except ObjectDoesNotExist as e:
        print(e)


def add_reminder(args, config):
    try:
        start_remind_before = parse_datetime(args.remind_before, Formats.timedelta, config)
        start_remind_from = parse_datetime(args.remind_from, Formats.datetime, config)
        remind_in = parse_datetime(args.remind_in, Formats.timedelta, config)
        datetimes = parse_datetime(args.datetimes, Formats.datetime_list, config)
        interval = parse_datetime(args.interval, Formats.timedelta, config)
        weekdays = parse_datetime(args.weekdays, Formats.weekdays, config)
    except ValueError:
        print('Error when parsing, please check the entered data and formats in the config file.')
        return

    user = identify_user(args, config)
    if user is None:
        return

    try:
        queries.add_reminder(user, start_remind_before, start_remind_from,
                         remind_in, datetimes, interval, weekdays)
    except ObjectDoesNotExist:
        print('User does not exist, please, create a new or select another one.')
        return


def addto_task(args, config):
    for attribute in ['reminders', 'subtasks', 'owners']:
        if getattr(args, attribute) is not None:
            user_choice_addto_task.get(attribute)(args, config)


def addto_event(args, config):
    for attribute in ['reminders', 'participants']:
        if getattr(args, attribute) is not None:
            user_choice_addto_event.get(attribute)(args, config)


def addto_task_reminders(args, config):
    user = identify_user(args, config)
    if user is None:
        return
    try:
        queries.add_reminders_to_task(user, args.id, args.reminders)
    except ObjectDoesNotExist as e:
        print(e)


def addto_task_subtasks(args, config):
    pass


def addto_task_owners(args, config):
    user = identify_user(args, config)
    if user is None:
        return
    try:
        queries.add_owners_to_task(user, args.id, args.owners)
    except ObjectDoesNotExist as e:
        print(e)


def addto_event_reminders(args, config):
    user = identify_user(args, config)
    if user is None:
        return
    try:
        queries.add_reminders_to_event(user, args.id, args.reminders)
    except ObjectDoesNotExist as e:
        print(e)


def addto_event_participants(args, config):
    pass


def del_all(db, args, config):
    del_task(db, args, config)
    del_event(db, args, config)


def del_task(db, args, config):
    search_info = make_search_info(lib.enums.Instances.task, args)
    db.delete(user, search_info)


def del_event(db, args, config):
    search_info = make_search_info(lib.enums.Instances.event, args)
    db.delete(user, search_info)


def do_all(db, args, config):
    do_task(db, args, config)
    do_event(db, args, config)


def do_task(db, args, config):
    search_info = make_search_info(lib.enums.Instances.task, args)
    db.do(user, search_info)


def do_event(db, args, config):
    search_info = make_search_info(lib.enums.Instances.event, args)
    db.do(user, search_info)


def remove_all(db, args, config):
    remove_task(db, args, config)
    remove_event(db, args, config)


def remove_task(db, args, config):
    search_info = make_search_info(lib.enums.Instances.task, args)
    db.remove(user, search_info)


def remove_event(db, args, config):
    search_info = make_search_info(lib.enums.Instances.event, args)
    db.remove(user, search_info)


def check_all(db, args, config):
    search_info = make_search_info(lib.enums.Instances.all, args)
    return search_info


def check_task(db, args, config):
    search_info = make_search_info(lib.enums.Instances.task, args)
    return search_info


def check_event(db, args, config):
    search_info = make_search_info(lib.enums.Instances.event, args)
    return search_info


def initialize():
    config_path = '/home/kharivitalij/nx_todo/config.ini'
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def identify_user(args, config):
    try:
        return args.user if args.user is not None else config['user']['name']
    except KeyError:
        print('Error during user definition, please, check your config file.')
        return None


def main():

    # arguments = 'del event -t testiruEm'.split()
    # arguments = 'add task TESTtask -d 2018/04/22 19:00 -rf 2018/04/05 13:00 -ri 0:0:0:5 -i 0:0:0:2 -wd sun'.split()
    # arguments = 'add task testask -d 2018/01/01 12:00'.split()
    #arguments = 'add reminder -rf 2018/04/03 12:01:02 -ri 3:2:2:1 -dt 2017/04/03 12:01:02 2016/04/03 19:01:00  -wd mon wed -i 0:0:1:1'.split()
    #arguments = 'addto task 2 -o nikitos123'.split()
    arguments = 'add task task3 -d 2018/03/30 19:00:23 -o sveta vital123'.split()
    args = parse(arguments)

    config = initialize()

    user_choice_command.get(args.command, lambda: print("No such command."))(args, config)


if __name__ == "__main__":
    main()
