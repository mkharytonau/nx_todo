from nxtodo.queries.access_decorators import (
    user_task_access,
    user_event_access,
    user_plan_access,
    user_reminder_access
)
from nxtodo.queries.common import (
    get_task,
    get_event,
    get_plan,
    get_reminder
)

from nxtodo.queries.logging_decorators import log_edit_query


@log_edit_query("Successfully edited '{}' task by user '{}'",
                "Error when edited '{}' task by user '{}': ")
@user_task_access
def edit_task(user_name, task_id, title=None, description=None,
              category=None, deadline=None, priority=None):
    task = get_task(task_id)
    if title:
        task.title = title
    if description:
        task.description = description
    if category:
        task.category = category
    if deadline:
        task.deadline = deadline
    if priority:
        task.priority = priority
    task.save()


@log_edit_query("Successfully edited '{}' event by user '{}'",
                "Error when edited '{}' event by user '{}': ")
@user_event_access
def edit_event(user_name, event_id, title=None, description=None,
               category=None, priority=None, from_datetime=None,
               to_datetime=None, place=None):
    event = get_event(event_id)
    if title:
        event.title = title
    if description:
        event.description = description
    if category:
        event.category = category
    if priority:
        event.priority = priority
    if from_datetime:
        event.from_datetime = from_datetime
    if to_datetime:
        event.to_datetime = to_datetime
    if place:
        event.place = place
    event.save()


@log_edit_query("Successfully edited '{}' plan by user '{}'",
                "Error when edited '{}' plan by user '{}': ")
@user_plan_access
def edit_plan(user_name, plan_id, title=None, description=None,
              category=None, priority=None):
    plan = get_plan(plan_id)
    if title:
        plan.title = title
    if description:
        plan.description = description
    if category:
        plan.category = category
    if priority:
        plan.priority = priority
    plan.save()


@log_edit_query("Successfully edited '{}' reminder by user '{}'",
                "Error when edited '{}' reminder by user '{}': ")
@user_reminder_access
def edit_reminder(user_name, reminder_id, description=None,
                  start_remind_before=None, start_remind_from=None,
                  stop_remind_in=None, remind_in=None, datetimes=None,
                  interval=None, weekdays=None):
    reminder = get_reminder(reminder_id)
    if description:
        reminder.description = description
    if start_remind_before:
        reminder.start_remind_before = start_remind_before
    if start_remind_from:
        reminder.start_remind_from = start_remind_from
    if stop_remind_in:
        reminder.stop_remind_in = stop_remind_in
    if remind_in:
        reminder.remind_in = remind_in
    if datetimes:
        reminder.datetimes = datetimes
    if interval:
        reminder.interval = interval
    if weekdays:
        reminder.weekdays = weekdays
    reminder.save()