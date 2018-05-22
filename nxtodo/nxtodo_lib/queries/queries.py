from django.core.exceptions import ObjectDoesNotExist
from nxtodo_lib.thirdparty import enums
from nxtodo_lib.nxtodo_db.models import User
from nxtodo_lib.nxtodo_db.models import Task
from nxtodo_lib.nxtodo_db.models import Event
from nxtodo_lib.nxtodo_db.models import Reminder


def get_user(name):
    try:
        return User.objects.get(name=name)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("There is no user '{}'".format(name))


def get_task(task_id):
    try:
        return Task.objects.get(id=task_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist('There is no task with id={}'.format(task_id))


def get_event(event_id):
    try:
        return Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist('There is no event with id={}'.format(event_id))


def get_reminder(reminder_id):
    try:
        return Reminder.objects.get(id=reminder_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist('There is no reminder with id={}'.format(event_id))



def show(user, search_info):
    ws = getattr(user, working_space[search_info.instance])  # working_space[search_info.instance]
    if search_info.all:
        return ws.filter(('status', search_info.status))
    return ws.filter((search_info.attribute, search_info.value), (('status', search_info.status)))


def add_user(name):
    user = User.create(name)
    user.save()


def add_task(user, title, description, category, deadline,
             priority, status, owners):
    u = get_user(user)
    task = Task.create(title, description, category, deadline,
                       priority, status)
    task.save()
    u.tasks.add(task)
    if owners is not None:
        add_owners_to_task(user, task.id, owners)


def add_event(user, title, description, category, from_datetime,
              to_datetime, place, participants):
    u = get_user(user)
    event = Event.create(title, description, category, from_datetime,
                         to_datetime, place)
    event.save()
    u.events.add(event)
    if participants is not None:
        add_participants_to_event(user, event.id, participants)


def add_reminder(user, start_remind_before, start_remind_from, remind_in,
                 datetimes, interval, weekdays):
    reminder = Reminder.create(start_remind_before, start_remind_from, remind_in,
                               datetimes, interval, weekdays)
    reminder.user = get_user(user)
    reminder.save()


def add_owners_to_task(user, task_id, owners):
    task = get_task(task_id)
    for owner in owners:
        u = get_user(owner)
        task.user_set.add(u)


def add_reminders_to_task(user, task_id, reminders_ids):
    task = get_task(task_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        if reminder.task is not None:
            rem = Reminder.create(reminder.start_remind_before, reminder.start_remind_from,
                                  reminder.remind_in, reminder.datetimes, reminder.interval,
                                  reminder.weekdays)
            rem.user = get_user(user)
            rem.task = task
            rem.save()
        else:
            reminder.task = task


def add_participants_to_event(user, event_id, participants):
    event = get_event(event_id)
    for participant in participants:
        u = get_user(participant)
        event.user_set.add(u)


def add_reminders_to_event(user, event_id, reminders_ids):
    event = get_event(event_id)
    for id in reminders_ids:
        reminder = get_reminder(id)
        if reminder.event is not None:
            rem = Reminder.create(reminder.start_remind_before, reminder.start_remind_from,
                                  reminder.remind_in, reminder.datetimes, reminder.interval,
                                  reminder.weekdays)
            rem.user = get_user(user)
            rem.event = event
            rem.save()
        else:
            reminder.event = event


def delete(self, user, search_info):
    ws = getattr(user, working_space[search_info.instance])  # working_space[search_info.instance]
    if search_info.all:
        ws.all().update(status=enums.Statuses.archived.value)
    else:
        ws.filter((search_info.attribute, search_info.value)). \
            update(status=enums.Statuses.archived.value)


def do(self, user, search_info):
    ws = getattr(user, working_space[search_info.instance])  # working_space[search_info.instance]
    if search_info.all:
        ws.all().update(status=enums.Statuses.fulfilled.value)
    else:
        ws.filter((search_info.attribute, search_info.value)). \
            update(status=enums.Statuses.fulfilled.value)


def remove(self, user, search_info):
    ws = getattr(user, working_space[search_info.instance])  # working_space[search_info.instance]
    if search_info.all:
        ws.all().delete()
    else:
        ws.filter((search_info.attribute, search_info.value)).delete()


def check(self, user, search_info, style):
    founded = self.find_instance_by(search_info)
    notifications = self.get_notifications(founded, style)
    self.write()
    return notifications


def get_notifications(self, arr, style):
    notifications = []
    for obj in arr:
        notification = obj.reminder.check(style)
        if notification is not None:
            notifications.append(notification)
    return notifications

