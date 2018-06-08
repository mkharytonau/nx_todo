from django.core.exceptions import ObjectDoesNotExist
from nxtodo import queries

from .common import identify_user

USER_CHOICE_EDIT = {
    'task': lambda args, config: edit_task(args, config),
    'event': lambda args, config: edit_event(args, config),
    'plan': lambda args, config: edit_plan(args, config),
    'reminder': lambda args, config: edit_reminder(args, config),
}


def edit(args, config):
    USER_CHOICE_EDIT.get(args.kind)(args, config)


def edit_task(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.edit_task(user, args.id, args.title, args.description,
                          args.category, args.deadline, args.priority)
    except ObjectDoesNotExist as e:
        print(e)
    except PermissionError as e:
        print(e)


def edit_event(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.edit_event(user, args.id, args.title, args.description,
                           args.category, args.priority, args.fromdt,
                           args.todt, args.place)
    except ObjectDoesNotExist as e:
        print(e)
    except PermissionError as e:
        print(e)


def edit_plan(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.edit_plan(user, args.id, args.title, args.description,
                          args.category, args.priority)
    except ObjectDoesNotExist as e:
        print(e)
    except PermissionError as e:
        print(e)


def edit_reminder(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.edit_plan(
            user, args.id, args.description, args.start_remind_before,
            args.start_remind_from, args.stop_remind_in, args.remind_in,
            args.datetimes, args.interval, args.weekdays
        )
    except ObjectDoesNotExist as e:
        print(e)
    except PermissionError as e:
        print(e)
