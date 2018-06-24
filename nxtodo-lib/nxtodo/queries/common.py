from datetime import datetime
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist
from nxtodo.db.models import (
    User,
    Task,
    Event,
    Plan,
    Reminder
)
from nxtodo.db.task import UserTasks
from nxtodo.db.event import UserEvents
from nxtodo.db.plan import UserPlans
from nxtodo.common import (
    Owner,
    Entities,
    ReminderStatuses
)
from nxtodo.queries.logging_decorators import log_get_query
from nxtodo.common.exceptions import ObjectDoesNotFound


def create_filters(id=None, title=None, category=None, priority=None,
                   status=None, place=None, description=None, name=None):
    """Function to create filters.

    It is creates a dict object, that contains fields will be used in query.

    """

    filters = {}
    if id:
        filters['id'] = id
    if title:
        filters['title'] = title
    if category:
        filters['category'] = category
    if priority:
        filters['priority'] = priority
    if status:
        filters['status'] = status
    if place:
        filters['place'] = place
    if description:
        filters['description'] = description
    if name:
        filters['name'] = name
    return filters


def get_user(name):
    """
    Returns user by name.
    """
    try:
        return User.objects.get(name=name)
    except ObjectDoesNotExist:
        raise ObjectDoesNotFound("There is no user '{}'.".format(name))


def get_task(task_id):
    """
    Returns task by id.
    """
    try:
        return Task.objects.get(id=task_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotFound(
            'There is no task with id={}.'.format(task_id))


def get_event(event_id):
    """
    Returns event by id.
    """
    try:
        return Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotFound(
            'There is no event with id={}.'.format(event_id))


def get_plan(plan_id):
    """
    Returns plan by id.
    """
    try:
        return Plan.objects.get(id=plan_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotFound(
            'There is no plan with id={}.'.format(plan_id))


def get_reminder(reminder_id):
    """
    Returns reminder by id.
    """
    try:
        return Reminder.objects.get(id=reminder_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotFound(
            'There is no reminder with id={}.'.format(reminder_id))


def get_users(name=None):
    """
    Returns users by name, all users when 'name' argument is None.
    """
    filters = create_filters(name=name)
    selection = User.objects.filter(**filters)
    if not len(selection):
        raise ObjectDoesNotFound('There is no users with selected filters.')
    return selection


def get_objects_owners(obj):
    """
    Defines obj type and returns objects owners.
    """
    type = obj.get_type()
    owners = []
    for user in obj.user_set.all():
        if type == Entities.TASK:
            relation = UserTasks.objects.get(user=user, task=obj)
        elif type == Entities.EVENT:
            relation = UserEvents.objects.get(user=user, event=obj)
        elif type == Entities.PLAN:
            relation = UserPlans.objects.get(user=user, plan=obj)
        else:
            raise TypeError
        owners.append(Owner(user.name, relation.access_level))

    return owners


@log_get_query("Successfully returned {} reminders to '{}' user",
               "Error when '{}' user tried to get reminders: ")
def get_reminders(user, description=None, status=None, id=None, orderby=None):
    """
    Returns users reminders filtered by args.
    """
    user = get_user(user)
    filters = create_filters(id, description=description)
    selection = user.reminder_set.filter(**filters)

    if status == ReminderStatuses.ACTIVE.value:
        now = datetime.now()
        selection = selection.filter(start_remind_from__lte=now).\
            filter(stop_remind_in__gte=now)

    if status == ReminderStatuses.ARCHIVED.value:
        now = datetime.now()
        part_one = selection.filter(start_remind_from__gt=now)
        part_two = selection.filter(stop_remind_in__lt=now)
        selection = list(chain(part_one, part_two))

    if orderby:
        selection = selection.order_by(orderby)

    if not len(selection):
        raise ObjectDoesNotFound('There is no reminders '
                                 'with selected filters.')
    return selection


@log_get_query("Successfully returned {} tasks to '{}' user",
               "Error when '{}' user tried to get tasks: ")
def get_tasks(user, title=None, category=None, deadline=None, priority=None,
              status=None, id=None, orderby=None):
    """
    Returns users tasks filtered by args.
    """
    user = get_user(user)
    filters = create_filters(id, title, category,
                                              priority, status)
    selection = user.tasks.filter(**filters)

    if deadline:
        selection = selection.filter(deadline__lte=deadline)

    if orderby:
        selection = selection.order_by(orderby)

    if not len(selection):
        raise ObjectDoesNotFound('There is no tasks with selected filters.')
    return selection


@log_get_query("Successfully returned {} events to '{}' user",
               "Error when '{}' user tried to get events: ")
def get_events(user, title=None, category=None, fromdt=None, priority=None,
               status=None, place=None, id=None, orderby=None):
    """
    Returns users events filtered by args.
    """
    user = get_user(user)
    filters = create_filters(id, title, category,
                                              priority, status,
                                              place)
    selection = user.events.filter(**filters)
    if fromdt:
        selection = selection.filter(from_datetime__lte=fromdt)

    if orderby:
        selection = selection.order_by(orderby)

    if not len(selection):
        raise ObjectDoesNotFound('There is no events with selected filters.')
    return selection


@log_get_query("Successfully returned {} plans to '{}' user",
               "Error when '{}' user tried to get plans: ")
def get_plans(user, title=None, category=None, priority=None, status=None,
              id=None, orderby=None):
    """
    Returns users plans filtered by args.
    """
    user = get_user(user)
    filters = create_filters(id, title, category,
                                              priority, status)
    selection = user.plans.filter(**filters)

    if orderby:
        selection = selection.order_by(orderby)

    if not len(selection):
        raise ObjectDoesNotFound('There is no plans with selected filters.')
    return selection
