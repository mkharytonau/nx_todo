from django.core.exceptions import ObjectDoesNotExist
from functools import wraps


from nxtodo.nxtodo_db.models import (
    UserTasks,
    UserEvents,
    UserPlans
)
from nxtodo.thirdparty import (
    AccessLevels,
    ADMINS_NAME
)

from nxtodo.queries.common import (
    get_user,
    get_task,
    get_event,
    get_plan,
    get_reminder
)


def user_task_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0] == ADMINS_NAME:
            user = get_user(args[0])
            task = get_task(args[1])

            try:
                relation = UserTasks.objects.get(user=user, task=task)
            except ObjectDoesNotExist:
                msg = ("Invalid operation, you are not the owner "
                       "of the '{}' task.").format(task.id)
                raise PermissionError(msg)

            if relation.access_level == AccessLevels.EDIT.value:
                func(*args, **kwargs)
            else:
                msg = ("Permission denied, you can't "
                       "edit '{}' task.").format(task.id)
                raise PermissionError(msg)
        else:
            func(*args, **kwargs)

    return wrapper


def user_event_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0] == ADMINS_NAME:
            user = get_user(args[0])
            event = get_event(args[1])

            try:
                relation = UserEvents.objects.get(user=user, event=event)
            except ObjectDoesNotExist:
                msg = ("Invalid operation, you are not the owner "
                       "of the '{}' event.").format(event.id)
                raise PermissionError(msg)

            if relation.access_level == AccessLevels.EDIT.value:
                func(*args, **kwargs)
            else:
                msg = ("Permission denied, you can't "
                       "edit '{}' event.").format(event.id)
                raise PermissionError(msg)
        else:
            func(*args, **kwargs)

    return wrapper


def user_plan_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0] == ADMINS_NAME:
            user = get_user(args[0])
            plan = get_plan(args[1])

            try:
                relation = UserPlans.objects.get(user=user, plan=plan)
            except ObjectDoesNotExist:
                msg = ("Invalid operation, you are not the owner "
                       "of the '{}' plan.").format(plan.id)
                raise PermissionError(msg)

            if relation.access_level == AccessLevels.EDIT.value:
                func(*args, **kwargs)
            else:
                msg = ("Permission denied, you can't "
                       "edit '{}' plan.").format(plan.id)
                raise PermissionError(msg)
        else:
            func(*args, **kwargs)

    return wrapper


def user_reminder_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_user(args[0])
        reminder = get_reminder(args[1])
        if reminder.user.name == user.name:
            func(*args, **kwargs)
        else:
            msg = ("Permission denied, you can't "
                   "edit '{}' reminder.").format(reminder.id)
            raise PermissionError(msg)

    return wrapper
