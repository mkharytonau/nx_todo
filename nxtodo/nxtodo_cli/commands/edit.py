from django.core.exceptions import ObjectDoesNotExist
from nxtodo.queries import queries
from nxtodo_cli import (Formats,
                        parse_datetime)

from .identify_user import identify_user

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
        deadline = parse_datetime(
            args.deadline,
            Formats.DATETIME,
            config['date_formats'][Formats.DATETIME.value]
        )
    except ValueError:
        print('Error when parsing, please check the entered data and formats '
              'in the config file.')
        return

    try:
        queries.add_task(user, args.title, args.description, args.category,
                         deadline, args.priority, args.status, args.owners)
    except ObjectDoesNotExist as e:
        print(e)
