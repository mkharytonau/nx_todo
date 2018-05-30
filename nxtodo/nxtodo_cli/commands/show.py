from datetime import datetime
from .identify_user import identify_user
from nxtodo import queries
from nxtodo_cli import nxCalendar
from nxtodo_cli import ColoredDate
from nxtodo_cli import show_task_table
from nxtodo_cli import show_event_table


user_choice_show = {
    'all': lambda args, config: show_all(args, config),
    'task': lambda args, config: show_task(args, config),
    'event': lambda args, config: show_event(args, config)
}


def show(args, config):
    user_choice_show.get(args.kind)(args, config)


def show_all(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    tasks_count = True
    try:
        tasks = queries.get_tasks(user, args.title, args.category,
                                  args.priority, args.status)
    except Exception as e:
        print(e)
        tasks_count = False

    try:
        events = queries.get_events(user, args.title, args.category,
                                  args.priority, args.status)
    except Exception as e:
        print(e)
        if not tasks_count:
            return

    calendar = nxCalendar(datetime.today())
    linked_tasks = []
    linked_events = []
    try:
        for task in tasks:
            if task.deadline is not None:
                cdate = ColoredDate(task.deadline.date(),
                                    int(config['colors']['task_bg']),
                                    int(config['colors']['foreground']))
                linked_tasks.append(cdate)
        for event in events:
            if event.from_datetime is not None:
                cdate = ColoredDate(event.from_datetime.date(),
                                    int(config['colors']['event_bg']),
                                    int(config['colors']['foreground']))
                linked_events.append(cdate)
    except KeyError:
        print("Your config file is incorrect, please, check 'colors' section.")
        show_task_table(tasks, config)
        return
    calendar.linked_objects += linked_tasks
    calendar.linked_objects += linked_events
    try:
        month_num = int(config['nxcalendar']['month_num'])
        if not 0 < month_num < 7:
            raise ValueError('month_num is integer in range(0, 7),'
                             'please, check your config file.')
    except ValueError as e:
        print(e)
        show_task_table(tasks, config)
        show_event_table(events, config)
        return
    calendar.show(month_num)

    show_task_table(tasks, config)
    show_event_table(events, config)


def show_task(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return
    try:
        id = int(args.id) if args.id is not None else None
        tasks = queries.get_tasks(user, args.title, args.category,
                                  args.priority, args.status, id)
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
        id = int(args.id) if args.id is not None else None
        events = queries.get_events(user, args.title, args.category,
                                    args.priority, args.status, args.place, id)
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