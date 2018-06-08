from django.core.exceptions import ObjectDoesNotExist
from nxtodo import queries

from .common import identify_user

USER_CHOICE_ADD = {
    'user': lambda args, config: add_user(args, config),
    'task': lambda args, config: add_task(args, config),
    'event': lambda args, config: add_event(args, config),
    'plan': lambda args, config: add_plan(args, config),
    'reminder': lambda args, config: add_reminder(args, config)
}


def add(args, config):
    USER_CHOICE_ADD.get(args.kind)(args, config)


def add_user(args, config):
    queries.add_user(args.name)


def add_task(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.add_task(
            user, args.title, args.description, args.category,
            args.deadline, args.priority, args.owners
        )
    except ObjectDoesNotExist as e:
        print(e)


def add_event(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.add_event(
            user, args.title, args.fromdt, args.todt,
            args.description, args.category, args.priority,
            args.place, args.participants
        )
    except ObjectDoesNotExist as e:
        print(e)


def add_plan(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.add_plan(
            user, args.title, args.description, args.category, args.priority,
            args.tasks, args.events, args.reminders
        )
    except ObjectDoesNotExist as e:
        print(e)


def add_reminder(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.add_reminder(
            user, args.description, args.remind_before,
            args.remind_from, args.stop_in, args.remind_in,
            args.datetimes, args.interval, args.weekdays
        )
    except ObjectDoesNotExist as e:
        print(e)
