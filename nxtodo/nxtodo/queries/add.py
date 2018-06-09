from datetime import datetime

from nxtodo.nxtodo_db.models import (
    User,
    Task,
    Event,
    Plan,
    Reminder,
    UserTasks,
    UserEvents,
    UserPlans
)
from nxtodo.thirdparty import AccessLevels

from .addto import (
    add_owners_to_task,
    add_participants_to_event,
    add_tasks_to_plan,
    add_events_to_plan,
    add_reminders_to_plan
)
from .common import get_user
from .logging_decorators import log_add_queri


def add_user(user_name):
    user = User.create(user_name)
    user.save()


@log_add_queri('Successfully added task {} to user {}', 'Error when adding {} task: ')
def add_task(user_name, title, description=None, category=None, deadline=None,
             priority=None, owners=None):
    user = get_user(user_name)
    task = Task.create(title, description, category, deadline,
                       priority)
    task.save()
    relation = UserTasks(user=user, task=task, assign_date=datetime.now(),
                         access_level=AccessLevels.EDIT.value)
    relation.save()
    if owners:
        try:
            add_owners_to_task(user_name, task.id, owners)
        except PermissionError as e:
            print(e)


def add_event(user_name, title, from_datetime, to_datetime, description=None,
              category=None, priority=None, place=None, participants=None):
    user = get_user(user_name)
    event = Event.create(title, description, category, priority,
                         from_datetime, to_datetime, place)
    event.save()
    relation = UserEvents(user=user, event=event, assign_date=datetime.now(),
                          access_level=AccessLevels.EDIT.value)
    relation.save()
    if participants:
        try:
            add_participants_to_event(user_name, event.id, participants)
        except PermissionError as e:
            print(e)


def add_plan(user_name, title, description=None, category=None, priority=None,
             tasks=None, events=None, reminders=None):
    user = get_user(user_name)
    plan = Plan.create(title, description, category, priority)
    plan.save()
    relation = UserPlans(user=user, plan=plan, assign_date=datetime.now(),
                         access_level=AccessLevels.EDIT.value)
    relation.save()
    try:
        if tasks:
            add_tasks_to_plan(user_name, plan.id, tasks)
        if events:
            add_events_to_plan(user_name, plan.id, events)
        if reminders:
            add_reminders_to_plan(user_name, plan.id, reminders)
    except PermissionError as e:
        print(e)


def add_reminder(user, description=None, start_remind_before=None,
                 start_remind_from=None, stop_remind_in=None, remind_in=None,
                 datetimes=None, interval=None, weekdays=None):
    reminder = Reminder.create(description, start_remind_before,
                               start_remind_from, stop_remind_in, remind_in,
                               datetimes, interval, weekdays)
    reminder.user = get_user(user)
    reminder.save()