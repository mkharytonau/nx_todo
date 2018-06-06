from django.core.exceptions import ObjectDoesNotExist
from nxtodo.queries import queries
from nxtodo_cli import (Formats,
                        parse_datetime)

from .identify_user import identify_user

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
        deadline = parse_datetime(args.deadline, Formats.DATETIME,
                                  config['date_formats'][
                                      Formats.DATETIME.value])
    except ValueError:
        print('Error when parsing, please check the entered data and formats '
              'in the config file.')
        return

    try:
        queries.add_task(user, args.title, args.description, args.category,
                         deadline, args.priority, args.status, args.owners)
    except ObjectDoesNotExist as e:
        print(e)


def add_event(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        from_datetime = parse_datetime(args.fromdt, Formats.DATETIME,
                                       config['date_formats'][
                                           Formats.DATETIME.value])
        to_datetime = parse_datetime(args.todt, Formats.DATETIME,
                                     config['date_formats'][
                                         Formats.DATETIME.value])
    except ValueError:
        print('Error when parsing, please check the entered data and formats '
              'in the config file.')
        return

    try:
        queries.add_event(user, args.title, args.description, args.category,
                          args.priority, args.status, from_datetime,
                          to_datetime, args.place, args.participants)
    except ObjectDoesNotExist as e:
        print(e)


def add_plan(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    try:
        queries.add_plan(user, args.title, args.description, args.category,
                         args.priority, args.status, args.tasks, args.events,
                         args.reminders)
    except ObjectDoesNotExist as e:
        print(e)


def add_reminder(args, config):
    try:
        user = identify_user(args, config)
    except KeyError as e:
        print(e)
        return

    error_message = 'Error when parsing, please check the entered data and ' \
                    'formats in the config file.'
    try:
        start_remind_before = parse_datetime(args.remind_before,
                                             Formats.TIMEDELTA,
                                             config['date_formats'][
                                                 Formats.TIMEDELTA.value])
        start_remind_from = parse_datetime(args.remind_from, Formats.DATETIME,
                                           config['date_formats'][
                                               Formats.DATETIME.value])
        stop_remind_in = parse_datetime(args.stop_in, Formats.DATETIME,
                                        config['date_formats'][
                                            Formats.DATETIME.value])
        remind_in = parse_datetime(args.remind_in, Formats.TIMEDELTA,
                                   config['date_formats'][
                                       Formats.TIMEDELTA.value])
        datetimes = parse_datetime(args.datetimes, Formats.DATETIME_LIST,
                                   config['date_formats'][
                                       Formats.DATETIME_LIST.value])
        interval = parse_datetime(args.interval, Formats.TIMEDELTA,
                                  config['date_formats'][
                                      Formats.TIMEDELTA.value])
        weekdays = parse_datetime(args.weekdays, Formats.WEEKDAYS,
                                  config['date_formats'][
                                      Formats.WEEKDAYS.value])
    except ValueError:
        print(error_message)
        return
    except IndexError:
        print(error_message)
        return

    try:
        queries.add_reminder(user, args.description, start_remind_before,
                             start_remind_from, stop_remind_in, remind_in,
                             datetimes, interval, weekdays)
    except ObjectDoesNotExist:
        print(
            'User does not exist, please, create a new or select another one.')
        return
