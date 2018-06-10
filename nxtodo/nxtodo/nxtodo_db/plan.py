from collections import namedtuple

from django.db import models
from nxtodo.thirdparty import (
    Statuses,
    Entities
)

from .base import Base
from .event import Event
from .task import Task



class Plan(Base):
    tasks = models.ManyToManyField(Task)
    events = models.ManyToManyField(Event)
    reminders = models.ManyToManyField('Reminder', through='PlanReminders')

    @classmethod
    def create(cls, title, description, category, priority, created_by):
        plan = cls(
            title=title,
            description=description,
            category=category,
            priority=priority,
            status=Statuses.INPROCESS.value,
            created_by=created_by
        )
        return plan

    @staticmethod
    def get_type():
        return Entities.PLAN

    def get_planned_objects(self, user_name, now):
        actual_date = self.get_notification(user_name, now)
        if not actual_date:
            return None
        Planned_objects = namedtuple('Planned_objects',
                                     'tasks events created_at')
        return Planned_objects(self.tasks.all(), self.events.all(),
                               actual_date)