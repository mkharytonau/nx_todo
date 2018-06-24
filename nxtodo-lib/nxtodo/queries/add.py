from nxtodo.db.models import (
    User,
    Task,
    Event,
    Plan,
    Reminder
)
from nxtodo.queries.addto import (
    add_owners_to_task,
    add_participants_to_event,
    add_owners_to_plan,
    add_tasks_to_plan,
    add_events_to_plan,
    add_reminders_to_plan,
    add_reminders_to_task,
    add_reminders_to_event,
    add_subtasks_to_task
)
from nxtodo.queries.common import get_user
from nxtodo.queries.logging_decorators import (
    log_add_query,
    log_user_query
)
from nxtodo.common import ADMINS_NAME


@log_user_query("Successfully added user '{}'",
                "Error when adding user '{}': ")
def add_user(username):
    """Create user 'username' and save if in database.

    :param username: username of created user
    :return: username

    """

    user = User.create(username)
    user.save()
    return user.name


@log_add_query("Successfully added task id='{}' by user '{}'",
               "Error when adding task by user '{}': ")
def add_task(executor, title, description=None, category=None, deadline=None,
             priority=None, owners=None, reminders=None, subtasks=None):
    """Create task, save it and add owners, reminders, subtasks if they were
    passed into arguments.

    :param executor: the username of the person who adds the task
    :param title: task title
    :param description: task description
    :param category:  task category
    :param deadline: task deadline - python datetime object
    :param priority: task priority
    :param owners: list of Owner(username, access_level) objects
    :param reminders: list of reminders ids
    :param subtasks: list of subtasks ids
    :return: id

    """

    task = Task.create(title, description, category, deadline,
                       priority, executor)
    task.save()

    if owners:
        add_owners_to_task(ADMINS_NAME, task.id, owners)
    if reminders:
        add_reminders_to_task(ADMINS_NAME, task.id, reminders)
    if subtasks:
        add_subtasks_to_task(ADMINS_NAME, task.id, subtasks)
    return task.id


@log_add_query("Successfully added event id='{}' by user '{}'",
               "Error when adding event by user '{}': ")
def add_event(executor, title, from_datetime=None, to_datetime=None,
              description=None, category=None, priority=None, place=None,
              participants=None, reminders=None):
    """Create event, save it and add participants, reminders if they were
    passed into arguments.

    :param executor: the username of the person who adds the event
    :param title: event title
    :param from_datetime: event start date and time
    :param to_datetime: event end date and time
    :param description: event description
    :param category: event category
    :param priority: event priority
    :param place: event place
    :param participants: list of Owner(username, access_level) objects
    :param reminders: list of reminders ids
    :return: id

    """

    event = Event.create(title, description, category, priority,
                         from_datetime, to_datetime, place, executor)
    event.save()

    if participants:
        add_participants_to_event(ADMINS_NAME, event.id, participants)
    if reminders:
        add_reminders_to_event(ADMINS_NAME, event.id, reminders)
    return event.id


@log_add_query("Successfully added plan id='{}' by user '{}'",
               "Error when adding plan by user '{}': ")
def add_plan(executor, title, description=None, category=None, priority=None,
             tasks=None, events=None, reminders=None, owners=None):
    """Create plan, save it and add tasks, events, owners, reminders if they were
    passed into arguments.

    :param executor: the username of the person who adds the plan
    :param title: plan title
    :param description: plan description
    :param category: plan category
    :param priority: plan priority
    :param tasks: list of tasks ids attached to plan
    :param events: list of events ids attached to plan
    :param reminders: list of reminders ids attached to plan
    :param owners: list of Owner(username, access_level) objects
    :return:

    """

    plan = Plan.create(title, description, category, priority, executor)
    plan.save()
    if owners:
        add_owners_to_plan(ADMINS_NAME, plan.id, owners)
    if tasks:
        add_tasks_to_plan(ADMINS_NAME, plan.id, tasks)
    if events:
        add_events_to_plan(ADMINS_NAME, plan.id, events)
    if reminders:
        add_reminders_to_plan(ADMINS_NAME, plan.id, reminders)
    return plan.id


@log_add_query("Successfully added reminder id='{}' by user '{}'",
               "Error when adding reminder by user '{}': ")
def add_reminder(user_name, description=None, start_remind_before=None,
                 start_remind_from=None, stop_remind_in=None, remind_in=None,
                 datetimes=None, interval=None, weekdays=None):
    """Create reminder, save it and attach it to user.

    :param user_name:
    :param description:
    :param start_remind_before:
    :param start_remind_from:
    :param stop_remind_in:
    :param remind_in:
    :param datetimes:
    :param interval:
    :param weekdays:
    :return:

    """

    reminder = Reminder.create(description, start_remind_before,
                               start_remind_from, stop_remind_in, remind_in,
                               datetimes, interval, weekdays)
    reminder.user = get_user(user_name)
    reminder.save()
    return reminder.id
