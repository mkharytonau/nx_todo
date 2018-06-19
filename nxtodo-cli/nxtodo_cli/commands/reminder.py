from nxtodo import queries
from nxtodo.common.exceptions import ObjectDoesNotFound
from nxtodo_cli.commands.common import with_printing_exception
from nxtodo_cli.displaying import show_reminder_table

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


@with_printing_exception
def add_reminder(user_name, args):
    reminder_id = queries.add_reminder(
        user_name, args.description, args.remind_before,
        args.remind_from, args.stop_in, args.remind_in,
        args.datetimes, args.interval, args.weekdays
    )
    print(reminder_id)


def show_reminder(user_name, args, config):
    try:
        reminders = queries.get_reminders(user_name, args.description, args.id)
    except ObjectDoesNotFound as e:
        print(e)
        return

    show_reminder_table(reminders, config)


@with_printing_exception
def remove_reminder(user_name, args):
    queries.remove_reminder(user_name, args.id)


@with_printing_exception
def edit_reminder(user_name, args):
    queries.edit_plan(
        user_name, args.id, args.description, args.start_remind_before,
        args.start_remind_from, args.stop_remind_in, args.remind_in,
        args.datetimes, args.interval, args.weekdays
    )


@with_printing_exception
def add_reminders_to_plan(user_name, args):
    queries.add_reminders_to_plan(user_name, args.plan, args.ids)


@with_printing_exception
def remove_reminders_from_plan(user_name, args):
    queries.remove_reminders_from_plan(user_name, args.plan, args.ids)


@with_printing_exception
def add_reminders_to_task(user_name, args):
    queries.add_reminders_to_task(user_name, args.task, args.ids)


@with_printing_exception
def remove_reminders_from_task(user_name, args):
    queries.remove_reminders_from_task(user_name, args.task, args.ids)


@with_printing_exception
def add_reminders_to_event(user_name, args):
    queries.add_reminders_to_event(user_name, args.event, args.ids)


@with_printing_exception
def remove_reminders_from_event(user_name, args):
    queries.remove_reminders_from_event(user_name, args.event, args.ids)
