#!/usr/bin/python3

import parser
from datetime import datetime
from nxtodo import Database
from nxtodo import MyDaemon
from nxtodo import Reminder
from nxtodo import thirdparty
from nxtodo import parse_datetime
from nxtodo import nxcalendar
from nxtodo import Task
from nxtodo import Event
from colored import bg, fg, attr


user_choice_command = {
    'show': lambda args: show(args),
    'add': lambda args: add(args),
    'del': lambda args: delete(args),
    'edit': lambda args: edit(args),
    'check': lambda args: check(args)
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

user_choice_edit = {
    'task': lambda args: edit_task(args),
    'event': lambda args: edit_event(args)
}

user_choice_check = {
    'all': lambda args: check_all(args),
    'task': lambda args: check_task(args),
    'event': lambda args: check_event(args)
}


def show(args):
    search_info = make_search_info(None, args)
    cal = nxcalendar.nxCalendar(datetime.today())
    if args.kind == 'task':
        search_info.instance = thirdparty.Classes.task
        founded_tasks = db.show(search_info)
        cal.linked_objects += [nxcalendar.ColoredDate(task.deadline.year, task.deadline.month,
                                                      task.deadline.day, thirdparty.Colors.taskbg)
                               for task in founded_tasks]
        cal.show(3)
        thirdparty.print_list(founded_tasks, args)
    if args.kind == 'event':
        search_info.instance = thirdparty.Classes.event
        founded_events = db.show(search_info)
        cal.linked_objects += [nxcalendar.ColoredDate(event.from_datetime.year, event.from_datetime.month,
                                                      event.from_datetime.day, thirdparty.Colors.eventbg)
                               for event in founded_events]
        cal.show(3)
        thirdparty.print_list(founded_events, args)
    if args.kind == 'all':
        search_info.instance = thirdparty.Classes.task
        founded_tasks = db.show(search_info)
        search_info.instance = thirdparty.Classes.event
        founded_events = db.show(search_info)
        cal.linked_objects += [nxcalendar.ColoredDate(task.deadline.year, task.deadline.month,
                                                      task.deadline.day, thirdparty.Colors.taskbg)
                               for task in founded_tasks]
        cal.linked_objects += [nxcalendar.ColoredDate(event.from_datetime.year, event.from_datetime.month,
                                                      event.from_datetime.day, thirdparty.Colors.eventbg)
                               for event in founded_events]
        cal.show(3)
        print('{csbg}{csfg}Tasks:{ce}'.format(csbg=bg('229'), csfg=fg(235), ce=attr('reset')))
        thirdparty.print_list(founded_tasks, args)
        print('{csbg}{csfg}Events:{ce}'.format(csbg=bg('indian_red_1a'), csfg=fg(235), ce=attr('reset')))
        thirdparty.print_list(founded_events, args)


def add(args):
    user_choice_add.get(args.kind)(args)


def delete(args):
    user_choice_del.get(args.kind)(args)

def edit(args):
    user_choice_edit.get(args.kind)(args)


def check(args):
    daemon = MyDaemon('/tmp/nxtodo_daemon.pid')
    if args.kind == 'stop':
        daemon.stop()
        return
    search_info = user_choice_check.get(args.kind)(args)
    if search_info.instance == thirdparty.Classes.all:
        search_info.instance = thirdparty.Classes.task
        notifications_task = db.check(search_info, thirdparty.Styles.terminal)
        search_info.instance = thirdparty.Classes.event
        notifications_event = db.check(search_info, thirdparty.Styles.terminal)
        notifications = notifications_task + notifications_event
    else:
        notifications = db.check(search_info, thirdparty.Styles.terminal)
    thirdparty.print_notifications(notifications)
    if args.background:
        daemon.start(db, search_info)


def add_task(args):
    try:
        deadline = parse_datetime.parse_datetime(args.deadline, thirdparty.Formats.ordinary)
        parent = thirdparty.Parent(args.title, deadline)
        reminder = Reminder.parse_create(args, deadline, parent, thirdparty.Classes.task)
    except ValueError:
        return
    task = Task(
        args.title,
        args.description,
        reminder,
        args.category,
        args.owners,
        deadline,
        args.priority,
        args.status,
        args.subtasks
    )
    db.add(thirdparty.Classes.task, task)


def add_event(args):
    try:
        from_datetime = parse_datetime.parse_datetime(args.fromdt, thirdparty.Formats.ordinary)
        to_datetime = parse_datetime.parse_datetime(args.todt, thirdparty.Formats.ordinary)
        parent = thirdparty.Parent(args.title, from_datetime, to_datetime)
        reminder = Reminder.parse_create(args, from_datetime, parent, thirdparty.Classes.event)
    except ValueError:
        return
    event = Event(
        args.title,
        args.description,
        reminder,
        args.category,
        from_datetime,
        to_datetime,
        args.place,
        args.participants
    )
    db.add(thirdparty.Classes.event, event)


def del_all(args):
    del_task(args)
    del_event(args)


def del_task(args):
    search_info = make_search_info(thirdparty.Classes.task, args)
    db.delete(search_info)


def del_event(args):
    search_info = make_search_info(thirdparty.Classes.event, args)
    db.delete(search_info)


def check_all(args):
    search_info = make_search_info(thirdparty.Classes.all, args)
    return search_info


def check_task(args):
    search_info = make_search_info(thirdparty.Classes.task, args)
    return search_info


def check_event(args):
    search_info = make_search_info(thirdparty.Classes.event, args)
    return search_info


def make_search_info(instance, args):
    if args.all:
        return thirdparty.SearchInfo(instance, None, None, True)
    for attribute in ['title', 'category']:
        if not getattr(args, attribute) is None:
            return thirdparty.SearchInfo(instance, attribute, getattr(args, attribute))
    return None


def initialize():
    global db
    db = Database()
    db.load()


def main():

    initialize()

    #arguments = 'del event -t testiruEm'.split()
    #arguments = 'add task TESTtask -d 2018/04/22 19:00 -rf 2018/04/05 13:00 -ri 0:0:0:5 -i 0:0:0:2 -wd sun'.split()
    arguments = 'show all -a'.split()
    args = parser.parse(arguments)
    user_choice_command.get(args.command, lambda args: print("No such command."))(args)


if __name__ == "__main__":
    main()
