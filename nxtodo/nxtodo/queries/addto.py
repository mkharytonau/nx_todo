from datetime import datetime

from nxtodo.nxtodo_db.models import (
    UserTasks,
    UserEvents,
    UserPlans,
    TaskReminders,
    EventReminders,
    PlanReminders
)
from nxtodo.thirdparty.exceptions import Looping

from .access_decorators import (
    user_task_access,
    user_event_access,
    user_plan_access
)
from .common import (
    get_user,
    get_task,
    get_event,
    get_plan,
    get_reminder
)


@user_task_access
def add_owners_to_task(user_name, task_id, owners):
    task = get_task(task_id)
    for owner in owners:
        user = get_user(owner.user_name)
        relation = UserTasks(user=user, task=task, assign_date=datetime.now(),
                             access_level=owner.access_level)
        relation.save()


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


@user_task_access
def add_reminders_to_task(user_name, task_id, reminders_ids):
    task = get_task(task_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        relation = TaskReminders(task=task, reminder=reminder)
        relation.save()


@user_event_access
def add_participants_to_event(user_name, event_id, participants):
    event = get_event(event_id)
    for participant in participants:
        user = get_user(participant.user_name)
        relation = UserEvents(user=user, event=event,
                              assign_date=datetime.now(),
                              access_level=participant.access_level)
        relation.save()


@user_event_access
def add_reminders_to_event(user_name, event_id, reminders_ids):
    event = get_event(event_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        relation = EventReminders(event=event, reminder=reminder)
        relation.save()


@user_plan_access
def add_tasks_to_plan(user_name, plan_id, tasks_ids):
    plan = get_plan(plan_id)
    for id in tasks_ids:
        task = get_task(id)
        task.prepare_to_plan()
        plan.tasks.add(task)


@user_plan_access
def add_events_to_plan(user_name, plan_id, events_ids):
    plan = get_plan(plan_id)
    for id in events_ids:
        event = get_event(id)
        event.prepare_to_plan()
        plan.events.add(event)


@user_plan_access
def add_reminders_to_plan(user_name, plan_id, reminders_ids):
    plan = get_plan(plan_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        relation = PlanReminders(plan=plan, reminder=reminder)
        relation.save()

@user_plan_access
def add_owners_to_plan(user_name, plan_id, owners):
    plan = get_plan(plan_id)
    for owner in owners:
        user = get_user(owner.user_name)
        relation = UserPlans(user=user, plan=plan, assign_date=datetime.now(),
                             access_level=owner.access_level)
        relation.save()