from datetime import datetime

from nxtodo.thirdparty.exceptions import ObjectDoesNotFound
from nxtodo import queries
from nxtodo.thirdparty import (
    Owner,
    AccessLevels
)
from nxtodo_cli.view import (
    show_event_table,
    show_notification_table
)
from nxtodo_cli.nxcalendar import (
    ColoredDate,
    nxCalendar,
)

USER_CHOICE_EVENT = {
    'add': lambda user, args, config: add_event(user, args),
    'show': lambda user, args, config: show_event(user, args, config),
    'check': lambda user, args, config: check_event(user, args, config),
    'complete': lambda user, args, config: complete_event(user, args),
    'edit': lambda user, args, config: edit_event(user, args),
    'remove': lambda user, args, config: remove_event(user, args),
    'share': lambda user, args, config: share_event(user, args),
    'unshare': lambda user, args, config: unshare_event(user, args),
    'toplan': lambda user, args, config: add_events_to_plan(user, args),
    'fromplan': lambda user, args, config: remove_events_from_plan(user, args),
}


def handle_event(user, args, config):
    USER_CHOICE_EVENT.get(args.command)(user, args, config)


def add_event(user_name, args):
    try:
        participants = [Owner(user_name, AccessLevels.EDIT.value)]
        if args.participants:
            participants += args.participants
        event_id = queries.add_event(
            user_name, args.title, args.fromdt, args.todt,
            args.description, args.category, args.priority,
            args.place, participants, args.reminders
        )
        print(event_id)
    except ObjectDoesNotFound as e:
        print(e)


def show_event(user_name, args, config):
    try:
        events = queries.get_events(user_name, args.title, args.category,
                                    args.fromdt, args.priority, args.status,
                                    args.place, args.id)
    except ObjectDoesNotFound as e:
        print(e)
        return

    calendar = nxCalendar(datetime.today())
    linked_objects = []
    try:
        for event in events:
            if event.from_datetime is not None:
                cdate = ColoredDate(event.from_datetime.date(),
                                    int(config['colors']['event_bg']),
                                    int(config['colors']['foreground']))
                linked_objects.append(cdate)
    except KeyError:
        print("Your config file is incorrect, please, check 'colors' section.")
        show_event_table(events, config)
        return
    calendar.linked_objects += linked_objects
    try:
        month_num = int(config['nxcalendar']['month_num'])
        if not 0 < month_num < 7:
            raise ValueError('month_num is integer in range(0, 7),'
                             'please, check your config file.')
    except ValueError as e:
        print(e)
        show_event_table(events, config)
        return

    calendar.show(month_num)
    show_event_table(events, config)


def check_event(user_name, args, config):
    try:
        notifications = queries.check_events(
            user_name, args.title, args.category, args.fromdt,
            args.priority, args.status, args.place, args.id
        )
    except Exception as e:
        print(e)
        return

    show_notification_table(notifications, config)


def complete_event(user_name, args):
    try:
        queries.complete_event(user_name, args.id)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def edit_event(user_name, args):
    try:
        queries.edit_event(user_name, args.id, args.title, args.description,
                           args.category, args.priority, args.fromdt,
                           args.todt, args.place)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_event(user_name, args):
    try:
        queries.remove_event(user_name, args.id)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def share_event(user_name, args):
    try:
        queries.add_participants_to_event(user_name, args.id,
                                          args.participants)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def unshare_event(user_name, args):
    try:
        queries.remove_participants_from_event(user_name, args.id,
                                               args.participants)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def add_events_to_plan(user_name, args):
    try:
        queries.add_events_to_plan(user_name, args.plan, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_events_from_plan(user_name, args):
    try:
        queries.remove_events_from_plan(user_name, args.plan, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)
