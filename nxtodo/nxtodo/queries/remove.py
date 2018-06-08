from .common import (
    get_user,
    get_task,
    get_event,
    get_plan,
    get_reminder
)
from .access_decorators import (
    user_task_access,
    user_event_access,
    user_plan_access,
    user_reminder_access
)


def remove_user(name):
    get_user(name).delete()


@user_task_access
def remove_task(user_name, task_id):
    get_task(task_id).delete()


@user_event_access
def remove_event(user_name, event_id):
    get_event(event_id).delete()


@user_plan_access
def remove_plan(user_name, plan_id):
    get_plan(plan_id).delete()


@user_reminder_access
def remove_reminder(user_name, reminder_id):
    get_reminder(reminder_id).delete()