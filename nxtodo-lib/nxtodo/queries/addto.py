from datetime import datetime

from nxtodo.common.constants import ADMINS_NAME
from nxtodo.common.exceptions import Looping
from nxtodo.db.event import (
    UserEvents,
    EventReminders
)
from nxtodo.db.plan import (
    UserPlans,
    PlanReminders
)
from nxtodo.db.task import (
    UserTasks,
    TaskReminders
)
from nxtodo.queries.access_decorators import (
    user_task_access,
    user_event_access,
    user_plan_access
)
from nxtodo.queries.common import (
    get_user,
    get_task,
    get_event,
    get_plan,
    get_reminder,
    get_objects_owners
)
from nxtodo.queries.logging_decorators import log_addto_query


@log_addto_query("Successfully added {} owners to task '{}' by user '{}'",
                 "Error when adding {} owners to task '{}' by user '{}'")
@user_task_access
def add_owners_to_task(user_name, task_id, owners):
    task = get_task(task_id)
    for owner in owners:
        user = get_user(owner.user_name)
        try:
            relation = UserTasks.objects.get(user=user, task=task)
        except:
            relation = UserTasks(user=user, task=task,
                                 assign_date=datetime.now(),
                                 access_level=owner.access_level)
            relation.save()


@log_addto_query("Successfully added {} subtasks to task '{}' by user '{}'",
                 "Error when adding {} subtasks to task '{}' by user '{}'")
@user_task_access
def add_subtasks_to_task(user_name, task_id, subtasks_ids):
    task = get_task(task_id)
    for id in subtasks_ids:
        subtask = get_task(id)
        if not subtask.check_cycles(task):
            task.subtasks.add(subtask)
        else:
            msg = ("You can't add subtask id={} to task id={}, because "
                   "the task id={} already exists in the subtasks of the "
                   "task id={}").format(id, task_id, task_id, id)
            raise Looping(msg)


@log_addto_query("Successfully added {} reminders to task '{}' by user '{}'",
                 "Error when adding {} reminders to task '{}' by user '{}'")
@user_task_access
def add_reminders_to_task(user_name, task_id, reminders_ids):
    task = get_task(task_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        relation = TaskReminders(task=task, reminder=reminder)
        relation.save()


@log_addto_query("Successfully added {} participants to event '{}' by user '{}'",
                 "Error when adding {} participants to event '{}' by user '{}'")
@user_event_access
def add_participants_to_event(user_name, event_id, participants):
    event = get_event(event_id)
    for participant in participants:
        user = get_user(participant.user_name)
        try:
            relation = UserEvents.objects.get(user=user, event=event)
        except:
            relation = UserEvents(user=user, event=event,
                                  assign_date=datetime.now(),
                                  access_level=participant.access_level)
            relation.save()


@log_addto_query("Successfully added {} reminders to event '{}' by user '{}'",
                 "Error when adding {} reminders to event '{}' by user '{}'")
@user_event_access
def add_reminders_to_event(user_name, event_id, reminders_ids):
    event = get_event(event_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        relation = EventReminders(event=event, reminder=reminder)
        relation.save()


@log_addto_query("Successfully added {} tasks to plan '{}' by user '{}'",
                 "Error when adding {} tasks to plan '{}' by user '{}'")
@user_plan_access
def add_tasks_to_plan(user_name, plan_id, tasks_ids):
    plan = get_plan(plan_id)
    for id in tasks_ids:
        task = get_task(id)
        add_owners_to_task(ADMINS_NAME, id, get_objects_owners(plan))
        task.prepare_to_plan()
        plan.tasks.add(task)


@log_addto_query("Successfully added {} events to plan '{}' by user '{}'",
                 "Error when adding {} events to plan '{}' by user '{}'")
@user_plan_access
def add_events_to_plan(user_name, plan_id, events_ids):
    plan = get_plan(plan_id)
    for id in events_ids:
        event = get_event(id)
        add_participants_to_event(ADMINS_NAME, id, get_objects_owners(plan))
        event.prepare_to_plan()
        plan.events.add(event)


@log_addto_query("Successfully added {} reminders to plan '{}' by user '{}'",
                 "Error when adding {} reminders to plan '{}' by user '{}'")
@user_plan_access
def add_reminders_to_plan(user_name, plan_id, reminders_ids):
    plan = get_plan(plan_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        relation = PlanReminders(plan=plan, reminder=reminder)
        relation.save()


@log_addto_query("Successfully added {} owners to plan '{}' by user '{}'",
                 "Error when adding {} owners to plan '{}' by user '{}'")
@user_plan_access
def add_owners_to_plan(user_name, plan_id, owners):
    plan = get_plan(plan_id)
    for owner in owners:
        user = get_user(owner.user_name)
        relation = UserPlans(user=user, plan=plan, assign_date=datetime.now(),
                             access_level=owner.access_level)
        relation.save()