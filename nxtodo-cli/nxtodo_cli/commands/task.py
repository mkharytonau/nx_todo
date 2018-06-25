import sys
from datetime import datetime

from nxtodo import queries
from nxtodo.common import (
    Owner,
    AccessLevels
)
from nxtodo.common.exceptions import ObjectDoesNotFound
from nxtodo_cli.commands.common import with_printing_exception
from nxtodo_cli.displaying import (
    ColoredDate,
    nxCalendar,
)
from nxtodo_cli.displaying import (
    show_task_table,
    show_notification_table
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


@with_printing_exception
def add_task(user_name, args):
    owners = [Owner(user_name, AccessLevels.EDIT.value)]
    if args.owners:
        owners += args.owners
    task_id = queries.add_task(
        user_name, args.title, args.description, args.category,
        args.deadline, args.priority, owners, args.reminders,
        args.subtasks
    )
    print(task_id)


def show_task(user_name, args, config):
    try:
        tasks = queries.get_tasks(
            user_name, args.title, args.category, args.deadline,
            args.priority, args.status, args.id
        )
    except ObjectDoesNotFound as e:
        print(e, file=sys.stderr)
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
        print(e, file=sys.stderr)
        show_task_table(tasks, config)
        return

    calendar.show(month_num)
    show_task_table(tasks, config)


def check_task(user_name, args, config):
    try:
        notifications = queries.get_tasks_notifications(
            user_name, args.title, args.category, args.deadline,
            args.priority, args.status, args.id
        )
    except Exception as e:
        print(e, file=sys.stderr)
        return

    show_notification_table(notifications, config)


@with_printing_exception
def complete_task(user_name, args):
    queries.complete_task(user_name, args.id)


@with_printing_exception
def edit_task(user_name, args):
    queries.edit_task(user_name, args.id, args.title, args.description,
                      args.category, args.deadline, args.priority)


@with_printing_exception
def remove_task(user_name, args):
    queries.remove_task(user_name, args.id)


@with_printing_exception
def share_task(user_name, args):
    queries.add_owners_to_task(user_name, args.id, args.owners)


@with_printing_exception
def unshare_task(user_name, args):
    queries.remove_owners_from_task(user_name, args.id, args.owners)


@with_printing_exception
def add_tasks_to_plan(user_name, args):
    queries.add_tasks_to_plan(user_name, args.plan, args.ids)


@with_printing_exception
def remove_tasks_from_plan(user_name, args):
    queries.remove_tasks_from_plan(user_name, args.plan, args.ids)
