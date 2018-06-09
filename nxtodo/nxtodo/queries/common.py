from django.core.exceptions import ObjectDoesNotExist
from nxtodo.nxtodo_db.models import (
    User,
    Task,
    Event,
    Plan,
    Reminder
)

from nxtodo.thirdparty import common_functions


def get_user(name):
    try:
        return User.objects.get(name=name)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("There is no user '{}'".format(name))


def get_task(task_id):
    try:
        return Task.objects.get(id=task_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(
            'There is no task with id={}'.format(task_id))


def get_event(event_id):
    try:
        return Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(
            'There is no event with id={}'.format(event_id))


def get_plan(plan_id):
    try:
        return Plan.objects.get(id=plan_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(
            'There is no plan with id={}'.format(plan_id))


def get_reminder(reminder_id):
    try:
        return Reminder.objects.get(id=reminder_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(
            'There is no reminder with id={}'.format(reminder_id))


def get_users(name=None):
    filters = common_functions.create_filters(name=name)
    selection = User.objects.filter(**filters)
    if not len(selection):
        raise ObjectDoesNotExist('There is no users with selected filters.')
    return selection


def get_reminders(user, description=None, id=None):
    user = get_user(user)
    filters = common_functions.create_filters(id, description=description)
    selection = user.reminder_set.filter(**filters)
    if not len(selection):
        raise ObjectDoesNotExist('There is no reminders '
                                 'with selected filters.')
    return selection


def get_tasks(user, title=None, category=None, priority=None, status=None,
              id=None):
    user = get_user(user)
    filters = common_functions.create_filters(id, title, category,
                                              priority, status)
    selection = user.tasks.filter(**filters)
    if not len(selection):
        raise ObjectDoesNotExist('There is no tasks with selected filters.')
    return selection


def get_events(user, title=None, category=None, priority=None, status=None,
               place=None, id=None):
    user = get_user(user)
    filters = common_functions.create_filters(id, title, category,
                                              priority, status,
                                       place)
    selection = user.events.filter(**filters)
    if not len(selection):
        raise ObjectDoesNotExist('There is no events with selected filters.')
    return selection


def get_plans(user, title=None, category=None, priority=None, status=None,
              id=None):
    user = get_user(user)
    filters = common_functions.create_filters(id, title, category,
                                              priority, status)
    selection = user.plans.filter(**filters)
    if not len(selection):
        raise ObjectDoesNotExist('There is no plans with selected filters.')
    return selection