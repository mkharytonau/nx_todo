from datetime import datetime

from nxtodo.nxtodo_db.models import (
    Task,
    Event
)
from nxtodo.thirdparty import Statuses

from .addto import (
    add_owners_to_task,
    add_participants_to_event,
    add_reminders_to_task,
    add_reminders_to_event
)
from .common import (
    get_plans,
    get_tasks,
    get_events
)


def check_tasks(user, title=None, category=None, priority=None, status=None,
                id=None):
    tasks = get_tasks(user, title, category, priority, status, id)
    notifications = []
    for task in tasks:
        notification = task.get_notification(datetime.now())
        if notification:
            notifications.append(notification)
    if not notifications:
        raise Exception('There is no notifications for tasks.')
    return notifications


def check_events(user, title=None, category=None, priority=None, status=None,
                place=None, id=None):
    events = get_events(user, title, category, priority, status, place, id)
    notifications = []
    for event in events:
        notification = event.get_notification(datetime.now())
        if notification:
            notifications.append(notification)
    if not notifications:
        raise Exception('There is no notifications for events.')
    return notifications


def check_plans(user, title=None, category=None, priority=None, status=None,
                id=None, now=datetime.now()):
    plans = get_plans(user, title, category, priority, status, id)
    for plan in plans:
        planned_objects = plan.notify(now)
        if not planned_objects:
            return
        for task in planned_objects.tasks:
            duplicate_task(user, task, planned_objects.created_at)
        for event in planned_objects.events:
            duplicate_event(user, event, planned_objects.created_at)


def duplicate_task(user, task, created_at):
    new_task = Task.create(task.title, task.description, task.category,
                           task.deadline, task.priority)
    new_task.created_at = created_at
    new_task.status = Statuses.INPROCESS.value
    new_task.save()

    add_owners_to_task(new_task.id, [user])
    add_reminders_to_task(user, new_task.id,
                          [rem.id for rem in task.reminder_set.all()])


def duplicate_event(user, event, created_at):
    new_event = Event.create(event.title, event.description,
                             event.category, event.priority,
                             event.from_datetime, event.to_datetime,
                             event.place)
    new_event.created_at = created_at
    new_event.status = Statuses.PROCESSING.value
    new_event.save()

    add_participants_to_event(new_event.id, [user])
    add_reminders_to_event(user, new_event.id,
                           [rem.id for rem in event.reminder_set.all()])