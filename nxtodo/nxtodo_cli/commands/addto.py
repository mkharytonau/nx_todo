from django.core.exceptions import ObjectDoesNotExist

from nxtodo import queries
from .identify_user import identify_user

user_choice_addto = {
    'task': lambda args, config: addto_task(args, config),
    'event': lambda args, config: addto_event(args, config)
}

user_choice_addto_task = {
    'reminders': lambda args, config: addto_task_reminders(args, config),
    'subtasks': lambda args, config: addto_task_subtasks(args, config),
    'owners': lambda args, config: addto_task_owners(args, config)
}

user_choice_addto_event = {
    'reminders': lambda args, config: addto_event_reminders(args, config),
    'participants': lambda args, config: addto_event_participants(args, config)
}


def addto(args, config):
    user_choice_addto.get(args.kind)(args, config)


def addto_task(args, config):
    for attribute in ['reminders', 'subtasks', 'owners']:
        if getattr(args, attribute) is not None:
            user_choice_addto_task.get(attribute)(args, config)


def addto_event(args, config):
    for attribute in ['reminders', 'participants']:
        if getattr(args, attribute) is not None:
            user_choice_addto_event.get(attribute)(args, config)


def addto_task_reminders(args, config):
    user = identify_user(args, config)
    if user is None:
        return
    try:
        queries.add_reminders_to_task(user, args.id, args.reminders)
    except ObjectDoesNotExist as e:
        print(e)


def addto_task_subtasks(args, config):
    pass


def addto_task_owners(args, config):
    user = identify_user(args, config)
    if user is None:
        return
    try:
        queries.add_owners_to_task(user, args.id, args.owners)
    except ObjectDoesNotExist as e:
        print(e)


def addto_event_reminders(args, config):
    user = identify_user(args, config)
    if user is None:
        return
    try:
        queries.add_reminders_to_event(user, args.id, args.reminders)
    except ObjectDoesNotExist as e:
        print(e)


def addto_event_participants(args, config):
    pass