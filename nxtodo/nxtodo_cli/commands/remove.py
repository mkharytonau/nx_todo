from django.core.exceptions import ObjectDoesNotExist

from .common import identify_user
from nxtodo import queries


USER_CHOICE_REMOVE = {
    'task': lambda args, config: remove_task(args, config),
    'event': lambda args, config: remove_event(args, config),
    'plan': lambda args, config: remove_plan(args, config),
    'reminder': lambda args, config: remove_reminder(args, config)
}


def remove(args, config):
    USER_CHOICE_REMOVE.get(args.kind)(args, config)


def remove_task(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.remove_task(user, args.id)
    except ObjectDoesNotExist as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_event(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.remove_event(user, args.id)
    except ObjectDoesNotExist as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_plan(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.remove_plan(user, args.id)
    except ObjectDoesNotExist as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_reminder(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.remove_reminder(user, args.id)
    except ObjectDoesNotExist as e:
        print(e)
    except PermissionError as e:
        print(e)