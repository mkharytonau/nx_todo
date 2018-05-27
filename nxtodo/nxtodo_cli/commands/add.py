from django.core.exceptions import ObjectDoesNotExist
from nxtodo_cli import parse_datetime
from nxtodo_cli import Formats
from nxtodo import queries
from .identify_user import identify_user


user_choice_add = {
    'user': lambda args, config: add_user(args, config),
    'task': lambda args, config: add_task(args, config),
    'event': lambda args, config: add_event(args, config),
    'reminder': lambda args, config: add_reminder(args, config)
}


def add(args, config):
    user_choice_add.get(args.kind)(args, config)


def add_user(args, config):
    queries.add_user(args.name)


def add_task(args, config):
    try:
        deadline = parse_datetime(args.deadline, Formats.datetime,
                                  config['date_formats'][Formats.datetime.value])
    except ValueError:
        print('Error when parsing, please check the entered data and formats in the config file.')
        return

    user = identify_user(args, config)
    if user is None:
        return

    try:
        queries.add_task(user, args.title, args.description, args.category, deadline,
                         args.priority, args.status, args.owners)
    except ObjectDoesNotExist as e:
        print(e)


def add_event(args, config):
    try:
        from_datetime = parse_datetime(args.fromdt, Formats.datetime,
                                       config['date_formats'][Formats.datetime.value])
        to_datetime = parse_datetime(args.todt, Formats.datetime,
                                     config['date_formats'][Formats.datetime.value])
    except ValueError:
        print('Error when parsing, please check the entered data and formats in the config file.')
        return

    user = identify_user(args, config)
    if user is None:
        return

    try:
        queries.add_event(user, args.title, args.description, args.category, from_datetime,
                          to_datetime, args.place, args.participants)
    except ObjectDoesNotExist as e:
        print(e)


def add_reminder(args, config):
    error_message = 'Error when parsing, please check the entered data and formats in the config file.'
    try:
        start_remind_before = parse_datetime(args.remind_before, Formats.timedelta,
                                             config['date_formats'][Formats.timedelta.value])
        start_remind_from = parse_datetime(args.remind_from, Formats.datetime,
                                           config['date_formats'][Formats.datetime.value])
        remind_in = parse_datetime(args.remind_in, Formats.timedelta,
                                   config['date_formats'][Formats.timedelta.value])
        datetimes = parse_datetime(args.datetimes, Formats.datetime_list,
                                   config['date_formats'][Formats.datetime_list.value])
        interval = parse_datetime(args.interval, Formats.timedelta,
                                  config['date_formats'][Formats.timedelta.value])
        weekdays = parse_datetime(args.weekdays, Formats.weekdays,
                                  config['date_formats'][Formats.weekdays.value])
    except ValueError:
        print(error_message)
        return
    except IndexError:
        print(error_message)
        return


    user = identify_user(args, config)
    if user is None:
        return

    try:
        queries.add_reminder(user, start_remind_before, start_remind_from,
                         remind_in, datetimes, interval, weekdays)
    except ObjectDoesNotExist:
        print('User does not exist, please, create a new or select another one.')
        return