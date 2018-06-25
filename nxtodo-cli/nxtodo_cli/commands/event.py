import sys
from datetime import datetime

from nxtodo.common.exceptions import ObjectDoesNotFound
from nxtodo_cli.commands.common import with_printing_exception
from nxtodo import queries
from nxtodo.common import (
    Owner,
    AccessLevels
)
from nxtodo_cli.displaying import (
    show_event_table,
    show_notification_table
)
from nxtodo_cli.displaying import (
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


@with_printing_exception
def add_event(user_name, args):
    participants = [Owner(user_name, AccessLevels.EDIT.value)]
    if args.participants:
        participants += args.participants
    event_id = queries.add_event(
        user_name, args.title, args.fromdt, args.todt,
        args.description, args.category, args.priority,
        args.place, participants, args.reminders
    )
    print(event_id)


def show_event(user_name, args, config):
    try:
        events = queries.get_events(user_name, args.title, args.category,
                                    args.fromdt, args.priority, args.status,
                                    args.place, args.id)
    except ObjectDoesNotFound as e:
        print(e, file=sys.stderr)
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
        print(e, file=sys.stderr)
        show_event_table(events, config)
        return

    calendar.show(month_num)
    show_event_table(events, config)


def check_event(user_name, args, config):
    try:
        notifications = queries.get_events_notifications(
            user_name, args.title, args.category, args.fromdt,
            args.priority, args.status, args.place, args.id
        )
    except Exception as e:
        print(e, file=sys.stderr)
        return

    show_notification_table(notifications, config)


@with_printing_exception
def complete_event(user_name, args):
    queries.complete_event(user_name, args.id)


@with_printing_exception
def edit_event(user_name, args):
    queries.edit_event(user_name, args.id, args.title, args.description,
                       args.category, args.priority, args.fromdt,
                       args.todt, args.place)


@with_printing_exception
def remove_event(user_name, args):
    queries.remove_event(user_name, args.id)


@with_printing_exception
def share_event(user_name, args):
    queries.add_participants_to_event(user_name, args.id, args.participants)


@with_printing_exception
def unshare_event(user_name, args):
    queries.remove_participants_from_event(user_name, args.id,
                                           args.participants)


@with_printing_exception
def add_events_to_plan(user_name, args):
    queries.add_events_to_plan(user_name, args.plan, args.ids)


@with_printing_exception
def remove_events_from_plan(user_name, args):
    queries.remove_events_from_plan(user_name, args.plan, args.ids)
