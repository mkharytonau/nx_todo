from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from nxtodo.common import (
    AccessLevels,
    ADMINS_NAME
)
from nxtodo.db.event import UserEvents
from nxtodo.db.plan import UserPlans
from nxtodo.db.task import UserTasks
from nxtodo.queries.common import (
    get_user,
    get_task,
    get_event,
    get_plan,
    get_reminder
)


def user_task_access(func):
    """
    Decorator, which checks the level of user access to the task.
    """
    @wraps(func)
    def wrapper(username, task_id, *args, **kwargs):
        if not username == ADMINS_NAME:
            user = get_user(username)
            task = get_task(task_id)

            try:
                relation = UserTasks.objects.get(user=user, task=task)
            except ObjectDoesNotExist:
                msg = ("Invalid operation, you are not the owner "
                       "of the '{}' task.").format(task.id)
                raise PermissionError(msg)

            if relation.access_level == AccessLevels.EDIT.value:
                func(username, task_id, *args, **kwargs)
            else:
                msg = ("Permission denied, you can't "
                       "edit '{}' task.").format(task.id)
                raise PermissionError(msg)
        else:
            func(username, task_id, *args, **kwargs)

    return wrapper


def user_event_access(func):
    """
    Decorator, which checks the level of user access to the event.
    """
    @wraps(func)
    def wrapper(username, event_id, *args, **kwargs):
        if not username == ADMINS_NAME:
            user = get_user(username)
            event = get_event(event_id)

            try:
                relation = UserEvents.objects.get(user=user, event=event)
            except ObjectDoesNotExist:
                msg = ("Invalid operation, you are not the owner "
                       "of the '{}' event.").format(event.id)
                raise PermissionError(msg)

            if relation.access_level == AccessLevels.EDIT.value:
                func(username, event_id, *args, **kwargs)
            else:
                msg = ("Permission denied, you can't "
                       "edit '{}' event.").format(event.id)
                raise PermissionError(msg)
        else:
            func(username, event_id, *args, **kwargs)

    return wrapper


def user_plan_access(func):
    """
    Decorator, which checks the level of user access to the plan.
    """
    @wraps(func)
    def wrapper(username, plan_id, *args, **kwargs):
        if not username == ADMINS_NAME:
            user = get_user(username)
            plan = get_plan(plan_id)

            try:
                relation = UserPlans.objects.get(user=user, plan=plan)
            except ObjectDoesNotExist:
                msg = ("Invalid operation, you are not the owner "
                       "of the '{}' plan.").format(plan.id)
                raise PermissionError(msg)

            if relation.access_level == AccessLevels.EDIT.value:
                func(username, plan_id, *args, **kwargs)
            else:
                msg = ("Permission denied, you can't "
                       "edit '{}' plan.").format(plan.id)
                raise PermissionError(msg)
        else:
            func(username, plan_id, *args, **kwargs)

    return wrapper


def user_reminder_access(func):
    """
    Decorator, which checks the level of user access to the reminder.
    """
    @wraps(func)
    def wrapper(username, reminder_id, *args, **kwargs):
        user = get_user(username)
        reminder = get_reminder(reminder_id)
        if reminder.user.name == user.name:
            func(username, reminder_id, *args, **kwargs)
        else:
            msg = ("Permission denied, you can't "
                   "edit '{}' reminder.").format(reminder.id)
            raise PermissionError(msg)

    return wrapper
