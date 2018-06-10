from datetime import datetime
from collections import namedtuple

from nxtodo.nxtodo_db.models import (
    Task,
    Event,
    UserTasks,
    UserEvents
)
from nxtodo.thirdparty import (
    Statuses,
    Owner
)

from .addto import (
    add_owners_to_task,
    add_participants_to_event,
    add_reminders_to_task,
    add_reminders_to_event
)
from .add import (
    add_task,
    add_event
)
from .common import (
    get_task,
    get_event,
    get_plans,
    get_tasks,
    get_events
)


def check_tasks(user, title=None, category=None, priority=None, status=None,
                id=None, now=datetime.now()):
    tasks = get_tasks(user, title, category, priority, status, id)
    notifications = []
    for task in tasks:
        notification = task.get_notification(user, now)
        if notification:
            notifications.append(notification)
    if not notifications:
        raise Exception('There is no notifications for tasks.')
    return notifications


def check_events(user, title=None, category=None, priority=None, status=None,
                place=None, id=None, now=datetime.now()):
    events = get_events(user, title, category, priority, status, place, id)
    notifications = []
    for event in events:
        notification = event.get_notification(user, now)
        if notification:
            notifications.append(notification)
    if not notifications:
        raise Exception('There is no notifications for events.')
    return notifications


def check_plans(user, title=None, category=None, priority=None, status=None,
                id=None, now=datetime.now()):
    plans = get_plans(user, title, category, priority, status, id)
    for plan in plans:
        planned_objects = plan.get_planned_objects(user, now)
        if not planned_objects:
            return
        for task in planned_objects.tasks:
            duplicate_task(plan, task, planned_objects.created_at)
        for event in planned_objects.events:
            duplicate_event(plan, event, planned_objects.created_at)


def duplicate_task(plan, task, created_at):
    owners = []
    for user in task.user_set.all():
        relation = UserTasks.objects.get(user=user, task=task)
        owners.append(Owner(user.name, relation.access_level))
    reminders = [reminder.id for reminder in task.reminders.all()]
    executor = "{}(Plan)".format(plan.title)
    task_id = add_task(executor, task.title, task.description, task.category,
                       task.deadline, task.priority, owners, reminders)
    new_task = get_task(task_id)
    new_task.created_at = created_at
    new_task.save()


def duplicate_event(plan, event, created_at):
    participants = []
    for user in event.user_set.all():
        relation = UserEvents.objects.get(user=user, event=event)
        participants.append(Owner(user.name, relation.access_level))
    reminders = [reminder.id for reminder in event.reminders.all()]
    executor = "{}(Plan)".format(plan.title)
    event_id = add_event(executor, event.title, event.from_datetime,
                         event.to_datetime, event.description, event.category,
                         event.priority, event.place, participants, reminders)
    new_event = get_event(event_id)
    new_event.created_at = created_at
    new_event.save()