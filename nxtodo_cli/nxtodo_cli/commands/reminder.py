from nxtodo import queries
from nxtodo.thirdparty.exceptions import ObjectDoesNotFound
from nxtodo_cli import show_reminder_table

USER_CHOICE_REMINDER = {
    'add': lambda user, args, config: add_reminder(user, args),
    'show': lambda user, args, config: show_reminder(user, args, config),
    'remove': lambda user, args, config: remove_reminder(user, args),
    'edit': lambda user, args, config: edit_reminder(user, args),
    'toplan': lambda user, args, config: add_reminders_to_plan(user, args),
    'fromplan': lambda user, args, config: remove_reminders_from_plan(user,
                                                                      args),
    'totask': lambda user, args, config: add_reminders_to_task(user, args),
    'fromtask': lambda user, args, config: remove_reminders_from_task(user,
                                                                      args),
    'toevent': lambda user, args, config: add_reminders_to_event(user, args),
    'fromevent': lambda user, args, config: remove_reminders_from_event(user,
                                                                        args),
}


def handle_reminder(user, args, config):
    USER_CHOICE_REMINDER.get(args.command)(user, args, config)


def add_reminder(user_name, args):
    try:
        reminder_id = queries.add_reminder(
            user_name, args.description, args.remind_before,
            args.remind_from, args.stop_in, args.remind_in,
            args.datetimes, args.interval, args.weekdays
        )
        print(reminder_id)
    except ObjectDoesNotFound as e:
        print(e)


def show_reminder(user_name, args, config):
    try:
        reminders = queries.get_reminders(user_name, args.description, args.id)
    except ObjectDoesNotFound as e:
        print(e)
        return

    show_reminder_table(reminders, config)


def remove_reminder(user_name, args):
    try:
        queries.remove_reminder(user_name, args.id)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def edit_reminder(user_name, args):
    try:
        queries.edit_plan(
            user_name, args.id, args.description, args.start_remind_before,
            args.start_remind_from, args.stop_remind_in, args.remind_in,
            args.datetimes, args.interval, args.weekdays
        )
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def add_reminders_to_plan(user_name, args):
    try:
        queries.add_reminders_to_plan(user_name, args.plan, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_reminders_from_plan(user_name, args):
    try:
        queries.remove_reminders_from_plan(user_name, args.plan, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def add_reminders_to_task(user_name, args):
    try:
        queries.add_reminders_to_task(user_name, args.task, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_reminders_from_task(user_name, args):
    try:
        queries.remove_reminders_from_task(user_name, args.task, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def add_reminders_to_event(user_name, args):
    try:
        queries.add_reminders_to_event(user_name, args.event, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)


def remove_reminders_from_event(user_name, args):
    try:
        queries.remove_reminders_from_event(user_name, args.event, args.ids)
    except ObjectDoesNotFound as e:
        print(e)
    except PermissionError as e:
        print(e)
