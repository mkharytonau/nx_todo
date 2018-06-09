from django.core.exceptions import ObjectDoesNotExist

from .common import identify_user
from nxtodo import queries
from nxtodo.thirdparty import (
    CompletionError
)


USER_CHOICE_COMPLETE = {
    'task': lambda args, config: complete_task(args, config),
    'event': lambda args, config: complete_event(args, config)
}


def complete(args, config):
    USER_CHOICE_COMPLETE.get(args.kind)(args, config)


def complete_task(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.complete_task(user, args.id)
    except ObjectDoesNotExist as e:
        print(e)
    except CompletionError as e:
        print(e)
    except PermissionError as e:
        print(e)


def complete_event(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.complete_event(user, args.id)
    except ObjectDoesNotExist as e:
        print(e)
    except PermissionError as e:
        print(e)