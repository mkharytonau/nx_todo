from nxtodo.queries.common import (
    get_user,
    get_task,
    get_event,
    get_plan,
    get_reminder
)
from nxtodo.queries.access_decorators import (
    user_task_access,
    user_event_access,
    user_plan_access,
    user_reminder_access
)
from nxtodo.queries.logging_decorators import (
    log_query,
    log_user_query
)


@log_user_query("Successfully removed user '{}'",
                "Error when removing '{}' user: ")
def remove_user(name):
    get_user(name).delete()


@log_query("Successfully removed '{}' task by user '{}'",
           "Error when removing '{}' task by user '{}': ")
@user_task_access
def remove_task(user_name, task_id):
    get_task(task_id).delete()


@log_query("Successfully removed '{}' event by user '{}'",
           "Error when removing '{}' event by user '{}': ")
@user_event_access
def remove_event(user_name, event_id):
    get_event(event_id).delete()


@log_query("Successfully removed '{}' plan by user '{}'",
           "Error when removed '{}' plan by user '{}': ")
@user_plan_access
def remove_plan(user_name, plan_id):
    get_plan(plan_id).delete()


@log_query("Successfully removed '{}' reminder by user '{}'",
           "Error when removing '{}' reminder by user '{}': ")
@user_reminder_access
def remove_reminder(user_name, reminder_id):
    get_reminder(reminder_id).delete()