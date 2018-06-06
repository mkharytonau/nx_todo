from django.core.exceptions import ObjectDoesNotExist

from nxtodo.queries import queries
from .identify_user import identify_user
from nxtodo_cli import show_notification_table


USER_CHOICE_CHECK = {
    'task': lambda args, config: check_task(args, config),
    'event': lambda args, config: check_event(args, config),
    'plan': lambda args, config: check_event(args, config)
}


def check(args, config):
    USER_CHOICE_CHECK.get(args.kind)(args, config)


def check_task(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        notifications = queries.check_tasks(user, args.title, args.category,
                                            args.priority, args.status,
                                            args.id)
    except Exception as e:
        print(e)
        return

    show_notification_table(notifications, config)


def check_event(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        notifications = queries.check_events(user, args.title, args.category,
                                             args.priority, args.status,
                                             args.place, args.id)
    except Exception as e:
        print(e)
        return

    show_notification_table(notifications, config)


def check_plan(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.check_plans(user, args.title, args.category, args.priority,
                            args.status, args.id)
    except ObjectDoesNotExist as e:
        print(e)
        return
