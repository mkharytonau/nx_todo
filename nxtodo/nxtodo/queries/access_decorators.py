from nxtodo.nxtodo_db.models import (
    UserTasks,
    UserEvents,
    UserPlans
)
from nxtodo.thirdparty import AccessLevels

from .common import (
    get_user,
    get_task,
    get_event,
    get_plan,
    get_reminder
)


def user_task_access(func):
    def wrapper(*args, **kwargs):
        user = get_user(args[0])
        task = get_task(args[1])
        relation = UserTasks.objects.get(user=user, task=task)
        if relation.access_level == AccessLevels.EDIT.value:
            func(*args, **kwargs)
        else:
            msg = ("Permission denied, you can't "
                   "edit '{}' task").format(task.id)
            raise PermissionError(msg)

    return wrapper


def user_event_access(func):
    def wrapper(*args, **kwargs):
        user = get_user(args[0])
        event = get_event(args[1])
        relation = UserEvents.objects.get(user=user, event=event)
        if relation.access_level == AccessLevels.EDIT.value:
            func(*args, **kwargs)
        else:
            msg = ("Permission denied, you can't "
                   "edit '{}' event").format(event.id)
            raise PermissionError(msg)

    return wrapper


def user_plan_access(func):
    def wrapper(*args, **kwargs):
        user = get_user(args[0])
        plan = get_plan(args[1])
        relation = UserPlans.objects.get(user=user, plan=plan)
        if relation.access_level == AccessLevels.EDIT.value:
            func(*args, **kwargs)
        else:
            msg = ("Permission denied, you can't "
                   "edit '{}' plan").format(plan.id)
            raise PermissionError(msg)

    return wrapper


def user_reminder_access(func):
    def wrapper(*args, **kwargs):
        user = get_user(args[0])
        reminder = get_reminder(args[1])
        if reminder.user.id == user.id:
            func(*args, **kwargs)
        else:
            msg = ("Permission denied, you can't "
                   "edit '{}' reminder").format(reminder.id)
            raise PermissionError(msg)

    return wrapper
