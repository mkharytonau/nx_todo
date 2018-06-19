"""
module contains main logic for manipulation with models:
- "add" group of methods
- "addto" group of methods
- "check" group of methods
- "common" group of methods, it's contains common for all groups methods
- "complete" group of methods
- "edit" group of methods
- "remove" group of methods
"""

from nxtodo.queries.access_decorators import (
    user_task_access,
    user_event_access,
    user_plan_access,
    user_reminder_access
)
from nxtodo.queries.add import (
    add_user,
    add_task,
    add_event,
    add_plan,
    add_reminder
)
from nxtodo.queries.addto import (
    add_owners_to_task,
    add_subtasks_to_task,
    add_participants_to_event,
    add_reminders_to_task,
    add_reminders_to_event,
    add_reminders_to_plan,
    add_tasks_to_plan,
    add_events_to_plan,
    add_owners_to_plan
)
from nxtodo.queries.check import (
    get_tasks_notifications,
    get_events_notifications,
    check_plans
)
from nxtodo.queries.common import (
    get_user,
    get_task,
    get_tasks,
    get_event,
    get_events,
    get_plan,
    get_users,
    get_plans,
    get_reminder,
    get_reminders,
    get_objects_owners
)
from nxtodo.queries.complete import (
    complete_task,
    complete_event
)
from nxtodo.queries.edit import (
    edit_task,
    edit_event,
    edit_plan,
    edit_reminder
)
from nxtodo.queries.remove import (
    remove_user,
    remove_task,
    remove_event,
    remove_plan,
    remove_reminder
)
