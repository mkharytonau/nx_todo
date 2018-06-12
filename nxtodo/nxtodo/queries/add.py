from nxtodo.nxtodo_db.models import (
    User,
    Task,
    Event,
    Plan,
    Reminder
)
from nxtodo.queries.addto import (
    add_owners_to_task,
    add_participants_to_event,
    add_owners_to_plan,
    add_tasks_to_plan,
    add_events_to_plan,
    add_reminders_to_plan,
    add_reminders_to_task,
    add_reminders_to_event,
    add_subtasks_to_task
)
from nxtodo.queries.common import get_user
from nxtodo.queries.logging_decorators import (
    log_add_query,
    log_user_query
)
from nxtodo.thirdparty import ADMINS_NAME


@log_user_query("Successfully added user '{}'",
                "Error when adding user '{}': ")
def add_user(user_name):
    user = User.create(user_name)
    user.save()
    return user.name


@log_add_query("Successfully added task id='{}' by user '{}'",
               "Error when adding task by user '{}': ")
def add_task(executor, title, description=None, category=None, deadline=None,
             priority=None, owners=None, reminders=None, subtasks=None):
    task = Task.create(title, description, category, deadline,
                       priority, executor)
    task.save()

    if owners:
        add_owners_to_task(ADMINS_NAME, task.id, owners)
    if reminders:
        add_reminders_to_task(ADMINS_NAME, task.id, reminders)
    if subtasks:
        add_subtasks_to_task(ADMINS_NAME, task.id, subtasks)
    return task.id


@log_add_query("Successfully added event id='{}' by user '{}'",
               "Error when adding event by user '{}': ")
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
    return event.id


@log_add_query("Successfully added plan id='{}' by user '{}'",
               "Error when adding plan by user '{}': ")
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
    return plan.id


@log_add_query("Successfully added reminder id='{}' by user '{}'",
               "Error when adding reminder by user '{}': ")
def add_reminder(user_name, description=None, start_remind_before=None,
                 start_remind_from=None, stop_remind_in=None, remind_in=None,
                 datetimes=None, interval=None, weekdays=None):
    reminder = Reminder.create(description, start_remind_before,
                               start_remind_from, stop_remind_in, remind_in,
                               datetimes, interval, weekdays)
    reminder.user = get_user(user_name)
    reminder.save()
    return reminder.id
