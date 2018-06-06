from django.core.exceptions import ObjectDoesNotExist
from nxtodo.queries import queries

from .identify_user import identify_user

USER_CHOICE_ADDTO = {
    'task': lambda args, config: addto_task(args, config),
    'event': lambda args, config: addto_event(args, config)
}

USER_CHOICE_ADDTO_TASK = {
    'reminders': lambda args, config: addto_task_reminders(args, config),
    'subtasks': lambda args, config: addto_task_subtasks(args, config),
    'owners': lambda args, config: addto_task_owners(args, config)
}

USER_CHOICE_ADDTO_EVENT = {
    'reminders': lambda args, config: addto_event_reminders(args, config),
    'participants': lambda args, config: addto_event_participants(args, config)
}


def addto(args, config):
    USER_CHOICE_ADDTO.get(args.kind)(args, config)


def addto_task(args, config):
    for attribute in ['reminders', 'subtasks', 'owners']:
        if getattr(args, attribute) is not None:
            USER_CHOICE_ADDTO_TASK.get(attribute)(args, config)


def addto_event(args, config):
    for attribute in ['reminders', 'participants']:
        if getattr(args, attribute) is not None:
            USER_CHOICE_ADDTO_EVENT.get(attribute)(args, config)


def addto_task_reminders(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.add_reminders_to_task(user, args.id, args.reminders)
    except ObjectDoesNotExist as e:
        print(e)


def addto_task_subtasks(args, config):
    pass


def addto_task_owners(args, config):
    try:
        queries.add_owners_to_task(args.id, args.owners)
    except ObjectDoesNotExist as e:
        print(e)


def addto_event_reminders(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.add_reminders_to_event(user, args.id, args.reminders)
    except ObjectDoesNotExist as e:
        print(e)


def addto_event_participants(args, config):
    try:
        queries.add_participants_to_event(args.id, args.participants)
    except ObjectDoesNotExist as e:
        print(e)
