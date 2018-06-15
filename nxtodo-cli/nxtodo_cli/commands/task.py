from datetime import datetime

from nxtodo import queries
from nxtodo.thirdparty import (
    Owner,
    AccessLevels
)
from nxtodo.thirdparty.exceptions import (
    ObjectDoesNotFound,
    CompletionError
)
from nxtodo_cli.displaying import (
    show_task_table,
    show_notification_table
)
from nxtodo_cli.displaying import (
    ColoredDate,
    nxCalendar,
)

USER_CHOICE_TASK = {
    'add': lambda user, args, config: add_task(user, args),
    'show': lambda user, args, config: show_task(user, args, config),
    'check': lambda user, args, config: check_task(user, args, config),
    'complete': lambda user, args, config: complete_task(user, args),
    'edit': lambda user, args, config: edit_task(user, args),
    'remove': lambda user, args, config: remove_task(user, args),
    'share': lambda user, args, config: share_task(user, args),
    'unshare': lambda user, args, config: unshare_task(user, args),
    'toplan': lambda user, args, config: add_tasks_to_plan(user, args),
    'fromplan': lambda user, args, config: remove_tasks_from_plan(user, args),
}


def handle_task(user, args, config):
    USER_CHOICE_TASK.get(args.command)(user, args, config)


def add_task(user_name, args):
    try:
        owners = [Owner(user_name, AccessLevels.EDIT.value)]
        if args.owners:
            owners += args.owners
        task_id = queries.add_task(
            user_name, args.title, args.description, args.category,
            args.deadline, args.priority, owners, args.reminders,
            args.subtasks
        )
        print(task_id)
    except ObjectDoesNotFound as e:
        print(e)


def show_task(user_name, args, config):
    try:
        tasks = queries.get_tasks(
            user_name, args.title, args.category, args.deadline,
            args.priority, args.status, args.id
        )
    except ObjectDoesNotFound as e:
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


def check_task(user_name, args, config):
    try:
        notifications = queries.check_tasks(
            user_name, args.title, args.category, args.deadline,
            args.priority, args.status, args.id
        )
    except Exception as e:
        print(e)
        return

    show_notification_table(notifications, config)


def complete_task(user_name, args):
    try:
        queries.complete_task(user_name, args.id)
    except ObjectDoesNotFound as e:
        print(e)
    except CompletionError as e:
        print(e)
    except PermissionError as e:
        print(e)


def edit_task(user_name, args):
    try:
        queries.edit_task(user_name, args.id, args.title, args.description,
                          args.category, args.deadline, args.priority)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_task(user_name, args):
    try:
        queries.remove_task(user_name, args.id)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def share_task(user_name, args):
    try:
        queries.add_owners_to_task(user_name, args.id, args.owners)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def unshare_task(user_name, args):
    try:
        queries.remove_owners_from_task(user_name, args.id, args.owners)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def add_tasks_to_plan(user_name, args):
    try:
        queries.add_tasks_to_plan(user_name, args.plan, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_tasks_from_plan(user_name, args):
    try:
        queries.remove_tasks_from_plan(user_name, args.plan, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)
