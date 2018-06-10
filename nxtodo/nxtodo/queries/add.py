from datetime import datetime

from nxtodo.nxtodo_db.models import (
    User,
    Task,
    Event,
    Plan,
    Reminder
)
from nxtodo.thirdparty import (
    ADMINS_NAME
)

from .addto import (
    add_owners_to_task,
    add_participants_to_event,
    add_owners_to_plan,
    add_tasks_to_plan,
    add_events_to_plan,
    add_reminders_to_plan,
    add_reminders_to_task,
    add_reminders_to_event
)
from .common import get_user
from .logging_decorators import log_add_query


def add_user(user_name):
    user = User.create(user_name)
    user.save()


@log_add_query('Successfully added task {} to user {}', 'Error when adding {} task: ')
def add_task(executor, title, description=None, category=None, deadline=None,
             priority=None, owners=None, reminders=None):
    task = Task.create(title, description, category, deadline,
                       priority, executor)
    task.save()
    if owners:
        add_owners_to_task(ADMINS_NAME, task.id, owners)
    if reminders:
        add_reminders_to_task(ADMINS_NAME, task.id, reminders)
    return task.id


def add_event(executor, title, from_datetime, to_datetime, description=None,
              category=None, priority=None, place=None, participants=None,
              reminders=None):
    event = Event.create(title, description, category, priority,
                         from_datetime, to_datetime, place, executor)
    event.save()
    if participants:
        add_participants_to_event(ADMINS_NAME, event.id, participants)
    if reminders:
        add_reminders_to_event(ADMINS_NAME, event.id, reminders)
    return event


def add_plan(executor, title, description=None, category=None, priority=None,
             tasks=None, events=None, reminders=None, owners=None):
    plan = Plan.create(title, description, category, priority, executor)
    plan.save()
    if tasks:
        add_tasks_to_plan(ADMINS_NAME, plan.id, tasks)
    if events:
        add_events_to_plan(ADMINS_NAME, plan.id, events)
    if reminders:
        add_reminders_to_plan(ADMINS_NAME, plan.id, reminders)
    if owners:
        add_owners_to_plan(ADMINS_NAME, plan.id, owners)
    return plan


def add_reminder(user_name, description=None, start_remind_before=None,
                 start_remind_from=None, stop_remind_in=None, remind_in=None,
                 datetimes=None, interval=None, weekdays=None):
    reminder = Reminder.create(description, start_remind_before,
                               start_remind_from, stop_remind_in, remind_in,
                               datetimes, interval, weekdays)
    reminder.user = get_user(user_name)
    reminder.save()
    return reminder