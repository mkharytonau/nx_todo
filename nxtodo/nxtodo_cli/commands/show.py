from datetime import datetime

from nxtodo.queries import queries
from nxtodo_cli import (ColoredDate,
                        nxCalendar,
                        show_event_table,
                        show_task_table,
                        show_plan_table,
                        show_reminder_table)

from .identify_user import identify_user

USER_CHOICE_SHOW = {
    'task': lambda args, config: show_task(args, config),
    'event': lambda args, config: show_event(args, config),
    'plan': lambda args, config: show_plan(args, config),
    'reminder': lambda args, config: show_reminder(args, config)
}


def show(args, config):
    USER_CHOICE_SHOW.get(args.kind)(args, config)


def show_task(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return
    try:
        tasks = queries.get_tasks(user, args.title, args.category,
                                  args.priority, args.status, args.id)
    except Exception as e:
        print(e)
        return

    calendar = nxCalendar(datetime.today())
    linked_objects = []
    try:
        for task in tasks:
            if task.deadline is not None:
                cdate = ColoredDate(task.deadline.date(),
                                    int(config['colors']['task_bg']),
                                    int(config['colors']['foreground']))
                linked_objects.append(cdate)
    except KeyError:
        print("Your config file is incorrect, please, check 'colors' section.")
        show_task_table(tasks, config)
        return
    calendar.linked_objects += linked_objects
    try:
        month_num = int(config['nxcalendar']['month_num'])
        if not 0 < month_num < 7:
            raise ValueError('month_num is integer in range(0, 7),'
                             'please, check your config file.')
    except ValueError as e:
        print(e)
        show_task_table(tasks, config)
        return

    calendar.show(month_num)
    show_task_table(tasks, config)


def show_event(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return
    try:
        events = queries.get_events(user, args.title, args.category,
                                    args.priority, args.status, args.place,
                                    args.id)
    except Exception as e:
        print(e)
        return

    calendar = nxCalendar(datetime.today())
    linked_objects = []
    try:
        for event in events:
            if event.from_datetime is not None:
                cdate = ColoredDate(event.from_datetime.date(),
                                    int(config['colors']['event_bg']),
                                    int(config['colors']['foreground']))
                linked_objects.append(cdate)
    except KeyError:
        print("Your config file is incorrect, please, check 'colors' section.")
        show_event_table(events, config)
        return
    calendar.linked_objects += linked_objects
    try:
        month_num = int(config['nxcalendar']['month_num'])
        if not 0 < month_num < 7:
            raise ValueError('month_num is integer in range(0, 7),'
                             'please, check your config file.')
    except ValueError as e:
        print(e)
        show_event_table(events, config)
        return

    calendar.show(month_num)
    show_event_table(events, config)


def show_plan(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        plans = queries.get_plans(user, args.title, args.category,
                                  args.priority, args.status, args.id)
    except Exception as e:
        print(e)
        return

    show_plan_table(plans, config)


def show_reminder(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        reminders = queries.get_reminders(user, args.description, args.id)
    except Exception as e:
        print(e)
        return

    show_reminder_table(reminders, config)
