from django.core.exceptions import ObjectDoesNotExist
from nxtodo.nxtodo_db.models import User, Task, Event, Plan, Reminder
from nxtodo.thirdparty import enums, functions


def get_user(name):
    try:
        return User.objects.get(name=name)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("There is no user '{}'".format(name))


def get_reminder(reminder_id):
    try:
        return Reminder.objects.get(id=reminder_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(
            'There is no reminder with id={}'.format(reminder_id))


def get_task(task_id):
    try:
        return Task.objects.get(id=task_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(
            'There is no task with id={}'.format(task_id))


def get_tasks(user, title=None, category=None, priority=None, status=None,
              id=None):
    user = get_user(user)
    filters = functions.create_filters(id, title, category, priority, status)
    selection = user.tasks.filter(**filters)
    if not len(selection):
        raise ObjectDoesNotExist('There is no tasks with selected filters.')
    return selection


def get_event(event_id):
    try:
        return Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(
            'There is no event with id={}'.format(event_id))


def get_events(user, title=None, category=None, priority=None, status=None,
               place=None, id=None):
    user = get_user(user)
    filters = functions.create_filters(id, title, category, priority, status,
                                       place)
    selection = user.events.filter(**filters)
    if not len(selection):
        raise ObjectDoesNotExist('There is no events with selected filters.')
    return selection


def get_plan(plan_id):
    try:
        return Plan.objects.get(id=plan_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(
            'There is no plan with id={}'.format(plan_id))


def get_plans(user, title=None, category=None, priority=None, status=None,
              id=None):
    user = get_user(user)
    filters = functions.create_filters(id, title, category, priority, status)
    selection = user.plans.filter(**filters)
    if not len(selection):
        raise ObjectDoesNotExist('There is no plans with selected filters.')
    return selection


def add_user(name):
    user = User.create(name)
    user.save()


def add_task(user, title, description=None, category=None, deadline=None,
             priority=None, status=None, owners=None):
    u = get_user(user)
    task = Task.create(title, description, category, deadline,
                       priority, status)
    task.save()
    u.tasks.add(task)
    if owners:
        add_owners_to_task(task.id, owners)


def add_event(user, title, from_datetime, to_datetime, description=None,
              category=None, priority=None, status=None, place=None,
              participants=None):
    u = get_user(user)
    event = Event.create(title, description, category, priority, status,
                         from_datetime, to_datetime, place)
    event.save()
    u.events.add(event)
    if participants:
        add_participants_to_event(event.id, participants)


def add_plan(user, title, description=None, category=None, priority=None,
             status=None, tasks=None, events=None, reminders=None):
    u = get_user(user)
    plan = Plan.create(title, description, category, priority, status)
    plan.save()
    u.plans.add(plan)
    if tasks:
        add_tasks_to_plan(plan.id, tasks)
    if events:
        add_events_to_plan(plan.id, events)
    if reminders:
        add_reminders_to_plan(user, plan.id, reminders)


def add_reminder(user, start_remind_before=None, start_remind_from=None,
                 stop_remind_in=None, remind_in=None, datetimes=None,
                 interval=None, weekdays=None):
    reminder = Reminder.create(start_remind_before, start_remind_from,
                               stop_remind_in, remind_in, datetimes, interval,
                               weekdays)
    reminder.user = get_user(user)
    reminder.save()


def add_owners_to_task(task_id, owners):
    task = get_task(task_id)
    for owner in owners:
        u = get_user(owner)
        task.user_set.add(u)


def add_reminders_to_task(user, task_id, reminders_ids):
    task = get_task(task_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        if not (reminder.task or reminder.event or reminder.plan):
            reminder.task = task
        else:
            rem = Reminder.create(reminder.start_remind_before,
                                  reminder.start_remind_from,
                                  reminder.stop_remind_in,
                                  reminder.remind_in, reminder.datetimes,
                                  reminder.interval,
                                  reminder.weekdays)
            rem.user = get_user(user)
            rem.task = task
            rem.save()


def add_participants_to_event(event_id, participants):
    event = get_event(event_id)
    for participant in participants:
        u = get_user(participant)
        event.user_set.add(u)


def add_reminders_to_event(user, event_id, reminders_ids):
    event = get_event(event_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        if not (reminder.task or reminder.event or reminder.plan):
            reminder.event = event
        else:
            rem = Reminder.create(reminder.start_remind_before,
                                  reminder.start_remind_from,
                                  reminder.remind_in, reminder.datetimes,
                                  reminder.interval,
                                  reminder.weekdays)
            rem.user = get_user(user)
            rem.event = event
            rem.save()


def add_tasks_to_plan(plan_id, tasks_ids):
    plan = get_plan(plan_id)
    for id in tasks_ids:
        task = get_task(id)
        task.prepare_to_plan()
        plan.tasks.add(task)


def add_events_to_plan(plan_id, events_ids):
    plan = get_plan(plan_id)
    for id in events_ids:
        event = get_event(id)
        event.prepare_to_plan()
        plan.events.add(event)


def add_reminders_to_plan(user, plan_id, reminders_ids):
    plan = get_plan(plan_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        if not (reminder.task or reminder.event or reminder.plan):
            reminder.plan = plan
        else:
            rem = Reminder.create(reminder.start_remind_before,
                                  reminder.start_remind_from,
                                  reminder.remind_in, reminder.datetimes,
                                  reminder.interval,
                                  reminder.weekdays)
            rem.user = get_user(user)
            rem.plan = plan
            rem.save()


def remove_user(name):
    get_user(name).delete()


def remove_plan(plan_id):
    get_plan(plan_id).delete()


def remove_plans(user, title):
    get_plans(user, title=title).delete()


def delete(self, user, search_info):
    ws = getattr(user, working_space[
        search_info.instance])  # working_space[search_info.instance]
    if search_info.all:
        ws.all().update(status=enums.Statuses.ARCHIVED.value)
    else:
        ws.filter((search_info.attribute, search_info.value)). \
            update(status=enums.Statuses.ARCHIVED.value)


def do(self, user, search_info):
    ws = getattr(user, working_space[
        search_info.instance])  # working_space[search_info.instance]
    if search_info.all:
        ws.all().update(status=enums.Statuses.FULFILLED.value)
    else:
        ws.filter((search_info.attribute, search_info.value)). \
            update(status=enums.Statuses.FULFILLED.value)


def remove(self, user, search_info):
    ws = getattr(user, working_space[
        search_info.instance])  # working_space[search_info.instance]
    if search_info.all:
        ws.all().delete()
    else:
        ws.filter((search_info.attribute, search_info.value)).delete()


def check(self, user, search_info, style):
    founded = self.find_instance_by(search_info)
    notifications = self.get_notifications(founded, style)
    self.write()
    return notifications
