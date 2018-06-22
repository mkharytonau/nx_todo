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
    get_reminder
)


@user_task_access
def remove_owners_from_task(username, task_id, owners):
    task = get_task(task_id)
    for owner in owners:
        user = get_user(owner)
        try:
            relation = UserTasks.objects.get(user=user, task=task)
            relation.delete()
        except:
            continue


@user_task_access
def remove_subtasks_from_task(username, task_id, subtasks_ids):
    task = get_task(task_id)
    for id in subtasks_ids:
        subtask = get_task(id)
        task.subtasks.remove(subtask)


@user_task_access
def remove_reminders_from_task(username, task_id, reminders_ids):
    task = get_task(task_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        try:
            relation = TaskReminders.objects.get(task=task, reminder=reminder)
            relation.delete()
        except:
            continue


@user_event_access
def remove_participants_from_event(username, event_id, participants):
    event = get_event(event_id)
    for participant in participants:
        user = get_user(participant)
        try:
            relation = UserEvents.objects.get(user=user, event=event)
            relation.delete()
        except:
            continue


@user_event_access
def remove_reminders_from_event(username, event_id, reminders_ids):
    event = get_event(event_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        try:
            relation = EventReminders.objects.get(event=event, reminder=reminder)
            relation.delete()
        except:
            continue


@user_plan_access
def remove_tasks_from_plan(username, plan_id, tasks_ids):
    plan = get_plan(plan_id)
    for id in tasks_ids:
        task = get_task(id)
        plan.tasks.remove(task)


@user_plan_access
def remove_events_from_plan(username, plan_id, events_ids):
    plan = get_plan(plan_id)
    for id in events_ids:
        event = get_event(id)
        plan.events.remove(event)


@user_plan_access
def remove_reminders_from_plan(username, plan_id, reminders_ids):
    plan = get_plan(plan_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        try:
            relation = PlanReminders.objects.get(plan=plan, reminder=reminder)
            relation.delete()
        except:
            continue


@user_task_access
def remove_owners_from_plan(username, plan_id, owners):
    plan = get_plan(plan_id)
    for owner in owners:
        user = get_user(owner)
        try:
            relation = UserPlans.objects.get(user=user, plan=plan)
            relation.delete()
        except:
            continue