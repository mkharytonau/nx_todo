from django.db import models

import nxtodo
from nxtodo import Statuses
from .base import Base
from .event import Event
from .task import Task


class Plan(Base):
    tasks = models.ManyToManyField(Task)
    events = models.ManyToManyField(Event)

    @classmethod
    def create(cls, title, description, category, priority, status):
        plan = cls(title=title, description=description, category=category,
                   priority=priority, status=status)
        return plan

    def notify(self, user, now):
        actual_date = self.get_actual_date(now)
        if not actual_date:
            return
        for task in self.tasks.all():
            Plan.duplicate_task(user, task)
        for event in self.events.all():
            Plan.duplicate_event(user, event)

    def get_actual_date(self, now):
        notifications = []
        for reminder in self.reminder_set.all():
            notification = reminder.notify(now)
            if notification:
                notifications.append(notification)
        if not notifications:
            return None
        notifications.sort(key=lambda obj: obj, reverse=True)
        return notifications[0]

    @staticmethod
    def duplicate_task(user, task, created_at):
        new_task = Task.create(task.title, task.description, task.category,
                               task.deadline, task.priority,
                               Statuses.PROCESSING.value)
        new_task.save()

        nxtodo.queries.add_owners_to_task(new_task.id, [user])
        nxtodo.queries.add_reminders_to_task(user, new_task.id,
                                      [rem.id for rem in
                                       task.reminder_set.all()])

    @staticmethod
    def duplicate_event(user, event):
        new_event = Event.create(event.title, event.description,
                                 event.category, event.priority,
                                 Statuses.PROCESSING.value, event.from_datetime,
                                 event.to_datetime, event.place)
        new_event.save()

        nxtodo.queries.add_participants_to_event(new_event.id, [user])
        nxtodo.queries.add_reminders_to_event(user, new_event.id,
                                      [rem.id for rem in
                                       event.reminder_set.all()])

    def __str__(self):
        return self.title