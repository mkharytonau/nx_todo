from datetime import datetime
from .identify_user import identify_user
from nxtodo import queries
from nxtodo_cli import nxCalendar
from nxtodo_cli import ColoredDate
from nxtodo_cli import show_task_table


user_choice_show = {
    'all': lambda args, config: show_all(args, config),
    'task': lambda args, config: show_task(args, config),
    'event': lambda args, config: show_event(args, config)
}


def show(args, config):
    user_choice_show.get(args.kind)(args, config)


def show_all(args, config):
    pass
    #calendar.linked_objects += [con.ColoredDate(task.deadline.year, task.deadline.month,
    #                                              task.deadline.day, int(config['colors']['taskbg']))
    #                       for task in founded_tasks]
    #calendar.linked_objects += [con.ColoredDate(event.from_datetime.year, event.from_datetime.month,
    #                                              event.from_datetime.day, int(config['colors']['eventbg']))
    #                       for event in founded_events]
    #calendar.show(config)


def show_task(args, config):
    user = identify_user(args, config)
    try:
        tasks = queries.get_tasks(user, args.title, args.category, args.priority, args.status)
    except Exception as e:
        print(e)
        return
    calendar = nxCalendar(datetime.today())
    linked_objects = [ColoredDate(task.deadline.date(), int(config['colors']['task_bg']),
                                  int(config['colors']['foreground']))
                      for task in tasks if task.deadline is not None]
    calendar.linked_objects += linked_objects
    calendar.show(config)
    show_task_table(tasks, config)


def show_event(args, config):
    search_info.instance = lib.enums.Instances.event
    founded_events = db.show(user, search_info)
    #calendar.linked_objects += [con.ColoredDate(event.from_datetime.year, event.from_datetime.month,
    #                                              event.from_datetime.day, int(config['colors']['eventbg']))
    #                       for event in founded_events]
    calendar.show(config)
    lib.functions.print_list(founded_events, config, args)