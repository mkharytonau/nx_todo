from datetime import datetime

from nxtodo.nxtodo_db.models import (
    Reminder,
    UserTasks
)

from .access_decorators import (
    user_task_access,
    user_event_access,
    user_plan_access
)
from .common import (
    get_user,
    get_task,
    get_event,
    get_plan,
    get_reminder
)


@user_task_access
def add_owners_to_task(user_name, task_id, owners):
    task = get_task(task_id)
    for owner in owners:
        user = get_user(owner.user_name)
        relation = UserTasks(user=user, task=task, assign_date=datetime.now(),
                             access_level=owner.access_level)
        relation.save()


@user_task_access
def add_reminders_to_task(user_name, task_id, reminders_ids):
    task = get_task(task_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        if reminder.task or reminder.event or reminder.plan:
            reminder = Reminder.create(reminder.description,
                                       reminder.start_remind_before,
                                       reminder.start_remind_from,
                                       reminder.stop_remind_in,
                                       reminder.remind_in, reminder.datetimes,
                                       reminder.interval, reminder.weekdays)
            reminder.user = get_user(user_name)
        reminder.task = task
        reminder.save()


@user_event_access
def add_participants_to_event(user_name, event_id, participants):
    event = get_event(event_id)
    for participant in participants:
        u = get_user(participant)
        event.user_set.add(u)


@user_event_access
def add_reminders_to_event(user_name, event_id, reminders_ids):
    event = get_event(event_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        if reminder.task or reminder.event or reminder.plan:
            reminder = Reminder.create(reminder.description,
                                       reminder.start_remind_before,
                                       reminder.start_remind_from,
                                       reminder.stop_remind_in,
                                       reminder.remind_in, reminder.datetimes,
                                       reminder.interval, reminder.weekdays)
            reminder.user = get_user(user_name)
        reminder.event = event
        reminder.save()


@user_plan_access
def add_tasks_to_plan(user_name, plan_id, tasks_ids):
    plan = get_plan(plan_id)
    for id in tasks_ids:
        task = get_task(id)
        task.prepare_to_plan()
        plan.tasks.add(task)


@user_plan_access
def add_events_to_plan(user_name, plan_id, events_ids):
    plan = get_plan(plan_id)
    for id in events_ids:
        event = get_event(id)
        event.prepare_to_plan()
        plan.events.add(event)


@user_plan_access
def add_reminders_to_plan(user, plan_id, reminders_ids):
    plan = get_plan(plan_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        if reminder.task or reminder.event or reminder.plan:
            reminder = Reminder.create(reminder.description,
                                       reminder.start_remind_before,
                                       reminder.start_remind_from,
                                       reminder.stop_remind_in,
                                       reminder.remind_in, reminder.datetimes,
                                       reminder.interval, reminder.weekdays)
            reminder.user = get_user(user)
        reminder.plan = plan
        reminder.save()