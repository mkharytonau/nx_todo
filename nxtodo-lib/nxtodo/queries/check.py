from datetime import datetime

from nxtodo.common.exceptions import NoNotifications
from nxtodo.queries.add import (
    add_task,
    add_event
)
from nxtodo.queries.common import (
    get_task,
    get_event,
    get_plans,
    get_tasks,
    get_events,
    get_objects_owners
)


def get_tasks_notifications(user, title=None, category=None, deadline=None,
                            priority=None, status=None, id=None,
                            now=None, maxdelta=0):
    """
    Receive notifications from tasks or raise NoNotifications exception.
    """
    if not now:
        now = datetime.now()
    tasks = get_tasks(user, title, category, deadline, priority, status, id)
    notifications = []
    for task in tasks:
        notification = task.get_notification(user, now, maxdelta)
        if notification:
            notifications.append(notification)
    if not notifications:
        raise NoNotifications('There is no notifications for tasks.')
    return notifications


def get_events_notifications(user, title=None, category=None, fromdt=None,
                             priority=None, status=None, place=None, id=None,
                             now=None, maxdelta=0):
    """
    Receive notifications from events or raise NoNotifications exception.
    """
    if not now:
        now = datetime.now()
    events = get_events(user, title, category, fromdt, priority,
                        status, place, id)
    notifications = []
    for event in events:
        notification = event.get_notification(user, now, maxdelta)
        if notification:
            notifications.append(notification)
    if not notifications:
        raise NoNotifications('There is no notifications for events.')
    return notifications


def check_plans(user, title=None, category=None, priority=None, status=None,
                id=None, now=None):
    """
    Checks plan for notifications and duplicates attached tasks and events.
    """
    if not now:
        now = datetime.now()
    try:
        plans = get_plans(user, title, category, priority, status, id)
    except:
        plans = []

    for plan in plans:
        planned_objects = plan.get_planned_objects(user, now)
        if not planned_objects:
            continue
        for task in planned_objects.tasks:
            duplicate_task(plan.title, task, planned_objects.created_at)
        for event in planned_objects.events:
            duplicate_event(plan.title, event, planned_objects.created_at)


def duplicate_task(executor, task, created_at):
    """Duplicate existing task: get owners, reminders attached to task
    and simply add a new one.

    :param executor: who duplicates a task
    :param task: task to duplicate
    :param created_at: datetime in which task will be created

    """

    owners = get_objects_owners(task)
    reminders = [reminder.id for reminder in task.reminders.all()]
    executor = "{}(Plan)".format(executor)
    task_id = add_task(executor, task.title, task.description, task.category,
                       task.deadline, task.priority, owners, reminders)
    new_task = get_task(task_id)
    new_task.created_at = created_at
    new_task.save()


def duplicate_event(executor, event, created_at):
    """Duplicate existing event: get participants, reminders attached to event
    and simply add a new one.

    :param executor: who duplicates a event
    :param task: event to duplicate
    :param created_at: datetime in which event will be created

    """

    participants = get_objects_owners(event)
    reminders = [reminder.id for reminder in event.reminders.all()]
    executor = "{}(Plan)".format(executor)
    event_id = add_event(executor, event.title, event.from_datetime,
                         event.to_datetime, event.description, event.category,
                         event.priority, event.place, participants, reminders)
    new_event = get_event(event_id)
    new_event.created_at = created_at
    new_event.save()